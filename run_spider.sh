echo 'conn = new Mongo();db = conn.getDB("myscope");db.all.remove();' > mongo.js
mongo mongo.js
echo 'del '
rm mongo.js
echo 'rm '
cd server/crawler/
scrapy runspider myscope_spider.py
echo 'spider over '
cd -
mongodump -d myscope -c all
echo 'dump'
scp -C -r dump/ hi-hi.cn:/tmp/
#rm dump -Rf
echo 'copy'
ssh hi-hi.cn << EOF
echo 'ssh '
mongorestore -d myscope -c all2 --drop /tmp/dump/myscope/all.bson
echo 'restore'
rm /tmp/dump -R
echo 'del'
exit
EOF
echo 'run success'




