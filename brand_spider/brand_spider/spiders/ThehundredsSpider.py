import scrapy
import re

# "scrapy crawl thehundreds -o thehundreds.csv"

class ThehundredsSpider(scrapy.Spider):
    name = "thehundreds"
    start_urls = [
        "https://thehundreds.com/collections/dad-hats",
        "https://thehundreds.com/collections/snapbacks",
        "https://thehundreds.com/collections/new-era-hats",
        "https://thehundreds.com/collections/beanies",
        # "https://thehundreds.com/collections/jackets",
        # "https://thehundreds.com/collections/sweatshirts",
        # "https://thehundreds.com/collections/shirts",
        # "https://thehundreds.com/collections/graphic-t-shirts",
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_page":self.start_urls.index(start_url) + 1})

    def parse(self, response):
        goods_page = response.meta["goods_page"]
        goods_urls = response.xpath("//a[@class='grid__image']/@href").extract()
        for goods_url in goods_urls:
            goods_order = goods_urls.index(goods_url)
            yield scrapy.Request(url="https://thehundreds.com/products/%s.js"%goods_url.split("/")[-1],callback=self.info_json_parse,meta={"goods_order":goods_order + 1,
                                                                                                                                              "goods_page":goods_page,
                                                                                                                                              "goods_url":"https://thehundreds.com%s"%goods_url})

    def info_json_parse(self,response):
        goods_info = eval(response.text.replace('true','"true"').replace('false','"false"').replace('null','"null"'))
        goods_data = {}
        goods_data["goods_name"] = goods_info["title"]
        goods_data["goods_price"] = "$%s"%str(goods_info["price"]//100)
        goods_data["goods_color"] = goods_info["options"][1]["values"]
        goods_data["goods_size"] = [i.replace("\\","") for i in goods_info["options"][0]["values"]]
        goods_data["goods_details"] = [i for i in  re.findall(r">(.*?)<",goods_info["description"]) if i.replace(".","").strip() != ""]
        goods_data["goods_order"] = response.meta["goods_order"]
        goods_data["goods_gender"] = "all"
        goods_data["goods_page"] = response.meta["goods_page"]
        goods_data["goods_url"] = response.meta["goods_url"]
        yield scrapy.Request(url=response.meta["goods_url"],callback=self.info_web_parse,meta={"goods_data":goods_data})

    def info_web_parse(self,response):
        goods_data = response.meta["goods_data"]
        goods_color = goods_data["goods_color"]
        for g_color in goods_color:
            goods_datas = goods_data
            goods_datas["goods_color"] = g_color
            goods_datas["goods_images"] = ["https:%s"%i for i in response.xpath("//div[@data-variant='%s']/img/@src"%g_color).extract() if "960x" in i]
            goods_datas["goods_model"] = response.xpath("//input[@value='%s']/@data-variant"%g_color).extract()[0]
            goods_datas["goods_discount_price"] = "$0"

            yield {
                "goods_name": goods_datas["goods_name"],
                "goods_model": goods_datas["goods_model"],
                "goods_price": goods_datas["goods_price"],
                "goods_discount_price": goods_datas["goods_discount_price"],
                "goods_color":  goods_datas["goods_color"],
                "goods_size": str(goods_datas["goods_size"]),
                "goods_details": str(goods_datas["goods_details"]),
                "goods_images": str(goods_datas["goods_images"]),
                "goods_num": goods_datas["goods_order"],
                "gender": goods_datas["goods_gender"],
                "goods_page": goods_datas["goods_page"],
                "goods_url": goods_datas["goods_url"],
            }

            print(goods_datas["goods_name"],goods_datas["goods_page"],goods_datas["goods_order"])