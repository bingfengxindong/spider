import scrapy
import time
import uuid

# "scrapy crawl adidas -o adidas.csv"

class ZaraSpider(scrapy.Spider):
    name = "zara"
    start_urls = [
        "https://www.zara.com/ww/en/man-accessories-hats-caps-l546.html?v1=1181304",
        "https://www.zara.com/ww/en/woman-accessories-headwear-l1013.html?v1=1180390",
        "https://www.zara.com/ww/en/kids-girl-accessories-headwear-l332.html?v1=1211513",
        "https://www.zara.com/ww/en/kids-boy-accessories-hats-l183.html?v1=1211017",
        "https://www.zara.com/ww/en/kids-babygirl-accessories-headwear-l92.html?v1=1211514",
        "https://www.zara.com/ww/en/kids-babyboy-accessories-hats-l9.html?v1=1211515",
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    def start_requests(self):
        for start_url in self.start_urls:
            goods_gender = start_url.split("/")[-1].split("-")[0]
            if goods_gender == "kids":
                goods_gender = start_url.split("/")[-1].split("-")[1]
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_gender":goods_gender,
                                                                                              "goods_page":self.start_urls.index(start_url) + 1,})

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//a[@class='area']/@href|//a[@class='name _item']/@href|//a[@class='name _item ']/@href").extract()
        for goods_url in goods_urls:
            yield scrapy.Request(url=goods_url, callback=self.info_parse, headers=self.headers,meta={"goods_url":goods_url,
                                                                                                     "goods_gender":goods_gender,
                                                                                                     "goods_order":goods_urls.index(goods_url) + 1,
                                                                                                     "goods_page":goods_page,},dont_filter=True)

    def info_parse(self,response):
        goods_url = response.meta["goods_url"]
        goods_gender = response.meta["goods_gender"]
        goods_order = response.meta["goods_order"]
        goods_page = response.meta["goods_page"]
        goods_name = response.xpath("//h1[@class='product-name']/text()").extract()
        if len(goods_name) == 0:
            goods_name = ["{}{}hat".format(goods_gender,str(uuid.uuid1()))]
        goods_name = goods_name[0]
        goods_model = goods_url.split("v1=")[-1].split("&")[0]
        goods_price = "€{}".format(eval(response.xpath("//section[@id='product']/script/text()").extract()[0])[0]["offers"]["price"])
        goods_discount_price = "€0"
        goods_color = response.xpath("//span[@class='_colorName']/text()").extract()[0]
        goods_size = [i.replace(" ","")for i in response.xpath("//span[@class='size-name']/@title").extract()]
        goods_details = [i for i in response.xpath("//p[@class='description']/text()").extract() if i != "Specific conditions for returns. Please review the Terms and Conditions for this item."]
        goods_images = ["https:{}".format(i.replace("/w/560/","/w/1024/")) for i in response.xpath("//a[@class='_seoImg main-image']/@href").extract()]
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