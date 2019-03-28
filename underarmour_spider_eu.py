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

path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"underarmour_eu.csv"),"w+",encoding="utf-8")
writer = csv.writer(file)
writer.writerow(("产品名字","产品型号","产品价格","产品以前价格","产品颜色","产品尺寸","产品详情","产品图片","产品标题","产品位置","适合人群","产品页面编号","产品评论","产品url"))
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context
#主url
urls = [
    "https://www.underarmour.com/en-us/mens/headwear/g/397d",
    "https://www.underarmour.com/en-us/womens/headwear/g/3c7d",
    "https://www.underarmour.com/en-us/boys/headwear/g/3f7d",
    "https://www.underarmour.com/en-us/girls/headwear/g/3i7d",

]
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }

def list_str(list_l):
    l_str = ""
    for i in list_l:
        l_str += i
    return l_str

def comment(driver_detail):
    page_source_detail = driver_detail.page_source
    all_html_detail = etree.HTML(page_source_detail)
    goods_comments = all_html_detail.xpath(
        "//div[@id='BVRRDisplayContentBodyID']/div/span/div[@class='BVRRReviewDisplayStyle3']")
    data = []
    for goods_comment in goods_comments:
        goods_comment_str = etree.tostring(goods_comment, encoding="utf-8")
        goods_comment_str = goods_comment_str.decode("utf-8")
        goods_comment_html = etree.HTML(goods_comment_str)
        goods_comment_stars = [i.strip()[0] for i in goods_comment_html.xpath("//img[@class='BVImgOrSprite']/@title")]
        goods_comment_comments = goods_comment_html.xpath("//span[@class='BVRRReviewText']/text()")
        goods_comment_times = goods_comment_html.xpath("//span[@class='BVRRValue BVRRReviewDate']/meta/@content")
        data.append({
            "goods_comment_star":goods_comment_stars[0],
            "goods_comment_comment":list_str(goods_comment_comments),
            "goods_comment_time":goods_comment_times[0],
        })
    return data

def comments_single(goods_comments):
    g_comments = []
    for i in range(len(goods_comments)):
        if goods_comments[i] not in g_comments:
            g_comments.append(goods_comments[i])
    data = []
    for g_comment in g_comments:
        for g_c in g_comment:
            data.append(g_c)
    return data

