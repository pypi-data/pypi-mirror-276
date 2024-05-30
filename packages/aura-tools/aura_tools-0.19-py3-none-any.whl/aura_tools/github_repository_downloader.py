import os
import shutil

import requests
import zipfile
import subprocess
from tqdm import tqdm


class GithubRepositoryDownloader:
    def __init__(self, repo_url, target_dir=None):
        self.repo_url = repo_url
        self.repo_name = os.path.splitext(os.path.basename(repo_url))[0]
        self.target_dir = target_dir or os.path.dirname(os.path.abspath(__file__))

    def download(self, mode="zip", force=False, delete_existing=False):
        if os.path.exists(self._get_code_dir()):
            if not force:
                print(f"目录 {self._get_code_dir()} 已存在,跳过下载。")
                return self._get_code_dir()
            if delete_existing:
                self._delete_code_dir()

        if mode == "zip":
            self._download_zip()
        else:
            self._download_clone()

        return self._get_code_dir()

    def _get_code_dir(self):
        return os.path.join(self.target_dir, self.repo_name)

    def _delete_code_dir(self):
        code_dir = self._get_code_dir()
        if os.path.exists(code_dir):
            shutil.rmtree(code_dir)

    def _download_zip(self):
        repo_url = self.repo_url.rstrip(".git")
        zip_url = f"{repo_url}/archive/refs/heads/main.zip"
        self._download_and_extract_zip(zip_url)

    def _download_clone(self):
        code_dir = self._get_code_dir()
        subprocess.run(["git", "clone", self.repo_url, code_dir], check=True)

    def _download_and_extract_zip(self, zip_url):
        response = requests.get(zip_url, stream=True)
        if response.status_code == 404:
            zip_url = f"{self.repo_url.rstrip('.git')}/archive/refs/heads/master.zip"
            response = requests.get(zip_url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("Content-Length", 0))
        block_size = 1024
        downloaded_size = 0

        with open("temp.zip", "wb") as file, tqdm(
                desc=f"Downloading {self.repo_name}",
                total=total_size,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
        ) as progress_bar:
            for data in response.iter_content(block_size):
                size = file.write(data)
                downloaded_size += size
                progress_bar.update(size)

        with zipfile.ZipFile("temp.zip", "r") as zip_file:
            temp_dir = os.path.join(self.target_dir, "temp")
            zip_file.extractall(temp_dir)

        os.remove("temp.zip")
        code_dir_name = os.listdir(temp_dir)[0]
        code_dir = self._get_code_dir()
        os.rename(os.path.join(temp_dir, code_dir_name), code_dir)
        os.rmdir(temp_dir)

if __name__ == '__main__':
    repo_url = "https://github.com/langchain4j/langchain4j.git"
    downloader = GithubRepositoryDownloader(repo_url)

    # 下载 ZIP 模式
    code_dir = downloader.download(mode="zip")
    #
    # # 下载 clone 模式
    # code_dir = downloader.download(mode="clone",force=True,delete_existing=True)
    #
    # # 文件目录已存在不下载模式
    # code_dir = downloader.download()
    #
    # # 文件目录已存在强制覆盖模式
    # code_dir = downloader.download(force=True)
    #
    # # 文件目录已存在先删除再下载模式
    # code_dir = downloader.download(delete_existing=True)
    print(code_dir)