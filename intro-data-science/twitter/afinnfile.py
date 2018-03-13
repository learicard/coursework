# import re
import urllib
import json

# parse tab-delim word-sentiment scores into a dict
sentScores = {}
for line in open("AFINN-111.txt"):
    term, score  = line.split("\t")
    sentScores[term] = int(score)

tweets = []
for line in open('output_large.txt'):
    try: 
        tweets.append(json.loads(line))
    except:
        pass

numTweets = len(tweets)

tweetScore = []
for tweet in tweets:
    try:
        words = tweet['text'].split()
    except:
        tweetSentiment = 0
        tweetScore.append(float(tweetSentiment))
    else:
        tweetSentiment = [sentScores.get(w,0) for w in words]
        print float(sum(tweetSentiment))
        tweetScore.append(float(sum(tweetSentiment)))

# notes on various approaches

# print sentScores.items()

# # define a fxn to find words in our dict
# def ismember(A,v):
#     B = [ [val in v for val in a] for a in A]
#     return B

#test = ismember(set(scores.viewkeys()), set('unsophisticated'))
#answer = [all(t) for t in test]

# findRegEx = re.compile(r'([a-z].*)')
# def findInText(text, names):
# for possibleName in set(findRegEx.findall(text)):
#     if possibleName in names:
#         return scores[possibleName]
#     return False

# dictionary = scores.keys() # returns a list
# for k in dictionary:
#     textProbe = findInText(k, set(scores.viewkeys()))
#     print(textProbe)

# # using append (not working??)
# query = []
# with open('output.txt') as f:
#     for line in f:
#         query.append(json.load(line))

# # using itertools (not working)
# i = iter(query)
# tweets = dict(izip(i, i))