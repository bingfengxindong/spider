from lxml import etree
from fake_useragent import UserAgent
import scrapy

class HerschelSpider(scrapy.Spider):
    name = "herschel"
    start_urls = [
        # "https://herschel.com/shop/mens/headwear",
        # "https://herschel.com/shop/womens/headwear",
        "https://herschel.com/shop/kids/headwear",
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

    def start_requests(self):
        for start_url in self.start_urls:
            goods_gender = start_url.split("/")[-2]
            goods_page = self.start_urls.index(start_url) + 1
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_gender":goods_gender,
                                                                                               "goods_page":goods_page,
                                                                                              },dont_filter=True)

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        g_urls = response.xpath("//a[@class='js-product-grid-link']/@href").extract()
        goods_price_infos = response.xpath("//div[@class='col-xs-6 text-right']").extract()
        for g_url in g_urls:
            goods_order = g_urls.index(g_url) + 1
            goods_price_info_html = etree.HTML(goods_price_infos[goods_order - 1])
            goods_price = "$%s"%goods_price_info_html.xpath("//span[@class='hsco-set-currency bfx-price']/text()")[0]
            goods_discount_price = goods_price_info_html.xpath("//span[@class='slash-price hsco-set-currency bfx-price']/text()")
            if goods_discount_price == []:
                goods_discount_price = "$0"
            else:
                goods_discount_price = "$%s"%goods_discount_price[0]
            if goods_gender == "kids":
                yield scrapy.Request(url="https://herschel.com%s" % g_url,callback=self.goods_url_parse,headers=self.headers,meta={"g_url": g_url,
                                                                                                                                     "goods_price": goods_price,
                                                                                                                                     "goods_discount_price": goods_discount_price,
                                                                                                                                     "goods_gender": goods_gender,
                                                                                                                                     "goods_page": goods_page,
                                                                                                                                     "goods_order": goods_order,
                                                                                                                                     })
            else:
                yield scrapy.Request(url="https://herschel.com%s"%g_url,callback=self.goods_url_parse,headers=self.headers,meta={"g_url":g_url,
                                                                                                                                      "goods_price":goods_price,
                                                                                                                                      "goods_discount_price":goods_discount_price,
                                                                                                                                      "goods_gender":goods_gender,
                                                                                                                                      "goods_page":goods_page,
                                                                                                                                      "goods_order":goods_order,
                                                                                                                                      },dont_filter=True)

    def goods_url_parse(self,response):
        g_url = response.meta["g_url"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_order = response.meta["goods_order"]
        g_name = g_url.split("/")[-1].split("?")[0]
        goods_models = set(response.xpath("//li[@class='colors-list__color']/label/@id|//li[@class='colors-list__color on']/label/@id|//li[@class='colors-list__color colors-list__desktopandmobile']/label/@id|//li[@class='colors-list__color colors-list__desktopandmobile on']/label/@id").extract())
        for goods_model in goods_models:
            goods_url = "https://herschel.com/shop/headwear/%s?v=%s"%(g_name,goods_model)
            if goods_gender == "kids":
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_model": goods_model,
                                                                                                       "goods_url": goods_url,
                                                                                                       "goods_price": goods_price,
                                                                                                       "goods_discount_price": goods_discount_price,
                                                                                                       "goods_gender": goods_gender,
                                                                                                       "goods_page": goods_page,
                                                                                                       "goods_order": goods_order,
                                                                                                       })
            else:
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_model":goods_model,
                                                                                                        "goods_url":goods_url,
                                                                                                        "goods_price": goods_price,
                                                                                                        "goods_discount_price": goods_discount_price,
                                                                                                        "goods_gender": goods_gender,
                                                                                                        "goods_page": goods_page,
                                                                                                        "goods_order": goods_order,
                                                                                                       },dont_filter=True)

    def info_parse(self,response):
        goods_name = response.xpath("//h2[@class='product-overview__title']/text()").extract()[0]
        goods_model = response.meta["goods_model"]
        goods_price = response.xpath("//span[@class='h4 hsco-product-price bfx-price']/text()|//span[@class='h4 hsco-product-price bfx-price text-error']/text()").extract()
        goods_url = response.meta["goods_url"]
        if goods_price == []:
            goods_price = response.meta["goods_price"]
        else:
            goods_price = goods_price[0]
        goods_discount_price = "$0"
        # goods_color = response.xpath("//h4[@class='hsco-product-color']/span/text()").extract()[0]
        goods_color = response.xpath("//label[@id='%s']/input/@data-color"%goods_model).extract()[0]
        goods_size = ["all"]
        goods_details = [i for i in response.xpath("//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/text()|//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/a/text()|//div[@class='pdp-features-container']/div[1]/div/div/div[@class='link--underline features-list']/div/ul/li/text()").extract() if i.strip() != ""]
        goods_images = ["https://herschel.com%s"%i for i in response.xpath("//label[@id='%s']/input/@data-images"%goods_model).extract()[0].split(",")]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_order = response.meta["goods_order"]
        print(goods_name)

        yield {
            "goods_name": goods_name,
            "goods_model": goods_model,
            "goods_price": "$%s"%goods_price.strip("$"),
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