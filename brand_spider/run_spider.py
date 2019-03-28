import os
import datetime
import sys

spider_name = [
                # "adidas",
                "champion","thehundreds","newera",
                "matix","marmot","captainfin","asos",
                "boohoo","newlook","monki","hippytree",
                "globebrand","ecouniverse",
                "herschel",
                "kith","nike",
                "life_is_good",
                "alpha",
                ]

#thehundreds,matix,marmot
def main():
    args = sys.argv[-1]
    if args == "-h" or args == "-help":
        print("Can choose the spider:"
              # "\n                     adidas"
              # "\n                     champion"
              # "\n                     thehundreds"
              # "\n                     newera"
              # "\n                     matix"
              # "\n                     marmot"
              # "\n                     captainfin"
              # "\n                     asos"
              # "\n                     boohoo"
              "\n                     newlook"
              # "\n                     monki"
              # "\n                     hippytree"
              # "\n                     alpha"
              # "\n                     globebrand"
              "\n                     herschel"
              # "\n                     ecouniverse"
              "\n                     kith"
              "\n                     nike"
              # "\n                     life_is_good"
              # "\n                     alpha"
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
