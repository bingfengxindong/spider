import scrapy

# "scrapy crawl asos -o asos.csv"

class AsosSpider(scrapy.Spider):
    name = "asos"
    start_urls = [
        "https://www.asos.com/women/new-in/accessories/cat/?cid=27109&currentpricerange=25-3505&nlid=ww|new%20in|new%20products&refine=attribute_1047:8238,8275,8245",
        "https://www.asos.com/women/accessories/hats/cat/?cid=6449&currentpricerange=35-770&nlid=ww|accessories|shop%20by%20product&refine=attribute_1047:8238,8275,8245,8243",
        "https://www.asos.com/women/outlet/accessories/cat/?cid=27392&currentpricerange=10-1325&nlid=ww|outlet|shop%20by%20product&refine=attribute_1047:8238,8275,8245",
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
            goods_page = self.start_urls.index(start_url) + 1
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_page":goods_page,
                                                                                              "url":start_url,
                                                                                              "json_page": 0,
                                                                                              })

    def parse(self, response):
        goods_page = response.meta["goods_page"]
        url = response.meta["url"]
        json_page = response.meta["json_page"]
        json_url = "https://api.asos.com/product/search/v1/categories/%s?channel=desktop-web&country=CN&currency=CNY&keyStoreDataversion=fcnu4gt-12&lang=en&limit=72&offset=%s&refine=attribute_1047%s&rowlength=4&store=24"%(url.split("?cid=")[-1].split("&")[0],json_page,url.split("attribute_1047")[-1])
        yield scrapy.Request(url=json_url,callback=self.json_parse,headers=self.headers,meta={"goods_page":goods_page,
                                                                                              "json_url_page":json_page // 72 + 1,
                                                                                              })
        urls = response.xpath("//a[@data-auto-id='loadMoreProducts']/@href").extract()
        if urls != []:
            yield scrapy.Request(url=urls[0],callback=self.parse,headers=self.headers,meta={"goods_page":goods_page,
                                                                                            "url": urls[0],
                                                                                            "json_page":json_page + 72,
                                                                                            })

    def json_parse(self,response):
        goods_page = response.meta["goods_page"]
        json_url_page = response.meta["json_url_page"]
        goods_infos = eval(response.text.replace("null","None").replace("false","False").replace("true","True"))
        goods_products = goods_infos["products"]
        for goods_product in goods_products:
            goods_name = goods_product["name"]
            goods_model = goods_product["id"]
            goods_price = goods_product["price"]["current"]["text"]
            g_discount_price = lambda x:"%s0"%goods_price[0] if x == "" else x
            goods_discount_price = g_discount_price(goods_product["price"]["rrp"]["text"])
            goods_color = goods_product["url"].split("clr=")[-1]
            goods_size = [i["size"] for i in goods_product["images"]]
            goods_order = (json_url_page - 1) * 72 + goods_products.index(goods_product) + 1
            goods_gender = "women"
            goods_url = "https://www.asos.com/%s"%goods_product["url"]
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                   "goods_model":goods_model,
                                                                                                   "goods_price":goods_price,
                                                                                                   "goods_discount_price":goods_discount_price,
                                                                                                   "goods_color":goods_color,
                                                                                                   "goods_size":goods_size,
                                                                                                   "goods_order":goods_order,
                                                                                                   "goods_gender":goods_gender,
                                                                                                   "goods_page":goods_page,
                                                                                                   "goods_url":goods_url,
                                                                                                   })

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_size = response.meta["goods_size"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_details = [i.replace("\xa0","") for i in response.xpath("//div[@class='product-description']/span/ul/li/text()|//div[@class='product-description']/span/ul/li/span/text()|//div[@class='product-description']/span/ul/li/ul/li/text()|//div[@class='about-me']/span/div/text()|//div[@class='about-me']/span/text()").extract()]
        goods_images = ["https:%s"%i.replace("$S$","$XXL$").replace("wid=40","wid=870") for i in response.xpath("//div[@class='thumbnails']/ul/li/a/img/@src").extract()]

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
