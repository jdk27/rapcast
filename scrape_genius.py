import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
from random import randint
import pandas as pd
import json
import random
import multiprocessing

# *********** functions ***********
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

# *********** urls *********** 

with open('nineties.json') as f:
    artist_urls = json.load(f) 

artist_urls =  {k.lower(): v for k, v in artist_urls.items()}

# *********** agent strings *********** 

agent_strings = ["Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7', 
'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', 
'Mozilla/5.0 (Linux; U; Android 2.3.1; en-us; MID Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', 
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)', 
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
'UCWEB/2.0 (Java; U; MIDP-2.0; Nokia203/20.37) U2/1.0.0 UCBrowser/8.7.0.218 U2/1.0.0 Mobile', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4', 
'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991', 
'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T599N Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 
'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SCH-S738C Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 
'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M840 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30', 
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0', 
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)', 
'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1', 
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1', 
'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1', 
'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; NOKIA; Lumia 710)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 625)', 
'Mozilla/5.0 (Series30Plus; Nokia225/20.10.11; Profile/Series30Plus Configuration/Series30Plus) Gecko/20100401 S40OviBrowser/3.8.1.2.0612', 
'UCWEB/2.0 (Symbian; U; S60 V5; en-US; Nokia5235) U2/1.0.0 UCBrowser/9.1.0.319 U2/1.0.0 Mobile', 
'Nokia6630/1.0 (2.3.129) SymbianOS/8.0 Series60/2.6 Profile/MIDP-2.0 Configuration/CLDC-1.1', 'Opera/9.80 (MAUI Runtime; Opera Mini/4.4.33576/66.299; U; en) Presto/2.12.423 Version/12.16'
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko) Version/5.0.6 Safari/533.22.3', 
'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)', 
'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2)', 'Mozilla/5.0 (Windows NT 6.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)', 
'Opera/9.80 (SpreadTrum; Opera Mini/4.4.31492/60.313; U; fr) Presto/2.12.423 Version/12.16', 
'Opera/9.80 (SpreadTrum; Opera Mini/4.4.31492/60.271; U; fr) Presto/2.12.423 Version/12.16', 
'Opera/9.80 (SpreadTrum; Opera Mini/4.4.31492/66.318; U; en) Presto/2.12.423 Version/12.16', 
'Opera/9.80 (SpreadTrum; Opera Mini/4.4.32739/75.35; U; en) Presto/2.12.423 Version/12.16', 
'Mozilla/5.0 (Linux; U; Android 6.0.1; en-US; Redmi Note 4 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.4.8.1012 Mobile Safari/537.36']

# more strings: https://developers.whatismybrowser.com/useragents/explore/

# *********** data read in ***********
lyric_count = pd.DataFrame(columns=['artist', 'corpus'])
raw_lyrics = pd.DataFrame(columns=['artist', 'corpus'])

# *********** scraping loop ***********

artists = {}
used_urls = []

def scrape(url):
    artists = {}

    for artist, urls in artist_urls.items(): 
        if url in urls:
            main_artist = artist
            
    headers = {}
    headers['User-Agent'] = random.choice(agent_strings)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    lyrics = soup.find_all('div', attrs={'class': 'lyrics'})

    lyrics = str(lyrics[0])
    lyrics = re.sub('<[^>]+>', '', lyrics)
    lyrics = lyrics.replace('\n', ' ')
    lyrics = lyrics.replace('(', '')
    lyrics = lyrics.replace(')', '')
    lyrics = lyrics.replace('\xe2\x80\x94', ' ')
    lyrics = lyrics.replace('\xe2\x80\x99', "'")
    lyrics = lyrics.replace('\xc3\xab','e')
    lyrics = lyrics.replace('\u201c','')
    lyrics = lyrics.replace('\u201d','')
    lyrics = lyrics.replace('\u2019','')
    lyrics = lyrics.replace('\u2018','')
    lyrics = lyrics.replace('!', '')
    lyrics = lyrics.replace('?', '')
    lyrics = lyrics.replace('&amp;', '&')
    lyrics = lyrics.replace(',', '')
    lyrics = lyrics.replace("'", '')
    lyrics = lyrics.replace('"', '')
    lyrics = lyrics.lower()

    last_artist = main_artist
    while find_between(lyrics, '[', ']')!='':
        bracket_text = find_between(lyrics, '[', ']')
        verse = find_between(lyrics, ']', '[')
        if ':' in bracket_text:
            artist = bracket_text.split(":",1)[1].lstrip()
        else: 
            artist = main_artist
        if artist not in artists:
            artists[artist] = []
        artists[artist].append(verse)
        lyrics = lyrics.replace('[' + bracket_text + ']', '', 1)
        lyrics = lyrics.replace(verse, '', 1)
        last_artist = artist

    if last_artist not in artists:
        artists[last_artist] = []
    artists[last_artist].append(lyrics)

    with open('./urls1990s/' + url[19:] + '.json', 'w') as outfile:
        json.dump(artists, outfile)

    time.sleep(randint(0,5))

    return artists

pool = multiprocessing.Pool(20)

artists, urls= zip(*artist_urls.items())
urls = [item for sublist in urls for item in sublist]
data = pool.map(scrape, urls)

for i in range(len(data)):
    if i==0:
        artists = data[i]
    else:
        for artist,verses in data[i].items():
            if artist in artists:
                for verse in verses:
                    artists[artist].append(verse)
            else:
                artists[artist] = verses

# *********** save output as json ***********

with open('lyrics_1990s.json', 'w') as outfile:
        json.dump(artists, outfile)     

# *********** reform output into pandas ***********

for artist, verses in artists.items():
        # raw lyrics
        if raw_lyrics[raw_lyrics.artist==artist].shape[0]>0:
            index = raw_lyrics.index[raw_lyrics['artist']==artist].tolist()[0]
            for verse in verses:
                raw_lyrics.at[index, 'corpus'] = raw_lyrics.iloc[index].corpus.append(verse)
        else:
            raw_lyrics = raw_lyrics.append({'artist':artist, 'corpus':verses}, ignore_index=True)
        # counted lyrics
        artists[artist] = " ".join(verses)
        artists[artist] = Counter(artists[artist].split())
        if lyric_count[lyric_count.artist==artist].shape[0]>0:
            index = lyric_count.index[lyric_count['artist']==artist].tolist()[0]
            lyric_count.at[index, 'corpus'] = sum([lyric_count.iloc[index].corpus, artists[artist]], Counter())
        else:
            lyric_count = lyric_count.append({'artist':artist, 'corpus':artists[artist]}, ignore_index=True)    

# *********** save output as csv ***********

lyric_count.to_csv('lyric_corpus_count_1990s.csv', index=False)
raw_lyrics.to_csv('lyric_corpus_1990s.csv', index=False)

print('done!!')