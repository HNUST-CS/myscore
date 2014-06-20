import re,md5
def pack(path):
    read = lambda name : open(name).read()
    md5s =lambda s : md5.md5(s).hexdigest()
    con = read(path)
    name = path.split('/')[-1].split('.')
    my_name = name[0]+'-'+md5s(con)+'.'+name[1]
    path_head = path.replace(name[0]+'.'+name[1],"")
    new_name = path_head+my_name
    open(new_name,'w').write(con)
    index = read('index.html')
    rep =name[0]+'.*?\.'+name[1]
    old_name = re.search(rep,index).group()
    open('index.html','w').write(index.replace(old_name,my_name))
    
pack('static/css/mycss.css')
pack('static/js/myjs.js')
