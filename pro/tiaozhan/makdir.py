# -*- coding: utf-8 -*-

import os

print os.getcwd()   #获得当前目录
# os.mkdir('/home/developer/Documents/image')
isExists = os.path.exists('/home/developer/Documents/image')
print(isExists)

# def creat_dir():
#     isExists = os.path.exists("image")
#     print isExists
#     if not isExists:
#         os.makedirs("image")
#     imagePath = os.path.abspath("image")
#     return imagePath


print os.path.abspath('image') #输出绝对路径