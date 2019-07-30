import os
import datetime
import sys

# gucci prada kenzo
#newlook herschel
spider_name = [
                "newlook",
                "herschel",
                "kith","nike",
                "zara","hm",
                "gucci","lining",
                "prada","kenzo",
                ]

def main():
    args = sys.argv[-1]
    if args == "-h" or args == "-help":
        print("Can choose the spider:"
              "\n                     newlook(zh)"
              "\n                     herschel"
              "\n                     kith"
              "\n                     nike(zh)"
              "\n                     zara"
              "\n                     hm"
              "\n                     gucci"
              "\n                     lining(zh)"
              "\n                     prada"
              "\n                     kenzo"
              )
    elif args in spider_name:
        path = os.path.join("..", "data", datetime.datetime.now().strftime("%Y-%m-%d"))
        if not os.path.exists(path):
            os.makedirs(path)
        spider_command = "scrapy crawl %s -o %s\%s.csv" % (args, path, args)
        os.system(spider_command)
    else:
        print("Not Found '%s'!"
              "\n  -h or -help"%args)

if __name__ == "__main__":
    main()
