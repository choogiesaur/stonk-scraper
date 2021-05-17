import os
import tweepy
import requests
import simplejson as json
from google.cloud import language_v1
import nltk
# From Stanford
nltk.download('punkt')
# From chunking
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
# From chunking
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
# Entity (SpaCy)
import spacy
from spacy import displacy
from collections import Counter
from spacy.matcher import Matcher, PhraseMatcher
import en_core_web_sm

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
stonks = ''
with open('stonks.txt') as f:
    for line in f:
        stonks += line    
#     stonks = [line.replace('\n','') for line in f]
# print(stonks)

# Old logic for identifying companies in stonks; to be replaced by Stanford NER tagger (entity_recognition function) or Google NLP NER
# for tweet in public_tweets:
#     print(tweet.text)
#     for company in stonks:
#         if company[0].lower() in tweet.text.lower() or company[1].lower() in tweet.text.lower():
#             print('Success', company, tweet.text)

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

# Token matching using SpaCy for ticker symbols and company names
def phraseMatching(tweet):
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    terms = []
    pattern = []
    temp = ''
    for stonk in stonks:
        temp = temp + stonk
        if stonk == '\n':
            terms.append(temp.strip('\n'))
            temp = ''
    for item in terms:
        patternDict = {}
        patternDict["LOWER"] = item.lower()
        dict_copy = patternDict.copy()
        temp = []
        temp.append(dict_copy)
        pattern.append(temp)
    print(pattern)
    # patternTest = [
    #     [{"LOWER": "spacex"}],
    #     [{"LOWER": "doge"}]
    # ]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("Match_By_Token", pattern)
    doc = nlp(tweet)
    matches = matcher(doc)
    matchedTokens = []
    for match_id, start, end in matches:
        span = doc[start:end]
        matchedTokens.append(span.text)
    print(matchedTokens)

for tweet in public_tweets:
    print(tweet.text)
    phraseMatching(tweet.text)

# Previous testing using tokenizing and NLTK library

# Test function for tokenizing words
def preprocess(tweet):
    for tweet in tweet:
        tokenized_text = nltk.word_tokenize(tweet.text)
        classified_text = nltk.pos_tag(tokenized_text)
        return classified_text

tweets = preprocess(public_tweets)
print(tweets)

# Noun chunking. The rule applied is a noun phrase is formed when an optional determiner is found, followed
# by either an adjective or a noun.
pattern = 'NP: {<DT>?<JJ>*<NN>}'
pat = nltk.RegexpParser(pattern)
new_pat = pat.parse(tweets)
# print(new_pat)
# Format chunks of stonks
iob_tagged = tree2conlltags(new_pat)
# pprint(iob_tagged)

# Recognize named entities in chunks using ne_chunk()
# for tweet in public_tweets:
#     ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(tweet.text)))
#     print(ne_tree)

# for tweet in public_tweets:
#     doc = nlp(tweet.text)
#     # pprint([(X.text, X.label_) for X in doc.ents])
#     pprint([(X, X.ent_iob_, X.ent_type_) for X in doc])