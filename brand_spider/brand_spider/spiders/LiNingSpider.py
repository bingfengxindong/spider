from fake_useragent import UserAgent
from lxml import etree

import scrapy
import time
import uuid
import random

# "scrapy crawl adidas -o adidas.csv"

class LiNingSpider(scrapy.Spider):
    name = "lining"
    start_urls = [
        "http://store.lining.com/shop/goodsCate-sale,desc,1,17s17_133,17_133,17_133_m-0-0-17_133,17_133,17_133_m-1,4s0-0-0-min,max-0.html",
        "http://store.lining.com/shop/goodsCate-sale,desc,1,17s17_133,17_133,17_133_m-0-0-17_133,17_133,17_133_m-2,4s0-0-0-min,max-0.html",
    ]
    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'Upgrade-Insecure-sRequests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    # }

    def sleep_time(self):
        """
        睡眠0-2s之间的随机时间
        :return:
        """
        ran_time = random.uniform(0, 1)
        time.sleep(ran_time)

    def del_report(self,lis):
        li_drs = []
        for li in lis:
            if li not in li_drs:
                li_drs.append(li)
        return li_drs

    def upload_html(self,response):
        with open("./1.html","w",encoding="utf-8") as f:
            f.write(response.text)

    def random_headers(self):
        ua = UserAgent(verify_ssl=False)
        return {'User-Agent': ua.random,}

    def start_requests(self):
        for start_url in self.start_urls:
            if "17_133_m-1" in start_url:
                goods_gender = "mens"
            elif "17_133_m-2" in start_url:
                goods_gender = "womens"
            goods_page = self.start_urls.index(start_url)
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.random_headers(),meta={"url":start_url,
                                                                                                       "goods_gender":goods_gender,
                                                                                                       "goods_page":goods_page,})

    def parse(self, response):
        url = response.meta["url"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_infos = response.xpath("//div[@class='selItem']").extract()
        for goods_info in goods_infos:
            goods_info_html = etree.HTML(goods_info)
            goods_name = goods_info_html.xpath("//div[@class='hgoodsName']/text()")[0]
            goods_urls = goods_info_html.xpath("//div[@class='slaveItem']/@url")
            goods_order = goods_infos.index(goods_info) + 1 + (int(url.split("desc,")[1].split(",17s17")[0]) - 1) * 25
            for goods_url in goods_urls:
                self.sleep_time()
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.random_headers(),meta={"goods_name":goods_name,
                                                                                                                "goods_url":goods_url,
                                                                                                                "goods_gender":goods_gender,
                                                                                                                "goods_page":goods_page,
                                                                                                                "goods_order":goods_order,},dont_filter=True)
        if len(goods_infos) != 0:
            url = "{}desc,{},17s17{}".format(url.split("desc,")[0],int(url.split("desc,")[1].split(",17s17")[0]) + 1,url.split("desc,")[1].split(",17s17")[1])
            yield scrapy.Request(url=url,callback=self.parse,headers=self.random_headers(),meta={"url":url,
                                                                                                 "goods_gender":goods_gender,
                                                                                                 "goods_page":goods_page,})

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_url = response.meta["goods_url"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_order = response.meta["goods_order"]
        goods_model = response.xpath("//span[@id='partNumber']/span[@class='v']/text()").extract()[0]
        goods_price = response.xpath("//span[@id='offerPrice']/span[@class='v']/text()").extract()[0]
        goods_discount_price = response.xpath("//span[@id='listPrice']/span[@class='v']/text()").extract()[0]
        goods_color = response.xpath("//li[@class='thumbimgchecked']/a/@title").extract()[0]
        goods_size = ["all"]
        goods_details = [i.replace("\n","").strip() for i in response.xpath("//pre[@class='PD_desc']/span/text()").extract()]
        goods_images = response.xpath("//ul[@id='thumblist']/li/div/a/img/@big").extract()
        print(goods_name)

        yield {
            "goods_name": goods_name,
            "goods_model": goods_model,
            "goods_price": goods_price,
            "goods_discount_price": goods_discount_price,
            "goods_color": goods_color,
            "goods_size": str(goods_size),
            "goods_details": str(goods_details),
            "goods_images": str(goods_images),
            "goods_num": goods_order,
            "gender": goods_gender,
            "goods_page": goods_page,
            "goods_url": goods_url,
        }