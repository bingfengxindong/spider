from lxml import etree
import scrapy
import re

# "scrapy crawl marmot -o marmot.csv"

class MarmotSpider(scrapy.Spider):
    name = "marmot"
    start_urls = [
        "https://www.marmot.com/men/accessories/hats-caps-and-beanies/",
        # "https://www.marmot.com/men/jackets/?sz=48&start=0",
        # "https://www.marmot.com/men/tops/shirts/",
        # "https://www.marmot.com/men/tops/sweatshirts-and-hoodies/",
        # "https://www.marmot.com/men/tops/t-shirts-and-polos/",
        # "https://www.marmot.com/men/tops/baselayer/",
        "https://www.marmot.com/women/accessories/hats-caps-and-beanies/",
        # "https://www.marmot.com/women/jackets/?sz=48&start=0",
        # "https://www.marmot.com/women/tops/shirts/",
        # "https://www.marmot.com/women/tops/sweatshirts-and-hoodies/",
        # "https://www.marmot.com/women/tops/t-shirts-and-polos/",
        # "https://www.marmot.com/women/tops/baselayer/",
        "https://www.marmot.com/kids/boys/accessories/",
        # "https://www.marmot.com/kids/boys/jackets/",
        # "https://www.marmot.com/kids/boys/tops/",
        "https://www.marmot.com/kids/girls/accessories/",
        # "https://www.marmot.com/kids/girls/jackets/",
        # "https://www.marmot.com/kids/girls/tops/",
    ]
    headers = {
        ":authority":"www.marmot.com",
        ":method":"GET",
        ":scheme":"https",
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def start_requests(self):
        for start_url in self.start_urls:
            goods_page = self.start_urls.index(start_url) + 1
            goods_gender = lambda x:x.split("/")[3] if "kids" not in x else x.split("/")[4]
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"goods_page":goods_page,
                                                                                              "goods_gender":goods_gender(start_url),
                                                                                              "start_url":start_url,
                                                                                              },dont_filter=True)

    def parse(self, response):
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        start_url = response.meta["start_url"]
        goods_infos = response.xpath("//li[@class='grid-tile']").extract()
        for goods_info in goods_infos:
            goods_html_info = etree.HTML(goods_info)
            goods_name = [i.replace("\n","") for i in goods_html_info.xpath("//a[@class='name-link']/text()")][0]
            goods_urls = goods_html_info.xpath("//ul[@class='swatch-list']/li/a/@href")
            if "?" in start_url:
                goods_order = goods_infos.index(goods_info) + 1 + int(start_url.split("=")[-1])
            else:
                goods_order = goods_infos.index(goods_info) + 1
            for goods_url in goods_urls:
                self.headers[":path"] = goods_url.split(".com/")[-1]
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                       "goods_order":goods_order,
                                                                                                       "goods_url":goods_url,
                                                                                                       "goods_page":goods_page,
                                                                                                       "goods_gender":goods_gender,
                                                                                                       },dont_filter=True)
        if len(goods_infos) != 0 and "?" in start_url:
            url = "{}=48&start={}".format(start_url.split("=")[0],int(start_url.split("=")[-1]) + int(start_url.split("=")[-2].split("&")[0]))
            yield scrapy.Request(url=start_url, callback=self.parse, headers=self.headers,meta={"goods_page": goods_page,
                                                                                               "goods_gender": goods_gender,
                                                                                               "start_url": url,
                                                                                               },dont_filter=True)

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_order = response.meta["goods_order"]
        goods_url = response.meta["goods_url"]
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        print(response.xpath("//span[@class='price-sales']/text()").extract())
        goods_price = response.xpath("//span[@class='price-sales']/text()").extract()[0].strip("\n")
        if goods_price != "":
            goods_discount_price = "%s0"%goods_price[0]
        else:
            goods_discount_price = response.xpath("//span[@class='price-standard']/text()").extract()[0].strip("\n")
            goods_price = "$%s0"%str(float(goods_discount_price.strip("$")) // 2)
        goods_color = [i.strip("\n") for i in response.xpath("//span[@class='selected-value']/text()").extract() if i.strip("\n") != ""][0]
        goods_model = "%s-%s"%(goods_url.split("/")[-1].split(".html")[0],goods_url.split("_color=")[-1].split("&")[0])
        goods_size = [i.strip("\n") for i in response.xpath("//*[@id='product-content']/div[1]/ul/li[2]/div[2]/ul/li/a/text()").extract()]
        goods_details = [i.replace("\n","") for i in response.xpath("//div[@class='content-limit-inner']/text()|//ul[@class='content-limit-inner']/li/text()|//*[@id='pdpMain']/div[6]/div[4]/div[1]/div[3]/div/ul/li/div[2]/text()").extract()if i.replace("\n","") != ""][:-1]
        goods_images = [i.replace("hei=60","hei=1200").replace("wid=38","wid=1000") for i in response.xpath("//img[@class='productthumbnail']/@src").extract()]
        print(goods_name,goods_price,goods_discount_price)
        if "Mitt" not in goods_name or "Glove" not in goods_name:
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