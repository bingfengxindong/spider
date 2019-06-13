# from lxml import etree
# from selenium import webdriver
# from fake_useragent import UserAgent
# from multiprocessing import Pool
#
# import requests
# import random
# import time
# import ssl
# import csv
# import os
# import datetime
#
# path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
# if not os.path.exists(path):
#     os.makedirs(path)
# file = open(os.path.join(path,"nike.csv"),"w+",encoding="utf-8",newline="")
# writer = csv.writer(file)
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://store.nike.com/cn/zh_cn/pw/mens-hats-caps/7puZof1",
#     "https://store.nike.com/cn/zh_cn/pw/womens-hats-caps/7ptZof1",
# ]
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Upgrade-Insecure-sRequests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
# }
#
# def random_headers():
#     ua = UserAgent(verify_ssl=False)
#     return {'User-Agent': ua.random,}
#
# def sleep_time():
#     """
#     睡眠0-2s之间的随机时间
#     :return:
#     """
#     ran_time = random.uniform(0,1)
#     time.sleep(ran_time)
#
# def upload_html(text):
#     with open("./1.html","w",encoding="utf-8") as f:
#         f.write(text)
#
# def to_heavy(datas):
#     ls = []
#     for data in datas:
#         if data not in ls:
#             ls.append(data)
#     return ls
#
# def goods_url_parse(url):
#     # 获取页面源码
#     driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
#     driver.maximize_window()
#     sleep_time()
#     driver.get(url)
#     pagesource = driver.page_source
#     html = etree.HTML(pagesource)
#     driver.close()
#     return html
#
# def goods_info(url):
#     response = requests.get(url=url, headers=random_headers())
#     text = response.text
#     html = etree.HTML(text)
#     return html
#
# def goods_detail(url,goods_order,gender,goods_page):
#     goods_html = goods_url_parse(url)
#     goods_name = goods_html.xpath("//h1[@id='pdp_product_title']/text()")[0]
#     goods_price = goods_html.xpath("//div[@class='text-color-black']/text()|//div[@class='css-b9fpep']/text()|//div[@class='mb-1-sm text-color-black']/text()|//div[@class='text-color-primary-dark']/text()|//div[@class='mb-1-sm text-color-primary-dark']/text()")[0]
#     goods_discount_price = goods_html.xpath("//div[@class='text-color-grey u-strikethrough']/text()|//div[@class='text-color-secondary u-strikethrough']/text()")
#     goods_discount_price = "%s0" % goods_price[0] if len(goods_discount_price) == 0 else goods_discount_price[0]
#     goods_size = goods_html.xpath("//div[@class='mt4-sm mb2-sm mr0-lg ml0-lg availableSizeContainer mt5-sm mb3-sm fs16-sm']/label/text()")
#     goods_sizes = ["均码"] if len(goods_size) == 0 else goods_size
#     goods_title = goods_html.xpath("//h2[@class='fs16-sm pb1-sm']/text()|//h2[@class='headline-baseline-base pb1-sm']/text()")[0]
#     goods_urls = goods_html.xpath("//a[@class='colorway-anchor']/@href")
#     goods_urls = [url] if len(goods_urls) == 0 else goods_urls
#     for goods_url in goods_urls:
#         html = goods_url_parse(goods_url)
#         goods_details = html.xpath("//div[@class='pi-pdpmainbody']/p/b/text()|//div[@class='pi-pdpmainbody']/ul/li/text()|//div[@class='pi-pdpmainbody']/li/text()")
#         goods_model = [i for i in goods_details if "款式" in i][0].strip("款式：").strip()
#         goods_color = [i for i in goods_details if "显示颜色" in i][0].strip("显示颜色：").strip()
#         goods_images = to_heavy(html.xpath("//button[@data-sub-type='image']/div/picture[2]/img/@src"))
#
#         writer.writerow((
#             goods_name,
#             goods_model,
#             goods_price,
#             goods_discount_price,
#             goods_color,
#             goods_sizes,
#             goods_details,
#             goods_images,
#             goods_title,
#             goods_order,
#             gender,
#             goods_page,
#             goods_url,
#         ))
#         print("end--{}".format(goods_model))
#
#
# def main():
#     for url in urls:
#         gender = url.split("-")[0].split("/")[-1]
#         goods_page = urls.index(url) + 1
#         html = goods_url_parse(url)
#         goods_urls = html.xpath("//div[@class='grid-item-image']/div/a/@href")
#         for goods_url in goods_urls:
#             goods_order = goods_urls.index(goods_url) + 1
#             goods_detail(goods_url,goods_order,gender,goods_page)
#
# if __name__ == "__main__":
#     main()