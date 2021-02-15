import os
import tweepy
import requests

def get_api():
    consumer_key 	= os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
    access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api

api = get_api()

public_tweets = api.user_timeline('@elonmusk')

stonks = []
with open('stonks.txt') as f:
    # stonks = [item for line in f for item in line.strip()]
    stonks = [line.replace('\n','') for line in f]
print(stonks)

for tweet in public_tweets:
    print(tweet.text)
    for company in stonks:
        if company.lower() in tweet.text.lower():
            print('Success', company)

# print(tweet.__dict__)

# Imports the Google Cloud client library
from google.cloud import language_v1


# Instantiates a client
client = language_v1.LanguageServiceClient()

# The text to analyze
text = u"Hello, world!"
document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

print("Text: {}".format(text))
print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

# test signed commit on windows FR THIS TIME
