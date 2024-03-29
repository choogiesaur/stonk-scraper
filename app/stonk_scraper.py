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

class StonkScraper:
    def __init__(self, user='@elonmusk'):
        try:
            self.api_conn = self.get_api()
            self.user = user
            self.public_tweets = self.api_conn.user_timeline(screen_name = self.user)
            self.stonk_list = self.create_stonk_list()
            self.pattern = self.create_pattern(self.stonk_list)
        except:
            print("Could not establish API connection and initialize stonk class")

    # Make connection to Twitter API
    def get_api(self):
        
        consumer_key 	= os.getenv('TWITTER_API_KEY')
        consumer_secret = os.getenv('TWITTER_API_KEY_SECRET')
        access_token    = os.getenv('TWITTER_ACCESS_TOKEN')
        access_secret   = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)

        api = tweepy.API(auth)
        return api

    # Refresh list of public tweets
    def refresh_tweets(self):
        self.public_tweets = self.api_conn.user_timeline(screen_name = self.user)
    
    # Analyze sentiment of tweet using Google natural language library
    def analyze_sentiment(self, tweets):
        
        # Instantiate client
        credentials = service_account.Credentials.from_service_account_file('stonk_google_creds.json')
        client = language_v1.LanguageServiceClient(credentials=credentials)
        
        # Pass in text to analyze from stonks
        result = []
        for tweet in tweets:
            document = language_v1.Document(content=tweet.text, type_=language_v1.Document.Type.PLAIN_TEXT)
            
            # Detect tweet sentiment
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            sentiment_formatted= "Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude)
            text = "Text: {}".format(tweet.text) 
            result_dict = dict(text=text, sentiment=sentiment_formatted)
            result.append(result_dict)
        return result

    def create_stonk_list(self):
        
        # Empty array that will be used for creating the dictionary pattern of 'LOWER' as the key and company name as the value
        stonkList = []
        
        # Create list of stonks from stonks.txt
        stonks = ''
        with open('stonks.txt') as f:
            for line in f:
                stonks += line 

        # Create a list of strings where each string is an individual stonk
        temp = ''
        for stonk in stonks:
            temp = temp + stonk
            if stonk == '\n':
                stonkList.append(temp.strip('\n'))
                temp = ''
        
        return stonkList

    # Structure data in pattern recognizable by spaCy for named entity recognition
    def create_pattern(self, stonkList):

        # Empty array to add patterns that will be used for token matching with spaCy library
        pattern = []
        
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
        return pattern

    # Main token matching function using spacy for ticker symbols and company names
    def token_matching(self, tweets, pattern):
        
        # Result array for appending dictionaries with tweets and matched tokens
        result = []
        
        for tweet in tweets:
            nlp = spacy.load("en_core_web_sm")
            matcher = Matcher(nlp.vocab)
            matcher.add("Match_By_Token", pattern)
            doc = nlp(tweet.text)
            matches = matcher(doc)
            matchedTokens = []
            for match_id, start, end in matches:
                span = doc[start:end]
                matchedTokens.append(span.text)
            if matchedTokens:
                result_dict = dict(tweet=tweet.text, tokens=matchedTokens)
                result.append(result_dict)
        return result

if __name__ == "__main__":
    # Add configuration for app from config file
    app.config.from_pyfile('config.py')

    # Create instance of StonkScraper class
    stk = StonkScraper('@elonmusk')

    # Configure routes for app
    app.add_url_rule('/', view_func=routes.home)
    app.add_url_rule('/live', view_func=routes.live)
    app.add_url_rule('/demo', view_func=routes.demo)
    app.add_url_rule('/info', view_func=routes.info)
    app.add_url_rule('/fetch-stonks', view_func=routes.fetch)
    app.add_url_rule('/add-stonks', view_func=routes.add)

    # Run application with specified port and IP address
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True, threaded=True)