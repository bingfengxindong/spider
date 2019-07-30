import scrapy
import re
import time
# "scrapy crawl newlook -o newlook.csv"

class NewlookSpider(scrapy.Spider):
    name = "newlook"
    start_urls = [
        ["https://www.newlook.com/uk/mens/accessories/c/uk-mens-accessories?comp=NavigationBar%7Cmn%7Cmens%7Caccessories%7Chome%7Ctracking&LocationContext=NavigationBar%7CMegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&ParentContext=MegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&DataTrackerCode=NavigationBar%7Cmn%7Cmens%7Caccessories%7Chome%7Ctracking#/?q=:relevance:styleCodes:Caps:styleCodes:Hats&page=0&sort=relevance&content=false","mens","hats"],
        ["https://www.newlook.com/uk/womens/accessories/c/uk-womens-accessories?comp=NavigationBar%7Cmn%7Cwomens%7Caccessories%7Chome%7Cbold&LocationContext=NavigationBar%7CMegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&ParentContext=MegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&DataTrackerCode=NavigationBar%7Cmn%7Cwomens%7Caccessories%7Chome%7Cbold#/?q=:relevance:styleCodes:Hats&page=0&sort=relevance&content=false","womens","hats"],
        ["https://www.newlook.com/uk/mens/accessories/c/uk-mens-accessories?comp=NavigationBar%7Cmn%7Cmens%7Caccessories%7Chome%7Ctracking&LocationContext=NavigationBar%7CMegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&ParentContext=MegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&DataTrackerCode=NavigationBar%7Cmn%7Cmens%7Caccessories%7Chome%7Ctracking#/?q=:relevance:styleCodes:Backpacks:styleCodes:Cross%20Body%20Bags:styleCodes:Shoulder%20Bags&page=0&sort=relevance&content=false","mens","bags"],
        ["https://www.newlook.com/uk/womens/accessories/c/uk-womens-accessories?comp=NavigationBar%7Cmn%7Cwomens%7Caccessories%7Chome%7Cbold&LocationContext=NavigationBar%7CMegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&ParentContext=MegaNavigationBarComponent%7Cuk%20Mega%20Navigation%20Bar&DataTrackerCode=NavigationBar%7Cmn%7Cwomens%7Caccessories%7Chome%7Cbold#/?q=:relevance:styleCodes:Day%20Bags:styleCodes:Shoulder%20Bags:styleCodes:Cross%20Body%20Bags:styleCodes:Evening%20Bags:styleCodes:Clutch%20Bags:styleCodes:Top%20Handle%20Bags:styleCodes:Straw%20Bags:styleCodes:Backpacks:styleCodes:Tote%20Bags:styleCodes:Fringed%20Bags&page=0&sort=relevance&content=false","womens","bags"],
    ]
    json_urls = [
        "https://www.newlook.com/uk/mens/accessories/c/uk-mens-accessories/data-48.json?currency=GBP&language=en&lastIndexTime=1563334216194&page=0&q=:relevance:styleCodes:Caps:styleCodes:Hats&sort=relevance&text=",
        "https://www.newlook.com/uk/womens/accessories/c/uk-womens-accessories/data-48.json?currency=GBP&language=en&lastIndexTime=1563334216194&page=0&q=:relevance:styleCodes:Hats&sort=relevance&text=",
        "https://www.newlook.com/uk/mens/accessories/c/uk-mens-accessories/data-48.json?currency=GBP&language=en&lastIndexTime=1563334216194&page=0&q=:relevance:styleCodes:Backpacks:styleCodes:Cross+Body+Bags:styleCodes:Shoulder+Bags&sort=relevance&text=",
        "https://www.newlook.com/uk/womens/accessories/c/uk-womens-accessories/data-48.json?currency=GBP&language=en&lastIndexTime=1563334216194&page=0&q=:relevance:styleCodes:Day+Bags:styleCodes:Shoulder+Bags:styleCodes:Cross+Body+Bags:styleCodes:Evening+Bags:styleCodes:Clutch+Bags:styleCodes:Top+Handle+Bags:styleCodes:Straw+Bags:styleCodes:Backpacks:styleCodes:Tote+Bags:styleCodes:Fringed+Bags&sort=relevance&text=",
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
            url = start_url[0]
            goods_gender = start_url[1]
            goods_type = start_url[2]
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers,meta={"url":url,
                                                                                      "goods_page":self.start_urls.index(start_url) + 1,
                                                                                      "goods_gender":goods_gender,
                                                                                      "goods_type":goods_type,
                                                                                      # "proxy": "https://123.1.150.244:80",
                                                                                      },dont_filter=True)

    def parse(self, response):
        url = response.meta["url"]
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        goods_type = response.meta["goods_type"]
        goods_number = int(response.xpath("//p[@class='product-count']/text()").extract()[0].split(" ")[-2])
        page = goods_number // 48 + 1
        json_url = self.json_urls[goods_page - 1]
        for i in range(page):
            json_u = "{}lastIndexTime={}&page={}&q={}".format(json_url.split("lastIndexTime=")[0],int(time.time()*1000),i,json_url.split("&q=")[-1])
            yield scrapy.Request(url=json_u,
                                 callback=self.json_parse,
                                 headers=self.headers,
                                 meta={"goods_page":goods_page,
                                       "goods_gender":goods_gender,
                                       "goods_type":goods_type,
                                       "page":i,
                                       # "proxy":"https://123.1.150.244:80",
                                       })

    def json_parse(self,response):
        goods_page = response.meta["goods_page"]
        goods_gender = response.meta["goods_gender"]
        goods_type = response.meta["goods_type"]
        page = response.meta["page"]
        goods_infos = eval(response.text.replace("true","True").replace("false","False"))["data"]["results"]
        for goods_info in goods_infos:
            goods_name = goods_info["name"]
            goods_price = goods_info["price"]["formattedValue"]
            if "previousPrice" in goods_info.keys():
                goods_discount_price = goods_info["previousPrice"]["formattedValue"]
            else:
                goods_discount_price = "%s0"%goods_price[0]
            goods_size = [goods_info["sizeOptions"][0]["value"].replace(" ","").lower()]
            goods_order = goods_infos.index(goods_info) + 1 + (page * 48)
            colourOptions = goods_info["colourOptions"]
            for colourOption in colourOptions.values():
                goods_model = colourOption["code"]
                goods_color = colourOption["displayName"]
                goods_url = "https://www.newlook.com/uk%s"%colourOption["url"]
                time.sleep(2)
                yield scrapy.Request(url="https://www.newlook.com/uk/json/products/products.json?categoryCodes=&from=0&isGallery=true&limit=8&priorityProductRelationCount=0&productCodes=%s&productReferenceTypeCodes=&quickView=false&to=7"%goods_model,
                                     callback=self.json_image_parse,
                                     headers=self.headers,
                                     meta={"goods_name":goods_name,
                                           "goods_model":goods_model,
                                           "goods_price":goods_price,
                                           "goods_discount_price":goods_discount_price,
                                           "goods_color":goods_color,
                                           "goods_size":goods_size,
                                           "goods_order":goods_order,
                                           "goods_gender":goods_gender,
                                           "goods_page":goods_page,
                                           "goods_url":goods_url,
                                           "goods_type":goods_type,
                                           # "proxy":"https://123.1.150.244:80",
                                           })

    def json_image_parse(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_size = response.meta["goods_size"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_type = response.meta["goods_type"]
        goods_lists = eval(response.text.replace("false","False").replace("true","True"))["list"]
        if len(goods_lists) == 1:
            goods_images = ["https:%s?strip=true&qlt=80&w=1400"%i["url"] for i in goods_lists[0]["gallery"]]
        else:
            goods_images = "none"
        yield scrapy.Request(url="https://www.newlook.com/uk/json/multiProduct/productDetails.json?id=%s"%goods_model,
                             callback=self.json_description_json,
                             headers=self.headers,
                             meta={"goods_name": goods_name,
                                   "goods_model": goods_model,
                                   "goods_price": goods_price,
                                   "goods_discount_price": goods_discount_price,
                                   "goods_color": goods_color,
                                   "goods_size": goods_size,
                                   "goods_images": goods_images,
                                   "goods_order": goods_order,
                                   "goods_gender": goods_gender,
                                   "goods_page": goods_page,
                                   "goods_url": goods_url,
                                   "goods_type": goods_type,
                                   # "proxy": "https://123.1.150.244:80",
                                   })

    def json_description_json(self,response):
        goods_name = response.meta["goods_name"]
        goods_model = response.meta["goods_model"]
        goods_price = response.meta["goods_price"]
        goods_discount_price = response.meta["goods_discount_price"]
        goods_color = response.meta["goods_color"]
        goods_size = response.meta["goods_size"]
        goods_images = response.meta["goods_images"]
        goods_order = response.meta["goods_order"]
        goods_gender = response.meta["goods_gender"]
        goods_page = response.meta["goods_page"]
        goods_url = response.meta["goods_url"]
        goods_type = response.meta["goods_type"]
        goods_desc_info = eval(response.text.replace("false","False").replace("true","True"))
        if goods_images == "none":
            g_image = "https:%s?strip=true&qlt=80&w=1400"%goods_desc_info["data"][goods_model]["primaryImage"]["url"]
            goods_images = [g_image,g_image.replace(goods_model,"%sD1"%goods_model),g_image.replace(goods_model,"%sD2"%goods_model)]
        goods_details1 = [i.strip("-").strip() for i in re.findall(r">(.*?)<",goods_desc_info["data"][goods_model]["colourOptions"][goods_model]["description"]) if i != ""]
        goods_details2 = [i.strip() for i in re.findall(r">(.*?)<",goods_desc_info["data"][goods_model]["washCare"]) if i != ""]
        goods_details = goods_details1 + goods_details2
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
            "goods_type": goods_type,
        }