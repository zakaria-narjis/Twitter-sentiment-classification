import tweepy
import requests
import pandas as pd
import config
from twitter_app import App
from predictor import Predictor

app= App(bearer_token=config.bearer_token, 
                        consumer_key=config.consumer_key, 
                        consumer_secret=config.consumer_secret, 
                        access_token=config.access_token, 
                        access_token_secret=config.access_token_secret)

predictor=Predictor()
user_tweets,tweets_replies=app.fetch_tweets_replies('tunguz')
tweets_sentiments=predictor.predict_sentiment(tweets_replies)
tweets_sentiments.to_csv('sentiments.csv',index=False)