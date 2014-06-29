#encoding=utf8
import os  
import urllib2
from PIL import Image as im  
from PIL import ImageEnhance  

def process(img):    #处理图片  
    enhancer=ImageEnhance.Color(img)  
    enhancer=enhancer.enhance(0)   #变成黑白  
    enhancer=ImageEnhance.Brightness(enhancer) #这下面的参数是经过测试后图片效果最好的。。。  
    enhancer=enhancer.enhance(2)   #提高亮度  
    enhancer=ImageEnhance.Contrast(enhancer)  
    enhancer=enhancer.enhance(8)   #提高对比度  
    enhancer=ImageEnhance.Sharpness(enhancer)  
    enhancer=enhancer.enhance(20)  #锐化  
    return enhancer  

def createtemplate():    
    global template
    template=[]  
    for root,_,files in os.walk("./template"):  
        for file in files:  
            template.append(os.path.join(root,file))  

createtemplate()

def recognize(img):     
    """ 
        img, 
        numbers为验证码上面数字的个数, 
        template为模板列表, 
        rect,为要切割的矩形元组,有4个值,为左上右下 
    """  
    numbers=4
    rect=(4,3,40,16)
    image=process(img).crop((rect))  
    width,height=image.size  
    name=""  
    for i in range(numbers):  
        img=image.crop((int(width/numbers)*i,0,int(width/numbers)*(i+1),height))  
        subwidth,subheight=img.size  
        rank=[]  
        for item in template:  
            temp=im.open(item,"r")  
            diff=0  
            for w in range(subwidth):  
                for h in range(subheight):  
                    if(img.getpixel((w,h))!=temp.getpixel((w,h))):  
                        diff+=1  
            rank.append((diff,os.path.basename(item).split(".")[0]))  
        rank.sort()  
        name+=str(rank[0][1])  
    return name



