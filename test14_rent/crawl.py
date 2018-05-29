#coding:utf-8


from bs4 import BeautifulSoup
from urlparse import urljoin
import requests
import csv

url = 'http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_2200'

#已完成的页数序号，初始为0
page = 0

csv_file = open("rent.csv","wb")
#创建write对象，指定文件与分隔符
csv_writer = csv.writer(csv_file,delimiter=',')

while True:
    page+=1
    print "fetch: ",url.format(page=page)
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text,'lxml')
    house_list = html.select("ul.list > li")


    #循环在读不到新房源时结束
    if not house_list:
        break

    for house in house_list:
        #得到标签内的文本
        house_title = house.select("h2")[0].string.encode('utf8').split('】')[1]
        #得到标签内的属性值
        house_url = urljoin(url,house.select("a")[0]["href"])
        house_info_list = house_title.split()

        #如果第二列是公寓名则取第一列作为地址
        if "公寓" in house_info_list[1]:
            house_location = house_info_list[0]
        else:
            house_location = house_info_list[1]

        house_money = house.select(".money")[0].select("b")[0].string.encode('utf8')
        csv_writer.writerow([house_title,house_location,house_money,house_url])

csv_file.close()