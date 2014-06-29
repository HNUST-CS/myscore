#encoding=utf8
import os  
import urllib2
from PIL import Image as im  
from PIL import ImageEnhance  

def process(filename):    #处理图片  
    img=im.open(filename,"r")  
    enhancer=ImageEnhance.Color(img)  
    enhancer=enhancer.enhance(0)   #变成黑白  
    enhancer=ImageEnhance.Brightness(enhancer) #这下面的参数是经过测试后图片效果最好的。。。  
    enhancer=enhancer.enhance(2)   #提高亮度  
    enhancer=ImageEnhance.Contrast(enhancer)  
    enhancer=enhancer.enhance(8)   #提高对比度  
    enhancer=ImageEnhance.Sharpness(enhancer)  
    enhancer=enhancer.enhance(20)  #锐化  
    return enhancer  
  
def delims(image,numbers=4,index=0,rect=()):    #分割  
    """ 
        image为图片, 
        numbers为图片上验证码的个数, 
        index没什么用,生成临时图片要用的, 
        rect为要切割的矩形元组,有4个值,为左上右下 
    """   
    if len(rect):                               #图片会被处理成一定的大小再进行切割  
        image=image.crop((rect))  
    width,height=image.size  
    for i in range(numbers):  
        img=image.crop((int(width/numbers)*i,0,int(width/numbers)*(i+1),height))  
        img.save("./temp/%d_%d.jpg" % (index,i))  
  
def createtempfile(numbers=4,rect=()):           #生成临时文件,需要自己去里面找合适的图片作为模板  
    list=os.listdir("./number")  
    for index,i in enumerate(list):  
        delims(process("./number/{0}".format(i)),numbers,index,rect)  
  
def createtemplate():                            #生成模板列表  
    list=[]  
    for root,dirs,files in os.walk("./template"):  
        for file in files:  
            list.append(os.path.join(root,file))  
    return list  
  
def recognize(filename,numbers,template,rect):   #图片识别,找不同  
    """ 
        filename为要识别的验证码, 
        numbers为验证码上面数字的个数, 
        template为模板列表, 
        rect,为要切割的矩形元组,有4个值,为左上右下 
    """  
    if len(rect):  
        image=process(filename).crop((rect))  
    if not len(template):  
        print("模板列表不能为空,请先筛选作为模板的文件并放到template文件夹内!")  
        return   
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
    image.save("./recognized/"+name+".jpg")  
#    return name  
  
def recognize2(filename,numbers,template,rect):   #图片识别,找相同  
    if len(rect):  
        image=process(filename).crop((rect))  
    if not len(template):  
        print("模板列表不能为空!")  
        return   
    width,height=image.size  
    name=""  
    for i in range(numbers):  
        img=image.crop((int(width/numbers)*i,0,int(width/numbers)*(i+1),height))  
        subwidth,subheight=img.size  
        rank=[]  
        for item in template:  
            temp=im.open(item,"r")  
            same=0  
            for w in range(subwidth):  
                for h in range(subheight):  
                    if(img.getpixel((w,h))==temp.getpixel((w,h))):  
                        same+=1  
            rank.append((same,os.path.basename(item).split(".")[0]))  
        rank.sort(reverse=True)  
        name+=str(rank[0][1])  
    image.save("./recognized/"+name+".jpg")  
#    return name  
  
def downpic(numbers=10):             #下载图片,numbers为要下载的数目,仅作测试用  
    url="http://kdjw.hnust.cn/kdjw/verifycode.servlet"  
    for i in range(numbers):  
        open("./number/%d.jpg" % i,"wb").write(urllib2.urlopen(url).read())  
  
def createdir():  
    cwd=os.getcwd()+"/"  
    try:                             #生成需要的目录  
        os.mkdir(cwd+"number")       
    except:                          #文件夹存在则忽略  
        pass  
    try:  
        os.mkdir(cwd+"temp")  
    except:  
        pass  
    try:  
        os.mkdir(cwd+"template")  
    except:  
        pass  
    try:  
        os.mkdir(cwd+"recognized")  
    except:  
        pass  
  
def main():  
    import ipdb;ipdb.set_trace()
    # createdir()  
    # downpic(20)                     #下载的图片在number文件夹内  
    # createtempfile(rect=(4,3,40,16))#对图片进行处理,生成的临时图片在temp文件夹内,用于找合适的模板图片  
    """整理完模板后就可以进行验证码的识别了"""  
    list=createtemplate()           #生成模板列表,对比的时候需要用到  
    piclist=os.listdir("./number")  #列举需要识别的图片  
    for item in piclist:             #识别图片  
        recognize("./number/{0}".format(item),4,list,(4,3,40,16))  
# main()  


# createtempfile(rect=(4,3,40,16))