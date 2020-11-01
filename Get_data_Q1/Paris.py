import requests
import json
from pprint import pprint
from pymongo import MongoClient


def get_paris():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows" \
          "=251&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])

paris = get_paris()

paris_to_insert = [
    {
        'name': elem.get('fields', {}).get('name', '').title(),
        'geometry': elem.get('geometry'),
        'size': elem.get('fields', {}).get('capacity'),
        'source': {
            'dataset': 'Paris',
            'id_ext': elem.get('fields', {}).get('stationcode')
        },
        'tpe': elem.get('fields', {}).get('is_renting', '') == 'OUI'
    }
    for elem in paris
]

# atlas = MongoClient("mongodb+srv://1023924802:<mc7JDPTtGzXHRdsy>@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority")
atlas = MongoClient('mongodb+srv://1023924802:mc7JDPTtGzXHRdsy@cluster0.8smsh.mongodb.net/<ville>?retryWrites=true&w=majority')
db = atlas.paris
for paris in paris_to_insert:
    db.station.insert_one(paris)