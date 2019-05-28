import os
import csv

now_path = os.getcwd()
now_dirs = ["{}/{}".format(now_path,i) for i in os.listdir(os.getcwd())]
for now_dir in now_dirs:
    if os.path.isdir(now_dir):
        print(now_dir.split("/")[-1],[{i:len([j for j in csv.reader(open("{}/{}".format(now_dir, i),"r",encoding="utf-8"))])} for i in os.listdir(now_dir)])

