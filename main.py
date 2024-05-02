import streamlit as st
from streamlit_kpi import streamlit_kpi
import pandas as pd
import time
import plotly.express as px



st.header("Twitter Sentiment Analysis")
st.subheader("Please Enter your search string or #")
st.text_input(" ")
st.button("Search")

tweet_count = pd.read_csv("tweetcount.csv",parse_dates=['date_full'], dayfirst=True)

print(tweet_count)

c1,c2,c3 = st.columns((6,1,3))

c1.subheader("Tweet count by week")
c1.line_chart(tweet_count,x='date_full',y='tweets_count')

c2.empty()

c3.subheader("Pick the Date and #tweets for analysis")


min_date = c3.date_input("Start Date",min_value=min(tweet_count['date_full']),max_value=max(tweet_count['date_full']),value=min(tweet_count['date_full']))
max_date = c3.date_input("End Date",min_value=min_date,max_value=max(tweet_count['date_full']),value=max(tweet_count['date_full']))

tweet_count_selection = tweet_count.query("date_full>=@min_date and date_full<=@max_date")
tweet_count_value = sum(tweet_count_selection['tweets_count'])

c3.slider(label ="#tweets",min_value=10,max_value=tweet_count_value)
Analyze_tweets = c3.button("Get Tweets and Analyze")

while Analyze_tweets==True:
    Analyze_tweets=False
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    my_bar.progress(percent_complete + 1, text="Sentiment Analysis Results are ready")
    
    tweet_data = pd.read_csv("tweetdata_updated_1st day 100 tweets.csv")
    tweet_data_pos = pd.DataFrame(tweet_data.query("sentiment=='Positive'").sort_values('followers',ascending=False).reset_index(),columns=['username','followers'])
    tweet_data_neg = pd.DataFrame(tweet_data.query("sentiment=='Negative'").sort_values('followers',ascending=False).reset_index(),columns=['username','followers'])
    tweet_data_neu = pd.DataFrame(tweet_data.query("sentiment=='Neutral'").sort_values('followers',ascending=False).reset_index(),columns=['username','followers'])

    like_count = sum(tweet_data['like_count'])
    retweet_count = sum(tweet_data['retweet_count'])
    impression_count = sum(tweet_data['impression_count'])

    print(tweet_data_pos)
    print(tweet_data_neg)
    print(tweet_data_neu)

    c1,c2,c3 = st.columns(3)
    with c1:
        streamlit_kpi(key="zero",height=100,title="Likes ",value=like_count,icon="fa-solid fa-thumbs-up")

    with c2:
        streamlit_kpi(key="one",height=100,title="Retweets ",value=retweet_count,icon="fa-solid fa-retweet")

    with c3:
        streamlit_kpi(key="two",height=100,title="Impressions ",value=impression_count,icon="fa-solid fa-eye")

    

    fig = px.pie(names=tweet_data['sentiment'].unique(),values=tweet_data['sentiment'].value_counts())

    col1,col2,col3 = st.columns((4,1,3))
    with col1:
        col1.subheader("Sentiment Analysis")
        col1.plotly_chart(fig,use_container_width=True)
    with col2:
        col2.empty()
    with col3:
        col3.subheader("Top Influencers positive")
        if len(tweet_data_pos)>0:
            col3.dataframe(tweet_data_pos[:3])
        else:
            col3.write("No Positive Influencers")
        
        col3.subheader("Top Influencers negative")
        if len(tweet_data_neg)>0:
            col3.dataframe(tweet_data_neg[:3])
        else:
            col3.write("No negative Influencers")

        col3.subheader("Top Influencers Neutral")
        if len(tweet_data_neu)>0:
            col3.dataframe(tweet_data_neu[:3])
        else:
            col3.write("No Neutral Influencers")
    