for url in urls:
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    driver.get(url)
    sleep_time()
    # ac = driver.find_element_by_xpath("//span[@class='icon ua-close']")
    # ActionChains(driver).move_to_element(ac).click(ac).perform()
    # sleep_time()
    # ac1 = driver.find_element_by_xpath("//span[@class='icon ua-close']")
    # ActionChains(driver).move_to_element(ac1).click(ac1).perform()
    # sleep_time()
    driver.execute_script("window.scrollBy(0,100000)")
    sleep_time()
    driver.execute_script("window.scrollBy(0,100000)")
    sleep_time()
    driver.execute_script("window.scrollBy(0,100000)")
    sleep_time()
    page_source = driver.page_source
    all_html = etree.HTML(page_source)
    goods_urls = [i for i in all_html.xpath("//a[@class='product-img-link']/@href")]

    g_names = all_html.xpath("//div[@class='title']/text()")

    headers_detail = headers
    headers_detail["Host"] = "www.underarmour.com"
    headers_detail["Referer"] = url
    headers_detail["Upgrade - Insecure - Requests"] = "1"
    driver.close()
    #性别
    gender = url.split("/")[-4]
    print(len(goods_urls))
    for goods_url in goods_urls:
        # if "Headband" not in g_names[goods_urls.index(goods_url)] and "Headbands" not in g_names[goods_urls.index(goods_url)]:
        print(goods_url)
        sleep_time()
        response = requests.get(url=goods_url,headers=headers_detail)
        text = response.text
        html = etree.HTML(text)

        # 产品型号
        goods_models = []
        for g_m in html.xpath("//ul[@class='color-chip_list']/li/@title"):
            if "pid" in goods_url:
                goods_models.append("%s-%s"%(goods_url.split("pid")[1].split("-")[0],g_m.split("-")[-1].strip()))
            elif "pcid" in goods_url:
                goods_models.append("%s-%s"%(goods_url.split("pcid")[1].split("-")[0],g_m.split("-")[-1].strip()))
        goods_colors = [i for i in html.xpath("//ul[@class='color-chip_list']/li/@title")]
        print(goods_models)
        print(goods_colors)
        # 产品尺寸
        goods_size = html.xpath("//ul[@id='sizeChipList']/li/text()|//ul[@id='sizeChipList']/li/span/text()")
        print(goods_size)
        #产品详情
        goods_detail1 = html.xpath("//div[@class='science-paragraph']/text()")
        goods_detail2 = text.split("PRODUCT_DATA")[-1].split("SR")[0].strip('"').strip(":").strip().strip("\\n").strip(",")
        goods_detail3 = goods_detail2.split('"bullets":')[-1].split('"categoryName"')[0].strip(",")
        if len(goods_detail1) == 0:
            goods_detail = []
        else:
            goods_detail = [goods_detail1[0]]
        goods_detail.extend(eval(goods_detail3))

        #产品评论
        goods_comment_num = html.xpath("//span[@class='rating-count']/text()|//span[@class='rating-count']/span/text()")[0]
        if goods_comment_num != "0":
            driver_detail = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
            driver_detail.get(goods_url)
            sleep_time()
            ac2 = driver_detail.find_element_by_xpath("//span[@class='icon ua-close']")
            ActionChains(driver_detail).move_to_element(ac2).click(ac2).perform()
            sleep_time()
            ac3 = driver_detail.find_element_by_xpath("//span[@class='icon ua-close']")
            ActionChains(driver_detail).move_to_element(ac3).click(ac3).perform()
            sleep_time()
            goods_comments1 = comment(driver_detail)
            goods_comments = [goods_comments1]
            while True:
                try:
                    sleep_time()
                    comment_page = driver_detail.find_element_by_xpath("//a[@title='next']")
                    ActionChains(driver_detail).move_to_element(comment_page).click(comment_page).perform()
                    sleep_time()
                    goods_comments2 = comment(driver_detail)
                    goods_comments.append(goods_comments2)
                except Exception as e:
                    print(e)
                    break
            goods_comments = comments_single(goods_comments)
            print(goods_comments)
            print(len(goods_comments))
            driver_detail.close()
        else:
            goods_comments = "none"
        for goods_model in goods_models:
            goods_single_url = "%spid%s"%(goods_url.split("pid")[0],goods_model)
            # print(goods_single_url)
            response_detail = requests.get(url=goods_single_url, headers=headers)
            text_detail = response_detail.text
            html_detail = etree.HTML(text_detail)
            #产品名
            goods_name = html_detail.xpath("//h1[@itemprop='name']/span/text()")[0]
            print(goods_name)
            # 产品型号
            goods_model = goods_model.split(".")[0]
            print(goods_model)
            #产品价格
            g_price = html_detail.xpath("//span[@class='buypanel_productprice-value']/span/text()")
            if len(g_price) == 0:
                goods_price = html_detail.xpath("//span[@class='buypanel_productprice-value sale-price']/span[2]/text()")[0]
            else:
                goods_price = g_price[0]
            g_discount_price = html_detail.xpath("//span[@class='buypanel_productprice--orig']/span[2]/text()")
            if len(g_discount_price) == 0:
                goods_discount_price = 0
            else:
                goods_discount_price = g_discount_price[0]
            # print(goods_price)
            # print(goods_discount_price)
            #产品颜色
            goods_color = goods_colors[goods_models.index(goods_model)]
            # print(goods_color)
            #产品尺寸
            # goods_sizes = html_detail.xpath("//li[@class='size-chip']/text()|//li[@class='size-chip']/span/text()")
            goods_sizes = html_detail.xpath("//ul[@id='sizeChipList']/li/text()|//ul[@id='sizeChipList']/li/span/text()")
            # print(goods_sizes)
            #产品详情
            goods_details = goods_detail
            # print(goods_details)
            #产品图片
            text_data = text_detail.split('"PRODUCT_DATA":')[1].split('"SR":')[0].strip().strip("\\n").strip(",").replace("false","'false'").replace("true","'true'").replace("null","'null'")
            text_datas = eval(text_data)
            g_image1 = text_datas["imageUrl"]
            if "F" in g_image1:
                g_image2 = g_image1.replace("F","B")
            elif "B" in g_image1:
                g_image2 = g_image1.replace("B","F")
            goods_images = [g_image1,g_image2]
            print(goods_images)

            # print(goods_images)
            #产品标题
            goods_title = html.xpath("//div[@class='buypanel_cattitle']/text()")[0]
            # print(goods_title)
            #产品位置
            goods_num = [i for i in goods_urls].index(goods_url) + 1
            # print(goods_num)
            #产品人群
            goods_gender = gender
            # print(goods_gender)
            #产品页面编号
            goods_page = urls.index(url) + 1
            # print(goods_page)
            #产品评论
            goods_comments = goods_comments
            # print(goods_comments)
            #产品url
            g_url = goods_url
            # print(g_url)

            #"goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"
            goods_info = {
                "goods_name":goods_name,
                "goods_model":goods_model,
                "goods_price":goods_price,
                "goods_discount_price":goods_discount_price,
                "goods_color":goods_color,
                "goods_size":goods_sizes,
                "goods_details":goods_details,
                "goods_images":goods_images,
                "goods_title":goods_title,
                "goods_num":goods_num,
                "gender":goods_gender,
                "goods_page":goods_page,
                "goods_comments":goods_comments,
                "goods_url":g_url,
            }

            writer.writerow((
                goods_info["goods_name"],
                goods_info["goods_model"],
                goods_info["goods_price"],
                goods_info["goods_discount_price"],
                goods_info["goods_color"],
                goods_info["goods_size"],
                goods_info["goods_details"],
                goods_info["goods_images"],
                goods_info["goods_title"],
                goods_info["goods_num"],
                goods_info["gender"],
                goods_info["goods_page"],
                goods_info["goods_comments"],
                goods_info["goods_url"],
            ))
        print("*"*100)