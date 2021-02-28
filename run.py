import concurrent.futures
import configparser
import functools
import os
import time

import requests


class YandeRe():

    _current_donwload = 0

    # 包含之前下载的
    _actual_download = 0

    def __init__(self, end_page, proxies={'http': '', 'https': ''}, limit=100, start_page=1, max_workers=10, max_retries=2, timeout=4, filepath='yande.re'):
        self.proxies = proxies
        self.end_page = end_page
        self.limit = limit
        self.start_page = start_page
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.timeout = timeout
        self.filepath = filepath
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers)
        self.download_files = self.last_download_files()
        if not os.path.exists(filepath):
            os.path.os.mkdir(filepath)
        self.session = self.create_session()

    def create_session(self):
        adapters = requests.adapters.HTTPAdapter(
            pool_connections=self.max_workers, pool_maxsize=self.max_workers, max_retries=self.max_retries)
        session = requests.Session()
        session.proxies.update(self.proxies)
        session.mount('http://', adapters)
        session.mount('https://', adapters)
        session.request = functools.partial(
            session.request, timeout=self.timeout)
        return session

    def down_image(self, url, filename):
        if filename in self.download_files:
            self._actual_download += 1
            print(f'{filename} already downloaded')
            return
        print(f"downloading {filename}")
        image = self.session.get(url).content
        with open(os.path.join(self.filepath, filename), 'wb') as f:
            f.write(image)
            print(f"download {filename} succedded!")
            self._current_donwload += 1
            self._actual_download += 1

    def get_img_urls(self, page):
        post = self.session.get(
            f'https://yande.re/post.json?limit={self.limit}&page={page}').json()
        file_map = {
            'original': [(i['file_url'], i['id']) for i in post],
            'jpeg': [(i['jpeg_url'], i['id']) for i in post],
            'sample': [(i['sample_url'], i['id']) for i in post]
        }
        img_urls = file_map['original']
        return img_urls

    def last_download_files(self):
        ids = list()
        for root, dirs, files in os.walk(self.filepath):
            for f in files:
                ids.append(f)
        return ids

    def speed(self):
        while True:
            # ad = self._actual_download
            time.sleep(3)
            print(f'actual download {self._actual_download}')
            print(f'current download {self._current_donwload}')

    def run(self):
        self.executor.submit(self.speed)
        for i in range(self.start_page, self.end_page):
            img_urls = self.get_img_urls(page=i)
            result = {self.executor.submit(
                self.down_image, i[0], f'{i[1]}{os.path.splitext(i[0])[1]}'): i for i in img_urls}
            concurrent.futures.as_completed(result)


def main():
    config = configparser.ConfigParser()
    config.optionxform = str
    try:
        config.read('config.ini')
    except FileNotFoundError as e:
        print('config.ini file not found')
        return
    config = config['DFF']
    try:
        start_page = int(config['start_page'])
        end_page = int(config['end_page'])
        max_workers = int(config['max_workers'])
        filepath = config['filepath']
        proxies = {
            'http': config['proxy'],
            'https': config['proxy']
        }
        max_retries = int(config['max_retries'])
        timeout = float(config['timeout'])
    except Exception as e:
        pass
    yandere = YandeRe(start_page=start_page, end_page=end_page, filepath=filepath, proxies=proxies,
                      max_workers=max_workers,  max_retries=max_retries, timeout=timeout)
    yandere.run()


if __name__ == '__main__':
    main()
