# from lxml import etree
# from selenium import webdriver
# from fake_useragent import UserAgent
# from selenium.webdriver import ActionChains
# from selenium.common.exceptions import NoSuchElementException
# from retrying import retry
#
# import requests
# import random
# import time
# import ssl
# import csv
# import os
# import datetime
#
# path = os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"))
# if not os.path.exists(path):
#     os.makedirs(path)
# file = open(os.path.join(".","data",datetime.datetime.now().strftime("%Y-%m-%d"),"tommy_hilfiger.csv"),"w+",encoding="utf-8",newline="")
# writer = csv.writer(file)
# writer.writerow(("goods_name","goods_model","goods_price","goods_discount_price","goods_color","goods_size","goods_details","goods_images","goods_num","gender","goods_page","goods_url"))
#
# ssl._create_default_https_context = ssl._create_stdlib_context
#
# urls = [
#     "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=MEN_ACCESSORIES_HATS&disableProductCompare=true&categoryId=33674&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=MEN_ACCESSORIES_HATS&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
#     # "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=SCARVES_HATS_GLOVES_cat330002&disableProductCompare=true&categoryId=33689&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=SCARVES_HATS_GLOVES_cat330002&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
#     # "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=MS_BOYS_SHOES_ACCESSOIRES&disableProductCompare=true&categoryId=3074457345617402769&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=MS_BOYS_SHOES_ACCESSOIRES&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
#     # "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=MS_KIDS_GIRLS_SHOES_ACCESSORIES&disableProductCompare=true&categoryId=3074457345617402768&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=MS_KIDS_GIRLS_SHOES_ACCESSORIES&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
#     # "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=SHOES%26ACCESSORIES_TJ_M&disableProductCompare=true&categoryId=3074457345617389280&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=SHOES%26ACCESSORIES_TJ_M&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
#     # "https://usa.tommy.com/ProductListingView?imageBadgeIgnoreCategoryCodeParam=SHOES%26ACCESSORIES_TJ_W&disableProductCompare=true&categoryId=3074457345617389272&pageSize=30&catalogId=10551&langId=-1&isHomeDepartment=false&currentCategoryIdentifier=SHOES%26ACCESSORIES_TJ_W&storeId=10151&beginIndex=0&minFacetCount=1&facet=ads_f15522_ntk_cs%3A%22Hat%22",
# ]
#
# def sleep_time():
#     """
#     睡眠0-2s之间的随机时间
#     :return:
#     """
#     ran_time = random.uniform(0,1)
#     time.sleep(ran_time)
#
# # 输入毫秒级的时间，转出正常格式的时间
# def timeStamp(timeNum):
#     timeStamp = float(timeNum/1000)
#     timeArray = time.localtime(timeStamp)
#     otherStyleTime = time.strftime("%Y/%m/%d", timeArray)
#     return otherStyleTime
#
# def goods_parse(driver):
#     # 获取页面源码
#     pagesource = driver.page_source
#     html = etree.HTML(pagesource)
#     return html
#
# def random_headers():
#     ua = UserAgent(verify_ssl=False)
#     return {
#         "User-Agent": ua.random,
#         "cookie":"optimizelyEndUserId=oeu1554959643029r0.2978650843942847; TH_newsletter=true; _pxvid=bd3d6cae-5c19-11e9-9582-0242ac12000c; user_type=New; CT_CID=DIRECT; CT_KWD=; CT_AD=; CT_ADGROUP=; CT_MATCH=; CT_REF=https%3A//www.google.com.hk/; CT_TestId=0; CT_Plmnt=; CT_AdPos=; CT_ENTRYURL=https%3A//usa.tommy.com/en; CT_CrtDate=4/11/2019%2013%3A14%3A3; CT_UID=1554959644179.3071; CT_Type=1; _ga=GA1.2.210081675.1554959644; ftr_ncd=6; _gcl_au=1.1.337358401.1554959644; __wid=597809987; _fbp=fb.1.1554959644513.1277744520; _scid=948ac9c4-6a22-49d4-a49a-7d4cca02e212; __zlcmid=rli9arHBD9HOXA; sr_browser_id=1128c2e4-f5e5-4bc0-95f1-258545c26db4; __utmz=230066073.1555028011.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); WC_PERSISTENT=Ob8QtfbbLyNKyBtbtd5CgmeFk15Wv3zO%2FY2R6GIu2z8%3D%3B2019-04-11+20%3A34%3A37.371_1555029277369-30510_10151_-1002%2C-1%2CUSD_10151; s_tlm_v31gvo=glp-flyout-men%7C20190401; s_tlm_v31=%5B%5B%27glp-flyout-men%257C2019040120190312%27%2C%271555057930157%27%5D%5D; _gid=GA1.2.78294025.1555288683; storeType=full; __utma=230066073.210081675.1554959644.1555288683.1555292594.6; __utmc=230066073; AMCVS_699ED7075501EBBF0A4C98C6%40AdobeOrg=1; AMCV_699ED7075501EBBF0A4C98C6%40AdobeOrg=-1303530583%7CMCIDTS%7C18002%7CMCMID%7C36714981754197913682146696522369726724%7CMCAAMLH-1555897394%7C11%7CMCAAMB-1555897394%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1555299794s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_cc=true; ats-cid-AM-141075-sid=49280180x; b1pi=!9qEIkZEnsC28ESt3rPJ8u1oN0JYwV4V3Sbx7ti1+djJENAIPMjoOW+kMJd3w5DdfMkmonbaz; WC_SESSION_ESTABLISHED=true; WC_AUTHENTICATION_-1002=-1002%2C17pWqhPbvjH%2BLsEDIp9QPz6eezZmW1l9oiQicFtzla0%3D; WC_ACTIVEPOINTER=-1%2C10151; JSESSIONID=0000CTSiZG-e7lFpPc2MuRtTCRw:1b03gsoav; WC_USERACTIVITY_-1002=-1002%2C10151%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C1565041233%2CTfbwts4w3ORzdppb2PRPicIadM6FDCRabIEQ0I5hXDvX6zS0YKCnwvsk0F36DhSTTc7rhNZHueo6vv1kE2Per6aTLaE%2BqyxraQnQgfubjs2%2FZyTpagaav22eTkOFtBjCqqdKTf02RQQbvq3fPeGAJ9EtXy7UEt4TnHvdWQ59EDJEnPmCb7XzcYyWaK7XO0EKfPwyJUXcQwz7XK0tgVTUb9SGt9mpL%2FWKy5V5lihOKrK7JXyGgvBbJGh9Fxghebbw; WC_GENERIC_ACTIVITYDATA=[1429500056%3Atrue%3Afalse%3A0%3Ab9PJlSLMNK5hl4OYDfgXRdC5HWKcVMAA1r%2BZrIyyET0%3D][com.ibm.commerce.context.ExternalCartContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|10003%2610003%26null%26-2000%26null%26null%26null][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null%26null%26null%26null%26null%26null][com.ibm.commerce.catalog.businesscontext.CatalogContext|10551%26null%26false%26false%26false][CTXSETNAME|Store][com.ibm.commerce.context.base.BaseContext|10151%26-1002%26-1002%26-1][com.ibm.commerce.context.audit.AuditContext|1555029277369-30510][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null%26null%26null][com.ibm.commerce.context.globalization.GlobalizationContext|-1%26USD%26-1%26USD]; previous_page_name=Kids: Girls: Shoes & Accessories: product detail page; s_sq=%5B%5BB%5D%5D; _sctr=1|1555257600000; ADRUM=s=1555295632985&r=https%3A%2F%2Fusa.tommy.com%2Fen%2Ftommy-hilfiger-children-kids-girls-boys-baby-infant%2Ftommy-hilfiger-children-kids-girls-shoes-accessories%2Fth-kids-straw-fedora-au00575%3F0; forterToken=987de7e791684e17a8d2592c06fd3f32_1555295634584__UDF43_6; sr_pik_session_id=cd16b5bd-59af-f563-7e24-d3e57f491e34; guid=9d8e33bf-74fb-4798-8ea6-a86c8085c62a+0abdc960ebc7e9c9dc280db31774683994d0473321295640e4ef80fde13ec3e7e7e62c6fce073e3cce5ba5f1f582aefb994d3fdc35b8272ff57237d8f52df0edb55e3eb76412283cefb3cae76fcbd16f4bcbf423704634f729baddb9800e351c7dc0feefb65ab4559cac764ac53fa3d1d6df0969c3e2df7fc60c64a5dabcf7895bf6eaced9e2764cc31685809380c0f8b89eb50be594757f926663dcb2272c8f7a2648c3e298fa28341d04de54320155817ebb9b1667ec225d99b966cde40a75e60c31065d4cd856b635c4f06ca6491486bc78087992c016d673b950e611341251bdc762e9d8d7098dfbdcadb74bcbc54f24772e139c45f6ca206b50cc7f7082; s_ppvl=Kids%253A%2520Girls%253A%2520Shoes%2520%2526%2520Accessories%253A%2520product%2520detail%2520page%2C77%2C8%2C2171%2C1920%2C256%2C1920%2C1080%2C1%2CP; __utmb=230066073.9.10.1555292594; _px2=eyJ1IjoiZTk5ZTFjNDAtNWYyNi0xMWU5LWFjZmUtOTM4ZjU4NzYyZDA1IiwidiI6ImJkM2Q2Y2FlLTVjMTktMTFlOS05NTgyLTAyNDJhYzEyMDAwYyIsInQiOjE1NTUyOTY0MTkzNzgsImgiOiJiYzM1NWQyYjIwNzJhZGQyMTY2MTIzODBmZTRiNWZlYmVkYTRiMjcwYTBlZDdjZTEyYmNmYTRkMWNmYTExN2RiIn0=; mp_604aafbf2f30d1f03bc54e55c879f4bb_mixpanel=%7B%22distinct_id%22%3A%20%2216a0ad1351b751-03255ef479f35d-5f1d3a17-1fa400-16a0ad1351cb30%22%2C%22%24device_id%22%3A%20%2216a0ad1351b751-03255ef479f35d-5f1d3a17-1fa400-16a0ad1351cb30%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com.hk%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com.hk%22%7D; utag_main=v_id:016a0ad133db0010065d6366f32303071001806900bd0$_sn:6$_ss:0$_st:1555297436133$vapi_domain:tommy.com$ses_id:1555292594096%3Bexp-session$_pn:9%3Bexp-session; s_tlm_gpv_pn=no%20value; _gat_GUA=1; mp_tommy_hilfiger_mixpanel=%7B%22distinct_id%22%3A%20%2216a0ad136191a-0942b0a5ff822e-5f1d3a17-1fa400-16a0ad1361a74%22%7D; s_ppv=Kids%253A%2520Girls%253A%2520Shoes%2520%2526%2520Accessories%253A%2520product%2520detail%2520page%2C47%2C23%2C1337%2C1920%2C256%2C1920%2C1080%2C1%2CP",
#     }
# def upload_html(text):
#     with open("./1.html","w",encoding="utf-8") as f:
#         f.write(text)
#
# def ip_s():
#     url = "https://www.kuaidaili.com/free/inha/{}/".format(random.randint(100,800))
#     sleep_time()
#     ip_text = requests.get(url=url, headers={"User-Agent": UserAgent(verify_ssl=False).random, })
#     ip_html = etree.HTML(ip_text.text)
#     ips = ip_html.xpath("//td[@data-title='IP']/text()")
#     print("ip ok!num:{}".format(len(ips)))
#     return ips
#
# g_discount_price = lambda x,y:"{}0".format(y[0]) if x == [] else x[0]
#
# @retry(stop_max_attempt_number=5)
# def goods_info(url):
#     ip = random.choice(ip_s())
#     # print(ip)
#     response = requests.get(url=url, headers=random_headers(),proxies={"http":ip})
#     text = response.text
#     upload_html(text)
#     html = etree.HTML(text)
#     return html
#
# def goods_driver():
#     driver = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome Dev\Application\chromedriver")
#     return driver
#
# def goods_info_parse(url):
#     html = goods_info(url)
#     g_infos = html.xpath("//div[@class='productCell']")
#     for g_info in g_infos:
#         g_info_html = etree.HTML(etree.tostring(g_info, encoding="utf-8").decode("utf-8"))
#         goods_name = g_info_html.xpath("//div[@class='productName']/a/text()")[0]
#         goods_price = g_info_html.xpath("//div[@id='price_display']/input[@type='hidden']/@value")[0].split("-")[0].strip()
#         goods_discount_price = g_discount_price(g_info_html.xpath("//div[@id='price_display']/span[@class='price listPrice']/text()"),goods_price)
#
#         goods_urls = g_info_html.xpath("//ul[@class='productswatches clearfix']/li/a/@href|//ul[@class='productswatches clearfix hidden']/li/a/@href")
#         goods_colors = g_info_html.xpath("//ul[@class='productswatches clearfix']/li/a/img/@data-color-family|//ul[@class='productswatches clearfix hidden']/li/a/img/@data-color-family")
#         goods_model = g_info_html.xpath("//ul[@class='productswatches clearfix']/li/@data-part-number|//ul[@class='productswatches clearfix hidden']/li/@data-part-number")
#
#         for goods_url in goods_urls:
#             sleep_time()
#             info_html = goods_info(goods_url)
#             goods_sizes = info_html.xpath("//ul[@id='sizes']/li/span/text()")
#             print(goods_url,goods_sizes)
#
#         # writer.writerow((
#         #     goods_name,
#         #     goods_model,
#         #     goods_price,
#         #     "{}0".format(goods_price[0]),
#         #     goods_color,
#         #     goods_sizes,
#         #     goods_details,
#         #     goods_images,
#         #     goods_order,
#         #     goods_gender,
#         #     goods_page,
#         #     goods_url,
#         # ))
#
# def main():
#     for url in urls:
#         goods_info_parse(url)
#
# if __name__ == "__main__":
#     main()