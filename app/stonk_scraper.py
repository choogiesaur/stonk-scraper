import os
import tweepy
import requests
import routes
from re import template
from google.cloud import language_v1
import spacy
from spacy.matcher import Matcher
from flask import Flask
from flask import current_app as app
from google.oauth2 import service_account

# Make connection to Twitter API
def get_api():
    
    consumer_key 	= os.getenv('TWITTER_API_KEY')
    consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
    access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
    access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    return api

# Analyze sentiment of tweet using Google natural language library
def analyze_sentiment():
    
    # Instantiate client
    credentials = service_account.Credentials.from_service_account_file('stonk_google_creds.json')
    client = language_v1.LanguageServiceClient(credentials=credentials)
    
    # Pass in text to analyze from stonks
    for tweet in publicTweets:
        document = language_v1.Document(content=tweet.text, type_=language_v1.Document.Type.PLAIN_TEXT)
        
        # Detect tweet sentiment
        sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        print("Text: {}".format(tweet.text))
        print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

def create_stonk_list():
    
    # Create a list of strings where each string is an individual stonk
    temp = ''
    for stonk in stonks:
        temp = temp + stonk
        if stonk == '\n':
            stonkList.append(temp.strip('\n'))
            temp = ''

# Structure data in pattern recognizable by spaCy for named entity recognition
def create_pattern(stonkList):

    # Create a pattern dictionary for each symbol or stock name
    for item in stonkList:

        patternDict = {}
        
        # Generic-ified:
        company = []
        if ' ' in item:
            company = item.split(' ')
        else:
            company.append(item)

        # Generate pattern for companies with space
        temp = []
        for item in company:
            # Create dictionary list where each word in the company name is a value in its own dictionary
            # Copied so multiple dictionaries with the same key "lower" can be created
            patternDict["LOWER"] = item.lower()
            dict_copy = patternDict.copy()
            temp.append(dict_copy)
            if item == company[-1]:
                pattern.append(temp)

            # Create pattern for company name in the form of a twitter handle
            patternDict["LOWER"] = '@' + item.lower()
            dict_copy_handle = patternDict.copy()
            tempHandle = []
            tempHandle.append(dict_copy_handle)
            pattern.append(tempHandle)
            tempHandle = []

# Main token matching function using spacy for ticker symbols and company names
def token_matching(tweet, pattern):
    
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

if __name__ == "__main__":
    # Add configuration for app from config file
    app.config.from_pyfile('config.py')

    # Configure routes for app
    app.add_url_rule('/', view_func=routes.home)
    app.add_url_rule('/live', view_func=routes.live)
    app.add_url_rule('/demo', view_func=routes.demo)
    app.add_url_rule('/info', view_func=routes.info)
    app.add_url_rule('/fetch-stonks', view_func=routes.fetch)
    
    # Create API object
    api = get_api()

    # Gather tweets from Elon Musk's timeline
    user = '@elonmusk'
    publicTweets = api.user_timeline(screen_name = user)

    # Create list of stonks from stonks.txt
    stonks = ''
    with open('stonks.txt') as f:
        for line in f:
            stonks += line   

    # Call analyze sentiment function to get score and magnitude of tweets
    analyze_sentiment()

    # Empty array that will be used for creating the dictionary pattern of 'LOWER' as the key and company name as the value
    stonkList = []

    # Create list of strings of stonk names and ticker symbols
    create_stonk_list()

    # Empty array to add patterns that will be used for token matching with spaCy library
    pattern = []

    # Store data in structure for spaCy
    create_pattern(stonkList)

    # Matching for tweets
    for tweet in publicTweets:
        print(tweet.text)
        token_matching(tweet.text, pattern)

    # Run application with specified port and IP address
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)