import tweepy
import requests
import pandas as pd

consumer_key="QsUPTJrRilV4CJmlGnF3uFcQi"
consumer_secret="WgzG5aU3398lXdgzecZH3az9WYhyDSG8S5TAAU8sUBh9eOwNWw"
access_token="755913179595673601-y1HzykMtpT2zAvFeX9T1o7QqJHxYlG2"
access_token_secret="nH0A0ORFLqOzgdL5dcA2tfUyKPbYD9x8JYnziZO0Qaorw"
bearer_token="AAAAAAAAAAAAAAAAAAAAAAWpjAEAAAAAhKnoECdNTK3xLJt6v%2BT1wYxdbv8%3DjwXjxlsEhleFx589jEEqmHmSbW163haupZ3zuTrVxi67VWJgbX"

client = tweepy.Client(bearer_token=bearer_token, 
                        consumer_key=consumer_key, 
                        consumer_secret=consumer_secret, 
                        access_token=access_token, 
                        access_token_secret=access_token_secret, 
                        return_type = requests.Response,
                        wait_on_rate_limit=True)
'''
query = 'from:tunguz -is:retweet'

tweets=client.search_recent_tweets(query,tweet_fields=['author_id','conversation_id'],max_results=10)

tweets_dict = tweets.json() 
print(tweets_dict['meta']['result_count'])

tweets_data = tweets_dict['data'] 

df = pd.json_normalize(tweets_data) 
print(df)'''


replies=client.search_recent_tweets('conversation_id:1591103002990891015 -is:retweet',tweet_fields=['author_id','created_at'],user_fields=['username'],expansions='author_id')
replies_dict=replies.json()
replies_data=replies_dict['data']
replies_names=replies_dict['includes']['users']


rdf=pd.json_normalize(replies_data) 
rdf_=pd.json_normalize(replies_names)
rdf_=rdf_.rename(columns={'id':'author_id'})

ndf=pd.merge(rdf,rdf_, on='author_id', how='left')
ndf=ndf.drop('edit_history_tweet_ids',axis=1)
print(ndf)