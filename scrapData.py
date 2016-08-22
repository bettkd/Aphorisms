from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import sys
import csv
import cookielib
from cookielib import CookieJar
import random
import re
from container import Aphorism
import time

'''
	:params - string URL (youtube url query for song)
	:return - string soup (rendered html)
'''
def make_soup(url):
	cj = CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	agents = ["Chrome/19.0.1084.52", "Safari/536.5", "Mozilla/5.0", "Chrome/19.0.1084.52"]
	opener.addheaders = [('User-agent', random.choice(agents))]
	data = opener.open(url).read()
	soup = BeautifulSoup(data, "html.parser")
	soup.prettify()
	return (soup)

'''
	:params - string URL (youtube url query for song)
	:return - string URI (best videoID for given song)
'''
def scrapData(url):
	aphorisms = []
	soup = make_soup(url)
	temps = str(soup).split("<hr color")
	
	#print soup
	for temp in temps:
		#print temp
		theme = re.findall(r'th_id=[0-9]+">(.+?) </a></strong>+?', temp)
		author = re.findall(r'aut_id=[0-9]+">(.+)</a></p><a+?', temp)
		text = re.findall(r'<strong>(.*) <p style', temp)
		#print text 
		#print "***********************************************\n**********************************"
		if not theme:
			continue
		else:
			_theme = [t.strip() for t in theme]
		if not author:
			continue
		else:
			_author = author[0].strip()
		if not text:
			continue
		else:
			_text = text[0].strip()

		aphorisms.append(Aphorism(_theme, _author, _text))
	return aphorisms


def main():
	base_url = "http://www.aphorism4all.com/all_aforism.php?all=all&p="
	pages = range(11,25)
	random.shuffle(pages)

	collection = []

	for page in pages:
		url = base_url + str(page)
		print "Loading: " + url
		try:
			aphorisms = scrapData(url)
			collection.extend(aphorisms)
		except Exception, e:
			print "--::Error: %s" % e
			time.sleep(5)
			pages.append(page)
			continue
	
	for item in collection:
		print item.text

	print "Retrieved %d" % len(collection)
	print "Expected %d" % (len(pages) * 20)


	#for aphorism in aphorisms:
	#	print aphorism.theme
		#pass

if __name__ == '__main__':
	main()
