from fake_useragent import UserAgent
from lxml import etree

import scrapy
import time
import uuid
import random

# "scrapy crawl adidas -o adidas.csv"

class KenzoSpider(scrapy.Spider):
    name = "kenzo"
    start_urls = [
        "https://www.kenzo.com/eu/en/accessories/accessories-unisex/hats-beanies-gloves",
    ]

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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.random_headers(),meta={"url":start_url,})

    def parse(self, response):
        goods_urls = response.xpath("//a[@class='product']/@href").extract()
        for goods_url in goods_urls:
            goods_order = goods_urls.index(goods_url)
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.random_headers(),meta={"goods_url":goods_url,
                                                                                                            "goods_order":goods_order,})

    def info_parse(self,response):
        goods_url = response.meta["goods_url"]
        goods_order = response.meta["goods_order"]
        goods_name = response.xpath("//h1[@itemprop='name']/text()").extract()[0]
        goods_model = goods_url.split("/")[-1].split("?")[0].strip(".html")
        goods_price = response.xpath("//div[@class='productpage-fiche-price']/div/div/text()").extract()[0].replace("\n","").replace("\t","").strip()
        goods_discount_price = "{}0".format(goods_price[0])
        goods_color = response.xpath("//li[@class='selected']/span[@class='color-tooltip']/text()").extract()[0]
        goods_size = ["all"]
        goods_details1 = [i.replace("\n","").replace("\t","").strip() for i in response.xpath("//div[@itemprop='description']/div/text()").extract() if i.replace("\n","").replace("\t","").strip() != ""]
        goods_details2 = [i.replace("\n","").replace("\t","").strip() for i in response.xpath("//div[@class='productpage-fiche-size expandable']/div/text()").extract() if i.replace("\n","").replace("\t","").strip() != ""]
        goods_details3 = [i.replace("\n","").replace("\t","").strip() for i in response.xpath("//div[@class='productpage-fiche-compo expandable']/div/text()|//div[@class='productpage-fiche-compo expandable']/div/p/text()").extract() if i.replace("\n","").replace("\t","").strip() != ""]
        goods_details = goods_details1 + goods_details2 + goods_details3
        goods_images = response.xpath("//img[@itemprop='image']/@src").extract()
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
            "gender": "all",
            "goods_page": 1,
            "goods_url": goods_url,
        }