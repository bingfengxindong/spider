import scrapy
import time

# "scrapy crawl matix -o matix.csv"
# "需要改改顺序，这个数据是一个页面的"

class MatixSpider(scrapy.Spider):
    name = "matix"
    start_urls = [
        "https://matixclothing.com/collections/headwear?page=1",
        # "https://matixclothing.com/collections/jackets?page=1",
        # "https://matixclothing.com/collections/flannels?page=1",
        # "https://matixclothing.com/collections/sweaters?page=1",
        # "https://matixclothing.com/collections/wovens?page=1",
        # "https://matixclothing.com/collections/sweatshirts?page=1",
        # "https://matixclothing.com/collections/knits?page=1",
        # "https://matixclothing.com/collections/tees?page=1",
        # "https://matixclothing.com/collections/tanks?page=1",

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
            yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"start_url":start_url,
                                                                                              "page":int(start_url[-1]),})

    def parse(self, response):
        start_url = response.meta["start_url"]
        print(start_url)
        page = response.meta["page"]
        goods_names = response.xpath("//h2[@class='product-name']/a/@title").extract()
        goods_sizes = response.xpath("//li[@class='avactive']/a/text()|//li[@class='notactve']/text()").extract()
        goods_prices = [i.strip("From ") for i in response.xpath("//span[@class='amout']/span/text()").extract()]
        goods_urls = ["https://matixclothing.com%s" % i for i in response.xpath("//h2[@class='product-name']/a/@href").extract()]
        goods_images = ["https:%s"%i.replace("large","1024x1024") for i in response.xpath("//div[@class='product-thumbnail']/a/img[1]/@src").extract()]
        for goods_url in goods_urls:
            g_order = goods_urls.index(goods_url)
            yield scrapy.Request(url=goods_url,callback=self.info_parse,headers=self.headers,meta={"goods_url":goods_url,
                                                                                                   "g_order":g_order,
                                                                                                   "goods_name":goods_names[g_order],
                                                                                                   "goods_size":goods_sizes[g_order],
                                                                                                   "goods_price":goods_prices[g_order],
                                                                                                   "goods_image":goods_images[g_order],
                                                                                                   "page":page,
                                                                                                   })
        if len(goods_urls) != 0:
            start_url = "{}={}".format(start_url.split("=")[0],int(start_url.split("=")[-1]) + 1)
            yield scrapy.Request(url=start_url, callback=self.parse, headers=self.headers, meta={"start_url": start_url,
                                                                                                 "page": int(start_url[-1]),})

    def info_parse(self,response):
        goods_url = response.meta["goods_url"]
        g_order = response.meta["g_order"]
        goods_name = response.meta["goods_name"]
        goods_size = [response.meta["goods_size"]]
        goods_price = response.meta["goods_price"]
        goods_image = response.meta["goods_image"]
        page = response.meta["page"]
        goods_model = goods_url.split("=")[-1]
        goods_color_image = [i.replace("\n","").replace("\t","").replace("</script>","") for i in response.text.split('<div class="product-description">')[-1].split('<div class="product-actions-wrapper">')[0].split("<script>") if i.replace("\n","").replace("\t","").replace("</div><!-- /.product-description -->","").replace("</script>","").replace("var thumbn=[];","").strip() != ""]
        goods_colors = [i.split(";")[0].strip().split("'")[1] for i in goods_color_image]
        goods_color_images = ["https:%s"%i.split(";")[5].strip().split('"')[1].replace("83x","1024x1024") for i in goods_color_image]
        goods_color = goods_colors[goods_color_images.index(goods_image)]

        yield {
            "goods_name":goods_name,
            "goods_model":goods_model,
            "goods_price":goods_price,
            "goods_discount_price":"%s0"%goods_price[0],
            "goods_color":goods_color,
            "goods_size":str(goods_size),
            "goods_details":"[]",
            "goods_images":str([goods_image]),
            "goods_num": g_order + 1,
            "gender":"all",
            "goods_page":page,
            "goods_url":goods_url,
        }