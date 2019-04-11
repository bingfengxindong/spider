from fake_useragent import UserAgent
from lxml import etree

import scrapy
import time
import uuid
import random

# "scrapy crawl adidas -o adidas.csv"

class PradaSpider(scrapy.Spider):
    name = "prada"
    start_urls = [
        "https://www.prada.com/us/en/men/accessories/hats/_jcr_content/par/component-plp-section.1.sortBy_0.html",
        "https://www.prada.com/us/en/women/accessories/hats/_jcr_content/par/component-plp-section.1.sortBy_0.html",
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
            goods_gender = start_url.split("/")[5]
            goods_page = self.start_urls.index(start_url) + 1
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.random_headers(),meta={"url":start_url,
                                                                                                       "goods_gender":goods_gender,
                                                                                                       "goods_page":goods_page,})

    def parse(self, response):
        url = response.meta["url"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//a[@class='product-link d-inline-block mx-1 mx-md-auto']/@href").extract()
        for goods_url in goods_urls:
            goods_json_url = "https://www.prada.com/us/en/{}/accessories/hats/products.glb.getProductsByPartNumbers.json?partNumbers={}".format(goods_gender,goods_url.split(".")[2])
            goods_order = goods_urls.index(goods_url) + 1 + (int(url.split(".")[3]) - 1) * 12
            yield scrapy.Request(url=goods_json_url,callback=self.info_json_parse,headers=self.random_headers(),meta={"goods_order":goods_order,
                                                                                                                 "goods_gender":goods_gender,
                                                                                                                 "goods_page":goods_page,
                                                                                                                 "goods_url":"https://www.prada.com{}".format(goods_url),})
        url = "{}.{}.{}.{}.{}.{}".format(url.split(".")[0],url.split(".")[1],url.split(".")[2],int(url.split(".")[3]) + 1,url.split(".")[4],url.split(".")[5])
        yield scrapy.Request(url=url,callback=self.parse,headers=self.random_headers(),meta={"url":url,
                                                                                             "goods_gender":goods_gender,
                                                                                             "goods_page":goods_page,})

    def info_json_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_info = eval(response.text.replace("true","True").replace("false","False"))["response"]["catalogEntryView"][0]
        goods_name = goods_info["name"]
        goods_model = goods_info["mfPartNumber_ntk"]
        g_price = goods_info["price"][0]["formattedPrice"]
        goods_price = "{}{}".format(g_price.split(" ")[1],g_price.split(" ")[0])
        goods_discount_price = "{}0".format(g_price.split(" ")[1])
        goods_color = goods_info["colors"]
        goods_size = [i["value"] for i in goods_info["sizeCodes"]]
        goods_details = goods_info["shortDescription"].split("\n")
        goods_details.append(goods_info["longDescription"])
        goods_images = ["{}/_jcr_content/renditions/cq5dam.web.white.1280x1280.jpeg".format(i["attachmentAssetPath"]) for i in goods_info["attachments"]]
        print(goods_images)

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