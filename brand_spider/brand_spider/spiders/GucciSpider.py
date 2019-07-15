from fake_useragent import UserAgent

import scrapy
import time
import uuid
import random

# "scrapy crawl adidas -o adidas.csv"

class GucciSpider(scrapy.Spider):
    name = "gucci"
    start_urls = [
        "https://www.gucci.com/us/en/c/productgrid?categoryCode=men-accessories-hats-and-gloves&show=Page&page=0",
        "https://www.gucci.com/us/en/c/productgrid?categoryCode=women-accessories-hats-and-gloves&show=Page&page=0",
        "https://www.gucci.com/us/en/c/productgrid?categoryCode=children-boys-accessories&show=Page&page=0",
        "https://www.gucci.com/us/en/c/productgrid?categoryCode=girls-soft-accessories&show=Page&page=0",

        # "https://www.gucci.com/us/en/c/productgrid?categoryCode=men-bags-backpacks&show=Page&page=0",
        # "https://www.gucci.com/us/en/c/productgrid?categoryCode=women-handbags-belt&show=Page&page=0",
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
            goods_gender = start_url.split("=")[1].split("-")[0]
            if goods_gender == "children":
                goods_gender = "boys"
            goods_page = self.start_urls.index(start_url)
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.random_headers(),meta={"url":start_url,
                                                                                                       "goods_gender":goods_gender,
                                                                                                       "goods_page":goods_page,})

    def parse(self, response):
        url = response.meta["url"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_infos = eval(response.text.replace("true","True").replace("false","False").replace("null","None"))["products"]["items"]
        print(len(goods_infos))
        for goods_info in goods_infos:
            goods_name = goods_info["productName"]
            goods_model = goods_info["productCode"]
            goods_price = goods_info["price"]
            if goods_price == None:
                goods_price = "$0"
            goods_price = goods_price.replace(" ","").replace(",","")
            goods_discount_price = "{}0".format(goods_price[0])
            goods_color = goods_info["variant"]
            goods_images = ["https:{}".format(i["src"].replace("316x316","1200x1200")) for i in goods_info["alternateGalleryImages"]]
            goods_url = "https://www.gucci.com/us/en{}".format(goods_info["productLink"])
            goods_order = goods_infos.index(goods_info) + 1 + (36 * int(url.split("&page=")[-1]))
            self.sleep_time()
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.random_headers(),meta={"goods_name":goods_name,
                                                                                                            "goods_model":goods_model,
                                                                                                            "goods_price":goods_price,
                                                                                                            "goods_discount_price":goods_discount_price,
                                                                                                            "goods_color":goods_color,
                                                                                                            "goods_images":goods_images,
                                                                                                            "goods_gender":goods_gender,
                                                                                                            "goods_page":goods_page,
                                                                                                            "goods_order":goods_order,
                                                                                                            "goods_url":goods_url,
                                                                                                            },dont_filter=True)
        if len(goods_infos) != 0:
            url = "{}&page={}".format(url.split("&page=")[0],int(url.split("&page=")[-1]) + 1)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.random_headers(),meta={"url":url,
                                                                                                 "goods_gender": goods_gender,
                                                                                                 "goods_page": goods_page,})

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_images = response.meta["goods_images"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_order = response.meta["goods_order"]
        goods_url = response.meta["goods_url"]
        goods_size = self.del_report([i.replace("\n","").replace("\xa0","").replace(" ","") for i in response.xpath("//select[@name='size']/option/text()").extract() if i.replace("\n","").replace("\xa0","").replace(" ","") != "SelectSize"])
        goods_details = [i.replace("\n","").strip() for i in response.xpath("//div[@class='product-detail']/p/text()|//div[@class='product-detail']/ul/li/text()").extract()]
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