from pprint import pprint
from pymongo import MongoClient,DESCENDING
atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')

# db.bar.createIndex({point:"2dsphere"});#SET geometry.coordinates as 2dsphere
ville = []
loc=[]
temp = input('Please select a city：0-lille,1-lyon，2-paris，3-rennes,Press Enter to end:')
ville=list(map(int,temp.strip().split()))
print(ville[0])
temp2 = input('Please enter latitude and longitude,Separated by spaces,Press Enter to end:')
loc=list(map(int,temp2.strip().split()))
print(loc)

if ville[0]==0:
	db=atlas.lille
elif ville[0]==1:
	db=atlas.lyon
elif ville[0]==2:
	db=atlas.paris
elif ville[0]==3:
	db=atlas.rennes
else:
	print('wrong key')

station_closest = db.station.find({
    "geometry.coordinates": {
     "$nearSphere": {
       "$geometry": {
          "type": "Point" ,
          "coordinates": [ loc[0], loc[1] ]
       }
     }
   }})[0]
pprint(station_closest)
try:
	info = db.datas.find({"station_id" : station_closest["_id"],}).sort("data", DESCENDING).next()
	pprint('NAME :'+station_closest['name'])
	pprint(info)
except StopIteration:
    pass