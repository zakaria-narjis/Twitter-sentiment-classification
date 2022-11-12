import tweepy
import requests
import pandas as pd

class App:
    def __init__(self,bearer_token,consumer_key,consumer_secret,access_token,access_token_secret):
        self.client = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)

    def fetch_replies(self,conversation_id):
        replies=self.client.search_recent_tweets('conversation_id:{id} -is:retweet'.format(id=conversation_id),tweet_fields=['author_id','created_at'],user_fields=['username'],expansions='author_id')                    
        replies_dict=replies.json()
        replies_data_df=pd.json_normalize(replies_dict['data']) 
        replies_names_df=pd.json_normalize(replies_dict['includes']['users']) 
        return pd.merge(replies_data_df,replies_names_df, on='author_id', how='left')

    def fetch_tweets(self,username):
        query = 'from:{usr} -is:retweet'.format(usr=username)
        tweets = self.client.search_recent_tweets(query,tweet_fields=['author_id','conversation_id'],max_results=10)
        tweets_dict = tweets.json() 
        tweets_df = pd.json_normalize(tweets_dict['data'] ) 
        return tweets_df

    def fetch_tweets_replies(self,username):
        user_tweets=self.fetch_tweets(username)
        
        for conversation in user_tweets['conversation_id'].tolist():
            self.fetch_replies(conversation)
