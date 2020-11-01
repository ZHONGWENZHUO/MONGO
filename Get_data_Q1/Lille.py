import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_lille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=3000&facet=" \
          "libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

lille = get_lille()

lille_to_insert = [
    {
        'name': elem.get('fields', {}).get('nom', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
        'source': {
            'dataset': 'Lille',
            'id_ext': elem.get('fields', {}).get('libelle')
        },
        'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE'
    }
    for elem in lille
]

# atlas = MongoClient("mongodb+srv://1023924802:<mc7JDPTtGzXHRdsy>@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority")
atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')
db = atlas.lille
for lille in lille_to_insert:
    db.station.insert_one(lille)