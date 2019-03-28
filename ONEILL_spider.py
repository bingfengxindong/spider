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
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"ONEILL.csv"),"w+",encoding="utf-8",newline="")
# writer = csv.writer(file)
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
# #主url
# urls = [
#     "https://us.oneill.com/collections/mens-hats?page=1",
#     "https://us.oneill.com/collections/womens-hats",
#     "https://us.oneill.com/collections/boys-8-14-accessories",
#     "https://us.oneill.com/collections/girls-7-14-accessories",
#     # "https://us.oneill.com/collections/mens-sale-accessories?page=1",
#     # "https://us.oneill.com/collections/womens-sale-accessories",
#     # "https://us.oneill.com/collections/mens-tees",
#
# ]
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
#     }
#
# def oneill(url,headers):
#     response = requests.get(url=url,headers=headers)
#     text = response.text
#     html = etree.HTML(text)
#     goods_urls = html.xpath("//a[@class='product_img_link']/@href")
#     headers_detail = headers
#     headers_detail["referer"] = url
#     goods_next = html.xpath("//li[@class='pagination_next']/a/@href")
#     return {
#         "goods_urls":goods_urls,
#         "headers_detail":headers_detail,
#         "goods_next":goods_next,
#     }
#
# def oneill_goods(url,goods_urls,goods_url,headers_detail,goods_page):
#     sleep_time()
#     # print(goods_url)
#     #产品顺序
#     goods_num = goods_urls.index(goods_url) + 1
#
#     goods_url = "https://us.oneill.com%s" % goods_url
#     response_detail = requests.get(url="%s.json" % goods_url.split("?")[0], headers=headers_detail)
#     text_detail = response_detail.text
#     dict_detail = json.loads(text_detail)
#     if "hats" in dict_detail["product"]["tags"] or "HAT" in dict_detail["product"]["tags"] or "HAT" in dict_detail["product"]["title"]:
#         #产品名字
#         goods_name = dict_detail["product"]["title"]
#         # print(goods_num,goods_name)
#         #产品型号
#         goods_model = dict_detail["product"]["variants"][0]["sku"]
#         # print(goods_model)
#         #产品价格
#         goods_price = "$%s"%dict_detail["product"]["variants"][0]["price"]
#         goods_discount_price = dict_detail["product"]["variants"][0]["compare_at_price"]
#         if goods_discount_price == None:
#             goods_discount_price = "$0"
#         else:
#             goods_discount_price = "$%s"%goods_discount_price
#         # print(goods_price,goods_discount_price)
#         #产品颜色
#         goods_color = dict_detail["product"]["options"][1]["values"][0]
#         # print(goods_color)
#         #产品尺码
#         goods_sizes = dict_detail["product"]["options"][0]["values"]
#         # print(goods_sizes)
#         #产品详情
#         goods_detail = dict_detail["product"]["body_html"]
#         goods_detail_html = etree.HTML(goods_detail)
#         goods_details = [i.replace("'","-").replace('"',"").replace("\xa0"," ") for i in goods_detail_html.xpath("//li/text()")]
#         if "\n" in goods_details:
#             goods_details.remove("\n")
#         print(goods_details)
#         #产品图片
#         goods_images = [i["src"] for i in dict_detail["product"]["images"]]
#         # print(goods_images)
#         #产品顺序
#         # print(goods_num)
#         #适合人群
#         # gender = dict_detail["product"]["product_type"]
#         gender = url.split("/")[-1].split("-")[0]
#         print(gender)
#
#         # "产品名字", "产品型号", "产品价格", "产品以前价格", "产品颜色", "产品尺寸", "产品详情", "产品图片", "产品标题", "适合人群"
#         goods_info = {
#             "goods_name": goods_name,
#             "goods_model": goods_model,
#             "goods_price": goods_price,
#             "goods_discount_price": goods_discount_price,
#             "goods_color": goods_color,
#             "goods_size": goods_sizes,
#             "goods_details": goods_details,
#             "goods_images": goods_images,
#             "goods_num": goods_num,
#             "gender": gender,
#         }
#         print(goods_info)
#         writer.writerow((
#             goods_info["goods_name"],
#             goods_info["goods_model"],
#             goods_info["goods_price"],
#             goods_info["goods_discount_price"],
#             goods_info["goods_color"],
#             goods_info["goods_size"],
#             goods_info["goods_details"],
#             goods_info["goods_images"],
#             goods_info["goods_num"],
#             goods_info["gender"],
#             goods_page,
#             goods_url,
#         ))
#         print("%s抓取完成" % goods_model)
#
# #产品页面编号
# goods_page = 1
# for url in urls:
#     g_urls = []
#     while True:
#         print(url,goods_page)
#         goods_data = oneill(url,headers)
#         for goods_url in goods_data["goods_urls"]:
#             g_urls.append(goods_url)
#         if len(goods_data["goods_next"]) == 0:
#             break
#         else:
#             url = "https://us.oneill.com%s" % goods_data["goods_next"][0]
#         headers_detail = goods_data["headers_detail"]
#     print(len(g_urls))
#     for g_url in g_urls:
#         oneill_goods(url,g_urls,g_url,headers_detail,goods_page)
#     goods_page += 1