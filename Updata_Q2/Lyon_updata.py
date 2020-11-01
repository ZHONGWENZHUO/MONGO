from pymongo import MongoClient
import time
import dateutil.parser
from Get_data_Q1 import Lyon

atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')

db = atlas.lyon

# db.datas.create_index([('station_id', 1), ('date', -1)], unique=True)



def get_station_id(id_ext):
	tps = db.station.find_one({'source.id_ext': id_ext}, {'_id': 1})
	return tps['_id']


while True:
	print('update')
	villes = Lyon.get_lyon()
	datas = [
		{
			"bike_availbale": elem.get('fields', {}).get('available'),
			"stand_availbale": elem.get('fields', {}).get('availabl_1'),
			"date": dateutil.parser.parse(elem.get('fields', {}).get('last_upd_1')),
			"station_id": get_station_id(elem.get('fields', {}).get('gid'))
		}
		for elem in villes
	]

	try:
		db.datas.insert_many(datas, ordered=False)
	except:
		pass

	time.sleep(10)

