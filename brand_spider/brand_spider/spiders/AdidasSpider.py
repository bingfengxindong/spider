import scrapy
import time

# "scrapy crawl adidas -o adidas.csv"

class AdidasSpider(scrapy.Spider):
    name = "adidas"
    start_urls = [
        "https://www.adidas.com.cn/plp/waterfall.json?commingsoontype=&ni=47&pr=-&pn=1&pageSize=120&isSaleTop=false&cp=1&ps=1&iz=120&ci=39",
        "https://www.adidas.com.cn/plp/waterfall.json?commingsoontype=&ni=99&pr=-&pn=1&pageSize=120&isSaleTop=false&cp=1&ps=1&iz=120&ci=89",
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"url":start_url,
                                                                                              "goods_page":self.start_urls.index(start_url),
                                                                                              })
    def parse(self, response):
        url = response.meta["url"]
        goods_page = response.meta["goods_page"]
        num = int(url.split("cp=")[-1].split("&ps=")[0])
        if eval(response.text.replace("true", "True").replace("false", "False"))["returnObject"] != {}:
            goods_infos = eval(response.text.replace("true","True").replace("false","False"))["returnObject"]["view"]["items"]
            for goods_info in goods_infos:
                goods_name = goods_info["t"]
                goods_model = goods_info["c"]
                goods_price = "￥%s"%goods_info["sp"]
                goods_discount_price = "￥0"
                gender = lambda x:"men" if url.split("ni=")[-1].split("&pr=")[0] == "47" else "women"
                goods_gender = gender(url)
                goods_title = goods_info["st"]
                goods_order = goods_infos.index(goods_info) + 1 + 20 * (num - 1)
                goods_url = "https://www.adidas.com.cn/item/%s?locale=zh_CN"%goods_model
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                       "goods_model":goods_model,
                                                                                                       "goods_price":goods_price,
                                                                                                       "goods_discount_price":goods_discount_price,
                                                                                                       "goods_order":goods_order,
                                                                                                       "goods_gender":goods_gender,
                                                                                                       "goods_title":goods_title,
                                                                                                       "goods_page":goods_page,
                                                                                                       "goods_url":goods_url,
                                                                                                       },dont_filter=True)
            url = "%scp=%s&ps=%s"%(url.split("cp=")[0],num + 1,url.split("&ps=")[-1])
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,
                                                                                        "goods_page":goods_page,
                                                                                        })
    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_title = response.meta["goods_title"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_color = response.xpath("//div[@class='pdp-color events-color-close']/h3/text()").extract()[0].split("(")[0]
        goods_size = [i.replace("\n","").replace("\t","") for i in response.xpath("//ul[@class='float-clearfix']/li/a/text()").extract() if i.replace("\n","").replace("\t","") != ""]
        goods_details = response.xpath("//div[@class='float-clearfix']/div/p/text()|//div[@class='float-clearfix']/div/ul/li/p/text()").extract()
        goods_images = ["https:%s"%i for i in response.xpath("//div[@class='scroll-background-image']/a/img/@data-smartzoom").extract()]
        goods_comment_itemstyle = response.xpath("//input[@id='itemStyle']/@value").extract()[0]
        goods_comment_url = "https://www.adidas.com.cn/product/showItemRateByStyleAndStar?style=%s&pageNum=1&score="%goods_comment_itemstyle
        print(goods_comment_url)