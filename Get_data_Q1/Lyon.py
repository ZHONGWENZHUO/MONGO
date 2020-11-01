import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_lyon():
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=250&facet" \
          "=name&facet=commune&facet=bonus&facet=status&facet=available&facet=availabl_1&facet=availabili&facet=" \
          "availabi_1&facet=last_upd_1"

    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


lyon = get_lyon()


lyon_to_insert = [
    {
        'name': elem.get('fields', {}).get('name', '').title(),
        'geometry': elem.get('fields', {}).get('geo_shape'),
        'size': elem.get('fields', {}).get('bike_stand'),
        'source': {
            'dataset': 'Lyon',
            'id_ext': elem.get('fields', {}).get('gid')
        },
        'tpe': elem.get('fields', {}).get('banking', '') == 't'
    }
    for elem in lyon
]


# atlas = MongoClient("mongodb+srv://1023924802:<mc7JDPTtGzXHRdsy>@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority")
atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')
db = atlas.lyon
for lyon in lyon_to_insert:
    db.station.insert_one(lyon)