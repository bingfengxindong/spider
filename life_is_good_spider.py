# from lxml import etree
#
# import requests
# import random
# import time
# import csv
# import ssl
# import os
# import datetime
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
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"life_is_good.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品位置","适合人群","产品页面编号","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
# #主url
# url = "https://www.lifeisgood.com/sale/accessories/hats-and-headwear/"
# headers = {
#     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
#     }
# response = requests.get(url=url,headers=headers)
# text = response.text
# html = etree.HTML(text)
# #爬去每个帽子详情的url
# goods_urls = html.xpath("//li[@class='grid-tile']/div[@class='product-tile large']/div[@class='product-image']/a/@href")
#
# #爬取详情页面
# headers_detail = headers
# headers_detail["referer"] = url
# headers_detail["upgrade-insecure-requests"] = "1"
# for goods_url in goods_urls:
#     sleep_time()
#     response_detail = requests.get(url=goods_url,headers=headers_detail)
#     text_detail = response_detail.text
#     html_detail = etree.HTML(text_detail)
#
#     #产品名字
#     goods_name = html_detail.xpath("//h1/text()")[0]
#     # print(goods_name)
#     # if goods_name == "LIG Mountains Chill Cap":
#     #     with open("./1.html","w",encoding="utf-8") as f:
#     #         f.write(text_detail)
#     # print(goods_name)
#     #产品型号
#     goods_model = html_detail.xpath("//span[@itemprop='productID']/text()")[0]
#     # print(goods_model)
#
#     #产品价格
#     # goods_price = ""
#     # if len(html_detail.xpath("//div[@class='product-price']/span/text()")) == 1:
#     #     goods_price = html_detail.xpath("//div[@class='product-price']/span/text()")[0]
#     # elif len(html_detail.xpath("//div[@class='product-price']/div/text()")) == 1:
#     #     goods_price = html_detail.xpath("//div[@class='product-price']/div/text()")[0].strip()
#     # goods_discount_price = "$0"
#     goods_price = html_detail.xpath("//span[@class='price-sales']/text()")
#     goods_discount_price = html_detail.xpath("//span[@class='price-standard']/text()")
#     if goods_price == []:
#         goods_price = [i.replace("\n", "") for i in html_detail.xpath("//div[@class='product-price']/div/text()") if i.replace("\n", "") != ""]
#     if goods_discount_price == []:
#         goods_discount_price = ["$0"]
#     # print(goods_price)
#     goods_price = goods_price[0]
#     goods_discount_price = goods_discount_price[0]
#     # print(goods_price)
#     # print(goods_discount_price)
#
#     #产品颜色
#     goods_color = html_detail.xpath("//span[@class='selected-value']/text()")[0]
#     goods_colors = []
#     goods_colors.append(goods_color)
#     # print(goods_color)
#
#     #产品尺寸
#     goods_size = ""
#     goods_content = html_detail.xpath("//div[@class='product-variations']/ul/li/span")
#     if len(goods_content) == 4:
#         goods_sizes = html_detail.xpath("//div[@class='product-variations']/ul/li/span/text()")[3]
#         goods_size = []
#         goods_size.append(goods_sizes)
#     elif len(goods_content) == 3:
#         goods_sizes = html_detail.xpath("//div[@class='product-variations']/ul/li/div[@class='value']/ul/li/a/text()")
#         goods_size = []
#         for i in goods_sizes:
#             goods_size.append(i.strip())
#     # print(goods_name,goods_size,goods_price,goods_discount_price)
#
#     #产品描述
#     goods_det1 = html_detail.xpath("//div[@class='product-description']/p/text()")
#     goods_det2 = html_detail.xpath("//div[@class='product-description']/ul/li/text()")
#     # goods_det2.insert(0,goods_det1)
#     goods_detail = goods_det1 + goods_det2
#     # print(goods_detail)
#
#     #产品图片
#     # goods_image = []
#     # goods_images = []
#     # goods_img = html_detail.xpath("//ul[@class='slides']/li/a/img/@src")[0:2]
#     goods_images = [eval(i)["url"] for i in html_detail.xpath("//ul[@class='slides']/li/a/img/@data-lgimg")[0:2]]
#     # for k in goods_img:
#     #     goods_images.append(k)
#     #     print(k)
#     # goods_image.append(goods_images)
#
#     # print(goods_images)
#
#     #适合人群
#     gender = "all"
#     # print(gender)
#
#     #产品位置
#     goods_num = goods_urls.index(goods_url) + 1
#     # print(goods_num)
#
#     goods_info = {
#         "goods_name": goods_name,
#         "goods_model": goods_model,
#         "goods_price": goods_price,
#         "goods_discount_price": goods_discount_price,
#         "goods_color": goods_color,
#         "goods_size": goods_size,
#         "goods_details": goods_detail,
#         "goods_images": goods_images,
#         "goods_num": goods_num,
#         "gender": gender,
#     }
#     # print(goods_info)
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
#         1,
#         goods_url,
#     ))
#     print("%s抓取完成"%goods_name)