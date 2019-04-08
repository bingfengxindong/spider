from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains

import requests
import random
import time
import csv
import ssl
import os
import datetime
import re


def sleep_time():
    """
    睡眠0-2s之间的随机时间
    :return:
    """
    ran_time = random.uniform(0,2)
    # print(ran_time)
    time.sleep(ran_time)

path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"stussy.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context
#主url
urls = [
    # "https://www.stussy.com/us/mens/tees",
    # "https://www.stussy.com/us/mens/long-sleeve-tees",
    # "https://www.stussy.com/us/mens/shirts",
    # "https://www.stussy.com/us/mens/hoodies-sweaters",
    # "https://www.stussy.com/us/mens/jackets",
    # "https://www.stussy.com/us/womens/tees",
    # "https://www.stussy.com/us/womens/shirts",
    # "https://www.stussy.com/us/womens/hoodies-sweaters",
    # "https://www.stussy.com/us/womens/jackets",
    # "https://www.stussy.com/us/womens/dresses",
    "https://www.stussy.com/us/accessories/hats-beanies",
]
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
for url in urls:
    response = requests.get(url=url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    headers_detail = headers
    headers_detail["referer"] = url
    # 适合人群
    gender = url.split("us/")[-1].split("/")[0]
    if gender == "accessories":
        gender = "all"
    goods_page = urls.index(url) + 1
    #爬去每个帽子详情的url
    goods_urls = html.xpath("//ul[@class='product-swatch-information']/li[1]/a/@href")

    for goods_url in goods_urls:
        # if goods_url.split("?")[1].split("=")[0] == "color_hat":
        #产品顺序
        goods_num = goods_urls.index(goods_url) + 1
        driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
        driver.get(goods_url)
        pagesource = driver.page_source
        html_detail = etree.HTML(pagesource)
        #产品名字
        goods_name = html_detail.xpath("//h1[@itemprop='name']/text()")[0].strip("\\n").strip()
        #产品价格
        goods_price = html_detail.xpath("//span[@class='price d-inline']/text()")
        if goods_price == []:
            goods_price = html_detail.xpath("//span[@class='price d-none']/text()")
            if goods_price == []:
                goods_price = html_detail.xpath("//span[@class='price']/text()")
            else:
                goods_price = goods_price[0]
        else:
            goods_price = goods_price[0]
        goods_discount_price = "$0"
        #产品颜色
        colors = html_detail.xpath("//span[@class='swatch-img']/@title")
        #产品型号
        goods_model = html_detail.xpath("//label[@class='option-label active']/@for|//label[@class='option-label inactive']/@for")
        goods_models = []
        for gm_i in range(len(goods_model)):
            goods_models.append("%s-%s-%s"%(goods_url.split("?")[0].split("/")[-1],goods_model[gm_i].split("-")[-1],colors[gm_i].lower()))
        #产品尺寸
        goods_size = html_detail.xpath("//label[@class='option-label inactive available']/span/text()|//label[@class='option-label inactive unavailable']/span/text()")
        if goods_size == []:
            goods_size = ["all"]
        #产品描述
        goods_details = html_detail.xpath("//div[@itemprop='description']/ul/li/text()")
        #产品图片
        goods_images = []
        for g_model in goods_model:
            img_xpath = "//ul[@id='product-gallery-%s']/div/div/li/img[@class='product-hero-image']/@src"%g_model.split("-")[-1]
            g_images = html_detail.xpath(img_xpath)
            goods_images.append(g_images)
        driver.close()
        # "产品名字", "产品型号", "产品价格", "产品以前价格", "产品颜色", "产品尺寸", "产品详情", "产品图片", "产品标题", "适合人群"
        for col_i in range(len(colors)):
            goods_info = {
            "goods_name": goods_name,
            "goods_model": goods_models[col_i],
            "goods_price": goods_price,
            "goods_discount_price": goods_discount_price,
            "goods_color": colors[col_i],
            "goods_size": goods_size,
            "goods_details": goods_details,
            "goods_images": goods_images[col_i],
            "goods_num": goods_num,
            "gender": gender,
            }
            print(goods_info)
            writer.writerow((
                goods_info["goods_name"],
                goods_info["goods_model"],
                goods_info["goods_price"],
                goods_info["goods_discount_price"],
                goods_info["goods_color"],
                goods_info["goods_size"],
                goods_info["goods_details"],
                goods_info["goods_images"],
                goods_info["goods_num"],
                goods_info["gender"],
                goods_page,
                goods_url,
            ))
            print("%s抓取完成" % goods_model)