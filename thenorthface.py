from lxml import etree
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent

import requests
import random
import time
import ssl
import csv
import os
import datetime

path = os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","goods_info",datetime.datetime.now().strftime("%Y-%m-%d"),"thenorthface.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context

urls = [
    "https://www.thenorthface.com/shop/mens-accessories-hats",
    "https://www.thenorthface.com/shop/womens-accessories-caps",
    "https://www.thenorthface.com/shop/kids-girls-accessories",
    "https://www.thenorthface.com/shop/kids-boys-accessories",
]


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-sRequests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}

def sleep_time():
    """
    睡眠0-2s之间的随机时间
    :return:
    """
    ran_time = random.uniform(0,1)
    time.sleep(ran_time)

# 输入毫秒级的时间，转出正常格式的时间
def timeStamp(timeNum):
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
    return otherStyleTime

def goods_parse(driver):
    # 获取页面源码
    pagesource = driver.page_source
    html = etree.HTML(pagesource)
    return html

def goods_info(url):
    response = requests.get(url=url, headers={'User-Agent': UserAgent(verify_ssl=False).random})
    text = response.text
    html = etree.HTML(text)
    return html

def goods_driver():
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    return driver

def move_goods_list(driver):
    ActionChains(driver).move_to_element(driver.find_element_by_xpath("//a[@class='social-icon icon-facebook']")).perform()
    sleep_time()
    html = goods_parse(driver)
    goods_count = int(html.xpath("//span[@class='product-list-item-count item-count']/text()")[0])
    goods_name = html.xpath("//span[@class='product-block-name-wrapper']/text()")
    return [goods_count,goods_name]

def goods_comment(url):
    goods_comment_response = requests.get(url=url, headers={'User-Agent': UserAgent(verify_ssl=False).random})
    goods_comment_json = eval(goods_comment_response.text.replace("true", "True").replace("false", "False").replace("null", "None"))["results"][0]["reviews"]
    g_comments = [{"goods_comment_star": i["metrics"]["rating"],
                    "goods_comment_time": timeStamp(i["details"]["created_date"]),
                    "goods_comment_comment": i["details"]["comments"].replace("\ud83d\ude0d","").replace("\","),} for i in goods_comment_json]
    return g_comments

goods_imgs = lambda x:[x["i"]["n"]] if isinstance(x,dict) else [i["i"]["n"] for i in x]

def url_parse(url,goods_page):
    gender = url.split("-")[0].split("/")[-1]
    if gender == "kids":
        gender = url.split("-")[1]
    driver = goods_driver()
    sleep_time()
    driver.get(url)
    sleep_time()
    html = goods_parse(driver)
    goods_count = int(html.xpath("//span[@class='product-list-item-count item-count']/text()")[0])
    goods_name = html.xpath("//span[@class='product-block-name-wrapper']/text()")
    while True:
        if len(goods_name) != goods_count:
            goods_c_n = move_goods_list(driver)
            goods_count = goods_c_n[0]
            goods_name = goods_c_n[1]
        else:
            break
    goods_type_infos = goods_parse(driver).xpath("//div[@class='product-block product-block-js lanes']")
    for goods_type_info in goods_type_infos:
        goods_type_info_html = etree.HTML(etree.tostring(goods_type_info,encoding="utf-8").decode("utf-8"))
        goods_url = goods_type_info_html.xpath("//a[@class='product-block-name-link']/@href")[0]
        goods_types = goods_type_info_html.xpath("//div[@class='product-block-color-swatches-container swatches-container']/div/@id")

        goods_name = goods_type_info_html.xpath("//span[@class='product-block-name-wrapper']/text()")[0]
        goods_price = goods_type_info_html.xpath("//span[@class='product-block-price product-block-offer-price offer-price product-price-amount-js']/text()|//span[@class='product-block-price product-block-range-price range product-price-amount-js']/text()")[0].replace("\n","").replace("\t","").strip()
        goods_discount_price = "{}0".format(goods_price[0])
        goods_color_models = goods_type_info_html.xpath("//div[@class='product-block-color-swatches-container swatches-container']/div/@title")
        goods_colors = [i.split("(")[0].strip().lower() for i in goods_color_models]
        goods_models = [i.split("(")[1].strip(")").strip().replace(" ","_") for i in goods_color_models]
        goods_details = [i.replace("\n","").replace("\t","") for i in goods_type_info_html.xpath("//div[@class='product-addl-info-details']/text()|//div[@class='product-addl-info-FEATURE']/ul/li/text()|//div[@class='product-addl-info-SPEC']/ul/li/text()")]
        goods_order = goods_type_infos.index(goods_type_info) + 1
        for goods_type in goods_types:
            goods_model = goods_models[goods_types.index(goods_type)]
            goods_color = goods_colors[goods_types.index(goods_type)]
            g_url = "{}?variationId={}".format(goods_url.split("?")[0],goods_type)
            goods_html = goods_info(g_url)
            goods_sizes = goods_html.xpath("//div[@class='product-content-form-attr-container attr-container attr-container-js swatches ']/button/@data-attribute-value")

            goods_image_json_response = requests.get(url="https://images.thenorthface.com/is/image/TheNorthFace/{}_IS?req=set,json,UTF-8&labelkey=label&handler=s7sdkJSONResponse".format(goods_models[goods_types.index(goods_type)]), headers={'User-Agent': UserAgent(verify_ssl=False).random})
            goods_image_json = eval(goods_image_json_response.text.replace("/*jsonp*/s7sdkJSONResponse(","").replace(',"");',""))
            goods_images = ["https://images.thenorthface.com/is/image/{}?fit=constrain,1&wid=1080&hei=1080&fmt=jpg&$VFDP-VIEWER-THUMBNAIL$".format(i) for i in goods_imgs(goods_image_json["set"]["item"])]

            goods_comments = []
            try:
                goods_comment_url = "https://display.powerreviews.com/m/957729/l/en_US/product/{}/reviews?paging.from=0&paging.size=10&filters=&search=&sort=Newest&image_only=false&apikey=dc148023-20d1-4554-864d-fec4a6902345".format(goods_model.split("_")[0])
                while True:
                    g_comments = goods_comment(goods_comment_url)
                    goods_comments += g_comments
                    goods_comment_url = "{}?paging.from={}&paging.size=10&filters=&search=&sort=Newest&image_only=false&apikey=dc148023-20d1-4554-864d-fec4a6902345".format(goods_comment_url.split("?paging.from=")[0], int(goods_comment_url.split("?paging.from=")[-1].split("&")[0]) + 10)
                    if len(g_comments) == 0:
                        break
            except:
                pass
            print(goods_name)

            writer.writerow((
                goods_name,
                goods_model,
                goods_price,
                goods_discount_price,
                goods_color,
                goods_sizes,
                goods_details,
                goods_images,
                "",
                goods_order,
                gender,
                goods_page,
                goods_comments,
                g_url,
            ))
    driver.close()

def main():
    for url in urls:
        goods_page = urls.index(url) + 1
        url_parse(url,goods_page)

if __name__ == "__main__":
    main()