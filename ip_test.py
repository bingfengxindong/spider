import requests
import random
from lxml import etree
from fake_useragent import UserAgent

# for ip in ips:
#     # print(ip)
#     p = requests.get('http://icanhazip.com', headers=head, proxies={"https":ip})
#     print(p.text)

def random_headers():
    ua = UserAgent(verify_ssl=False)
    return {
        "User-Agent": ua.random,
    }

def upload_html(text):
    with open("./1.html","w",encoding="utf-8") as f:
        f.write(text)

def ip_s():
    ip_text = requests.get(url="https://www.kuaidaili.com/free/inha/",headers=random_headers())
    ip_html = etree.HTML(ip_text.text)
    ips = ip_html.xpath("//td[@data-title='IP']/text()")
    return ips

print(ip_s())

# import copy
#
# def list_indexs(ls,a):
#     ls1 = copy.copy(ls)
#     ls_index = []
#     for i in ls1:
#         if a in ls1:
#             ls_index.append(ls1.index(a))
#             ls1[ls1.index(a)] = "{}a".format(ls1[ls1.index(a)])
#     return ls_index
#
# list = [3, 4, 5, 6, 6, 5, 4, 3, 2, 1, 7, 8, 8, 3]
# a = 3
# print(list_indexs(list,a))
#
#
# print([i[0] for i in enumerate(list) if i[1] == 3])