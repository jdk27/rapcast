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

urls = ["https://genius.com/Drake-nice-for-what-lyrics", 'https://genius.com/Drake-gods-plan-lyrics', 
'https://genius.com/Drake-passionfruit-lyrics', 'https://genius.com/Drake-portland-lyrics']

# *********** data read in ***********
# in first instance, create dataframe, in all later instances, read in
df = pd.DataFrame(columns=['artist', 'corpus'])

# later:
# df = pd.read_csv('lyric_corpus.csv')

# *********** scraping loop ***********

main_artist = 'drake'

artists = {}

for url in urls:
	print(url)
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

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

	# time.sleep(randint(5,10))

for artist, verses in artists.iteritems():
		artists[artist] = " ".join(verses)
		artists[artist] = Counter(artists[artist].split())
		if df[df.artist==artist].shape[0]>0:
			index = df.index[df['artist']==artist].tolist()[0]
			df.at[index, 'corpus'] = sum([df.iloc[index].corpus, artists[artist]], Counter())
		else:
			df = df.append({'artist':artist, 'corpus':artists[artist]}, ignore_index=True)
			

df.to_csv('lyric_corpus.csv', index=False)






