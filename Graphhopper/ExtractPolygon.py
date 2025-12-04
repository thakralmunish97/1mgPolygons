import pandas as pd
from enum import Enum
import requests
import os
import json
from enum import Enum
from datetime import datetime, timedelta
from io import StringIO


class Key(Enum):
    AUTH_KEY = "{authKey}"
    STORE_LAT = "{storeLat}"
    STORE_LONG = "{storeLong}"
    DISTANCE_IN_M = "{distanceInM}"
    POLYGONS = "polygons"
    GEOMETRY = "geometry"
    COORDINATES = "coordinates"
    FEATURES = "features"


class City(Enum):
    KOLKATA = "KOL"


UNDERSCORE = "_"

KEY = "0fb3b5da-8a29-43fa-9dba-bd91c59e2f25"
CREATE_POLYGON_URL = "https://graphhopper.com/api/1/isochrone?key={authKey}&point={storeLat},{storeLong}&buckets=1&distance_limit={distanceInM}&profile=car"

CREATE_POLYGON_HEADERS = {
    "content-type": "application/json",
    "origin": "https://explorer.graphhopper.com",
    "priority": "u=1, i",
    "referer": "https://explorer.graphhopper.com/",
    "sec-fetch-mode": "cors"
}


def formUrl(lat, long, distance):
    url = (CREATE_POLYGON_URL
           .replace(Key.AUTH_KEY.value, KEY)
           .replace(Key.STORE_LAT.value, lat)
           .replace(Key.STORE_LONG.value, long)
           .replace(Key.DISTANCE_IN_M.value, str(distance)))
    return url


def downloadPolygon(lat, long, distance):
    url = formUrl(lat, long, distance)
    response = requests.get(url, headers=CREATE_POLYGON_HEADERS)
    if response.status_code == 200:
        return response.json().get(Key.POLYGONS.value)[0].get(Key.GEOMETRY.value).get(Key.COORDINATES.value)
    else:
        raise Exception("Unable to Download Polygon")


def getPolygonJson(coordinates):
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": []
                }
            }
        ]
    }
    (data.get(Key.FEATURES.value)[0].get(Key.GEOMETRY.value)[Key.COORDINATES.value]) = coordinates
    return data

def createPolygonGeoJsonFile(city, storeCode, distance, polygonJson):
    today = datetime.now().strftime("%b_%d_%Y").upper()
    fileName = (storeCode
                + UNDERSCORE
                + str(distance) + "M"
                + UNDERSCORE
                + city
                + UNDERSCORE
                + today)
    fileName = os.path.join("..", "Polygons", fileName + ".geojson")
    with open(fileName, 'w') as f:
        json.dump(polygonJson, f, indent=2)


def createPolygon(city, storeCode, distance, lat, long):
    coordinates = downloadPolygon(lat, long, distance)
    polygonJson = getPolygonJson(coordinates)
    createPolygonGeoJsonFile(city, storeCode, distance, polygonJson)
