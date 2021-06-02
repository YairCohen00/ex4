import json
import urllib.parse
import requests

file = open("dests.txt", encoding="utf-8")
api_key = "Insert your API key here"
dist_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destinations}&key={key}"
geo_url = "https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}"
places = []
result_dict = {}
for place in file:
    place = place.strip()
    info = ()
    try:
        res = requests.get(dist_url.format(origin='תל אביב', destinations=place, key=api_key))
        res1 = requests.get(geo_url.format(address=place, key=api_key))
    except Exception as e:
        print(f'HTTP error - failed to get data, {e}')
        continue
    if not res.ok or not res1.ok:
        print(f'API error for {place}')
    if not res.json().get('rows') or not res1.json().get('results'):
        print(f'No results for {place}')
        continue
    distance_result = res.json().get('rows')[0].get('elements')
    if not distance_result:
        print('Missing values in response')
        continue
    distance_result = distance_result[0]
    geo_result = res1.json().get('results')
    if not geo_result:
        print('Missing values in response')
        continue
    geo_result = geo_result[0].get('geometry', {})
    info = (distance_result.get('distance', {}).get('text'),
            distance_result.get('duration', {}).get('text'),
            geo_result.get('location', {}).get('lng'),
            geo_result.get('location', {}).get('lat'),
    )
    result_dict[place] = info
print(result_dict)
only_distance =[]
for place in result_dict:
    dest_distance = (place,result_dict[place][0][:-3])
    only_distance.append(dest_distance)
    print("The distance from Tel-Aviv to " + place + " is "+result_dict[place][0])
    print("The travel time from Tel-Aviv to " + place + " is "+result_dict[place][1])
    print("The longitude of " + place + " is "+str(result_dict[place][2]))
    print("The latitude of " + place + " is "+str(result_dict[place][3]))
    print("---------------------------------------------------------")
top3_distances=sorted(only_distance,key=lambda x:x[1],reverse=True)[:3]
print("the top 3 distance from tel aviv are: ")
i = 1
for place in top3_distances:
    print(str(i)+") "+place[0] +" "+place[1] +" Km")
    i+=1






