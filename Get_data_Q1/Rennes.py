import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_rennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps" \
          "-reel&q=&rows=251&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles" \
          "&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

rennes = get_rennes()

rennes_to_insert = [
    {
        'name': elem.get('fields', {}).get('nom', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
        'source': {
            'dataset': 'Rennes',
            'id_ext': elem.get('fields', {}).get('idstation')
        },
        'tpe': elem.get('fields', {}).get('etat', '') == 'En fonctionnement'
    }
    for elem in rennes
]

# atlas = MongoClient("mongodb+srv://1023924802:<mc7JDPTtGzXHRdsy>@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority")
atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')
db = atlas.rennes
for rennes in rennes_to_insert:
    db.station.insert_one(rennes)