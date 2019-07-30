from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains

import requests
import random
import time
import ssl
import csv
import os
import datetime
import re

#eu

def file_csv():
    path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
    if not os.path.exists(path):
        os.makedirs(path)
    file = open(os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"),"vans.csv"),"w+",encoding="utf-8",newline="")
    writer = csv.writer(file)
    writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url","goods_type"))
    return writer

ssl._create_default_https_context = ssl._create_stdlib_context

urls = [
    ["https://www.vans.com/shop/mens-accessories-hats-snapbacks","mens","hats"],
    ["https://www.vans.com/shop/womens-accessories-hats","womens","hats"],
    ["https://www.vans.com/shop/kids-boys-accessories-hats","boys","hats"],
    ["https://www.vans.com/shop/mens-accessories-backpacks-bags", "mens", "bags"],
    ["https://www.vans.com/shop/womens-accessories-backpacks-bags", "womens", "bags"],
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

def random_headers():
    ua = UserAgent(verify_ssl=False)
    return {'User-Agent': ua.random,}

def upload_html(text):
    with open("./1.html","w",encoding="utf-8") as f:
        f.write(text)

def goods_parse_html(driver):
    # 获取页面源码
    pagesource = driver.page_source
    html = etree.HTML(pagesource)
    return html

def goods_info_html(url):
    response = requests.get(url=url, headers=random_headers())
    text = response.text
    html = etree.HTML(text)
    return html

def goods_json_text(url):
    response = requests.get(url=url, headers=random_headers())
    text = response.text
    return text

def text_html(text):
    return etree.HTML(text)

def goods_driver():
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    return driver

def goods_info_parse(u,goods_page,writer):
    url = u[0]
    goods_gender = u[1]
    goods_type = u[2]
    goods = goodss(url)
    for g in goods:
        g_text = etree.tostring(g,encoding="utf-8")
        g_html = text_html(g_text)
        goods_name = g_html.xpath("//span[@class='product-block-name-wrapper']/text()")[0]
        goods_price = g_html.xpath("//span[@class='product-block-price product-block-offer-price offer-price product-price-amount-js']/text()")[0].replace("\n","").replace("\t","").strip()
        goods_url = g_html.xpath("//a[@class='product-block-name-link']/@href")[0]
        g_info_html = goods_info_html(goods_url)
        goods_model = g_info_html.xpath("//button[@class='attr-box selected ']/img/@id|//button[@class='attr-box selected clicked']/img/@id")[0]
        goods_color = g_info_html.xpath("//span[@class='product-content-form-attr-selected attr-selected attribute-label-value attribute-label-value-js attr-selected-color-js']/text()")[0]
        goods_sizes = g_info_html.xpath("//select[@id='attr-size']/option/text()")[1:]
        goods_details = [i.replace("\n","").replace("\t","").strip() for i in g_info_html.xpath("//div[@id='product-detail-1']/text()")]
        gimg_url = "https://images.vans.com/is/image/Vans/{}_is?req=set,json,UTF-8&labelkey=label".format(goods_model.split("-")[0])
        goods_images = re.findall(r'{"i":{"n":"(.*?)"}',goods_json_text(gimg_url))
        goods_images = ["https://images.vans.com/is/image/Vans/{}?fit=constrain,1&wid=1080&hei=1080&fmt=jpg&$VFDP-VIEWER-THUMBNAIL$".format(i.split("/")[1]) for i in goods_images]
        goods_num = goods.index(g) + 1
        print(goods_name)
        writer.writerow((
            goods_name,
            goods_model,
            goods_price,
            "$0",
            goods_color,
            goods_sizes,
            goods_details,
            goods_images,
            goods_num,
            goods_gender,
            goods_page,
            goods_url,
            goods_type,
        ))

def goodss(url):
    driver = goods_driver()
    sleep_time()
    driver.get(url)
    sleep_time()
    js = "var q=document.documentElement.scrollTop=100000"
    for i in range(10):
        driver.execute_script(js)
        sleep_time()
    html = goods_parse_html(driver)
    driver.close()
    goodss = html.xpath("//div[@class='product-block product-block-js ']")
    return goodss

def main():
    writer = file_csv()
    for url in urls:
        goods_page = urls.index(url) + 1
        goods_info_parse(url,goods_page,writer)

if __name__ == "__main__":
    main()