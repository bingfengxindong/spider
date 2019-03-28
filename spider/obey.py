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
#
# path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
# if not os.path.exists(path):
#     os.makedirs(path)
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"obey.csv"),"w+",encoding="utf-8",newline="")
# writer = csv.writer(file)
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://obeyclothing.com/collections/men-headwear",
#     # "https://obeyclothing.com/collections/men-tees/Shortsleeve",
#     # "https://obeyclothing.com/collections/men-tees/Longsleeve",
#     # "https://obeyclothing.com/collections/men-knits",
#     # "https://obeyclothing.com/collections/men-shirts",
#     # "https://obeyclothing.com/collections/men-sweatshirts/crewnecks",
#     # "https://obeyclothing.com/collections/men-sweatshirts/pullovers",
#     # "https://obeyclothing.com/collections/men-outerwear",
#     "https://obeyclothing.com/collections/women-accessories/Hats",
#     # "https://obeyclothing.com/collections/women-tees",
#     # "https://obeyclothing.com/collections/women-tees/Longsleeve",
#     # "https://obeyclothing.com/collections/women-outerwear",
#     # "https://obeyclothing.com/collections/women-sweatshirts/Crewnecks",
#     # "https://obeyclothing.com/collections/women-sweatshirts/Pullovers",
# ]
# header = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Upgrade-Insecure-sRequests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
# }
#
# def sleep_time():
#     """
#     睡眠0-2s之间的随机时间
#     :return:
#     """
#     ran_time = random.uniform(0,1)
#     time.sleep(ran_time)
#
# def data_heavy(data):
#     ds = []
#     for i in data:
#         if i not in ds:
#             ds.append(i)
#     return ds
#
# def html_response(url):
#     response = requests.get(url=url,headers=header)
#     text = response.text
#     html = etree.HTML(text)
#     return html
#
# def json_response(url):
#     response = requests.get(url=url, headers=header)
#     text = response.text
#     json_html = json.loads(text)
#     return json_html
#
# def url_parse(url,goods_page,end_page=0):
#     goods_gender = url.split("-")[0].split("/")[-1]
#     url_html = html_response(url)
#     goods_urls = url_html.xpath("//div[@class='relative']/a/@href")
#     goods_image_htmls = url_html.xpath("//div[@class='product-images']")
#     next_page = url_html.xpath("//span[@class='next']/a/@href")
#     for goods_url in goods_urls:
#         #产品位置
#         goods_order = end_page + goods_urls.index(goods_url) + 1
#         goods_json_url = "https://obeyclothing.com{}.js".format(goods_url.split("?")[0])
#         goods_info = json_response(goods_json_url)
#         #产品名字
#         goods_name = goods_info["title"]
#         #产品价格
#         goods_price = "${}".format(goods_info["price"]/100)
#         goods_discount_price = "$0"
#         #产品尺寸
#         goods_size = goods_info["options"][1]["values"]
#         #产品描述
#         goods_details = [i.strip("<p>\xa0</p>").strip() for i in goods_info["description"].replace("\n","").replace("<li>","").replace("<span>","").replace("</span>","").split("</li>") if i.strip("<p>\xa0</p>").strip() != ""]
#         #产品颜色
#         goods_colors = goods_info["options"][0]["values"]
#         # 产品图片
#         goods_images = etree.HTML(etree.tostring(goods_image_htmls[goods_urls.index(goods_url)], encoding="utf-8")).xpath("//img/@src")
#         num = len(goods_images) // len(goods_colors)
#         goods_images = [goods_images[i*num:i*num + num] for i in range(len(goods_colors))]
#         # 产品型号
#         goods_models = [i["id"] for i in goods_info["variants"] if i["option2"] == "Small" or i["option2"] == "One Size"]
#         goods_models = ["{}-{}".format(i,goods_info["url"].split("/")[-1]) for i in goods_models]
#         print(len(goods_colors) == len(goods_images))
#         #产品url
#         g_urls = ["https://obeyclothing.com{}?variant={}".format(goods_info["url"],i["id"]) for i in goods_info["variants"] if i["option2"] == "Small" or i["option2"] == "One Size"]
#         for i in range(len(goods_images)):
#             writer.writerow((
#                 goods_name,
#                 goods_models[i],
#                 goods_price,
#                 goods_discount_price,
#                 goods_colors[i],
#                 str(goods_size),
#                 str(goods_details),
#                 str(goods_images[i]),
#                 goods_order,
#                 goods_gender,
#                 goods_page,
#                 g_urls[i],
#             ))
#
#     end_page += len(goods_urls)
#     if len(next_page) == 1:
#         next_url = "https://obeyclothing.com{}".format(next_page[0])
#         url_parse(next_url,goods_page,end_page)
#
# def main():
#     for url in urls:
#         goods_page = urls.index(url) + 1
#         url_parse(url,goods_page)
#         print("*"*100)
#
# if __name__ == "__main__":
#     main()