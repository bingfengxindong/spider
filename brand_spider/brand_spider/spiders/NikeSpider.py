import scrapy
import time
import random

# "scrapy crawl adidas -o adidas.csv"

class KithSpider(scrapy.Spider):
    name = "nike"
    start_urls = [
        "https://store.nike.com/cn/zh_cn/pw/mens-hats-caps/7puZof1",
        "https://store.nike.com/cn/zh_cn/pw/womens-hats-caps/7ptZof1",
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
            goods_gender = start_url.split("-")[0].split("/")[-1]
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,dont_filter=True,meta={"goods_gender":goods_gender,
                                                                                                                "goods_page":self.start_urls.index(start_url) + 1,})

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//div[@class='grid-item-image']/div/a/@href").extract()
        for goods_url in goods_urls:
            time.sleep(random.randint(0,10)/10)
            yield scrapy.Request(url=goods_url,callback=self.goods_url_parse,headers=self.headers,dont_filter=True,meta={"goods_url":goods_url,
                                                                                                                        "goods_order":goods_urls.index(goods_url) + 1,
                                                                                                                        "goods_gender":goods_gender,
                                                                                                                        "goods_page":goods_page,})

    def goods_url_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//a[@class='colorway-anchor']/@href").extract()
        if len(goods_urls) == 0:
            goods_urls = [response.meta["goods_url"]]
        for goods_url in goods_urls:
            time.sleep(random.randint(0, 10) / 10)
            yield scrapy.Request(url=goods_url,callback=self.goods_info_parse,headers=self.headers,dont_filter=True,meta={"goods_order":goods_order,
                                                                                                                         "goods_gender":goods_gender,
                                                                                                                         "goods_page":goods_page,
                                                                                                                         "goods_url":goods_url,})

    def goods_info_parse(self,response):
        # with open("./1.html","w",encoding="utf-8") as f:
        #     f.write(response.text)
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_name = response.xpath("//h1[@id='pdp_product_title']/text()").extract()[0]
        goods_details = response.xpath("//div[@class='pi-pdpmainbody']/p/b/text()|//div[@class='pi-pdpmainbody']/ul/li/text()|//div[@class='pi-pdpmainbody']/li/text()").extract()
        goods_model = [i for i in goods_details if "款式" in i][0].strip("款式：").strip()
        goods_color = [i for i in goods_details if "显示颜色" in i][0].strip("显示颜色：").strip()
        goods_price = response.xpath("//div[@class='text-color-black']/text()|//div[@class='mb-1-sm text-color-black']/text()").extract()[0]
        goods_discount_price = response.xpath("//div[@class='text-color-grey u-strikethrough']/text()").extract()
        if len(goods_discount_price) == 0:
            goods_discount_price = "%s0"%goods_price[0]
        else:
            goods_discount_price = goods_discount_price[0]
        goods_size = response.xpath("//div[@class='mt4-sm mb2-sm mr0-lg ml0-lg availableSizeContainer mt5-sm mb3-sm fs16-sm']/label/text()").extract()
        if len(goods_size) == 0:
            goods_size = ["均码"]
        # goods_images = response.xpath("//img[@class='css-10f9kvm u-full-width u-full-height']/@src|//ul[@class='exp-pdp-alt-images-carousel']/li/img/@data-large-image").extract()
        goods_images = response.xpath("//img[@class='css-viwop1 u-full-width u-full-height css-m5dkrx']/@src").extract()
        goods_title = response.xpath("//h2[@class='fs16-sm pb1-sm']/text()").extract()[0]
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