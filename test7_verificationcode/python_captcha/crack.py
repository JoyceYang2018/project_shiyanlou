#coding:utf-8

from PIL import Image
import hashlib
import time
import os

import math


class VectorCompare:
    #计算矢量大小
    def magnitude(self,concordance):
        total = 0
        for word,count in concordance.iteritems():
            total += count**2
        return math.sqrt(total)

    #计算余弦夹角，即相似度
    def relation(self,concordance1,concordance2):
        relevant = 0
        topvalue = 0
        for word,count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count*concordance2[word]
        return topvalue/(self.magnitude(concordance1)*self.magnitude(concordance2))


def buildvector(im):
    d1={}

    count=0
    for i in im.getdata():
        d1[count]=i
        count+=1
    return d1

v=VectorCompare()

iconset = ['0','1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


imageset=[]

#对图片集里的图片转换成每个字母对应的矢量集存放在imageset中
for letter in iconset:
    for img in os.listdir('./iconset/%s/'%(letter)):
        temp=[]
        if img != "Thumbs.db" and img != ".DS_Store":
            temp.append(buildvector(Image.open("./iconset/%s/%s"%(letter,img))))
        imageset.append({letter:temp})


im = Image.open("captcha.gif")
im2 = Image.new("P",im.size,255)
im.convert("P")
temp={}


#从im中提取出220,227颜色构造出im2的黑白二值图片（方便后期切割）
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix=im.getpixel((y,x))
        temp[pix]=pix
        if pix ==220 or pix==227:
            im2.putpixel((y,x),0)


inletter = False
foundletter = False
start = 0
end = 0

letters=[]

for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix!=255:
            inletter = True

    if foundletter ==False and inletter ==True:
        foundletter = True
        start=y

    if foundletter==True and inletter ==False:
        foundletter = False
        end =y
        letters.append((start,end))


    inletter = False


count = 0
for letter in letters:
    m = hashlib.md5()
    im3 = im2.crop((letter[0],0,letter[1],im2.size[1]))

    guess = []

    for image in imageset:
        for x,y in image.iteritems():
            if len(y)!=0:
                guess.append((v.relation(y[0], buildvector(im3)),x))

    guess.sort(reverse=True)
    print guess[0]

    count+=1



# im=Image.open('captcha.gif')
# #将图片转换为8为=位像素模式
# im.convert("P")
#
# #打印颜色直方图
# print(im.histogram())