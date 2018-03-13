import sys
import urllib
import json
from __future__ import print_function

# parse tab-delim word-sentiment scores into a dict
wordScores = {}
for line in open('AFINN-111.txt'):
	term, score  = line.split("\t")
	wordScores[term] = int(score)

# interpret all tweets using JSON
tweets = []
for line in open('output_large.txt'):
	try: 
		tweets.append(json.loads(line))
	except:
		pass

# determine the sentiment of each tweet & store in dict
tweetScore = []
tweetDict = {}
for tweet in tweets:
	try:
		text = tweet['text'].encode('utf-8')
	except:
		text = 'null'
		tweetSentiment = 0
		tweetScore = float(tweetSentiment)

	else:
		words = text.split()
		tweetSentiment = [wordScores.get(w,0) for w in words]
		tweetScore = float(sum(tweetSentiment))
		
	tweetDict[text] = tweetScore

# loop through all tweets. assign unknown words (0) the mean of their 
# parent tweet. Finally, take the mean of all instances.

newWordDict = {}
for tweet in tweets:
	try:
		text = tweet['text'].encode('utf-8')
		words = text.split()
	
	except:
		pass

	else:
		for w in words:
			if wordScores.get(w,0) == 0:

				if newWordDict.get(w, 'None') == 'None':
					newWordDict[w] = tweetDict[text]
				else:
					newWordDict[w] = newWordDict[w] + tweetDict[text]

			else:
				pass

for k, v in newWordDict.iteritems():
	print(k, end=' ')
	print(v)