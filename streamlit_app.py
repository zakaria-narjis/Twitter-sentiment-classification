import streamlit as st
import pandas as pd
import re 

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
        st.button('Generate',on_click=self.display_analysis,args=(username,))

    def generate_analysis(self,username):
        user_tweets,tweets_replies=self.app.fetch_tweets_replies(username)
        tweets_sentiments=self.predictor.predict_sentiment(tweets_replies)
    
    def generate_total_data(self,df):
        total_df=pd.DataFrame(df['sentiments'].value_counts())
        total_df['label']=['Positive','Negative']
        return total_df

    def generate_chart_data(self,df): 
        chart_df=df.copy()
        chart_df['day']=df.created_at.map(lambda x:re.sub('T(.+)','',x))  
        chart_df=chart_df[['day','sentiments']].groupby('day')['sentiments'].value_counts().to_frame(name='counts').reset_index() 
        return chart_df

    def display_analysis(self,username):
        total_df=self.generate_total_data(pd.read_csv('sentiments.csv'))
        chart_df=self.generate_chart_data(pd.read_csv('sentiments.csv'))
        total,chart,data=st.tabs(['Total','Chart','Data'])
        with total:
            st.header('Total positive/negative sentiments')
            st.bar_chart(data=total_df,x='label',y='sentiments')
        with chart:
            st.header('History')
            st.bar_chart(data=chart_df,x='day',y='counts')

if __name__=='__main__':
    s=Streamlitapp('taco','taco')
    s.run()