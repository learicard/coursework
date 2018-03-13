#!/usr/bin/env python
# tweet_sentiment.py

""" usage: tweet_sentiment.py <sentiment_scores_file> <livestream_twitter_data>
    this program calculates the sum of all sentiment scores in scraped twitter
    text and outputs the final score to STDOUT
"""

import sys
import urllib
import json

def main():

	# parse tab-delim word-sentiment scores into a dict
	sentScores = {}
	for line in open(sys.argv[1]):
		term, score  = line.split("\t")
		sentScores[term] = int(score)

	# interpret all tweets using JSON
	tweets = []
	for line in open(sys.argv[2]):
		try: 
			tweets.append(json.loads(line))
		except:
			pass

	# now calcuate the sum of sentiments for each tweet
	tweetScore = []
	for tweet in tweets:
		try:
			words = tweet['text'].split()
		except:
			tweetSentiment = 0
			print float(0)
			tweetScore.append(float(tweetSentiment))
		else:
			tweetSentiment = [sentScores.get(w,0) for w in words]
			print float(sum(tweetSentiment))
			tweetScore.append(float(sum(tweetSentiment)))

if __name__ == '__main__':
    main()