from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

import requests
import random
import time
import ssl
import csv
import os
import datetime

path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"),"converse.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url","goods_type"))

ssl._create_default_https_context = ssl._create_stdlib_context

urls = [
    ["https://www.converse.com.cn/men-accessories/category.htm?attributeParams=&propertyCode=cap&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1","men","hats"],
    ["https://www.converse.com.cn/women-accessories/category.htm?attributeParams=&propertyCode=cap&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1", "women", "hats"],

    ["https://www.converse.com.cn/men-accessories/category.htm?attributeParams=&propertyCode=bag&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1", "men", "bags"],
    ["https://www.converse.com.cn/women-accessories/category.htm?attributeParams=&propertyCode=bag&size=&maxprice=&minprice=&sort=showOrder&rowsNum=&isPaging=false&pageNo=1","women","bags"],
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

def random_headers():
    ua = UserAgent(verify_ssl=False)
    return {'User-Agent': ua.random,}

def upload_html(text):
    with open("./1.html","w",encoding="utf-8") as f:
        f.write(text)

def goods_info(url):
    response = requests.get(url=url, headers=random_headers())
    text = response.text
    html = etree.HTML(text)
    return html

def goods_driver():
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    return driver

def goods_info_parse(u,goods_page):
    goods_gender = u[1]
    goods_type = u[2]
    url = u[0]
    html = goods_info(url)
    goods_names = html.xpath("//dd[@class='p-l-name']/a/text()")
    goods_prices = html.xpath("//dd[@class='p-l-price']/text()|//dd[@class='p-l-price linethrough']/text()")
    goods_urls = ["https://www.converse.com.cn{}".format(i) for i in html.xpath("//dd[@class='p-l-name']/a/@href")]
    for goods_url in goods_urls:
        sleep_time()
        info_html = goods_info(goods_url)
        goods_name = goods_names[goods_urls.index(goods_url)]
        goods_price = goods_prices[goods_urls.index(goods_url)]
        goods_model = info_html.xpath("//div[@class='product-info']/div/text()")[1].split(":")[1].strip()
        goods_color = info_html.xpath("//div[@class='product-info']/div/text()")[0].split(":")[1].strip()
        goods_sizes = ["all"]
        goods_details = info_html.xpath("//div[@class='product-description']/li/text()")
        goods_images = ["https:{}".format(i.replace("1S_NEW","1L_NEW")) for i in info_html.xpath("//div[@class='product-thumb-list']/a/@data-img")]

        goods_order = goods_urls.index(goods_url) + 1 + (int(url.split("&pageNo=")[-1]) - 1) * 12
        print(goods_name)

        writer.writerow((
            goods_name,
            goods_model,
            goods_price,
            "{}0".format(goods_price[0]),
            goods_color,
            goods_sizes,
            goods_details,
            goods_images,
            goods_order,
            goods_gender,
            goods_page,
            goods_url,
            goods_type,
        ))
    print(goods_type)

    if len(goods_urls) != 0:
        url = "{}&pageNo={}".format(url.split("&pageNo=")[0],int(url.split("&pageNo=")[-1]) + 1)
        goods_info_parse([url,goods_gender,goods_type],goods_page)

def main():
    for url in urls:
        goods_page = urls.index(url) + 1
        goods_info_parse(url,goods_page)

if __name__ == "__main__":
    main()