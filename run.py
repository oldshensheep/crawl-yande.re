import concurrent.futures
import configparser
import functools
import logging
import os
from os.path import islink
import queue
import time

import requests


class YandeRe():
    _current_donwload = 0
    # 包含之前下载的
    _actual_download = 0

    _API_URL = 'https://yande.re/post.json'

    _q = queue.Queue()

    def __init__(self, end_page, proxies={'http': '', 'https': ''}, quality='original', limit=100, start_page=1,
                 max_workers=10, max_retries=2, timeout=4, filepath='yande.re', hproxy=''):
        self.proxies = proxies
        self.quality = quality
        self.end_page = end_page
        self.limit = limit
        self.start_page = start_page
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.timeout = timeout
        self.filepath = filepath
        if len(hproxy) != 0:
            self._API_URL = f'{hproxy}/{self._API_URL}'
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers)
        self.download_files = self.last_download_files()
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        if not os.path.exists(subdir := os.path.join(filepath, quality)):
            os.mkdir(subdir)
        self.filepath = subdir
        self.session = self.create_session()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='fuck.log', format='%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

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

    def down_image(self):
        url, id = self._q.get()
        filename = f'{id}{os.path.splitext(url)[1]}'
        if filename in self.download_files:
            self._actual_download += 1
            self.logger.info(f'{filename} already downloaded')
            self._q.task_done()
            return
        self.logger.info(f'downloading {filename}')
        try:
            image = self.session.get(url).content
        except Exception as e:
            self.logger.info(f'{e}\ndownload {filename} failed')
            print('请设置代理')
            return
        with open(os.path.join(self.filepath, filename), 'wb') as f:
            f.write(image)
        self.logger.info(f'download {filename} succeeded!')
        self._current_donwload += 1
        self._actual_download += 1
        self._q.task_done()

    def get_img_urls(self, page):
        self.logger.info(f'get_img_urls {page}')
        try:
            post = self.session.get(
                f'{self._API_URL}?limit={self.limit}&page={page}').json()
        except Exception as e:
            self.logger.info(f'{e}\nget_img_urls page{page} failed')
            print('请设置代理')
            return
        file_map = {
            'original': [(i['file_url'], i['id']) for i in post],
            'jpeg': [(i['jpeg_url'], i['id']) for i in post],
            'sample': [(i['sample_url'], i['id']) for i in post]
        }
        img_urls = file_map[self.quality]
        for img_url in img_urls:
            self._q.put(img_url)
        self.logger.info(f'get page {page} img urls succeeded')

    def last_download_files(self):
        ids = list()
        for root, dirs, files in os.walk(self.filepath):
            for f in files:
                ids.append(f)
        return ids

    def speed(self):
        while True:
            ad = self._actual_download
            cd = self._current_donwload
            time.sleep(3)
            if ad == self._actual_download and cd == self._current_donwload:
                print('没动静')
            else:
                self.logger.info(f'actual download {self._actual_download}')
                self.logger.info(f'current download {self._current_donwload}')

    def run(self):
        self.executor.submit(self.speed)
        page_list = list(range(self.start_page, self.end_page + 1))
        jobs = []
        while True:
            if len(page_list) <= 0:
                break
            if self._q.qsize() < 10:
                self.get_img_urls(page_list.pop(0))

            # 限制submit的数量，防止占用内存过大
            jobing_num = len(jobs)
            for job in jobs:
                if job.done():
                    jobs.remove(job)
                    jobing_num -= 1
            if self._q.qsize() > 0 and jobing_num <= 15:
                jobs.append(self.executor.submit(self.down_image))


def main():
    config = configparser.ConfigParser()
    config.optionxform = str
    try:
        config.read('config.ini')
    except FileNotFoundError as e:
        print('config.ini file not found')
        return
    config = config['DFF']
    start_page = int(config['start_page'])
    end_page = int(config['end_page'])
    max_workers = int(config['max_workers'])
    filepath = config['filepath']
    proxies = {
        'http': config['proxy'],
        'https': config['proxy']
    }
    max_retries = int(config['max_retries'])
    timeout = int(config['timeout'])
    quality = config['quality']
    hproxy = config['hproxy']
    yandere = YandeRe(start_page=start_page, end_page=end_page, filepath=filepath, proxies=proxies,
                      max_workers=max_workers, max_retries=max_retries, timeout=timeout, quality=quality, hproxy=hproxy)
    yandere.run()


if __name__ == '__main__':
    main()
