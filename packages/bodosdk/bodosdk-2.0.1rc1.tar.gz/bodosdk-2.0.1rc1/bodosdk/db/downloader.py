from concurrent.futures import ThreadPoolExecutor
from time import time, sleep

import requests
from requests import session
from requests.adapters import Retry, HTTPAdapter


class FileDownloader:
    def __init__(self, url, file_name):
        self.url = url
        self.download_complete = False
        self.result = None
        self.file_name = file_name

    def download(self):
        with session() as req:
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                method_whitelist=["HEAD", "GET", "OPTIONS"],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            http = requests.Session()
            http.mount("https://", adapter)
            http.mount("http://", adapter)
            response = req.get(self.url)
            with open(self.file_name, "wb") as temp_file:
                temp_file.write(response.content)
                self.result = temp_file
                self.download_complete = True


class DownloadManager:
    def __init__(self, job_uuid, urls):
        self.urls = urls
        self.job_uuid = job_uuid
        self.thread_executor = ThreadPoolExecutor(max_workers=len(urls))

    def download_files(self, timeout=3600):
        downloaders = []
        for index, url in enumerate(self.urls):
            downloader = FileDownloader(url, f"{self.job_uuid}-{index}.pq")
            downloaders.append(downloader)
            self.thread_executor.submit(downloader.download)

        start_time = time()

        while not all([downloader.download_complete for downloader in downloaders]):
            if time() - start_time > timeout:
                raise TimeoutError(
                    f"Could not download all resourlts withing {timeout} seconfs"
                )
            sleep(1)

            # Optionally, shutdown the executor if no more tasks will be submitted
        self.thread_executor.shutdown(wait=False)
