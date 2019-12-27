

# Desc: Get coordinates from address

# Not useable. Just find coords manually from google maps. 12/19



import geopy.distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic





l = [
['HUDSON FALLS CENTRAL SCHOOL DISTRICT', '80 E LABARGE ST	 	HUDSON FALLS	NY'],

['KINGSTON CITY SCHOOL DISTRICT', '21 WYNKOOP PL	 	KINGSTON	NY']
]





for i in l:
    
    name = i[0]
    addr = i[1].replace('\t', ' ')

    print('\n')
    geolocator = Nominatim(user_agent="app_name")
    full_loc = geolocator.geocode(addr)
    if not full_loc: continue
    coords = full_loc.latitude, full_loc.longitude




    print(name, coords)












