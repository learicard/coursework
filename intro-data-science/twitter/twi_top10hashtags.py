from __future__ import print_function
import sys
import urllib
import json
import re

#!/usr/bin/env python
# top_ten.py

""" usage: top_ten.py <livestream_twitter_data>
	prints the top 10 hashtags in your twitter data to STDOUT
"""

def main():

	# interpret all tweets using JSON
	tweets = []
	for line in open(sys.argv[1]):
		try: 
			tweets.append(json.loads(line))
		except:
			pass

	# find all of the hashTags
	hashMaster = []
	for tweet in tweets:
		try:
			hashTag = tweet['entities']['hashtags']
			if hashTag != []:
				hashMaster.append(hashTag)				
		except:
			pass

	# construct dict of {hashTag: count}
	hashCount = {}
	for tweet in hashMaster:
		for h in tweet:
			 hashTag = h['text'].encode('utf-8')
			 if hashCount.get(hashTag, 'None') == 'None':
			 	hashCount[hashTag] = 1
			 else:
			 	hashCount[hashTag] = hashCount[hashTag] + 1

	# find the top ten hashTags & print
	top10 = []
	hashOut= {}
	count = 1
	while count < 11:
		out = max(hashCount.iterkeys(), key=lambda k: hashCount[k])
		hashOut[out] = hashCount[out]
		top10.append(out)
		hashCount[out] = 0
		count = count + 1
		
	## print the top 10 items
	for item in top10:
		print(item, end=' ')
		print('%0.4f' % float(hashOut[item]))

if __name__ == '__main__':
    main()