import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow_hub as hub
from tensorflow import keras
import re


class Predictor:

    def __init__(self,threshold=0.5):
        self.model=keras.models.load_model('model.h5',custom_objects={'KerasLayer':hub.KerasLayer}, compile=False)
        self.threshold=threshold 
        
    def regex_filter(self,txt):
        regex_string = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))'
        output=txt
        output=re.sub(regex_string,'',output)
        output=re.sub('(@[^\s]*)\s|\s(@[^\s]*)','',output)
        output=re.sub('(#[^\s]*)\s|\s(#[^\s]*)','',output)
        output=re.sub('[\s]{2}','',output)
        return output
    
    def predict(self,preprocessed_tweets):
        outputs=outputs=np.where(self.model(preprocessed_tweets).numpy()> self.threshold, 1, 0)
        return outputs.reshape(-1)
    
    def preprocess(self,df):
        preprocessed_tweets=df.text.map(self.regex_filter).to_numpy()
        return preprocessed_tweets
    
    def predict_sentiment(self,df):
        df_copy=df.copy()
        preprocessed_tweets=self.preprocess(df)
        sentiment_array=self.predict(preprocessed_tweets)
        df_copy['sentiments']=sentiment_array
        return df_copy
        


