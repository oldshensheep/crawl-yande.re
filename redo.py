# from gevent import monkey
#
# monkey.patch_all(thread=False)

import requests
import concurrent.futures
import queue
import random
import os

random.seed(1)

_API_URL = 'https://yande.re/post.json'

_q = queue.Queue(maxsize=256)
filepath = 'E:/ye'


def create_session():
    return requests.session()


session = create_session()
current_page = 0


def parse_config():
    pass


def speed():
    _q.qsize()


def get_img_urls(start, end, quality='jpeg', limit=100):
    global current_page
    for page in range(start, end):
        try:
            post = session.get(f'{_API_URL}?limit={limit}&page={page}').json()
            current_page = page
        except Exception as e:
            print(e)
            return
        file_map = {
            'original': lambda post_json: [(i['file_url'], i['id']) for i in post_json],
            'jpeg': lambda post_json: [(i['jpeg_url'], i['id']) for i in post_json],
            'sample': lambda post_json: [(i['sample_url'], i['id']) for i in post_json],
        }
        img_urls = file_map[quality](post)
        for img_url in img_urls:
            _q.put(img_url)
            print(img_url)


def down_image():
    global current_page
    while not _q.empty() or current_page != 100:
        url, id = _q.get()
        filename = f'{id}{os.path.splitext(url)[1]}'
        if os.path.exists(os.path.join(filepath, filename)):
            return
        try:
            image = session.get(url).content
        except Exception as e:
            print(e)
            return
        with open(os.path.join(filepath, filename), 'wb') as f:
            f.write(image)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(get_img_urls, 1, 100)
        for i in range(10):
            executor.submit(down_image)
