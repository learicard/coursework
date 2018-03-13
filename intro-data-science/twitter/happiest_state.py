#!/usr/bin/env python
# happiest_state.py

""" usage: tweet_sentiment.py <sentiment_scores_file> <livestream_twitter_data>
"""

import sys
import urllib
import json
import re

def main():

	# parse tab-delim word-sentiment scores into a dict
	sentimentScores = {}
	for line in open(sys.argv[1]):
	#for line in open('AFINN-111.txt'):
		term, score  = line.split("\t")
		sentimentScores[term] = int(score)

	# interpret all tweets using JSON
	tweets = []
	for line in open(sys.argv[2]):
	#for line in open('output_large.txt'):
		try: 
			tweets.append(json.loads(line))
		except:
			pass

	# calcuate the sum of sentiments for each tweet
	stateScore = {}
	stateCount = {}
	for tweet in tweets:
		try:
			if tweet['place']['country_code'] == 'US':
				location = tweet['place']['full_name'].split(',')
				state = str(location[1]).strip()
				text = tweet['text'].encode('utf-8')
				wordList = re.findall(r"[\w']+", text)
				sentiment = [sentimentScores.get(word,0) for word in wordList]
				score = float(sum(sentiment))
				if stateScore.get(state, 'None') == 'None':
					stateScore[state] = score
					stateCount[state] = 1
				else:
					stateScore[state] = stateScore[state] + int(score)
					stateCount[state] = stateCount[state] + 1
			else:
				pass
		except:
			pass

	# determine the happiest state
	out = max(stateScore.iterkeys(), key=lambda k: stateScore[k])
	print(out)

if __name__ == '__main__':
    main()