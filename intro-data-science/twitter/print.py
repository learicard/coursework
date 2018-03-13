# Prints text scraped from Twitter
import urllib
import json

## Options
searchTerm = 'Microsoft'
numPages = 1

## Grab the data
url = ('http://search.twitter.com/search.json?q='
    + searchTerm + '&page=' + str(numPages))

queryI = urllib.urlopen(url)
queryO = json.load(queryI)

keyList = queryO.keys()      # this is a dict, so lets look at the keys
results = queryO["results"]  # this is a list, so lets look at an entry

# this is a dict, so lets look at all of the text using list comprehension
textOut = [r['text'] for r in results]

# now loop over the text, translating from unicode, and print the tweet
for i in range(0, len(textOut)):
	unicode_string = textOut[i]
	encoded_string = unicode_string.encode('utf-8')
	print encoded_string



	