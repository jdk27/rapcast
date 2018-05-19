import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
from random import randint
import pandas as pd
import json
import random

# *********** functions ***********
def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

# *********** urls *********** 

with open('artist_links.json') as f:
    artist_urls = json.load(f) 

# *********** agent strings *********** 

agent_strings = ["Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", 
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36', 
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1', 
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)', 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7', 
'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1']

# more strings: https://developers.whatismybrowser.com/useragents/explore/

# *********** dataframe set-up ***********

lyric_count = pd.DataFrame(columns=['artist', 'corpus'])
raw_lyrics = pd.DataFrame(columns=['artist', 'corpus'])

# *********** scraping loop ***********

artists = {}
used_urls = []
headers = {}

for artist, urls in artist_urls.items():
	print(artist)
	main_artist = artist
	for url in urls:
		print(url)

		if url in used_urls:
			continue
		else:
			used_urls.append(url)

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
		lyrics = lyrics.replace('\u2019','')
		lyrics = lyrics.replace('\u2018','')
		lyrics = lyrics.replace('!', '')
		lyrics = lyrics.replace('?', '')
		lyrics = lyrics.replace('&amp;', '&')
		lyrics = lyrics.replace(',', '')
		lyrics = lyrics.replace("'", '')
		lyrics = lyrics.replace('"', '')
		lyrics = lyrics.lower()


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

		artists[last_artist].append(lyrics)

		time.sleep(randint(5,10))

	with open('./tmp/' + artist + '_lyrics.json', 'w') as outfile:
		json.dump(artists[artist], outfile)

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
					
	# *********** save output ***********
	lyric_count.to_csv('lyric_corpus_count.csv', index=False)
	raw_lyrics.to_csv('lyric_corpus.csv', index=False)
