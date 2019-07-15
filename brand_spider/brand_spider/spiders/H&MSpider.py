import scrapy
import time
import uuid
import random

# "scrapy crawl adidas -o adidas.csv"

class HMSpider(scrapy.Spider):
    name = "hm"
    start_urls = [
        # "https://www2.hm.com/en_us/men/products/accessories.html?product-type=men_accessories&sort=stock&productTypes=cap,hat&image-size=small&image=model&offset=0&page-size=72",
        # "https://www2.hm.com/en_us/ladies/products/accessories.html?product-type=ladies_accessories&sort=stock&productTypes=beret,cap,hat&image-size=small&image=stillLife&offset=0&page-size=36",
        # "https://www2.hm.com/en_us/kids/products/view-all.html?sort=stock&productTypes=cap,hat&image-size=small&image=stillLife&offset=0&page-size=252",

        "https://www2.hm.com/en_us/men/products/view-all.html?sort=stock&productTypes=bag&image-size=small&image=model&offset=0&page-size=36",
        "https://www2.hm.com/en_us/women/products/view-all.html?sort=stock&productTypes=bag&image-size=small&image=model&offset=0&page-size=36",
        "https://www2.hm.com/en_us/kids/products/view-all.html?sort=stock&productTypes=bag&image-size=small&image=stillLife&offset=0&page-size=36",
    ]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-sRequests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }

    def sleep_time(self):
        """
        睡眠0-2s之间的随机时间
        :return:
        """
        ran_time = random.uniform(0, 1)
        time.sleep(ran_time)

    def upload_html(self,response):
        with open("./1.html","w",encoding="utf-8") as f:
            f.write(response.text)

    def start_requests(self):
        for start_url in self.start_urls:
            goods_gender = start_url.split("/")[4]
            if goods_gender == "ladies":
                goods_gender = "women"
            goods_page = self.start_urls.index(start_url)
            yield scrapy.Request(url=start_url,callback=self.num_parse,headers=self.headers,meta={"start_url":start_url,
                                                                                                "goods_gender":goods_gender,
                                                                                                "goods_page":goods_page,})

    def num_parse(self,response):
        all_num = response.xpath("//h2[@class='load-more-heading']/@data-total").extract()[0]
        start_url = response.meta["start_url"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        url = "{}page-size={}".format(start_url.split("page-size=")[0],all_num)
        yield scrapy.Request(url=url, callback=self.parse, headers=self.headers,meta={"goods_gender": goods_gender,
                                                                                        "goods_page": goods_page, })

    def parse(self, response):
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_urls = ["https://www2.hm.com{}".format(i) for i in response.xpath("//h3[@class='item-heading']/a/@href").extract()]
        for goods_url in goods_urls:
            self.sleep_time()
            goods_order = goods_urls.index(goods_url) + 1
            yield scrapy.Request(url=goods_url, callback=self.info_parse, headers=self.headers,meta={"goods_order":goods_order,
                                                                                                     "goods_gender":goods_gender,
                                                                                                     "goods_page":goods_page,
                                                                                                     "goods_url":goods_url,},dont_filter=True)

    def info_parse(self,response):
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_info = eval(response.text.split('var productArticleDetails =')[-1].split('</script><script type="text/template" id="fullscreenModalTmpl">')[0].strip().strip(";").replace("true","True").replace("false","False").replace("null","None").replace("isDesktop ?","").replace("' : '//","-----"))
        goods_name = goods_info["alternate"].split("- {alternatecolor}")[0].strip()
        goods_model = goods_info["articleCode"].strip()
        goods_price = goods_info[goods_model]["whitePrice"].strip()
        goods_discount_price = "{}0".format(goods_price[0])
        goods_color = goods_info[goods_model]["name"].strip()
        goods_size = [i["name"] for i in goods_info[goods_model]["sizes"]]
        goods_dels = [goods_info[goods_model]["description"].strip()]
        try:
            goods_dels1 = goods_info[goods_model]["compositions"]
        except KeyError:
            goods_dels1 = []
        goods_details = goods_dels + goods_dels1
        goods_images = ["https:{}".format(i["image"].split("-----")[0]) for i in goods_info[goods_model]["images"]]
        print(goods_name)

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