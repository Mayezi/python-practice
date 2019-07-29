import requests
from bs4 import BeautifulSoup
# 图片地址
dest_url = r'https://colorhub.me/search?tag=%E4%B8%AD%E5%9B%BD'
r = requests.get(dest_url)
soup = BeautifulSoup(r.text,'html.parser')
# 链接
hrefs = [i.find('a')['href'] for i in soup.find_all('div',class_='card')];
# 标题
titles = [i.find('a')['title'] for i in soup.find_all('div',class_='card')];
for href,title in zip(hrefs,titles):
    res = requests.get(href)
    soup_res = BeautifulSoup(res.text,'html.parser')
    src = soup_res.find('img',class_="card-img-top")['src']
    pic_response=requests.get('https:'+src)
    # 下载保存图片
    with open(title + '.jpg', mode='wb') as fn:
        print('正在下载',title+'.jpg')
        fn.write(pic_response.content)
