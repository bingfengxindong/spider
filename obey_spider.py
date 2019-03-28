# from lxml import etree
#
# import requests
# import random
# import time
# import ssl
# import json
# import csv
# import os
# import datetime
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
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"obey.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品位置","适合人群","产品页面编号","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://obeyclothing.com/collections/men-headwear?page=1",
#     "https://obeyclothing.com/collections/women-accessories/Hats",
# ]
# header = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "Upgrade-Insecure-Requests":"1",
#     }
#
# def obey(url,header):
#     response = requests.get(url=url,headers=header)
#     text = response.text
#     html = etree.HTML(text)
#     goods_urls = html.xpath("//div[@class='relative']/a/@href")
#     goods_next = html.xpath("//span[@class='next']/a/@href")
#     return {
#         "goods_urls":goods_urls,
#         "goods_next":goods_next,
#     }
#
# def obey_goods(goods_urls,goods_url,header,goods_page):
#     goods_url_m = "https://obeyclothing.com" + goods_url
#     goods_url_n = goods_url_m.split("?")[0] + ".js"
#
#     response_detail = requests.get(url=goods_url_n,headers=header)
#     text_detail = response_detail.text
#     dict_detail = json.loads(text_detail)
#
#     #产品名字
#     goods_name = dict_detail["title"]
#     # print(goods_name)
#
#     #产品价格
#     goods_price = "$%s"%str(dict_detail["price"]/100)
#     goods_discount_price = "$0"
#     # print(goods_price)
#     # print(goods_discount_price)
#
#     #产品颜色
#     goods_color = dict_detail["options"][0]["values"]
#     if goods_name == "This Fight Hat":
#         goods_color = [goods_color[0]]
#     # print(goods_color)
#
#     #产品尺寸
#     goods_size = dict_detail["options"][1]["values"]
#     # print(goods_size)
#
#     #产品描述
#     goods_details = dict_detail["description"].replace("\n","").replace("<li>","").split("</li>")[0:-2]
#     # print(goods_details)
#
#     #产品图片
#     goods_images = dict_detail["images"]
#     goods_images = ["https:"+i for i in goods_images]
#     # print(goods_images)
#     # print(len(goods_images))
#     goods_col = []
#     a_list = ["1","2","3","1-2","2-2"]
#     for i in goods_images:
#         a = i.split("_")[-1].split(".")[0]
#         if a not in a_list:
#             if i.split("_")[-2] in ["1","2"]:
#                 goods_col.append(i.split("_")[-3])
#             else:
#                 goods_col.append(i.split("_")[-1].split(".")[0])
#         else:
#             goods_col.append(i.split("_")[-2])
#     # print(goods_col)
#     goods_cols = []
#     for j in goods_col:
#         if j not in goods_cols:
#             goods_cols.append(j)
#     # print(goods_cols)
#     goods_image = []
#     for k in goods_cols:
#         goods_image.append([i for i in goods_images if k in i])
#     # print(goods_image)
#
#
#     #适合人群
#     if "men" in url and "women" not in url:
#         gender = "men"
#     elif "women" in url:
#         gender = "women"
#     # print(gender)
#
#     #产品型号
#     goods_model = dict_detail["description"].split(":")[1][0:-5].strip()
#     # print(goods_model)
#
#     #产品位置
#     goods_num = goods_urls.index(goods_url) + 1
#     # print(goods_num)
#
#     #产品url
#     ids = [i["id"] for i in dict_detail["variants"]]
#     g_urls = ["%s=%s"%(goods_url_m.split("=")[0],i) for i in ids]
#
#     goods_infos = []
#     for n in range(len(goods_color)):
#         goods_infos.append({
#             "goods_name": goods_name,
#             "goods_model": "%s-%s"%(goods_model,goods_color[n]),
#             "goods_price": goods_price,
#             "goods_discount_price": goods_discount_price,
#             "goods_color": goods_color[n],
#             "goods_size": goods_size,
#             "goods_details": goods_details,
#             "goods_images": goods_image[n],
#             "goods_num": goods_num,
#             "gender": gender,
#             "goods_url": g_urls[n],
#         })
#
#     print("*"*100)
#     for goods_info in goods_infos:
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
#             goods_info["goods_url"],
#         ))
#     print("%s抓取完成" % goods_name)
#
# #产品页面编号
# goods_page = 1
# for url in urls:
#     g_urls = []
#     while True:
#         goods_data = obey(url,header)
#         for goods_url in goods_data["goods_urls"]:
#             g_urls.append(goods_url)
#         if len(goods_data["goods_next"]) == 0:
#             break
#         else:
#             url = "https://obeyclothing.com%s"%goods_data["goods_next"][0]
#     for g_url in g_urls:
#         obey_goods(g_urls, g_url, header, goods_page)
#     goods_page += 1
