import os
from re import template
import tweepy
import requests
import json as simplejason
import simplejson as json
import google
from google.cloud import language_v1
import spacy
from spacy import displacy
from collections import Counter
from spacy.matcher import Matcher
from flask import Flask, render_template
from flask import current_app as app
from google.oauth2 import service_account
# import routes

app = Flask(__name__)
app.config.from_pyfile('config.py')

# app.add_url_rule('/', view_func=routes.home)
# app.add_url_rule('/live', view_func=routes.live)
# app.add_url_rule('/demo', view_func=routes.demo)
# app.add_url_rule('/info', view_func=routes.info)

@app.route('/')
def home():
    """Landing page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}

    ]
    return render_template(
        'index.html',
        title="Stonk Scraper",
        description="Welcome to the Stonk Scraper! This is a natural language processing web app that performs named entity recognition and sentiment analysis for Elon Musk's twitter feed!"
    )

@app.route('/live', methods=['GET', 'POST', 'PUT'])
def live():
    """Live page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'live.html',
        title="Stonk Scraper",
        description="Live scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on live tweets."
    )


@app.route('/demo', methods=['GET', 'POST', 'PUT'])
def demo():
    """Demo page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'demo.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed. Click the buttons below for named entity recognition and sentiment analysis on sample data."
    )

@app.route('/info', methods=['GET', 'POST', 'PUT'])
def info():
    """Info page."""
    nav = [
        {'name': 'Live', 'url': 'live.html'},
        {'name': 'Demo', 'url': 'demo.html'},
        {'name': 'Info', 'url': 'info.html'}
    ]
    return render_template(
        'info.html',
        title="Stonk Scraper",
        description="Demo scraper for Elon's twitter feed."
    )

def getApi():
    # Get environment variables for Twitter API
    consumer_key 	= os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
    access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api

api = getApi()

# Gather tweets from Elon Musk's timeline; to be made generic in the future
user = '@elonmusk'
publicTweets = api.user_timeline(screen_name = user)

# Create list of stonks from stonks.txt
stonks = ''
with open('stonks.txt') as f:
    for line in f:
        stonks += line    

def analyzeSentiment():
    # Instantiate client
    credentials = service_account.Credentials.from_service_account_file('stonk_google_creds.json')
    client = language_v1.LanguageServiceClient(credentials=credentials)
    # Pass in text to analyze from stonks
    for tweet in publicTweets:
        print(tweet.text)
        document = language_v1.Document(content=tweet.text, type_=language_v1.Document.Type.PLAIN_TEXT)
        # Detect tweet sentiment
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        print("Text: {}".format(tweet.text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

analyzeSentiment()

# Empty array that will be used for creating the dictionary pattern of 'LOWER' as the key and company name as the value
stonkList = []

def createStonkList():
    # Create a list of strings where each string is an individual stonk
    temp = ''
    for stonk in stonks:
        temp = temp + stonk
        if stonk == '\n':
            stonkList.append(temp.strip('\n'))
            temp = ''

createStonkList()

# Empty array to add patterns that will be used for token matching with spaCy library
pattern = []

def createPattern(stonkList):
    # Create a pattern dictionary for each symbol or stock name
    for item in stonkList:
        # Empty dictionary for pattern creation
        patternDict = {}
        # Check to see if there is a space in the company name
        if ' ' in item:
            splitList = item.split(' ')
            temp = []
            for item in splitList:
                # Create dictionary list where each word in the company name is a value in its own dictionary
                # Copied so multiple dictionaries with the same key "lower" can be created
                patternDict["LOWER"] = item.lower()
                dict_copy = patternDict.copy()
                temp.append(dict_copy)
                if item == splitList[-1]:
                    pattern.append(temp)
                # Create pattern for company name in the form of a twitter handle
                patternDict["LOWER"] = '@' + item.lower()
                dict_copy_handle = patternDict.copy()
                tempHandle = []
                tempHandle.append(dict_copy_handle)
                pattern.append(tempHandle)
                tempHandle = []
        # Pattern for all companies without space in name
        else:
            # Create pattern for single word company; copied so multiple dictionaries with same key can be created
            patternDict["LOWER"] = item.lower()
            dict_copy = patternDict.copy()
            temp = []
            temp.append(dict_copy)
            pattern.append(temp)
            # Create pattern for single word company as Twitter handle
            patternDict["LOWER"] = '@' + item.lower()
            dict_copy_handle = patternDict.copy()
            temp = []
            temp.append(dict_copy_handle)
            pattern.append(temp)

createPattern(stonkList)

# Main token matching function using spaCy for ticker symbols and company names
def tokenMatching(tweet, pattern):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    matcher.add("Match_By_Token", pattern)
    doc = nlp(tweet)
    matches = matcher(doc)
    matchedTokens = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matchedTokens.append(span.text)
    if matchedTokens:
        print(matchedTokens)

# Matching for tweets
for tweet in publicTweets:
    print(tweet.text)
    tokenMatching(tweet.text, pattern)

# @app.context_processor
# def utility_processor():
#     def tweets():
#         result = ''
#         for tweet in publicTweets:
#             print(tweet.text)
#             test = tokenMatching(tweet.text, pattern)
#             result += tweet.text, test
#             return result
#     return dict(tweets=tweets)



# def tweets():
#     for tweet in publicTweets:
#         print(tweet.text)
#         tokenMatching(tweet.text, pattern)
#         return dict(tweets=tweets)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)