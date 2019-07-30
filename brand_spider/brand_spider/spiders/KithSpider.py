import scrapy
import time

# "scrapy crawl adidas -o adidas.csv"

class KithSpider(scrapy.Spider):
    name = "kith"
    start_urls = [
        # "https://kith.com/collections/mens-apparel-outerwear?page=1",
        # "https://kith.com/collections/mens-apparel-hoodies?page=1",
        # "https://kith.com/collections/mens-apparel-tees?page=1",
        # "https://kith.com/collections/mens-apparel-crewnecks?page=1",
        # "https://kith.com/collections/mens-apparel-button-ups?page=1",
        # "https://kith.com/collections/womens-apparel-outerwear?page=1",
        # "https://kith.com/collections/womens-apparel-hoodies?page=1",
        # "https://kith.com/collections/womens-apparel-tees?page=1",
        # "https://kith.com/collections/womens-apparel-tank-tops?page=1",
        # "https://kith.com/collections/womens-apparel-dresses?page=1",
        # "https://kith.com/collections/kids-apparel-outerwear?page=1",
        # "https://kith.com/collections/kids-apparel-hoodies?page=1",
        # "https://kith.com/collections/kids-apparel-tees?page=1",

        ["https://kith.com/collections/mens-accessories-hats?page=1", "mens", "hats"],
        ["https://kith.com/collections/womens-accessories/headwear?page=1", "womens", "hats"],
        ["https://kith.com/collections/kids-accessories/headwear?page=1", "kids", "hats"],

        ["https://kith.com/collections/mens-accessories-bags?page=1", "mens", "bags"],
        ["https://kith.com/collections/womens-accessories/bags?page=1", "womens", "bags"],
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    def upload_html(self,response):
        with open("./1.html","w",encoding="utf-8") as f:
            f.write(response.text)

    def start_requests(self):
        for start_url in self.start_urls:
            url = start_url[0]
            goods_gender = start_url[1]
            goods_type = start_url[2]
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,
                                                                                              "goods_page":self.start_urls.index(start_url) + 1,
                                                                                              "goods_gender":goods_gender,
                                                                                              "goods_type":goods_type,})

    def parse(self, response):
        url = response.meta["url"]
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        goods_type = response.meta["goods_type"]
        goods_urls = ["https://kith.com%s"%i for i in response.xpath("//li[@class='collection-product']/div/div/div/a[1]/@href").extract()]
        for goods_url in goods_urls:
            goods_order = goods_urls.index(goods_url) + 1 + (int(url.split("=")[1]) - 1)*12
            yield scrapy.Request(url=goods_url,callback=self.goods_info_parse,headers=self.headers,meta={"goods_order":goods_order,
                                                                                                         "goods_page":goods_page,
                                                                                                         "goods_url":goods_url,
                                                                                                         "goods_gender": goods_gender,
                                                                                                         "goods_type": goods_type,
                                                                                                         })
        if len(goods_urls) != 0:
            url = "%s=%s"%(url.split("=")[0],int(url.split("=")[1])+1)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url": url,
                                                                                        "goods_page": goods_page,
                                                                                        "goods_gender": goods_gender,
                                                                                        "goods_type": goods_type,
                                                                                        })

    def goods_info_parse(self,response):
        goods_gender = response.meta["goods_gender"]
        goods_order = response.meta["goods_order"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_type = response.meta["goods_type"]
        goods_name = response.xpath("//h1[@class='product-single__title']/text()").extract()[0]
        goods_details = [i.replace("<p>","").replace("</p>","").replace("<span>","").replace("</span>","").replace("\xa0","").replace("<strong>","").replace("</strong>","").strip() for i in response.xpath("//div[@id='product-single-description']/p").extract()]
        goods_details = [i for i in goods_details if i != ""]
        try:
            goods_model = goods_details[-3].split(":")[-1].strip()
            goods_color = goods_details[-2].split(":")[-1].strip()
        except:
            goods_model = goods_url.split("/")[-1].upper()
            goods_color = response.xpath("//h2[@class='product-single__color']/text()").extract()[0]
        goods_price = response.xpath("//button[@class='btn product-form__add-to-cart']/span/text()").extract()[0]
        goods_discount_price = "$0"
        goods_size = response.xpath("//div[@class='swatch clearfix']/div/label/span/text()").extract()
        goods_images = ["https:%s"%i.replace("300x300","2048x") for i in response.xpath("//div[@class='product-single__images']/div[1]/div/div/img/@src").extract()]

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
            "goods_type": goods_type,
        }
