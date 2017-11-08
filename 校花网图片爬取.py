import requests
import re
from bs4 import BeautifulSoup

def getGrils(gril_url):
    main_url = 'http://www.xiaohuar.com'
    header = {'User-Agent':'Baiduspider'}
    res = requests.get(gril_url,headers=header,timeout=10)
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text,'html.parser')
    for images in soup.select('.item'):
        img_url = main_url + images.select('.item_t .img a img')[0]['src']
        houzhui = img_url[-4:]
        img_alt = images.select('.item_t .img a img')[0]['alt'] + houzhui
        print(img_alt)
        img = requests.get(img_url)
        with open('./res/'+img_alt,'wb') as f:
            f.write(img.content)
    print("ok")

def url_change():
    for i in range(19,44):
        url = 'http://www.xiaohuar.com/list-1-'+str(i)+'.html'
        getGrils(url)
url_change()

