import scrapy

# "scrapy crawl happytree -o happytree.csv"

class HappytreeSpider(scrapy.Spider):
    name = "hippytree"
    start_urls = [
        "https://www.hippytree.com/shop/hats/page/1"
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
            yield scrapy.Request(url=start_url,
                                 callback=self.parse,
                                 headers=self.headers,
                                 meta={"url":start_url,},)

    def parse(self, response):
        url = response.meta["url"]
        goods_names = response.xpath("//span[@class='tile__name product-tile__name']/text()").extract()
        goods_urls = ["https://www.hippytree.com%s"%i for i in response.xpath("//a[@class='tile__link']/@href").extract()]
        for goods_url in goods_urls:
            goods_order = (int(url.split("page/")[-1]) - 1) * 48 + (goods_urls.index(goods_url) + 1)
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_url":goods_url,
                                                                                                   "goods_order":goods_order,
                                                                                                   })
        goods_paginations = response.xpath("//li[@class='pagination__item']/a/text()").extract()
        try:
            url = "%spage/%s"%(url.split("page/")[0],goods_paginations[goods_paginations.index(url.split("page/")[-1]) + 1])
        except IndexError:
            pass
        else:
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,},)

    def info_parse(self,response):
        goods_name = response.xpath("//h1[@class='product__name']/text()").extract()[0]
        goods_model = response.xpath("//span[@class='product__code']/text()").extract()[0]
        goods_price = [i.replace("\n","").replace("\t","").replace(" ","") for i in response.xpath("//p[@class='product__price']/text()|//p[@class='product__price']/span/text()").extract() if i.replace("\n","").replace("\t","").replace(" ","") != ""][0]
        g_discount_price = lambda x:x[0] if x != [] else "$0"
        goods_discount_price = g_discount_price(response.xpath("//p[@class='product__price']/s/text()").extract())
        goods_color = response.xpath("//p[@class='product__variation']/text()").extract()[0].split(":")[-1].strip()
        goods_size = [response.xpath("//label[@class='product__sizes-title']/text()").extract()[0].split(":")[-1].strip().replace(" ","").lower()]
        goods_details = [i.replace("\n","").replace("\r","") for i in response.xpath("//div[@class='product__description']/ul/li/text()").extract()]
        goods_images = ["https:%s"%i for i in response.xpath("//a[@class='product__thumb-link']/@href").extract()]
        goods_order = response.meta["goods_order"]
        goods_gender = "all"
        goods_page = 1
        goods_url = response.meta["goods_url"]

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