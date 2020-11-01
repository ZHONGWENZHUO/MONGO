from pymongo import MongoClient
import time
import dateutil.parser
from Get_data_Q1 import Rennes

atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')

db = atlas.rennes


# db.datas.create_index([('station_id', 1),('date', -1)], unique=True)





def get_station_id(id_ext):
    tps = db.station.find_one({'source.id_ext': id_ext }, {'_id': 1 })
    return tps['_id']



while True:
    print('update')
    rennes = Rennes.get_rennes()
    datas = [
        {
            "bike_availbale": elem.get('fields', {}).get('nombrevelosdisponibles'),
            "stand_availbale": elem.get('fields', {}).get('nombreemplacementsdisponibles'),
            "date": dateutil.parser.parse(elem.get('record_timestamp')),
            "station_id": get_station_id(elem.get('fields', {}).get('idstation'))
        }
        for elem in rennes
    ]

    try:
        db.datas.insert_many(datas, ordered=False)
    except:
        pass
    # for elem in rennes:
    #     print(dateutil.parser.parse(elem.get('record_timestamp')))

    time.sleep(10)
