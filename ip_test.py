import requests
import random
'''代理IP地址（高匿）'''
ips = [
    '221.6.201.18:9999',
    '113.200.56.13:8010',
    '101.37.79.125:3128',
    '171.221.239.11:808',
    '202.112.237.102:3128',
    '106.12.32.43:3128',
]
#国外
# ips = [
#     "123.1.150.244:80", #https
#     "47.52.210.47:80", #http
# ]

# proxy = {
#   'https': ips[random.choice([0,1,2,3,4,5])]
# }
'''head 信息'''
head = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
       'Connection': 'keep-alive'}
'''http://icanhazip.com会返回当前的IP地址'''
for ip in ips:
    # print(ip)
    p = requests.get('http://icanhazip.com', headers=head, proxies={"https":ip})
    print(p.text)