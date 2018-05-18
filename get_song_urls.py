import requests
import urllib.request
import json
import time
from random import randint
import pandas as pd 

client_access_token = ''

rappers = pd.read_csv('rappers.csv')

artists = rappers.Name.tolist()
artist_ids = {}
for artist in artists:
    search_term = artist
    _URL_API = "https://api.genius.com/"
    _URL_SEARCH = "search?q="
    querystring = _URL_API + _URL_SEARCH + urllib.request.quote(artist)
    request = urllib.request.Request(querystring)
    request.add_header("Authorization", "Bearer " + client_access_token)
    request.add_header("User-Agent", "")

    response = urllib.request.urlopen(request, timeout=3)
    raw = response.read().decode('utf-8')
    json_obj = json.loads(raw)

    artist_ids[artist] = json_obj['response']['hits'][0]['result']['primary_artist']['api_path']
    time.sleep(randint(5,10))
print(artist_ids)

urls = {}
i = 1
for artist, artist_id in artist_ids.items():
    urls[artist] = []
    while i <= 10:
        querystring = "https://api.genius.com" + artist_id + "/songs?sort=popularity&per_page=50&page=" + str(i)
        request = urllib.request.Request(querystring)
        request.add_header("Authorization", "Bearer " + client_access_token)
        request.add_header("User-Agent", "")
        response = urllib.request.urlopen(request, timeout=15)
        raw = response.read().decode('utf-8')
        json_obj = json.loads(raw)
        if json_obj['response']['next_page'] == None:
            break
        songs = json_obj['response']['songs']
        for song in songs:
            urls[artist].append(song['url'])
        i += 1
        time.sleep(randint(5,10))

    with open('./tmp/' + artist + '_links.json', 'w') as outfile:
        json.dump(urls[artist], outfile)

with open('artist_links.json', 'w') as outfile:
    json.dump(urls, outfile)

print('DONE!!')