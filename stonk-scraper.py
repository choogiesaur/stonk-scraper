import os
import tweepy
import requests
import simplejson as json
from google.cloud import language_v1
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

def get_api():
    # Get environment variables for Twitter API
    consumer_key 	= os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
    access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api

api = get_api()

# Gather tweets from Elon Musk's timeline
public_tweets = api.user_timeline('@elonmusk')

# Create list of stonks from stonks.txt
stonks = []
with open('stonks.txt') as f:
    stonks = [line.replace('\n','').split('|') for line in f]
# print(stonks)

# Old logic for identifying companies in stonks; to be replaced by Stanford NER tagger (entity_recognition function) or Google NLP NER
# for tweet in public_tweets:
#     print(tweet.text)
#     for company in stonks:
#         if company[0].lower() in tweet.text.lower() or company[1].lower() in tweet.text.lower():
#             print('Success', company, tweet.text)

# Old print statement to inspect tweet object
# print(tweet.__dict__)

def analyze_sentiment():
    # Instantiate client
    client = language_v1.LanguageServiceClient()
    # Pass in text to analyze from stonks
    for tweet in public_tweets:
        print(tweet.text)
        document = language_v1.Document(content=tweet.text, type_=language_v1.Document.Type.PLAIN_TEXT)
        # Detect tweet sentiment
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        print("Text: {}".format(tweet.text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

analyze_sentiment()

# Test function for NER using Stanford NER tagger
def entity_recognition():
    st = StanfordNERTagger('/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
					   '/usr/share/stanford-ner/stanford-ner.jar',
					   encoding='utf-8')
    for tweet in public_tweets:
        tokenized_text = word_tokenize(tweet.text)
        classified_text = st.tag(tokenized_text)
        print(classified_text)

# entity_recognition()

def get_tweet(doc):
# Function to pre-process tweets 