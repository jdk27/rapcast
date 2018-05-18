import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
from random import randint
import pandas as pd

# *********** functions ***********
def find_between(s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ''

# *********** urls *********** 

urls = ['https://genius.com/Drake-nice-for-what-lyrics', 'https://genius.com/Drake-gods-plan-lyrics', 
'https://genius.com/Drake-passionfruit-lyrics', 'https://genius.com/Drake-portland-lyrics']

# *********** data read in ***********
# in first instance, create dataframe, in all later instances, read in
# if artist_count==0:
lyric_count = pd.DataFrame(columns=['artist', 'corpus'])
raw_lyrics = pd.DataFrame(columns=['artist', 'corpus'])

# later: 
# else: 
	# lyric_count = pd.read_csv('lyric_corpus_count.csv')
	# raw_lyrics = pd.read_csv('lyric_corpus.csv')

# *********** scraping loop ***********

main_artist = 'drake'
artists = {}

for url in urls:
	print(url)
	r = requests.get(url)
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

for artist, verses in artists.iteritems():
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