from pymongo import MongoClient
import time
import dateutil.parser
from Get_data_Q1 import Paris

atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')

db = atlas.paris

# db.datas.create_index([('station_id', 1), ('date', -1)], unique=True)



def get_station_id(id_ext):
	tps = db.station.find_one({'source.id_ext': id_ext}, {'_id': 1})
	return tps['_id']


while True:
	print('update')
	villes = Paris.get_paris()
	datas = [
		{
			"bike_availbale": elem.get('fields', {}).get('numbikesavailable'),
			"stand_availbale": elem.get('fields', {}).get('numdocksavailable'),
			"date": dateutil.parser.parse(elem.get('fields', {}).get('duedate')),
			"station_id": get_station_id(elem.get('fields', {}).get('stationcode'))
		}
		for elem in villes
	]

	try:
		db.datas.insert_many(datas, ordered=False)
	except:
		pass

	time.sleep(10)

