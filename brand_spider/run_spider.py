import os
import datetime
import sys

spider_name = [
                "newlook",
                "herschel",
                "kith","nike",
                ]

#thehundreds,matix,marmot
def main():
    args = sys.argv[-1]
    if args == "-h" or args == "-help":
        print("Can choose the spider:"
              "\n                     newlook"
              "\n                     herschel"
              "\n                     kith"
              "\n                     nike"
              )
    elif args in spider_name:
        path = os.path.join(".", "data", datetime.datetime.now().strftime("%Y-%m-%d"))
        if not os.path.exists(path):
            os.makedirs(path)
        spider_command = "scrapy crawl %s -o %s\%s.csv" % (args, path, args)
        os.system(spider_command)
    else:
        print("Not Found '%s'!"
              "\n  -h or -help"%args)

if __name__ == "__main__":
    main()
