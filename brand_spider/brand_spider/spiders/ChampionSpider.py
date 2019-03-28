from lxml import etree
import scrapy
import re

# "scrapy crawl champion -o champion.csv"

class ChampionSpider(scrapy.Spider):
    name = "champion"
    start_urls = [
        "https://www.champion.com/shop/champion/men/hats-and-caps#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/hoodies-and-sweatshirts#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/short-sleeve-t-shirts#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/long-sleeve-t-shirts#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/graphic-tees#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/jackets-outerwear#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/baselayer-thermal#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/men/tank-tops#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        "https://www.champion.com/shop/champion/women/hats-and-caps#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/sweatshirts-and-tops#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/short-sleeve-shirts#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/long-sleeve-shirts#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/jackets-outerwear#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/tank-tops-cami#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/women-thermals#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
        # "https://www.champion.com/shop/champion/women/plus-size-tops#facet:&productBeginIndex:0&orderBy:&pageView:grid&minPrice:&maxPrice:&pageSize:20&",
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
                                                                                              "goods_page":self.start_urls.index(start_url) + 1,
                                                                                              })

    def parse(self, response):
        start_url = response.meta["start_url"]
        goods_gender = start_url.split("/")[5]
        goods_page = response.meta["goods_page"]
        goods_infos = response.xpath("//div[@class='each-product-container-row match-height-context-3']/div").extract()
        for goods_info in goods_infos:
            html = etree.HTML(goods_info)
            goods_name = html.xpath("//a[@class='item-name match-height-element-3']/text()")[0]
            # try:
            goods_price = [i.replace("\n", "").replace("\t", "") for i in html.xpath("//span[@class='vert-font current_price bfx-price']/text()")][0]
            # except:
            #     print(goods_name)
            goods_url = html.xpath("//div[@class='quickview-holder']/a/@href")[0]
            goods_colors = html.xpath("//button[@class='each-swatch subCatDefaultSwatch selected']/@onclick|//button[@class='each-swatch ']/@onclick")
            goods_colors = [re.findall(r"\'(.*?)\'",i) for i in goods_colors]
            g_model = [re.findall(r"\'(.*?)\'",i) for i in html.xpath("//div[@class='quickview-holder']/a/@onclick")][0][1]
            goods_order = goods_infos.index(goods_info)
            for goods_color in goods_colors:
                url = "%s&colorPref=%s"%(goods_url,goods_color[0])
                yield scrapy.Request(url=url,callback=self.info_parse,headers=self.headers,meta={"url":url,
                                                                                                "goods_name":goods_name,
                                                                                                "goods_color":goods_color[0],
                                                                                                 "g_model":g_model,
                                                                                                "goods_price":goods_price,
                                                                                                "goods_order":goods_order + 1,
                                                                                                "goods_gender":goods_gender,
                                                                                                "goods_page":goods_page,
                                                                                                })
        # if len(goods_infos) != 0:
        #     now_page = int(start_url.split("&productBeginIndex:")[-1].split("&")[0])
        #     start_url = "{}&productBeginIndex:{}&orderBy:{}".format(start_url.split("&productBeginIndex:")[0],now_page + 20,start_url.split("&productBeginIndex:")[-1].split("&orderBy:")[-1])
        #     yield scrapy.Request(url=start_url,callback=self.parse,headers=self.headers,meta={"start_url":start_url,
        #                                                                                       "goods_page":goods_page,})

    def info_parse(self,response):
        # 产品详情url
        goods_url = response.meta["url"]
        # 产品名字
        goods_name = response.meta["goods_name"].strip('"')
        # 产品颜色
        goods_color = response.meta["goods_color"]
        # 产品型号
        g_model = response.meta["g_model"]
        goods_model = "%s-%s"%(g_model,goods_color)
        # 产品价格
        goods_price = response.meta["goods_price"]
        goods_discount_price = "$0"
        # 产品尺寸
        goods_size = response.xpath("//*[@id='size_1']/ul/li/div/span/text()").extract()
        #产品详情
        goods_details = [i for i in [i.replace("\n","").replace("\t","").strip() for i in response.xpath("//*[@id='container']/div[13]/div/div/div[6]/div[4]/div/div[1]/text()|//*[@id='container']/div[13]/div/div/div[6]/div[4]/div/div[1]/ul/li/text()|//*[@id='more-details-content']/div/text()").extract()] if i != ""]
        #产品图片
        # goods_images = ["https:%s?defaultImage=%s/%s&layer=comp&fit=constrain,1&wid=852&hei=1080&fmt=jpg&resmode=sharp2&op_sharpen=1"%(i.split("?")[0],i.split("?")[0].split("/")[-2],i.split("?")[0].split("/")[-1]) for i in response.xpath("//div[@class='hidden-mobile']/img/@src").extract()]
        goods_images = ["https://hanes.scene7.com/is/image/Hanesbrands/HNS_%s_%s?defaultImage=Hanesbrands/HNS_%s_%s&layer=comp&fit=constrain,1&wid=852&hei=1080&fmt=jpg&resmode=sharp2&op_sharpen=1"%(g_model,goods_color,g_model,goods_color)]
        #产品位置
        goods_order = response.meta["goods_order"]
        #产品人群
        goods_gender = response.meta["goods_gender"]
        #产品页面编号
        goods_page = response.meta["goods_page"]

        print(goods_name)
        yield {
            "goods_name":goods_name,
            "goods_model":goods_model,
            "goods_price":goods_price,
            "goods_discount_price":goods_discount_price,
            "goods_color":goods_color,
            "goods_size":str(goods_size),
            "goods_details":str(goods_details),
            "goods_images":str(goods_images),
            "goods_num":goods_order,
            "gender":goods_gender,
            "goods_page":goods_page,
            "goods_url":goods_url,
        }