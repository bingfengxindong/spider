import scrapy
import re

# "scrapy crawl newera -o newera.csv"

class NewEraSpider(scrapy.Spider):
    name = "newera"
    start_urls = [
        "https://www.neweracap.co.uk/headwear/?p=1&category=headwear&gender=mens",
        "https://www.neweracap.co.uk/headwear/?p=1&category=headwear&gender=womens",
        "https://www.neweracap.co.uk/headwear/?p=1&category=headwear&gender=kids",
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
            yield scrapy.Request(url=start_url,
                                 callback=self.parse,
                                 headers=self.headers,
                                 meta={"url":start_url,
                                      "goods_page":self.start_urls.index(start_url) + 1,
                                      "goods_gender":start_url.split("=")[-1],
                                      })

    def parse(self, response):
        url = response.meta["url"]
        page = int(url.split("=")[1].split("&")[0])
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        goods_infos = [re.findall(r"\'(.*?)\'",i) for i in response.xpath("//*[@id='main']/div[3]/div[2]/div/div/a/@onclick").extract()]
        goods_names = [i[0] for i in goods_infos]
        goods_models = [i[1] for i in goods_infos]
        goods_orders = [int(i[-2]) + (page - 1) * 12 for i in goods_infos]
        goods_urls = ["https://www.neweracap.co.uk%s"%i for i in response.xpath("//*[@id='main']/div[3]/div[2]/div/div/a/@href").extract()]
        for goods_url in goods_urls:
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_name":goods_names[goods_urls.index(goods_url)],
                                                                                                   "url":url,
                                                                                                   "goods_model":goods_models[goods_urls.index(goods_url)],
                                                                                                   "goods_order":goods_orders[goods_urls.index(goods_url)],
                                                                                                   "goods_gender":goods_gender,
                                                                                                   "goods_page":goods_page,
                                                                                                   "goods_url":goods_url,
                                                                                                   })
        next_page = response.xpath("//a[@class='pagination__next']/@href").extract()
        if len(next_page) == 2:
            yield scrapy.Request(url="https://www.neweracap.co.uk/headwear/%s"%next_page[0],
                                 callback=self.parse,headers=self.headers,
                                 meta={"goods_gender":goods_gender,
                                       "goods_page": goods_page,
                                       "url":"https://www.neweracap.co.uk/headwear/%s"%next_page[0],})

    def info_parse(self,response):
        url = response.meta["url"]
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = [i.replace("now ","") for i in response.xpath("//*[@id='main']/div[1]/div/div[2]/p/text()|//*[@id='main']/div[1]/div/div[2]/p/span[2]/text()").extract() if i.replace("\r","").replace("\n","").replace("\xa0","").strip() != ""]
        goods_discount_price = [i.replace("Was ", "").replace("now ", "") for i in response.xpath("//*[@id='main']/div[1]/div/div[2]/p/span[1]/text()").extract()]
        if goods_price == [] and "-" in goods_discount_price[0]:
            goods_price = goods_discount_price[0].split(" - ")[-1]
            goods_discount_price = "£0"
        elif goods_discount_price != []:
            goods_price = goods_price[0]
            goods_discount_price = goods_discount_price[0]
        else:
            goods_price = goods_price[0]
            goods_discount_price = "£0"

        goods_color = response.xpath("//select[@id='SelectedColour']/option/text()").extract()[1]
        goods_size = [i.replace(" - Out of Stock","") for i in response.xpath("//select[@id='SelectedSize']/option/text()").extract()[1:]]
        goods_details = [i for i in response.xpath("//div[@class='product-detail__desc panel--mobile']/p/text()|//div[@class='product-detail__desc panel--mobile']/li/text()|//div[@class='product-detail__desc panel--mobile']/text()").extract() if i.replace("\r\n","").strip() != ""]
        goods_images = ["https://www.neweracap.co.uk%s"%i.replace("w=425","w=1000") for i in response.xpath("//img[@class='product__item-image']/@src").extract()]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]

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

        print(goods_name)
        print(goods_model)
        print(goods_price)
        print(goods_discount_price)
        print(goods_color)
        print(len(goods_size),goods_size)
        print(len(goods_details),goods_details)
        print(len(goods_images),goods_images)
        print(goods_order)
        print(goods_gender)
        print(goods_page)
        print(goods_url)
        print(url)
        print("*"*100)