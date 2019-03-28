import scrapy
import re

# "scrapy crawl monki -o monki.csv"

class MonkiSpider(scrapy.Spider):
    name = "monki"
    start_urls = [
        "https://www.monki.com/en_gbp/accessories/hats-scarves-and-gloves/hats.html?offset=0",
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"url":start_url,},)

    def parse(self, response):
        url = response.meta["url"]
        goods_urls = ["https://www.monki.com%s"%i for i in response.xpath("//div[@class='u-cols-lg-6-24 u-cols-md-6-24 u-cols-sm-10-12']/div/div[@class='image']/a/@href|//div[@class='u-cols-lg-6-24 u-cols-md-6-24 u-cols-sm-6-12']/div/div[@class='image']/a/@href").extract()]
        if len(goods_urls) != 0:
            for goods_url in goods_urls:
                goods_order = int(url.split("offset=")[-1]) + goods_urls.index(goods_url) + 1
                yield scrapy.Request(url=goods_url,callback=self.url_parse,headers=self.headers,meta={"goods_order":goods_order,})
            url = "%soffset=%s"%(url.split("offset=")[0],int(url.split("offset=")[-1]) + 7)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,},)

    def url_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_models = response.xpath("//div[@class='a-swatch js-swatch ']/@id|//div[@class='a-swatch js-swatch is-selected']/@id").extract()
        goods_infos = eval(response.text.split("var productArticleDetails = ")[-1].split("</script>")[0].strip().strip(";").replace("true","True").replace("false","False").replace("null","None"))
        for goods_model in goods_models:
            goods_info = goods_infos[goods_model.strip("swatch_")]
            goods_name = goods_info["title"]
            goods_model = goods_model.strip("swatch_")
            goods_price = goods_info["price"]
            goods_discount_price = "%s0"%goods_price[0]
            goods_color = goods_info["name"]
            goods_size = [i["sizeName"] for i in goods_info["variants"]]
            goods_details = [i.replace("<p>","").replace("<\\/p>","").replace("<em>","").replace("<\\/em>","").replace("&nbsp;","").replace("<!--3-->","").strip() for i in goods_info["description"].split("<br \/>") if i != ""]
            goods_details = [i for i in goods_details if i != ""]
            goods_gender = "all"
            goods_page = 1
            goods_url = goods_info["pdpLink"].replace("\\","")
            yield scrapy.Request(url=goods_url,callback=self.goods_url_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                        "goods_model":goods_model,
                                                                                                        "goods_price":goods_price,
                                                                                                        "goods_discount_price":goods_discount_price,
                                                                                                        "goods_color":goods_color,
                                                                                                        "goods_size":goods_size,
                                                                                                        "goods_details":goods_details,
                                                                                                        "goods_order":goods_order,
                                                                                                        "goods_gender":goods_gender,
                                                                                                        "goods_page":goods_page,
                                                                                                        "goods_url":goods_url,})

    def goods_url_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_size = response.meta["goods_size"]
        goods_details = response.meta["goods_details"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_images = ["https:%s"%i for i in response.xpath("//ul[@id='imageUnorderedList']/li/div/img/@src").extract()]

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
