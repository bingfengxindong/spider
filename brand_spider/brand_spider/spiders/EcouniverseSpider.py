from lxml import etree
import scrapy

# "scrapy crawl ecouniverse -o ecouniverse.csv"

class EcouniverseSpider(scrapy.Spider):
    name = "ecouniverse"
    start_urls = [
        "https://www.ecouniverse.com/category/2/eco-caps/"
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
        urls = ["https://www.ecouniverse.com%s"%i for i in response.xpath("//div[@class='categoryShortBlock']/a/@href|//div[@class='categoryShortBlock categoryShortTab']/a/@href").extract()]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.url_parse,headers=self.headers)

    def url_parse(self,response):
        goods_infos = response.xpath("//div[@class='productShort']|//div[@class='productShort productShortTab']").extract()
        for goods_info in goods_infos:
            goods_info_html = etree.HTML(goods_info)
            goods_name = goods_info_html.xpath("//div[@class='productShortTitle']/a/text()")[0]
            goods_price = goods_info_html.xpath("//div[@class='productShortTitle']/text()")[0]
            goods_url = "https://www.ecouniverse.com%s"%goods_info_html.xpath("//div[@class='productShortTitle']/a/@href")[0]
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers)

    def info_parse(self,response):
        pass