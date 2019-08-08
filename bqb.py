import os
import threading
import time
from queue import LifoQueue
import requests
from bs4 import BeautifulSoup
import re

def download_bqb(url,qsize):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_list = soup.find_all('img', class_='ui image lazy')
    for img in img_list:
        image = img.get('data-original')
        # 去除标题中的特殊字符，windows下建立文件会出错
        title = re.sub(r'[\\/:?<>|*]','',img.get('title'))
        try:
            with open('images/' + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print(title + '下载异常，源地址：' + image)
            break

def fetchUrl(urlQueue):
    while True:
        try:
            url = urlQueue.get_nowait()
            qsize = urlQueue.qsize()
            print(' %s 开始下载, Url: %s ，剩余页数: %s' % (threading.currentThread().name, url, qsize))
            download_bqb(url,qsize)
        except Exception as e:
            break
        print(' %s 下载完成, Url: %s ' % (threading.currentThread().name, url))

if __name__ == '__main__':
    # 表情包网址
    _url = 'https://fabiaoqing.com/biaoqing/lists/page/{}.html'
    urlQueue = LifoQueue()
    # 将url放入queue中
    for page in range(1, 201):
        # print(_url.format(page))
        urlQueue.put(_url.format(page))

    start_time = time.time()
    threads = []
    # 线程数量
    thread_num = 10
    # 开启线程
    for i in range(thread_num):
        t = threading.Thread(target=fetchUrl, args=(urlQueue,))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    end_time = time.time()
    print('done,cost', (end_time - start_time))

