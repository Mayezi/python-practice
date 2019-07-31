import os
import requests
from bs4 import BeautifulSoup

path='images/'
url='https://fabiaoqing.com/biaoqing/lists/page/{}.html'
urls=[url.format(i) for i in range(1,200)]
for page,i in enumerate(urls):
    response = requests.get(i)
    soup = BeautifulSoup(response.content, 'html.parser')
    img_list = soup.find_all('img', class_='ui image lazy')
    print('开始下载第{}页'.format(page+1))
    for img in img_list:
        image = img.get('data-original')
        title = img.get('title').replace('?', ' ').replace(':', '')
        try:
            with open(path + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print(title+'下载异常，源地址：'+image)
            break
