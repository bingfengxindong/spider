from lxml import etree
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

import requests
import random
import time
import ssl
import csv
import os
import datetime

path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
if not os.path.exists(path):
    os.makedirs(path)
file = open(os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"),"adidas.csv"),"w+",encoding="utf-8",newline="")
writer = csv.writer(file)
writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_title","goods_num","gender","goods_page","goods_comments","goods_url"))

ssl._create_default_https_context = ssl._create_stdlib_context

urls = [
    "https://www.adidas.com.cn/men_hats&gloves&scarves?t=headwear&sex=men",
    # "https://www.adidas.com.cn/men_sweats_clothing?t=fleece&sex=men",
    # "https://www.adidas.com.cn/men_jacketsandtracktops_clothing?t=jacket&sex=men",
    # "https://www.adidas.com.cn/search?t=tshirts&sex=men&ni=374&pf=25-40%2C%2C25-40%2C&pr=-&fo=p25%2Cp25&pn=1&pageSize=120&p=undefined-%E7%94%B7%E5%AD%90%26undefined-%E7%94%B7%E5%AD%90&isSaleTop=false",
    # "https://www.adidas.com.cn/men_bags?t=bag&sex=men",
    "https://www.adidas.com.cn/women_hats&gloves&scarves?t=headwear&sex=women",
    # "https://www.adidas.com.cn/women_sweats_clothing?t=fleece&sex=women",
    # "https://www.adidas.com.cn/women_jacketsandtracktops_clothing?t=jacket&sex=women",
    # "https://www.adidas.com.cn/women_bras_clothing_segment?t=bra&sex=women",
    # "https://www.adidas.com.cn/search?t=tshirts&sex=women&ni=377&pf=25-82%2C%2C25-82%2C&pr=-&fo=p25%2Cp25&pn=1&pageSize=120&p=undefined-%E5%A5%B3%E5%AD%90%26undefined-%E5%A5%B3%E5%AD%90&isSaleTop=false",
    # "https://www.adidas.com.cn/women_bags?t=bag&sex=women",
]


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-sRequests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
}

def random_headers():
    ua = UserAgent(verify_ssl=False)
    return {'User-Agent': ua.random,}

def sleep_time():
    """
    睡眠0-2s之间的随机时间
    :return:
    """
    ran_time = random.uniform(0,1)
    time.sleep(ran_time)

def upload_html(text):
    with open("./1.html","w",encoding="utf-8") as f:
        f.write(text)

def goods_url_parse(driver):
    # 获取页面源码
    pagesource = driver.page_source
    html = etree.HTML(pagesource)
    goods_urls = html.xpath("//div[@class='pro-big-img-box']/a/@href")
    return goods_urls

def goods_info(url):
    response = requests.get(url=url, headers=random_headers())
    text = response.text
    html = etree.HTML(text)
    return html

discount_price = lambda x:"0" if x == [] else x[0]

def exit_ten(driver,urls_len,url,u_len,goods_gender,goods_page):
    for i in range(0,10):
        exit_location = driver.find_element_by_xpath("//i[@class='icon icon-china']")
        ActionChains(driver).move_to_element(exit_location).perform()
        sleep_time()
        pagesource = driver.page_source
        html = etree.HTML(pagesource)
        goods_url = html.xpath("//div[@class='pro-big-img-box']/a/@href")
        if len(goods_url) == urls_len:
            break
    goods_urls = [i.replace("\n","").replace("\t","").strip() for i in goods_url_parse(driver)]
    # print(len(goods_urls))
    for goods_url in goods_urls:
        # 产品顺序
        goods_order = u_len + goods_urls.index(goods_url) + 1
        html_detail = goods_info("https://www.adidas.com.cn{}".format(goods_url.strip()))

        # 产品名字
        goods_name = html_detail.xpath("//div[@class='pdp-title none-sm']/h3/text()")[0]
        if "鞋" not in goods_name:
            # 产品价格
            goods_price = html_detail.xpath("//span[@class='goods-price price-single']/text()|//span[@class='goods-price']/text()")[0]
            goods_discount_price = discount_price(html_detail.xpath("//span[@class='goods-price']/del/text()")).replace("\n","").replace("\t","").strip()
            # 产品尺码
            goods_sizes = [i.replace("\n", "").replace("\t", "").strip() for i in html_detail.xpath("//ul[@class='float-clearfix']/li/a/text()") if i.replace("\n", "").replace("\t", "").strip() != ""]
            # 产品详情
            goods_details = html_detail.xpath("//div[@class='float-clearfix']/div/p/text()|//div[@class='float-clearfix']/div/ul/li/p/text()")
            # 产品评论
            goods_comments = []
            goods_comment_stars = html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div/div/div/div/@style|//ul[@class='evaluation-inner-ul']/li/div/div/div/div[2]/@style")
            goods_comment_star_list = [int((int(k.split(": ")[-1].split("%")[0].split(":")[-1]) / 100) * 5) for k in goods_comment_stars]
            goods_comment_times = html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='lev-box']/p[1]/text()")
            goods_comment_comments = [i.replace("\n", "").replace("\t", "") for i in html_detail.xpath("//ul[@class='evaluation-inner-ul']/li/div[@class='evaluation-detial']/p/text()")]
            # print(goods_name,len(goods_comment_stars),len(goods_comment_times),len(goods_comment_comments))
            for j in range(len(goods_comment_stars)):
                goods_comments.append({
                    "goods_comment_star": goods_comment_star_list[j],
                    "goods_comment_time": goods_comment_times[j],
                    "goods_comment_comment": goods_comment_comments[j],
                })

            #产品型号
            goods_model = goods_url.split("/")[-1].split("?")[0]
            #产品颜色
            goods_color = html_detail.xpath("//div[@class='pdp-color events-color-close']/h3/text()")[0].split("(")[0]
            # 产品图片
            goods_images = [i for i in html_detail.xpath("//div[@class='scroll-background-image icon-play-new']/a/img/@data-smartzoom")]
            # 适合人群
            gender = goods_gender
            #产品标题
            goods_title = html_detail.xpath("//div[@class='goods-tit']/text()")[0].strip("\n").strip("\t").strip()
            #产品页面编号
            goods_page = goods_page

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
                goods_title,
                goods_order,
                gender,
                goods_page,
                goods_comments,
                "https://www.adidas.com.cn{}".format(goods_url.strip()),
            ))

    if "search?" in url and len(goods_urls) != 0:
        url_sp = url.split("pn=")
        next_url = "{}pn={}{}".format(url_sp[0],int(url_sp[1][0]) + 1,url_sp[1][1:])
        u_len = len(goods_urls) + u_len
        url_parse(next_url,goods_page,u_len=u_len)

urls_lens = lambda x:0 if x == "" else int(x)

def url_parse(url,goods_page,u_len=0):
    goods_gender = url.split("sex=")[-1].split("&")[0]
    driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
    driver.maximize_window()
    sleep_time()
    driver.get(url)
    urls_len = urls_lens(etree.HTML(driver.page_source).xpath("//span[@class='m-list-num']/text()")[0].replace("\xa0", "").replace("件商品","").replace("[", "").replace("]", "").strip())
    exit_ten(driver, urls_len,url,u_len,goods_gender,goods_page)
    sleep_time()
    driver.close()

def main():
    for url in urls:
        goods_page = urls.index(url)
        url_parse(url,goods_page)

if __name__ == "__main__":
    main()