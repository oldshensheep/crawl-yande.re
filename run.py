import concurrent.futures
import functools
import logging
import os
import queue
import time
import requests


class YandeRe():
    _current_donwload = 0
    # 包含之前下载的
    _actual_download = 0

    _API_URL = 'https://yande.re/post.json'

    _q = queue.Queue(256)

    def __init__(self,
                 end_page,
                 proxies=None,
                 quality='original',
                 limit=100,
                 start_page=1,
                 max_workers=10,
                 max_retries=2,
                 timeout=4,
                 filepath='yande.re',
                 hproxy=''):
        if proxies is None:
            proxies = {'http': '', 'https': ''}
        self.proxies = proxies
        self.quality = quality
        self.end_page = end_page
        self.limit = limit
        self.start_page = start_page
        self.max_workers = max_workers
        self.max_retries = max_retries
        self.timeout = timeout
        self.filepath = filepath
        if hproxy is not None:
            self._API_URL = f'{hproxy}/{self._API_URL}'
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers + 2,
            initializer=lambda: print("fucked"))
        self.download_files = self.last_download_files()
        if not os.path.exists(filepath):
            os.mkdir(filepath)
        if not os.path.exists(subdir := os.path.join(filepath, quality)):
            os.mkdir(subdir)
        self.filepath = subdir
        self.session = self.create_session()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename='fuck.log',
            format=
            '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s - %(message)s',
            level=logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        self.logger.addHandler(ch)

    def create_session(self):
        adapters = requests.adapters.HTTPAdapter(max_retries=self.max_retries)
        session = requests.Session()
        session.proxies.update(self.proxies)
        session.mount('http://', adapters)
        session.mount('https://', adapters)
        session.request = functools.partial(session.request,
                                            timeout=self.timeout)
        return session

    def down_image(self):
        while True:
            url, id = self._q.get()
            filename = f'{id}{os.path.splitext(url)[1]}'
            if filename in self.download_files:
                self._actual_download += 1
                self.logger.info(f'{filename} already downloaded')
                continue
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

    def get_img_urls(self, start_page=0):
        page = start_page
        while True:
            self.logger.info(f'get img urls. page {page}')
            try:
                post = self.session.get(
                    f'{self._API_URL}?limit={self.limit}&page={page}').json()
            except Exception as e:
                self.logger.info(f'{e}\nget img urls. page {page} failed')
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
            page += 1

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
        self.executor.submit(self.get_img_urls, self.start_page)
        for i in range(self.max_workers):
            self.executor.submit(self.down_image)


def main():
    import config
    proxies = None
    if config.proxy is not None:
        proxies = {'http': config.proxy, 'https': config.proxy}
    yandere = YandeRe(start_page=config.start_page,
                      end_page=config.end_page,
                      filepath=config.filepath,
                      proxies=proxies,
                      max_workers=config.max_workers,
                      max_retries=config.max_retries,
                      timeout=config.timeout,
                      quality=config.quality,
                      hproxy=config.hproxy)
    yandere.run()


if __name__ == '__main__':
    main()
