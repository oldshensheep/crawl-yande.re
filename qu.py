import queue
import threading
import time
import concurrent.futures

q = queue.Queue(maxsize=10)


def Producer(name):
    count = 1
    while True:
        q.put("包子 %s" % count)
        print("做了包子", count)
        count += 1
        time.sleep(0.5)


def Consumer(name):
    while True:
        print("[%s] 取到[%s] 并且吃了它..." % (name, q.get()))
        time.sleep(1)


p = threading.Thread(target=Producer, args=("Lily",))
c = threading.Thread(target=Consumer, args=("Lilei",))
c1 = threading.Thread(target=Consumer, args=("Ahi",))

p.start()
c.start()
c1.start()
