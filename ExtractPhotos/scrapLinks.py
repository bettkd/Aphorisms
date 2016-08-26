from bs4 import BeautifulSoup
import urllib2
from urllib2 import urlopen
import sys
import csv
import cookielib
from cookielib import CookieJar
import random


base_uri = "https://pixabay.com/"

'''
	:summary - get the html object from a url
	:params - string url
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

def getPrimaryURIs(url):
	soup = make_soup(url)

	items = soup.find_all("div",
        {"class": lambda x: x and x == "item"})

	for item in items:
		uri = base_uri + item.find_all("a")[0].get("href")
		yield uri

def getSecondaryURLs(uri):
	soup = make_soup(uri)

	image = base_uri + soup.find_all("img", {"itemprop": lambda x: x and x == "contentURL"})[0].get("src")
	return image

def main():
	targetURI = "https://pixabay.com/en/photos/?orientation=vertical&image_type=photo&cat=nature&min_height=&colors=green&min_width=&order=popular&pagi="
	pagesCount = 144

	try:
		f = open('imageURLData.txt','a')
		for page in range(pagesCount):
			page += 1
			print "******* PAGE %d *********" % page  
			targetURL = targetURI + str(page)
			imageURIs = getPrimaryURIs(targetURL)
			for imageURI in imageURIs:
				print "Image: %s" % imageURI
				imageURL = getSecondaryURLs(imageURI)
				f.write(imageURL + "\n")

		f.close()
	except Exception, e:
		print "ERROR ENCOUNTERED, PASSED"
		pass

if __name__ == '__main__':
	main()