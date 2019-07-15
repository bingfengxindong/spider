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
import json


def sleep_time():
    """
    睡眠0-2s之间的随机时间
    :return:
    """
    ran_time = random.uniform(0,2)
    # print(ran_time)
    time.sleep(ran_time)

path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"),"underarmour_zh.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context
#主url
urls = [
    # "https://www.underarmour.cn/cmens-accessories-headwear/#11|Mens|Accessories|Headwear|4-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-longsleeve/#11|Mens|Tops|Longsleeve|2-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-hoody/#11|Mens|Tops|Hoody|3-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-outwear/#11|Mens|Tops|Outwear|4-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-shortsleeve/#11|Mens|Tops|Shortsleeve|5-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-sleeveless/#11|Mens|Tops|Sleeveless|6-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cmens-tops-polo/#11|Mens|Tops|Polo|7-MensCategory-MensCategory",
    "https://www.underarmour.cn/cmens-accessories-bag/#11|Mens|Accessories|Bag|3-MensCategory-MensCategory",
    # "https://www.underarmour.cn/cwomens-accessories-headwear/#11|Womens|Accessories|Headwear|4-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-longsleeve/#11|Womens|Tops|Longsleeve|2-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-hoody/#11|Mens|Tops|Hoody|3-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-outwear/#11|Womens|Tops|Outwear|4-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-sportbra/#11|Womens|Tops|SportsBras|5-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-shortsleeve/#11|Womens|Tops|Shortsleeve|6-WomensCategory",
    # "https://www.underarmour.cn/cwomens-tops-sleeveless/#11|Womens|Tops|Sleeveless|7-WomensCategory",
    "https://www.underarmour.cn/cwomens-accessories-bag/#11|Womens|Accessories|Bag|3-WomensCategory",
]
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
#产品页面编号
goods_page = 1
for url in urls:
    sleep_time()
    response = requests.get(url=url,headers=headers)
    text = response.text
    html = etree.HTML(text)
    #性别
    sex = url.split("/")[3].split("-")[0].strip("c").strip("s")
    #产品id
    goods_ids = html.xpath("//div[@class='good-con']/div/a/@id")
    #产品编号
    goods_nums = [i.split("-")[0].strip("/p") for i in html.xpath("//a[@class='good-txt']/@href")]
    # print(len(goods_nums),goods_nums)
    #产品详情url
    goods_urls = ["https://www.underarmour.cn/p%s.htm"%i for i in goods_ids]
    header_detail = headers
    header_detail["referer"] = url.split("/#")[0]
    for goods_url in goods_urls:
        sleep_time()
        response_detail = requests.get(url=goods_url, headers=header_detail)
        text_detail = response_detail.text
        html_detail = etree.HTML(text_detail)
        # 产品名字
        goods_name = html_detail.xpath("//div[@class='product-title']/h1/text()")[0]
        # print(goods_name)
        # 产品型号
        goods_model = "STYLE#%s"%goods_url.split("p")[-1].split(".")[0]
        # print(goods_model)
        # 产品价格
        goods_price = html_detail.xpath("//div[@class='product-price']/span/text()")[0].strip()
        goods_discount_price = "￥0"
        # print(goods_price,goods_discount_price)
        # 产品颜色
        goods_color = html_detail.xpath("//div[@class='product-color']/p[@class='none-sm']/text()")[0].split()[1]
        # print(goods_color)
        # 产品尺码
        goods_sizes = html_detail.xpath("//ul[@class='float-clearfix']/li/@title")
        # print(goods_sizes)
        # 产品详情
        goods_details = html_detail.xpath("//div[@class='descr-text']/div/span/text()|//div[@class='descr-text']/div/ul/li/text()")
        # print(goods_details)
        # 产品图片
        goods_images = html_detail.xpath("//input[@class='mediavimg']/@value")
        if goods_images[0].split("//")[0] == "":
            goods_images = ["https:%s"%i for i in goods_images]
        # print(goods_images)
        # 适合人群
        gender = sex
        # print(gender)
        # 产品顺序
        goods_num = goods_nums.index(goods_model.split("#")[-1].split("-")[0]) + 1
        # print(goods_num)

        # "产品名字", "产品型号", "产品价格", "产品以前价格", "产品颜色", "产品尺寸", "产品详情", "产品图片", "产品标题", "适合人群"
        goods_info = {
            "goods_name": goods_name,
            "goods_model": goods_model,
            "goods_price": goods_price,
            "goods_discount_price": goods_discount_price,
            "goods_color": goods_color,
            "goods_size": goods_sizes,
            "goods_details": goods_details,
            "goods_images": goods_images,
            "goods_num": goods_num,
            "gender": gender,
        }
        # print(goods_name)
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

    goods_page += 1