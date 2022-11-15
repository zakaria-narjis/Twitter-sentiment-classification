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
        st.write('The app can be very usefull for detecting insights on how you can improve your product or service.By analyzing how people talk about your brand on Twitter, you can understand whether they like a new feature you just launched for example.')
        st.write('You can start by entering a twitter username, the app will automaticaly analyse all the recents replies on the user\'s recent tweets (7 days max) and display results through charts.')
        st.write('You can find the whole project on my [repo](https://github.com/zakaria-narjis/Twitter-sentiment-classification).')
        st.header('Application:')
        username=st.text_input('Twitter user name')  
        a=st.button('Generate',on_click=self.display_analysis,args=(username,))

    def generate_analysis(self,username):
        user_tweets,tweets_replies=self.twitter_app.fetch_tweets_replies(username)
        tweets_sentiments=self.predictor.predict_sentiment(tweets_replies)
        return tweets_sentiments
    
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
        df=self.generate_analysis(username)
        df['day']=df.created_at.map(lambda x:re.sub('T(.+)','',x))  
        df['positive']=np.where(df['sentiments']==1,1,0)
        df['negative']=np.where(df['sentiments']==0,1,0)
        total_df=self.generate_total_data(df)
        chart_df=self.generate_chart_data(df)
        (mostpositive,positive_count),(mostnegative,negative_count)=self.generate_max_data(df)
        total,history,mpntr=st.tabs(['Total','History statistics','Repliers statistics'])

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
            col1.write('[twitter.com/{user}]'.format(user=mostpositive)+'(twitter.com/{user})'.format(user=mostpositive))
            col2.metric(label='Most Negative',value=negative_count)
            col2.write('[twitter.com/{user}]'.format(user=mostnegative)+'(twitter.com/{user})'.format(user=mostnegative))
