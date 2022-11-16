import tweepy
import requests
import pandas as pd
import os
from twitter_app import App
from predictor import Predictor
from streamlit_app import Streamlitapp

app= App(bearer_token=os.environ['bearer_token'], 
                        consumer_key=os.environ['consumer_key'], 
                        consumer_secret=os.environ['consumer_secret'], 
                        access_token=os.environ['access_token'], 
                        access_token_secret=os.environ['access_token_secret'])

predictor=Predictor()
streamlit_app=Streamlitapp(predictor,app)

if __name__=='__main__':
    streamlit_app.run()