import tweepy
import requests
import pandas as pd
import config
from twitter_app import App
from predictor import Predictor
from streamlit_app import Streamlitapp

app= App(bearer_token=config.bearer_token, 
                        consumer_key=config.consumer_key, 
                        consumer_secret=config.consumer_secret, 
                        access_token=config.access_token, 
                        access_token_secret=config.access_token_secret)

predictor=Predictor()
streamlit_app=Streamlitapp(predictor,app)

if __name__=='__main__':
    streamlit_app.run()