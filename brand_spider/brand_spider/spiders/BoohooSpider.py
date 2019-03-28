from lxml import etree
import scrapy
import re

# "scrapy crawl boohoo -o boohoo.csv"

class BoohooSpider(scrapy.Spider):
    name = "boohoo"
    start_urls = [
        "https://www.boohoo.com/mens/accessories/caps-hats-and-beanies",
        "https://www.boohoo.com/womens/accessories/hats-scarves",
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_page":self.start_urls.index(start_url) + 1,
                                                                                              "url":start_url,
                                                                                              })

    def parse(self, response):
        goods_page = response.meta["goods_page"]
        goods_infos = response.xpath("//li[@class='grid-tile ']|//li[@class='grid-tile new-row']").extract()
        url = response.meta["url"]
        page_size = lambda x:0 if "start=" not in x else int(url.split("start=")[-1])
        size = page_size(url)
        goods_gender = url.split("/")[3]
        for goods_info in goods_infos:
            goods_info_html = etree.HTML(goods_info)
            g_info = eval(goods_info_html.xpath("//div[@class='product-tile']/@data-product-tile")[0].replace("null","None"))
            goods_type = g_info["category"]
            if goods_type == "Hats" or goods_type == "Accessories":
                goods_order = goods_infos.index(goods_info) + 1 + size
                goods_name = g_info["name"]
                print(goods_name)
                g_model = g_info["id"]
                goods_price = goods_info_html.xpath("//span[@class='product-sales-price']/text()")[0]
                if goods_price == "N/A":
                    goods_price = "£0"
                    goods_discount_price = "£0"
                else:
                    goods_discount_price = goods_info_html.xpath("//span[@class='product-standard-price']/text()")
                    if len(goods_discount_price) == 0:
                        goods_discount_price = "£0"
                    else:
                        goods_discount_price = goods_discount_price[0]
                goods_urls = ["https://www.boohoo.com%s"%i for i in goods_info_html.xpath("//li[@class='product-swatch-item']/a/@href|//a[@class='thumb-link']/@href")]
                for goods_url in goods_urls:
                    yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                           "g_model":g_model,
                                                                                                           "goods_price":goods_price,
                                                                                                           "goods_discount_price":goods_discount_price,
                                                                                                           "goods_url":goods_url,
                                                                                                           "goods_page":goods_page,
                                                                                                           "goods_order":goods_order,
                                                                                                           "goods_gender":goods_gender,
                                                                                                           })
        url = response.xpath("//li[@class='pagination-item pagination-item-next']/a/@href").extract()
        if url != []:
            yield scrapy.Request(url=url[0],callback=self.parse,headers=self.headers,meta={"goods_page":goods_page,
                                                                                           "url":url[0],
                                                                                           })

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        g_model = response.meta["g_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_url = response.meta["goods_url"]
        goods_page = response.meta["goods_page"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_info = eval(response.xpath("//form[@class='pdpForm js-pdpForm']/@data-product-details").extract()[0].replace("null","None"))
        goods_color = goods_info["dimension65"]
        goods_size = goods_info["dimension68"].replace(" ","").lower()
        goods_model = "%s-%s"%(g_model,goods_color)
        detail = lambda x:x if len(x) != 0 else [""]
        goods_details1 = response.xpath("//li[@id='product-short-description-tab']/div/p/em/strong/text()").extract()
        goods_details2 = [re.sub(r"<.*?>","",detail(response.xpath("//li[@id='product-short-description-tab']/div/p[2]").extract())[0])]
        goods_details3 = response.xpath("//li[@id='product-custom-composition-tab']/div/text()|//li[@id='product-custom-composition-tab']/div/font/font/text()").extract()
        goods_details = goods_details1 + goods_details2 + goods_details3
        yield scrapy.Request(url="https://i1.adis.ws/s/boohooamplience/%s_ms.js?deep=true&protocol=https"%g_model.lower(),callback=self.img_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                                                                                                        "goods_model": goods_model,
                                                                                                                                                                                        "g_model": g_model,
                                                                                                                                                                                        "goods_price": goods_price,
                                                                                                                                                                                        "goods_discount_price": goods_discount_price,
                                                                                                                                                                                        "goods_color": goods_color,
                                                                                                                                                                                        "goods_size": goods_size,
                                                                                                                                                                                        "goods_details": goods_details,                                                                                                                                                                                        "goods_num": goods_order,
                                                                                                                                                                                        "goods_order": goods_order,                                                                                                                                                                                        "goods_num": goods_order,
                                                                                                                                                                                        "goods_gender": goods_gender,
                                                                                                                                                                                        "goods_page": goods_page,
                                                                                                                                                                                        "goods_url": goods_url,
                                                                                                                                                                                        })

    def img_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        g_model = response.meta["g_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_size = [response.meta["goods_size"]]
        goods_details = response.meta["goods_details"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        image_infos = eval(response.text.replace("imgSet(","").replace(");","").replace("\\",""))
        goods_images = [j["src"] for j in [i for i in image_infos["items"] if i["name"] == "%s_%s_ms"%(g_model.lower(),goods_color)][0]["set"]["items"]]

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