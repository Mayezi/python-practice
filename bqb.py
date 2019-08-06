from threading import Thread
import time
from queue import Queue

_url='https://fabiaoqing.com/biaoqing/lists/page/{}.html'
urlQueue = Queue()
# 将url放入queue中
for page in range(1,201):
    # print(_url.format(page))
    urlQueue.put(_url.format(page))

def fetchUrl(urlQueue):
    while True:
        try:
            url = urlQueue.get_nowait()
            qsize = urlQueue.qsize()
            print('{}==>{}'.format(url,qsize))
        except Exception as e:
            break
            print('Current Thread Name %s, Url: %s ' % (threading.currentThread().name, url))
        
        

if __name__ == '__main__':
    start_time = time.time()
    threads=[]
    # 线程数量
    thread_num = 1
    for i in range(thread_num):
        t = Thread(target=fetchUrl,args=(urlQueue,))
        threads.append(t)
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    end_time = time.time()
    print('done,cost',(end_time-start_time))            
             
