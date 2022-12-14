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

    def fetch_replies(self,conversation_id,username):
        replies=self.client.search_recent_tweets('conversation_id:{id} -is:retweet -from:{usr}'.format(id=conversation_id,usr=username),tweet_fields=['author_id','created_at'],user_fields=['username','location'],expansions='author_id',max_results=100)                       
        replies_dict=replies.json()
        if replies_dict['meta']['result_count']==0:
            return None
        else:
            replies_data_df=pd.json_normalize(replies_dict['data']) 
            replies_names_df=pd.json_normalize(replies_dict['includes']['users']) 
            replies_names_df=replies_names_df.rename(columns={'id':'author_id'})
            return pd.merge(replies_data_df,replies_names_df, on='author_id', how='left')

    def fetch_tweets(self,username):
        query = 'from:{usr} -is:retweet -is:reply'.format(usr=username)
        tweets = self.client.search_recent_tweets(query,tweet_fields=['author_id','conversation_id'],max_results=100)
        tweets_dict = tweets.json() 
        if tweets_dict['meta']['result_count']==0:
            return None
        else:
            tweets_df = pd.json_normalize(tweets_dict['data']) 
            tweets_df= tweets_df.drop('edit_history_tweet_ids',axis=1)
            return tweets_df

    #Retrieve all recent replies from the user's specified number of recent tweets (7 days max, max results=10)
    def fetch_tweets_replies(self,username):
        user_tweets=self.fetch_tweets(username)
        if user_tweets is None:
            return 0
        else:
            replies_list=[]
            for conversation_id in user_tweets['conversation_id'].tolist():
                replies=self.fetch_replies(conversation_id,username)
                if replies is None:
                    pass
                else:
                    replies=replies.drop('edit_history_tweet_ids',axis=1)
                    replies['conversation_id']=conversation_id
                    replies_list.append(replies)
            if replies_list==[]:
                return 1
            else:
                replies_df=pd.concat(replies_list,ignore_index=True)
                return user_tweets,replies_df


#BETA
"""
class App:
    def __init__(self,bearer_token,consumer_key,consumer_secret,access_token,access_token_secret):
        self.client = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)

    def fetch_tweets_replies(self,username):
        query = 'to:{usr}'.format(usr=username)
        replies = self.client.search_recent_tweets(query,tweet_fields=['author_id','created_at','conversation_id'],user_fields=['username','location'],expansions='author_id')
        replies_dict = replies.json() 
        if replies_dict['meta']['result_count']==0:
            return None
        else:     
            replies_data_df=pd.json_normalize(replies_dict['data']) 
            replies_names_df=pd.json_normalize(replies_dict['includes']['users']) 
            replies_names_df=replies_names_df.rename(columns={'id':'author_id'})
            replies_df=pd.merge(replies_data_df,replies_names_df, on='author_id', how='left')
            replies_df=replies_df.drop('edit_history_tweet_ids',axis=1)
            replies_df=replies_df.drop(replies_df[replies_df.username == username].index)
            if replies_df.empty==True:
                return None
            else:
                return replies_df
                """

