from __future__ import print_function
import sys
import urllib
import json
import re

#!/usr/bin/env python
# frequency.py

""" usage: frequency.py <livestream_twitter_data> 
    this program calculates the frequency of each term in utf-8 encoded
    twitter data (stripped via JSON)
"""

def main():
	
	# interpret all tweets using JSON
	tweets = []
	for line in open(sys.argv[1]):
		try: 
			tweets.append(json.loads(line))
		except:
			pass

	# loop through all tweets, counting instances of each word
	wordCount = {}
	wordTotal = 0
	for tweet in tweets:
		try:
			text = tweet['text'].encode('utf-8')
			wordList = re.findall(r"[\w']+", text)
		except:
			pass
		else:
			for word in wordList:
				wordTotal = wordTotal + 1
				if wordCount.get(word, 'None') == 'None':
					wordCount[word] = 1
				else:
					wordCount[word] = wordCount[word] + 1

	# calculate word freq as [ count of word / count of all words ]
	for word, frequency in wordCount.iteritems():
		frequency = float(wordCount[word]) / float(wordTotal)
		print(word, end=' ')
		print('%0.4f' % frequency)

if __name__ == '__main__':
    main()