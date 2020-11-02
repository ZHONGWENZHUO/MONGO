import datetime

from pymongo import MongoClient
from pprint import pprint

atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')


def begin(): #for choice city
	temp = input('Please select a city：0-lille,1-lyon，2-paris，3-rennes,Press Enter to end:')
	ville=list(map(int,temp.strip().split()))
	print(ville[0])
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
	return db
def find_station(db):#find station by name
	name = str(input('Please input the name:'))
	result= db.station.find_one({'name': {"$regex": ".*"+str(name)+".*"}})
	pprint(result)
	return result
def input_value():
	value=[]
	bike_availbale = int(input("please input number of bike_availbale : "))
	stand_availbale = int(input("please input number of stand_availbale : "))
	date = now_time = datetime.datetime.now()
	value.append(bike_availbale)
	value.append(stand_availbale)
	value.append(date)
	return value
def update_station(db):
	name = str(input('Please input the name:'))
	value = input_value()
	station = db.station.find_one({'name': {"$regex": ".*"+str(name)+".*"}})
	db.datas.update_one({
            '_id': station.get('_id')
        }, {
            '$set': {
                "bike_availbale": value[0],
                "stand_availbale": value[1],
                "date": value[2]
            }
        })
	print("update complete---------------------")
def delete_station(db):
	name = str(input('Please input the name:'))
	station = db.station.find_one({'name': {"$regex": ".*"+str(name)+".*"}})
	db.station.delete_one({'_id': station.get('_id')})
	db.datas.delete_one({'station_id': station.get('_id')})
	print("delete complete---------------------")
def deactivate_station(db):#At least four points need to be entered, and the first point needs to be the same as the fourth point
	tpe = False
	loc=[]
	point = input('Please enter latitude and longitude,Separated by spaces,Press Enter to end:')
	loc = list(map(float, point.strip().split()))
	print(loc)
	geo=[loc[i:i+2] for i in range(0, len(loc), 2)]
	db.station.update_many({
		"geometry.coordinates": {
			"$geoWithin": {
				"$geometry": {
					"type": "Polygon",
					"coordinates": [geo]
				}
			}
		}
	}, {
		'$set': {
			'tpe': tpe  # set tpe as false
		}
	})
def ratio(db):
	cursor=db.datas.find({})
	station=[]
	for i in cursor:
		bike=i.get('bike_availbale')
		stand=i.get('stand_availbale')
		week=(i.get('date')).strftime("%A")
		hours=int((i.get('date')).strftime("%H"))
		if week not in ['SATURDAY','SUNDAY'] and 18 <= hours <= 19 and stand!=0:
			ratio=bike/stand
			if(ratio<=0.02):
				station.append(i)
	print('Get: ' + str(len(station)) + ' station-------------------------------')
	for i in station:
		name=db.station.find_one({'_id':i.get('station_id')}).get('name')
		pprint(name)
def run(db):
	temp = int(input('Please select ：\n'
	             '0-Find a station by name\n'
	             '1-Update a station\n'
	             '2-Delete a station\n'
	             '3-deactivate all station in an area\n'
	             '4-give all stations with a ratio bike/total_stand under 20% between 18h and 19h00 (monday to friday)'
	             'Press Enter to end:'))
	if temp == 0:
		find_station(db)
	elif temp == 1:
		update_station(db)
	elif temp == 2:
		delete_station(db)
	elif temp == 3:
		deactivate_station(db)
	elif temp == 4:
		ratio(db)


if __name__ == '__main__':
	db=begin()
	# find_station(db)
	# update_station(db)
	#deactivate_station(db) #A set of data for testing 3.058288 50.629044 3.157181 50.714733 3.126501 50.61915 3.058288 50.629044
	# ratio(db)
	run(db)
