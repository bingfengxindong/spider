# from lxml import etree
# from selenium import webdriver
# from selenium.webdriver import ActionChains
#
# import requests
# import random
# import time
# import ssl
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
# file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"adidas.csv"),"w+",encoding="utf-8")
# writer = csv.writer(file)
# writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品标题","产品位置","适合人群","产品页面编号","产品评论","产品url"))
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://www.adidas.com.cn/men_hats&gloves&scarves",
#     "https://www.adidas.com.cn/women_hats&gloves&scarves",
# ]
#
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Upgrade-Insecure-sRequests': '1',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
# }
#
# goods_page = 1
# for url in urls:
#     sleep_time()
#     response = requests.get(url=url,headers=headers)
#     text = response.text
#     html = etree.HTML(text)
#     goods_urls = html.xpath("//div[@class='pro-big-img-box']/a/@href")
#     goods_cn_names = html.xpath("//div[@class='good-box']/a/span[1]/text()")
#     goods_labels = html.xpath("//div[@class='badge']")
#     goods_titles = html.xpath("//div[@class='goods-info']/span/text()")
#     # print(len(goods_urls))
#     # print(len(goods_cn_names))
#     # print(len(goods_labels))
#     # print(len(goods_titles))
#
#     for i in range(len(goods_urls)):
#         # if "帽" in goods_cn_names[i] or "头带" in goods_cn_names[i]:
#             # print(goods_urls[i])
#         sleep_time()
#         response_detail = requests.get(url="https://www.adidas.com.cn%s"%goods_urls[i],headers=headers)
#         text_detail = response_detail.text
#         html_detail = etree.HTML(text_detail)
#         #产品名字
#         try:
#             goods_name = html_detail.xpath("//div[@class='pdp-title none-sm']/h3/text()")[0]
#         except IndexError:
#             with open("./2.html","w",encoding="utf-8") as f:
#                 f.write(text_detail)
#         # print(goods_name)
#         #产品型号
#         goods_model = goods_urls[i].split("/")[-1].split("?")[0]
#         # print(goods_model)
#         #产品价格
#         try:
#             goods_price = html_detail.xpath("//span[@class='goods-price price-single']/text()|//span[@class='goods-price']/text()")[0]
#             goods_discount_price_a = html_detail.xpath("//span[@class='goods-price']/del/text()")
#             # print(goods_price,goods_discount_price_a)
#             if goods_discount_price_a == []:
#                 goods_discount_price = "0"
#             else:
#                 goods_discount_price = goods_discount_price_a[0]
#         except IndexError:
#             with open("./1.html","w",encoding="utf-8") as f:
#                 f.write(text_detail)
#         # print(goods_price,goods_discount_price)
#         #产品颜色
#         goods_color = html_detail.xpath("//div[@class='pdp-color events-color-close']/h3/text()")[0].split("(")[0]
#         # print(goods_color)
#         #产品尺码
#         goods_sizes = [i.replace("\n","").replace("\t","") for i in html_detail.xpath("//ul[@class='float-clearfix']/li/a/text()") if i.replace("\n","").replace("\t","") != ""]
#         # print(goods_sizes)
#         #产品详情
#         goods_details = html_detail.xpath("//div[@class='float-clearfix']/div/p/text()|//div[@class='float-clearfix']/div/ul/li/p/text()")
#         # print(goods_details)
#         #产品图片
#         # goods_images = html_detail.xpath("//div[@class='scroll-background-image icon-play-new']/a/img/@data-lasysrc")
#         goods_images = html_detail.xpath("//div[@class='scroll-background-image icon-play-new']/a/img/@data-smartzoom")
#         goods_images = [i for i in goods_images]
#         print(len(goods_images),goods_images)
#         #适合人群
#         gender = url.split("/")[-1].split("_")[0]
#         # print(gender)
#         #产品顺序
#         goods_num = i + 1
#         # print(goods_num)
#         #产品标签
#         if "NEW" in etree.tostring(goods_labels[i]).decode():
#             goods_label = "new"
#         else:
#             goods_label = "none"
#         # print(goods_label)
#         #评论
#         comment_button = html_detail.xpath("//a[@class='btn btn-black loading-more item-rate-loading-more none-sm']")
#         if len(comment_button) == 0:
#             goods_comment_none = html_detail.xpath("//div[@class='ass-left']/p/text()")
#             if len(goods_comment_none) != 0:
#                 goods_comments = "none"
#                 # print(goods_comment)
#             else:
#                 goods_comments = []
#                 goods_comment_stars = html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div/div/div/div/@style|//ul[@class='evaluation-inner-ul']/li/div/div/div/div[2]/@style")
#                 goods_comment_star_list = [int((int(k.split(": ")[-1].split("%")[0].split(":")[-1])/100)*5) for k in goods_comment_stars]
#                 goods_comment_times = html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='lev-box']/p/text()")
#                 goods_comment_comments = [i.replace("\n","").replace("\t","") for i in html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='evaluation-detial']/p/text()") if i.replace("\n","").replace("\t","") != ""]
#                 for j in range(len(goods_comment_stars)):
#                     goods_comments.append({
#                         "goods_comment_star":goods_comment_star_list[j],
#                         "goods_comment_time":goods_comment_times[j],
#                         "goods_comment_comment":goods_comment_comments[j],
#                     })
#                 # print(goods_comment_stars, goods_comment_times_comments)
#         else:
#             driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
#             sleep_time()
#             sleep_time()
#             sleep_time()
#             driver.get("https://www.adidas.com.cn%s"%goods_urls[i])
#             driver.execute_script("window.scrollBy(0,2000)")
#             exit_location = driver.find_element_by_xpath("//span[@class='table-check-review']|//span[@class='table-check-review is-active']")
#             ActionChains(driver).move_to_element(exit_location).click(exit_location).perform()
#             # element = driver.find_element_by_xpath("//a[@class='btn btn-black see-all e-see-all']")
#             # sleep_time()
#             # element.click()
#             exit_location1 = driver.find_element_by_xpath("//a[@class='btn btn-black see-all e-see-all']")
#             ActionChains(driver).move_to_element(exit_location1).click(exit_location1).perform()
#             driver_text = driver.page_source
#             driver_html = etree.HTML(driver_text)
#             goods_comment_stars = driver_html.xpath("//ul[@class='evaluation-inner-ul']/li/div/div/div/div/@style")
#             goods_comment_star_list = [int((int(k.split(": ")[-1].split("%")[0].split(":")[-1]) / 100) * 5) for k in goods_comment_stars]
#             goods_comment_times = driver_html.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='lev-box']/p/text()")
#             goods_comment_comments = [i.replace("\n","").replace("\t","") for i in driver_html.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='evaluation-detial']/p/text()") if i.replace("\n","").replace("\t","") != ""]
#             driver.close()
#             goods_comments = []
#             for j in range(len(goods_comment_stars)):
#                 goods_comments.append({
#                     "goods_comment_star": goods_comment_star_list[j],
#                     "goods_comment_time": goods_comment_times[j],
#                     "goods_comment_comment": goods_comment_comments[j],
#                 })
#             # print(goods_comment_stars,goods_comment_times,goods_comment_comments)
#         #特点
#         goods_title = goods_titles[i]
#         # print(goods_title)
#         goods_info = {
#             "goods_name":goods_name,
#             "goods_model":goods_model,
#             "goods_price":goods_price,
#             "goods_discount_price":goods_discount_price,
#             "goods_color":goods_color,
#             "goods_size":goods_sizes,
#             "goods_details":goods_details,
#             "goods_images":goods_images,
#             "goods_title":goods_title,
#             "goods_num":goods_num,
#             "gender": gender,
#             "goods_comments":goods_comments,
#         }
#         # print(goods_info)
#
#         #"产品名字", "产品型号", "产品价格", "产品以前价格", "产品颜色", "产品尺寸", "产品详情", "产品图片", "产品标题", "产品位置", "适合人群", "产品评论"
#         writer.writerow((
#             goods_info["goods_name"],
#             goods_info["goods_model"],
#             goods_info["goods_price"],
#             goods_info["goods_discount_price"],
#             goods_info["goods_color"],
#             goods_info["goods_size"],
#             goods_info["goods_details"],
#             goods_info["goods_images"],
#             goods_info["goods_title"],
#             goods_info["goods_num"],
#             goods_info["gender"],
#             goods_page,
#             goods_info["goods_comments"],
#             "https://www.adidas.com.cn%s" % goods_urls[i],
#         ))
#         print("*"*100)
#
#     goods_page += 1