# from lxml import etree
#
# from urllib.parse import unquote
# import requests
# import random
# import time
# import ssl
# import os
# import datetime
# import csv
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
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"nike.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品标题","产品位置","适合人群","产品页面编号","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://store.nike.com/cn/zh_cn/pw/mens-hats-caps/7puZof1",
#     "https://store.nike.com/cn/zh_cn/pw/womens-hats-caps/7ptZof1",
#     # "https://store.nike.com/cn/zh_cn/pw/boys-hats-caps/7pvZof1",
#     # "https://store.nike.com/cn/zh_cn/pw/girls-hats-caps/7pwZof1",
# ]
#
# header = {
#     "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.12 Safari/537.36",
#     "Upgrade-Insecure-Requests":"1",
#     }
#
# ips = [
#     '221.6.201.18:9999',
#     '113.200.56.13:8010',
#     '101.37.79.125:3128',
#     '171.221.239.11:808',
#     '202.112.237.102:3128',
#     '106.12.32.43:3128',
# ]
#
# def data(html_detail):
#     # 产品名字
#     goods_name = html_detail.xpath("//h1[@class='fs26-sm fs28-lg']/text()|//h1[@class='exp-product-title nsg-font-family--platform']/text()")[0]
#     # print(goods_name)
#     # 产品型号
#     goodsmodel = html_detail.xpath("//li[@class='description-preview__style-color ncss-li']/text()|//span[@class='exp-style-color']/text()")[0]
#     if ": " in goodsmodel:
#         goods_model = goodsmodel.split(": ")[1]
#     elif "： " in goodsmodel:
#         goods_model = goodsmodel.split("： ")[1]
#     # print(goods_model)
#     # 产品价格
#     goods_price = html_detail.xpath("//div[@class='text-color-black']/text()|//span[@class='exp-pdp-local-price js-pdpLocalPrice']/text()|//div[@class='mb-1-sm text-color-black']/text()")[0]
#     goodsdiscount_price = html_detail.xpath("//div[@class='text-color-grey u-strikethrough']/text()")
#     if len(goodsdiscount_price) != 0:
#         goods_discount_price = goodsdiscount_price[0]
#     else:
#         goods_discount_price = "￥0"
#     # print(goods_price,goods_discount_price)
#     # 产品颜色
#     goodscolor = html_detail.xpath("//li[@class='description-preview__color-description ncss-li']/text()|//span[@class='colorText']/text()")[0]
#     if "：" in goodscolor:
#         goods_color = goodscolor.split("： ")[1]
#     else:
#         goods_color = goodscolor
#     # print(goods_color)
#     # 产品尺寸
#     goods_size = ["all"]
#     # print(goods_size)
#     # 产品描述
#     goods_details = html_detail.xpath("//div[@class='pi-pdpmainbody']/p/b/text()|//div[@class='pi-pdpmainbody']/p/text()|//div[@class='pi-pdpmainbody']/ul/li/text()")
#     # print(len(goods_details),goods_details)
#     # 产品图片
#     goodsimages = html_detail.xpath("//img[@class='css-10f9kvm u-full-width u-full-height']/@src|//ul[@class='exp-pdp-alt-images-carousel']/li/img/@data-large-image")
#     goods_images = [i for i in goodsimages if "t_PDP_LOADING_v1" not in i]
#     # print(len(goods_images),goods_images)
#     #特点
#     goods_title = html_detail.xpath("//h2[@class='fs16-sm pb1-sm']/text()|//h2[@class='exp-product-subtitle nsg-font-family--platform']/text()")[0]
#     # print(goods_title)
#
#     return {
#         "goods_name":goods_name,
#         "goods_model":goods_model,
#         "goods_price":goods_price,
#         "goods_discount_price":goods_discount_price,
#         "goods_color":goods_color,
#         "goods_size":goods_size,
#         "goods_details":goods_details,
#         "goods_images":goods_images,
#         "goods_title":goods_title,
#     }
#
# #产品页面编号
# goods_page = 1
# for url in urls:
#     proxy = {
#         'https': ips[urls.index(url)]
#     }
#     # print(proxy)
#     print(url)
#     response = requests.get(url=url, headers=header,proxies=proxy)
#     text = response.text
#     html = etree.HTML(text)
#     goods_cn_names = html.xpath("//p[@class='product-subtitle nsg-font-family--base edf-font-size--regular nsg-text--medium-grey']/text()")
#     goods_urls = html.xpath("//div[@class='grid-item-image']/div/a/@href")
#
#     # 适合人群
#     gender = unquote(url.split("/")[-2].split("-")[0], "utf-8")
#     # print(gender)
#
#     for i in range(0,len(goods_cn_names)):
#         # if ("头带" not in goods_cn_names[i]) and ("发带" not in goods_cn_names[i]) and ("婴童套装" not in goods_cn_names[i]):
#         print(goods_urls[i])
#         response_detail = requests.get(url=goods_urls[i],headers=header,proxies=proxy)
#         text_detail = response_detail.text
#         html_detail = etree.HTML(text_detail)
#
#         a_list = html_detail.xpath("//a[@class='colorway-anchor']/@href")
#         # print(a_list)
#         # 产品顺序
#         goods_num = i + 1
#         # print(goods_num)
#
#         goods_infos = []
#         if len(a_list) == 0:
#              goods_info = data(html_detail)
#              goods_info["goods_num"] = goods_num
#              goods_info["gender"] = gender
#              goods_info["a_url"] = goods_urls[i]
#              goods_infos.append(goods_info)
#              # print(goods_info)
#         else:
#             for a_url in a_list:
#                 response_detail_a = requests.get(url=a_url, headers=header,proxies=proxy)
#                 text_detail_a = response_detail_a.text
#                 html_detail_a = etree.HTML(text_detail_a)
#                 goods_info = data(html_detail_a)
#                 goods_info["goods_num"] = goods_num
#                 goods_info["gender"] = gender
#                 goods_info["a_url"] = a_url
#                 goods_infos.append(goods_info)
#                 print(goods_info)
#
#         print(goods_infos)
#         # "产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品标题","产品位置","适合人群"
#         for goods_info_save in goods_infos:
#             writer.writerow((
#                 goods_info_save["goods_name"],
#                 goods_info_save["goods_model"],
#                 goods_info_save["goods_price"],
#                 goods_info_save["goods_discount_price"],
#                 goods_info_save["goods_color"],
#                 goods_info_save["goods_size"],
#                 goods_info_save["goods_details"],
#                 goods_info_save["goods_images"],
#                 goods_info_save["goods_title"],
#                 goods_info_save["goods_num"],
#                 goods_info_save["gender"],
#                 goods_page,
#                 goods_info_save["a_url"],
#             ))
#         print(gender,"*****"*20)
#     goods_page += 1