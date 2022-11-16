import streamlit as st
import pandas as pd
import re 
import numpy as np

class Streamlitapp:

    def __init__(self,predictor,twitter_app):
        self.predictor=predictor
        self.twitter_app=twitter_app
        pass
    
    def run(self):
        st.title('Twitter Sentiments Analyser')
        st.header('Description:')
        st.write('Twitter Sentiments Analyser is a streamlit app used for sentiment analysis on twitter. The application use machine learning and natural language processing to automaticaly identify and analyze feedback through replies on tweets.')
        st.write('The app can be very usefull for detecting insights on how you can improve your product or service. By analyzing how people talk about your brand on Twitter, you can understand whether they like a new feature you just launched for example.')
        st.write('You can start by entering a twitter username, the app will automaticaly analyse all the recents replies on the user\'s recent tweets (7 days max and 100 replies/tweets due to API limitations) and display the results.')
        st.write('You can find more details and the whole project on my [repo](https://github.com/zakaria-narjis/Twitter-sentiment-classification).')
        st.header('Application:')
        username=st.text_input('Twitter user name')  
        if st.button('Generate'):
            self.display_analysis(username)

    def generate_analysis(self,username):
        with st.spinner('Fetching tweets...'):
            output=self.twitter_app.fetch_tweets_replies(username)
        if output==0:
            st.error('No user or tweets was found with this username.', icon="🚨")
            return None,None
        elif output==1:
            st.error('No replies was found to the user\'s tweets.', icon="🚨")
            return None,None
        else:
            user_tweets,tweets_replies=output   
            with st.spinner('Analyzing replies sentiments...'):
                tweets_sentiments=self.predictor.predict_sentiment(tweets_replies)
            return tweets_sentiments,1

    def generate_tweets_stats(self,df):
        tweets_stats=df.copy()
        tweets_stats=tweets_stats[['conversation_id','positive','negative']].groupby(['conversation_id']).sum().reset_index()       
        tweets_stats['diff']=tweets_stats['positive']-tweets_stats['negative']
        tweets_stats=tweets_stats.style.highlight_max(['positive'],color='green',axis=0)
        tweets_stats=tweets_stats.highlight_min(['positive'],color='red',axis=0)
        tweets_stats=tweets_stats.highlight_max(['negative'],color='red',axis=0)
        tweets_stats=tweets_stats.highlight_min(['negative'],color='green',axis=0)
        tweets_stats=tweets_stats.highlight_max(['diff'],color='green',axis=0)
        tweets_stats=tweets_stats.highlight_min(['diff'],color='red',axis=0)
        return tweets_stats

    def generate_total_data(self,df):
        total_df=pd.DataFrame(df['sentiments'].value_counts())
        total_df['label']=['Positive','Negative']
        return total_df

    def generate_chart_data(self,df): 
        chart_df=df.copy()
        chart_df=chart_df[['day','positive','negative']].groupby('day').sum().reset_index()
        return chart_df

    def generate_max_data(self,df):
        chart_df=df.copy()
        chart_df=chart_df[['author_id','username','positive','negative']].groupby(['author_id','username']).sum().reset_index()
        mostpositive = chart_df['username'].loc[chart_df['positive'].idxmax()]
        mostnegative = chart_df['username'].loc[chart_df['negative'].idxmax()]
        positive_count=chart_df.loc[chart_df['positive'].idxmax()]['positive']
        negative_count=chart_df.loc[chart_df['negative'].idxmax()]['negative']
        return (mostpositive,positive_count),(mostnegative,negative_count)

    def display_analysis(self,username):
        df,flag=self.generate_analysis(username)
        if flag is None:
            return 0
        with st.spinner('Displaying results...'):
            df['day']=df.created_at.map(lambda x:re.sub('T(.+)','',x))  
            df['positive']=np.where(df['sentiments']==1,1,0)
            df['negative']=np.where(df['sentiments']==0,1,0)
            total_df=self.generate_total_data(df)
            chart_df=self.generate_chart_data(df)
            (mostpositive,positive_count),(mostnegative,negative_count)=self.generate_max_data(df)
            tweets_stats_df=self.generate_tweets_stats(df)
            total,history,mpntr,tweets_stats=st.tabs(['Total','History statistics','Repliers statistics','Tweets statistics'])
            
            with total:
                st.header('Total positive/negative sentiments')
                st.bar_chart(data=total_df,x='label',y='sentiments')
                
            with history:
                st.header('History')
                st.bar_chart(data=chart_df,x='day',y=['positive','negative'])

            with mpntr:
                st.header('Most positive/negative twitter repliers')
                col1, col2= st.columns(2)
                col1.metric(label='Most Positive',value=positive_count)
                col1.write('[twitter.com/{user}]'.format(user=mostpositive)+'(https://www.twitter.com/{user})'.format(user=mostpositive))
                col2.metric(label='Most Negative',value=negative_count)
                col2.write('[twitter.com/{user}]'.format(user=mostnegative)+'(https://www.twitter.com/{user})'.format(user=mostnegative))

            with tweets_stats:
                st.header('Sentiments statistics for all the recent user tweets')
                st.dataframe(tweets_stats_df)

        st.success('Finished successfully', icon="✅")

