from __future__ import print_function
import sys
import urllib
import json

#!/usr/bin/env python
# term_sentiment.py

""" usage: term_sentiment.py <sentiment_scores_file> <livestream_twitter_data>
    this program estimates the sentiment scores of unknown words using the 
    sum of all estimated sentiments from their parent tweets as defined in
    tweet_sentiment.py
"""

def main():

	# parse tab-delim word-sentiment scores into a dict
	wordScores = {}
	for line in open(sys.argv[1]):
		term, score  = line.split("\t")
		wordScores[term] = int(score)

	# interpret all tweets using JSON
	tweets = []
	for line in open(sys.argv[2]):
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

if __name__ == '__main__':
    main()