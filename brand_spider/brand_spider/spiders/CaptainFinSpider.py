from lxml import etree
import scrapy

# "scrapy crawl captainfin -o captainfin.csv"

class CaptainFinSpider(scrapy.Spider):
    name = "captainfin"
    start_urls = [
        "https://captainfin.com/collections/hats?page=1",
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"url":start_url,"goods_len":0})

    def parse(self, response):
        url = response.meta["url"]
        goods_len = response.meta["goods_len"]
        goods_infos = response.xpath("//div[@class='product-wrap']").extract()
        for goods_info in goods_infos:
            goods_info_html = etree.HTML(goods_info)
            goods_url = "https://captainfin.com%s" % goods_info_html.xpath("//a[@class='product-info__caption ']/@href")[0]
            g_price = goods_info_html.xpath("//span[@class='price ']/span/span/text()|//span[@class='price sale']/span/span/text()|//span[@class='price ']/span[@class='sold_out']/text()|//span[@class='price sale']/span[@class='sold_out']/text()")[0].replace(" ","")
            if g_price != "SoldOut":
                g_info = eval(goods_info_html.xpath("//div[@class='info']/div/div/@data-product")[0].replace("true",'"true"').replace("false",'"false"').replace("null",'"null"'))
                goods_name = g_info["title"]
                goods_model = g_info["id"]
                goods_price = "$%s"%(g_info["price"] // 100)
                g_discount_price = lambda x,y:"$0" if x == y or x == "null" else "$%s"%(x // 100)
                goods_discount_price = g_discount_price(g_info["compare_at_price"],g_info["price"])
                goods_color = g_info["variants"][0]["option1"].replace("\\","").lower()
                if goods_color == "default title":
                    goods_color = goods_url.split("-")[-1]
                goods_size = ["OS"]
                goods_details = [i.replace("\n","") for i in g_info["content"].replace("\\","").replace("<p>","").replace("</p>","").replace("<span>","").replace("</span>","").replace("<ul>","").replace("</ul>","").replace("</li>","").replace("<strong>","").replace("</strong>","").replace('<meta charset="utf-8">',"").split("<li>")]
                goods_images = ["https:%s"%i.replace("\\","") for i in g_info["images"]]
                goods_order = goods_infos.index(goods_info) + 1 + goods_len
                goods_gender = "all"

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
                    "goods_page": 1,
                    "goods_url": goods_url,
                }

        if len(goods_infos) != 0:
            url = "https://captainfin.com/collections/hats?page=%s"%(int(url.split("=")[-1]) + 1)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,"goods_len":len(goods_infos)})