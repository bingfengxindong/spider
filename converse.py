from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

import requests
import random
import time
import ssl
import csv
import os
import datetime

path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"thenorthface.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context

urls = [
    "https://www.converse.com.cn/men-accessories/category.htm?attributeParams=&propertyCode=cap&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1",
    "https://www.converse.com.cn/women-accessories/category.htm?attributeParams=&propertyCode=cap&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1",
]


# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Upgrade-Insecure-sRequests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
# }

headers_list = [
    {"User-Agent":"User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"},
    {"User-Agent":"User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"},
    {"User-Agent":"User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"},
    {"User-Agent":"User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    {"User-Agent":"User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"},
]

ips = [
    '221.6.201.18:9999',
    '113.200.56.13:8010',
    '101.37.79.125:3128',
    '171.221.239.11:808',
    '202.112.237.102:3128',
    '106.12.32.43:3128',
]

def sleep_time():
    """
    睡眠0-2s之间的随机时间
    :return:
    """
    ran_time = random.uniform(0,1)
    time.sleep(ran_time)

# 输入毫秒级的时间，转出正常格式的时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
    return otherStyleTime

def goods_parse(driver):
    # 获取页面源码
    pagesource = driver.page_source
    html = etree.HTML(pagesource)
    return html

def goods_info(url):
    headers = headers_list[random.randint(0,5)]
    response = requests.get(url=url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    return html

def goods_driver():
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    return driver

def goods_info_parse(url):
    html = goods_info(url)
    goods_names = html.xpath("//dd[@class='p-l-name']/a/text()")
    goods_prices = html.xpath("//dd[@class='p-l-price']/text()")
    goods_urls = ["https://www.converse.com.cn{}".format(i) for i in html.xpath("//dd[@class='p-l-name']/a/@href")]
    for goods_url in goods_urls:
        sleep_time()
        info_html = goods_info(goods_url)
        goods_color = info_html.xpath("//div[@class='product-info']/div/text()")
        print(goods_color)
    if len(goods_urls) != 0:
        url = "{}&pageNo={}".format(url.split("&pageNo=")[0],int(url.split("&pageNo=")[-1]) + 1)
        goods_info_parse(url)

def main():
    for url in urls:
        goods_info_parse(url)

if __name__ == "__main__":
    main()