import os
import tweepy
import requests

consumer_key 	= os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
