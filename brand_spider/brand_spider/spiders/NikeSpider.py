from fake_useragent import UserAgent
from lxml import etree
from selenium import webdriver

import scrapy
import time
import random

# "scrapy crawl adidas -o adidas.csv"

class KithSpider(scrapy.Spider):
    name = "nike"
    start_urls = [
        # "https://store.nike.com/cn/zh_cn/pw/mens-hats-caps/7puZof1",
        # "https://store.nike.com/cn/zh_cn/pw/womens-hats-caps/7ptZof1",

        # "https://store.nike.com/cn/zh_cn/pw/mens-bags-backpacks/7puZof2",
        "https://store.nike.com/cn/zh_cn/pw/womens-bags-backpacks/7ptZof2",
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def random_headers(self):
        ua = UserAgent(verify_ssl=False)
        return {'User-Agent': ua.random, }

    def upload_html(self,response):
        with open("./1.html","w",encoding="utf-8") as f:
            f.write(response.text)

    def sleep_time(self):
        """
        睡眠0-2s之间的随机时间
        :return:
        """
        ran_time = random.uniform(0, 1)
        time.sleep(ran_time)

    def to_heavy(self,datas):
        ls = []
        for data in datas:
            if data not in ls:
                ls.append(data)
        return ls


    def start_requests(self):
        for start_url in self.start_urls:
            goods_gender = start_url.split("-")[0].split("/")[-1]
            yield scrapy.Request(url=start_url,callback=self.parse,dont_filter=True,meta={"goods_gender":goods_gender,
                                                                                            "goods_page":self.start_urls.index(start_url) + 1,})

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_details = response.xpath("//div[@class='exp-product-wall']/div|//div[@class='exp-product-wall clearfix']/div").extract()
        print(len(goods_details))
        for goods_detail in goods_details:
            goods_detail_html = etree.HTML(goods_detail)
            goods_price = goods_detail_html.xpath("//span[@class='local nsg-font-family--base']/text()")[0]
            g_discount_price = goods_detail_html.xpath("//span[@class='overridden nsg-font-family--base']/text()")
            goods_discount_price = "{}0".format(goods_price[0]) if len(g_discount_price) == 0 else g_discount_price[0]
            goods_urls = goods_detail_html.xpath("//div[@class='color-options']/ul/li/a/@href")
            g_urls = goods_detail_html.xpath("//div[@class='grid-item-image-wrapper sprite-sheet sprite-index-0']/a/@href") if len(goods_urls) == 0 else goods_urls
            for g_url in g_urls:
                yield scrapy.Request(url=g_url,callback=self.goods_info_parse,dont_filter=True,meta={"goods_url":g_url,
                                                                                                        "goods_order":goods_details.index(goods_detail) + 1,
                                                                                                        "goods_gender":goods_gender,
                                                                                                        "goods_page":goods_page,
                                                                                                        "goods_price":goods_price,
                                                                                                        "goods_discount_price":goods_discount_price,})

    def goods_info_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_name = response.xpath("//h1[@id='pdp_product_title']/text()").extract()[0]
        goods_details = response.xpath("//div[@class='pi-pdpmainbody']/p/b/text()|//div[@class='pi-pdpmainbody']/ul/li/text()|//div[@class='pi-pdpmainbody']/li/text()").extract()
        goods_model = [i for i in goods_details if "款式" in i][0].strip("款式：").strip()
        goods_color = [i for i in goods_details if "显示颜色" in i][0].strip("显示颜色：").strip()
        goods_size = response.xpath("//div[@class='mt4-sm mb2-sm mr0-lg ml0-lg availableSizeContainer mt5-sm mb3-sm fs16-sm']/label/text()").extract()
        goods_size = ["均码"] if len(goods_size) == 0 else goods_size
        goods_images = self.to_heavy(response.xpath("//button[@data-sub-type='image']/div/picture[2]/img/@src").extract())
        goods_title = response.xpath("//h2[@class='fs16-sm pb1-sm']/text()|//h2[@class='headline-baseline-base pb1-sm']/text()").extract()[0]
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
            "goods_title": goods_title,
            "goods_num": goods_order,
            "gender": goods_gender,
            "goods_page": goods_page,
            "goods_url": goods_url,
        }