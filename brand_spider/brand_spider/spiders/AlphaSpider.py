import scrapy
import re

# "scrapy crawl alpha -o alpha.csv"

class AlphaSpider(scrapy.Spider):
    name = "alpha"
    start_urls = [
        "https://www.alphaclothing.co/collections/accessories"
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        goods_urls = ["https://www.alphaclothing.co%s.json"%i for i in response.xpath("//a[@itemprop='url']/@href").extract()]
        for goods_url in goods_urls:
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_order":goods_urls.index(goods_url) + 1,
                                                                                                   "goods_url":goods_url.split(".json")[0]
                                                                                                   },)

    def info_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_url = response.meta["goods_url"]
        goods_info = eval(response.text.replace("true","True").replace("false","False").replace("null","None"))
        goods_name = goods_info["product"]["title"].replace("\\","")
        goods_model = goods_info["product"]["id"]
        goods_price = "$%s"%goods_info["product"]["variants"][0]["price"]
        goods_discount_price = "$0"
        if "-snapback-" in goods_url:
            goods_color = goods_url.split("-snapback-")[-1]
        if "-cap-" in goods_url:
            if "-tribe-" in goods_url:
                goods_color = goods_url.split("-tribe-")[-1]
            elif "-stamp-" in goods_url:
                goods_color = goods_url.split("-stamp-")[-1]
            elif "-identity-" in goods_url:
                goods_color = goods_url.split("-identity-")[-1]
            elif "-washed-" in goods_url:
                goods_color = goods_url.split("-washed-")[-1]
            else:
                goods_color = goods_url.split("-cap-")[-1]
        goods_size = ["onesize"]
        goods_details = [i.replace("\xa0","").strip() for i in re.findall(r">(.*?)<",goods_info["product"]["body_html"]) if i.replace("\xa0","").strip() != ""]
        goods_images = [i["src"].replace("\\","") for i in goods_info["product"]["images"]]
        goods_gender = "all"
        goods_page = 1

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