from lxml import etree
import scrapy

# "scrapy crawl globebrand -o globebrand.csv"


class GlobebrandSpider(scrapy.Spider):
    name = "globebrand"
    start_urls = [
        "https://us.globebrand.com/collections/hats?page=1"
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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"url":start_url,})

    def parse(self, response):
        url = response.meta["url"]
        num = int(url.split("page=")[-1])
        goods_infos = response.xpath("//div[@class='grid-view-item']").extract()
        if len(goods_infos) != 0:
            for goods_info in goods_infos:
                goods_order = goods_infos.index(goods_info) + 1 + (num - 1) * 12
                goods_info_html = etree.HTML(goods_info)
                goods_name = goods_info_html.xpath("//div[@class='h4 grid-view-item__title']/text()")[0]
                goods_price = goods_info_html.xpath("//span[@class='product-price__price']/text()")[0]
                goods_images = ["https:%s"%i.replace("300x300","2048x") for i in goods_info_html.xpath("//div[@class='grid-view-item__image-wrapper js']/div/img/@src")]
                goods_url = "https://us.globebrand.com%s"%goods_info_html.xpath("//a[@class='grid-view-item__link grid-view-item__image-container']/@href")[0]
                yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_name,
                                                                                                       "goods_price":goods_price,
                                                                                                       "goods_images":goods_images,
                                                                                                       "goods_order":goods_order,
                                                                                                       "goods_url":goods_url,
                                                                                                       })
            url = "https://us.globebrand.com/collections/hats?page=%s"%(num + 1)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,})

    def info_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_order = response.meta["goods_order"]
        goods_price = response.meta["goods_price"]
        goods_images = response.meta["goods_images"]
        goods_url = response.meta["goods_url"]
        goods_discount_price = "$0"
        goods_model = response.xpath("//div[@class='product-single__meta']/span[2]/text()").extract()[0]
        goods_color = response.xpath("//div[@class='product-single__meta']/span[1]/text()").extract()[0].lower()
        goods_size = response.xpath("//div[@class='selector-wrapper-ac js product-form__item ']/select/option/@value").extract()
        goods_details = [i.replace("+","").replace("\xa0","").strip() for i in response.xpath("//div[@class='product-single__description rte']/p/text()|//div[@class='product-single__description rte']/ul/li/text()").extract() if i.replace("+","").replace("\xa0","").strip() != ""]
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