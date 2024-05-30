import json
import os

import requests

from bodosdk.db.downloader import DownloadManager
from bodosdk.db.exc import DatabaseError
from bodosdk.exceptions import TimeoutException
from bodosdk.interfaces import ICluster, IJobRun
import pyarrow.parquet as pq


class Cursor:
    def __init__(self, catalog: str, cluster: ICluster, timeout: int = 3600):
        self._catalog = catalog
        self.cluster = cluster
        self._timeout = timeout
        self._job: IJobRun = None
        self._current_row = None
        self._metadata = None
        self._results_urls = None
        self._file_index = 0
        self._results = []
        self._rows_stripped = 0

    @property
    def rownumber(self):
        return self._current_row

    @property
    def rowcount(self):
        self._wait_for_finished_job()
        self._load_metadata()
        if self._results_urls:
            return self._metadata["num_rows"]

    def execute(self, query: str, **kwargs):
        self._results_urls = None
        self._file_index = 0
        self._current_row = None
        self._results = []
        self._rows_stripped = 0
        self._job = self.cluster.run_sql_query(
            catalog=self._catalog,
            sql_query=query,
            args=kwargs,
            timeout=self._timeout,
            store_result=True,
        )
        self._wait_for_finished_job()
        self._load_metadata()
        return self

    def execute_async(self, query: str, **kwargs):
        self._results_urls = None
        self._file_index = None
        self._current_row = None
        self._results = []
        self._rows_stripped = 0
        self._job = self.cluster.run_sql_query(
            catalog=self._catalog, sql_query=query, args=kwargs, store_result=True
        )
        return self

    def fetchone(self):
        self._wait_for_finished_job()
        self._load_metadata()
        if self._current_row >= self.rowcount:
            return None
        if self._current_row >= len(self._results) + self._rows_stripped:
            self._load_next_file()
        record = self._results[self._current_row - self._rows_stripped]
        self._current_row += 1
        return record

    def _load_metadata(self):
        if not self._results_urls:
            self._results_urls = self._job.get_result_urls()
            metadata_url = self._results_urls[0]
            response = requests.get(metadata_url)
            self._metadata = json.loads(response.content)
            self._file_index = 0
            self._current_row = 0
            self.download_manager = DownloadManager(
                self._job.uuid, self._results_urls[1:]
            )
            self.tmp_files = self.download_manager.download_files(self._timeout)

    def _load_next_file(self):
        filename = f"{self._job.uuid}-{self._file_index}.pq"
        try:
            df = pq.read_table(filename).to_pandas()
            data = list(df.to_records(index=False))
        except FileNotFoundError:
            return None
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
        self._rows_stripped += len(self._results)
        self._results = data
        self._file_index += 1
        return True

    def fetchmany(self, size):
        self._wait_for_finished_job()
        self._load_metadata()
        if self._current_row >= self.rowcount:
            return None
        results = list(self._results)
        while size > len(results):
            if self._load_next_file():
                results.extend(self._results)
            else:
                break
        data_to_return = results[max(self._current_row - self._rows_stripped, 0):size]
        self._results = list(
            results[max(self._current_row - self._rows_stripped, 0) + size:]
        )
        self._current_row += min(size, len(results))
        self._rows_stripped = self._current_row
        return list(data_to_return)

    def fetchall(self):
        self._wait_for_finished_job()
        self._load_metadata()
        results = []
        results.extend(self._results)
        while self._load_next_file():
            results.extend(self._results)
        self._current_row = self.rowcount
        return results

    def _wait_for_finished_job(self):
        try:
            self._job.wait_for_status(
                ["SUCCEEDED", "FAILED", "CANCELLED"], tick=10, timeout=self._timeout
            )
        except TimeoutException:
            raise DatabaseError("Query timed out")
        if self._job.status in ["FAILED", "CANCELLED"]:
            raise DatabaseError(
                f"Query failed due to {self._job.reason}. {self._job.get_stderr()}"
            )

    def __iter__(self):
        row = self.fetchone()
        while row:
            yield row
            row = self.fetchone()


class Connection:
    def __init__(self, catalog: str, cluster: ICluster, timeout=3600):
        self._catalog = catalog
        self._cluster = cluster
        self._timeout = timeout

    def cursor(self):
        return Cursor(self._catalog, self._cluster, self._timeout)
