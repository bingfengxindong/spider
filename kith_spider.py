# from lxml import etree
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# import requests
# import random
# import time
# import csv
# import ssl
# import os
# import datetime
# import re
# import json
#
#
# def sleep_time():
#     """
#     睡眠0-2s之间的随机时间
#     :return:
#     """
#     ran_time = random.uniform(0,2)
#     # print(ran_time)
#     time.sleep(ran_time)
#
# path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
# if not os.path.exists(path):
#     os.makedirs(path)
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"kith.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品位置","适合人群","产品页面编号","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
#
# ssl._create_default_https_context = ssl._create_stdlib_context
# #主url
# urls = [
#     "https://kith.com/collections/accessories/headwear",
#     "https://kith.com/collections/kids-accessories",
# ]
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
#     }
#
# def data(dict_detail,goods_page,goods_url):
#     # 产品名字
#     goods_name = dict_detail["title"].split("-")[0].strip()
#     print(goods_name)
#     # 产品型号
#     goods_details = [i.strip("\n").strip("</p>") for i in dict_detail["description"].split("<p>")]
#     goods_details = [i for i in goods_details if i != ""]
#     goods_details = [i for i in goods_details if i != "\xa0"]
#     goods_details = [
#         i.replace("<span>\xa0</span>", " ").replace("\xa0", " ").replace("<span>", " ").replace("</span", " ").replace(
#             "&amp;", "").strip() for i in goods_details]
#     goods_model = goods_details[-3].split(":")[-1].strip()
#     # print(goods_model)
#     # 产品价格
#     print(dict_detail["price"],dict_detail["compare_at_price"])
#     goods_price = "$%s" % (int(dict_detail["price"]) / 100)
#     if dict_detail["compare_at_price"] == None:
#         goods_discount_price = "$0"
#     else:
#         goods_discount_price = "$%s" % (int(dict_detail["compare_at_price"]) / 100)
#     # print(goods_price,goods_discount_price)
#     # 产品颜色
#     goods_color = dict_detail["title"].split("-")[1].strip()
#     # print(goods_color)
#     # 产品尺寸
#     goods_sizes = dict_detail["options"][0]["values"]
#     # print(goods_sizes)
#     # 产品详情
#     # print(goods_details)
#     # 产品图片
#     goods_images = ["http:%s" % i for i in dict_detail["images"]]
#     # print(goods_images)
#     # 产品位置
#     goods_num = goods_json_urls.index(goods_json_url) + 1
#     # print(goods_num)
#     # 适合人群
#     if "mens" in dict_detail["tags"]:
#         gender = "men"
#     elif "kids" in dict_detail["tags"]:
#         gender = "kid"
#     # print(gender)
#     # "产品名字", "产品型号", "产品价格", "产品以前价格", "产品颜色", "产品尺寸", "产品详情", "产品图片", "产品位置", "适合人群"
#     goods_info = {
#         "goods_name": goods_name,
#         "goods_model": goods_model,
#         "goods_price": goods_price,
#         "goods_discount_price": goods_discount_price,
#         "goods_color": goods_color,
#         "goods_size": goods_sizes,
#         "goods_details": goods_details,
#         "goods_images": goods_images,
#         "goods_num": goods_num,
#         "gender": gender,
#     }
#     print(goods_info)
#     writer.writerow((
#         goods_info["goods_name"],
#         goods_info["goods_model"],
#         goods_info["goods_price"],
#         goods_info["goods_discount_price"],
#         goods_info["goods_color"],
#         goods_info["goods_size"],
#         goods_info["goods_details"],
#         goods_info["goods_images"],
#         goods_info["goods_num"],
#         goods_info["gender"],
#         goods_page,
#         goods_url,
#     ))
#     print("%s抓取完成" % goods_model)
#
# #产品页面编号
# goods_page = 1
# for url in urls:
#     response = requests.get(url=url,headers=headers)
#     text = response.text
#     html = etree.HTML(text)
#     goods_urls = html.xpath("//a[@class='product-card-info']/@href")
#     goods_json_urls = ["https://kith.com/products/%s.js"%i.split("/")[-1] for i in goods_urls]
#     header_detail = headers
#     for goods_json_url in goods_json_urls:
#         header_detail["referer"] = "https://kith.com/collections/accessories/products/%s"%goods_json_url.split("/")[-1].split(".")[0]
#         response_detail = requests.get(url=goods_json_url, headers=header_detail)
#         text_detail = response_detail.text
#         dict_detail = json.loads(text_detail)
#         goods_url = goods_json_url.split(".js")[0]
#         data(dict_detail,goods_page,goods_url)
#     goods_page += 1