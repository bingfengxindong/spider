from lxml import etree
import scrapy
import re

# "scrapy crawl alpha -o alpha.csv"

class LifeisgoodSpider(scrapy.Spider):
    name = "life_is_good"
    start_urls = [
        "https://www.lifeisgood.com/men/hats/",
        "https://www.lifeisgood.com/women/hats/",
        "https://www.lifeisgood.com/kids/hats/",
    ]
    headers = {
        ':authority': 'www.lifeisgood.com',
        ':method': 'GET',
        ':path': '/men/hats/',
        ':scheme': 'https',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def start_requests(self):
        for start_url in self.start_urls:
            self.headers[":path"] = "/{}/{}".format(start_url.split("/")[-2],start_url.split("/")[-1])
            goods_gender = start_url.split("/")[-2]
            goods_page = self.start_urls.index(start_url) + 1
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_gender":goods_gender,
                                                                                              "goods_page": goods_page,})

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//a[@class='name-link']/@href").extract()
        for goods_url in goods_urls:
            yield scrapy.Request(url=goods_url, callback=self.goods_info_parse, headers=self.headers,meta={"goods_url":goods_url,
                                                                                                           "goods_gender":goods_gender,
                                                                                                           "goods_order":goods_urls.index(goods_url) + 1,
                                                                                                           "goods_page":goods_page,})

    def data_heavy(self,data):
        datas = []
        for dt in data:
            if dt not in datas:
                datas.append(dt)
        return datas

    def goods_info_parse(self,response):
        goods_url = response.meta["goods_url"]
        goods_gender = response.meta["goods_gender"]
        goods_order = response.meta["goods_order"]
        goods_page = response.meta["goods_page"]
        goods_name = response.xpath("//h1/text()").extract()[0]
        goods_model = response.xpath("//span[@itemprop='productID']/text()|//div[@class='product-price']/div/text()").extract()[0]
        goods_price = response.xpath("//span[@class='price-sales']/text()|//span[@class='price-sales']/font/font/text()|//div[@class='product-price']/div/text()").extract()[0].replace("\n","").strip()
        goods_discount_price = response.xpath("//span[@class='price-standard']/text()").extract()
        if goods_discount_price == []:
            goods_discount_price = "$0"
        else:
            goods_discount_price = goods_discount_price
        goods_color = response.xpath("//span[@class='selected-value']/text()").extract()[0]
        goods_content = response.xpath("//div[@class='product-variations']/ul/li/span/text()").extract()
        if len(goods_content) == 4:
            goods_size = [goods_content[3]]
        elif len(goods_content) == 3:
            goods_size = [i.strip("\n") for i in response.xpath("//div[@class='product-variations']/ul/li/div[@class='value']/ul/li/a/text()").extract()]
        goods_det1 = response.xpath("//div[@class='product-description']/p/text()").extract()
        goods_det2 = response.xpath("//div[@class='product-description']/ul/li/text()").extract()
        goods_details = goods_det1 + goods_det2
        goods_images = self.data_heavy([eval(i)["url"] for i in response.xpath("//ul[@class='slides']/li/a/img/@data-lgimg").extract()])

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
