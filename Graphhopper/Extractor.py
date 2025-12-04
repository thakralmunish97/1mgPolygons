from ExtractPolygon import createPolygon
from enum import Enum

class City(Enum):
    KOLKATA = "KOL"
    BANGALORE = "BLR"
    MUMBAI = "MUM"
    HYDERABAD = "HYD"

city = City.KOLKATA.value
storeCode = ""
distance = 6000
lat = ""
long = ""

createPolygon(city, storeCode, distance, lat, long)