# from lxml import etree
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# import requests
# import random
# import time
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
#
# path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
# if not os.path.exists(path):
#     os.makedirs(path)
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"herschel.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品位置","适合人群","产品页面编号","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
#
# urls = [
#     "https://herschel.com/shop/mens/headwear",
#     "https://herschel.com/shop/womens/headwear",
#     "https://herschel.com/shop/kids/headwear",
#     ]
# header = {
#     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
#     "upgrade-insecure-requests":"1",
# }
# #产品页面编号
# goods_page = 1
#
# for url in urls:
#     driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
#     sleep_time()
#     driver.get(url)
#     exit_location = driver.find_element_by_xpath("//div[@id='regioncheck']/div/button")
#     ActionChains(driver).move_to_element(exit_location).click(exit_location).perform()
#     sleep_time()
#     view_more = driver.find_element_by_xpath("//button[@class='clp-view-more button button--primary progress-forward']/span[@class='not-spinner']")
#     ActionChains(driver).move_to_element(view_more).click(view_more).perform()
#     sleep_time()
#     #获取页面源码
#     pagesource = driver.page_source
#     html = etree.HTML(pagesource)
#     goods_urls = html.xpath("//div[@class='col-lg-4 col-md-6 col-xs-12 m-b-2']/div/div/div/div/a/@href")
#     # goods_names = html.xpath("//div[@class='col-xs-6 title-line']/text()")
#     # goods_name_indexs = sorted([goods_names.index(i) for i in set(goods_names)])
#     # goods_single_urls = []
#     # for goods_name_index in goods_name_indexs:
#     #     goods_single_urls.append(goods_urls[goods_name_index])
#
#     #获取商品详情
#     header["referer"] = url
#     for i in goods_urls:
#         goods_url = "https://herschel.com" + i
#         response_detail = requests.get(url=goods_url,headers=header)
#         text_detail = response_detail.text
#         html_detail = etree.HTML(text_detail)
#
#         #产品名字
#         goods_name = html_detail.xpath("//h2[@class='product-overview__title']/text()")[0]
#         # print(goods_name)
#
#         #产品型号
#         goods_models = html_detail.xpath("//div[@class='colors-list m-y-1 indented js-colors-list pdp-colors-list sm-hide']/ul/li[@class='colors-list__color']/label/input/@value")
#         # print(goods_models)
#
#         #产品价格
#         if goods_name == "Cold Weather Beanie | Sprout":
#             goods_price = "$14.99"
#         elif goods_name == "Brighton Cap":
#             goods_price = "$59.99"
#         elif goods_name == "Abbott Beanie":
#             goods_price = "$19.99"
#         else:
#             goods_price = "$%s"%html_detail.xpath("//span[@class='h4 hsco-product-price bfx-price']/text()")[0]
#         goods_discount_price = "$0"
#         # print(goods_price)
#         # print(goods_discount_price)
#
#         #产品颜色
#         goods_colors = html_detail.xpath("//div[@class='colors-list m-y-1 indented js-colors-list pdp-colors-list sm-hide']/ul/li[@class='colors-list__color']/label/img/@alt")
#         # print(goods_colors)
#
#         #产品尺寸
#         goods_size = ["all"]
#         # print(goods_size)
#
#         #产品描述
#         goods_detail = html_detail.xpath("//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/text()|//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/a/text()|//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/text()")
#         goods_details = []
#         for j in goods_detail:
#             if j.strip() != "":
#                 goods_details.append(j)
#         # print(goods_details)
#
#         #产品图片
#         goods_image = html_detail.xpath("//div[@class='colors-list m-y-1 indented js-colors-list pdp-colors-list sm-hide']/ul/li[@class='colors-list__color']/label/input/@data-images")
#         goods_images = []
#         for k in goods_image:
#             goods_img_urls = []
#             for a in k.split(","):
#                 goods_img_urls.append("%s%s"%("https://herschel.com",a))
#             goods_images.append(goods_img_urls)
#         # print(goods_images)
#
#         #适合人群
#         if "men" in url and "women" not in url:
#             gender = "men"
#         elif "women" in url:
#             gender = "women"
#         elif "kid" in url:
#             gender = "kid"
#         # print(gender)
#
#         #产品顺序
#         goods_num = goods_urls.index(i) + 1
#         goods_infos = []
#         for g_n in range(len(goods_models)):
#             goods_infos.append({
#                 "goods_name": goods_name,
#                 "goods_model": goods_models[g_n],
#                 "goods_price": goods_price,
#                 "goods_discount_price": goods_discount_price,
#                 "goods_color": goods_colors[g_n],
#                 "goods_size": goods_size,
#                 "goods_details": goods_details,
#                 "goods_images": goods_images[g_n],
#                 "goods_num": goods_num,
#                 "gender": gender,
#                 "goods_url": "%s=%s"%(goods_url.split("=")[0],goods_models[g_n]),
#             })
#         print(goods_infos)
#
#         for goods_info in goods_infos:
#             writer.writerow((
#                 goods_info["goods_name"],
#                 goods_info["goods_model"],
#                 goods_info["goods_price"],
#                 goods_info["goods_discount_price"],
#                 goods_info["goods_color"],
#                 goods_info["goods_size"],
#                 goods_info["goods_details"],
#                 goods_info["goods_images"],
#                 goods_info["goods_num"],
#                 goods_info["gender"],
#                 goods_page,
#                 goods_info["goods_url"],
#             ))
#         print("%s抓取完成" % goods_name)
#
#
#     driver.close()
#     goods_page += 1