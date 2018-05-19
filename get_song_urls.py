import requests
import urllib.request
import json
import time
from random import randint
import pandas as pd 
import numpy as np 
import random 

client_access_token = ''

artist_ids = np.load('artist_ids.npy').item()

agent_strings = ["Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7', 
'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1']

# more strings: https://developers.whatismybrowser.com/useragents/explore/

headers = {}
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

urls = {}
for artist, artist_id in artist_ids.items():
    print(artist)
    i = 1
    urls[artist] = []
    while i <= 10:
        headers = {}
        headers['User-Agent'] = random.choice(agent_strings)
        querystring = "https://api.genius.com" + artist_id + "/songs?sort=popularity&per_page=50&page=" + str(i)
        request = urllib.request.Request(querystring, headers=headers)
        request.add_header("Authorization", "Bearer " + client_access_token)
        request.add_header("User-Agent", "")
        response = urllib.request.urlopen(request, timeout=30)
        raw = response.read().decode('utf-8')
        json_obj = json.loads(raw)
        songs = json_obj['response']['songs']
        for song in songs:
            urls[artist].append(song['url'])
        i += 1
        if json_obj['response']['next_page'] == None:
            break
        time.sleep(randint(5,30))

    with open('./tmp/' + artist + '_links.json', 'w') as outfile:
        json.dump(urls[artist], outfile)

with open('artist_links.json', 'w') as outfile:
    json.dump(urls, outfile)

print('DONE!!')