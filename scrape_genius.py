import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
from random import randint

# urls = ["https://genius.com/Drake-nice-for-what-lyrics", 'https://genius.com/Drake-gods-plan-lyrics', 
# 'https://genius.com/Drake-passionfruit-lyrics', 'https://genius.com/Drake-portland-lyrics']

def find_between( s, first, last ):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

urls = ['https://genius.com/Drake-portland-lyrics']

lyric_corpus = []

for url in urls:
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")

	lyrics = soup.find_all('div', attrs={'class': 'lyrics'})

	lyrics = str(lyrics[0])
	lyrics = re.sub('<[^>]+>', '', lyrics)
	lyrics = re.sub(r'\[.*\]', '', lyrics)
	lyrics = lyrics.replace('\n', ' ')
	lyrics = lyrics.replace('(', '')
	lyrics = lyrics.replace(')', '')
	lyrics = lyrics.replace('\xe2\x80\x94', ' ')
	lyrics = lyrics.replace('\xe2\x80\x99', "'")
	lyrics = lyrics.replace('!', '')
	lyrics = lyrics.replace('?', '')
	lyrics = lyrics.replace('&amp;', '&')
	lyrics = lyrics.replace(',', '')
	lyrics = lyrics.replace("'", '')
	lyrics = lyrics.replace('"', '')
	lyrics = lyrics.lower()

	lyrics = Counter(lyrics.split())

	lyric_corpus.append(lyrics)
	# time.sleep(randint(5,10))

lyric_corpus = sum(lyric_corpus, Counter())
word_count = sum(lyric_corpus.values())