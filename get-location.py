
import exif
import geopy.geocoders
import json
import os

API_KEY = "99025665-32b6-43a2-82d2-ab8367ffb176"

def decimalCoords(coords, ref):
    deg = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        deg = -deg
    return deg

def getLocation(file):
    with open(file, 'rb') as src:
        img = exif.Image(src)
        if img.has_exif:
            try:
                coords = (decimalCoords(img.gps_latitude,
                          img.gps_latitude_ref),
                          decimalCoords(img.gps_longitude,
                          img.gps_longitude_ref))
                geolocator = geopy.geocoders.Yandex(api_key=API_KEY)
                location = geolocator.reverse(f"{coords[0]}, {coords[1]}")
                return location.address
            except:
                pass
    return ""

def loadTonIni(iniFile):
    data = {}
    with open(iniFile, 'r') as f:
        data = json.load(f)
    return data

def getName(id, data):
    for item in data:
        if id in item["ids"]:
            return item["person"]["name"]
    return ""

def getFaces(file, data):
    result = []
    try:
        base = os.path.basename(file)
        it = data["files"][base]
        persons = data["data"]
        faces = it["faces"]
        for key, face in faces.items():
            id = face['v']['p']
            name = getName(id, persons)
            if name:
                #print(name)
                result.append(name)
    except:
        pass

    return result

d = "/home/alex/Pictures/Владимир"
data = loadTonIni(d + "/.tonfotos.ini")
files = [d + "/IMG_20210508_124707.jpg", d + "/IMG_20210510_115406.jpg", d + "/IMG_20220103_112223.jpg"]
for f in files:
    print(f+":")
    print("\t", ", ".join(getFaces(f, data)))
    print("\t" + getLocation(f))
