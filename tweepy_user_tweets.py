# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 16:15:20 2021

@author: Federico.Benetti
"""

import pandas as pd
import tweepy
from datetime import datetime, timedelta
from dateutil import parser
import time
import random
import os

path_to_folder = r'/Users/federico/Desktop/Tweets_Scrape'
os.chdir(path_to_folder)

#define twitter account credentials
auth = tweepy.OAuthHandler('wayohHPzVugZIK6beAMrRR4ME', '4zNerikkkR4BAyWeg9PZOtrdMLMgk9PNpCy6JrYi2ZviEgHTZH')
auth.set_access_token('1452332035301945349-RthPNEmfgfs4QQmKa0sg9hjQkRic3E', 'Wh9ybfr0KYA8374iPVN9fx57178uPdk0fQkOFXxiYhcFX')

#access to the API
api = tweepy.API(auth)

#define start of the week
start_week = datetime(2022, 1, 1)

# =============================================================================
# Function to scrape user tweets
# =============================================================================
def get_user_tweets(userID, start_date, ndays):
    """
    Parameters
    ----------
    userID : string
        A Valid Twitter User ID.
    start_date : datetime
        A datatime object indicating the point in time from when the tweets are required.
    ndays: integer
        The number of days to scrape tweets for after the starting date.

    Returns
    -------
    None.
    """    
    #define end of the week
    end_date = start_date + timedelta(days = ndays)

    #scrape first bunch of tweets to get started with
    tweets = api.user_timeline(screen_name = userID, 
                               # 200 is the maximum allowed count
                               count = 200,
                               include_rts = False,
                               # Necessary to keep full_text 
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
    
    #get date of last tweet
    last_tweet_date = parser.parse(tweets[-1]._json.get('created_at'))
    
    
    #define list and components needed in the loop
    all_tweets = []
    all_tweets.extend(tweets)
    last_tweet_date = parser.parse(tweets[-1]._json.get('created_at')).replace(tzinfo=None)
    oldest_id = tweets[-1].id
    
    #loop over the time of interest
    while last_tweet_date.date() + timedelta(days = 1) > start_date.date():
        tweets = api.user_timeline(
                               screen_name = userID, 
                               # 200 is the maximum allowed count
                               count = 150,
                               include_rts = False,
                               max_id = oldest_id - 1,
                               # Necessary to keep full_text otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
        last_tweet_date = parser.parse(tweets[-1]._json.get('created_at')).replace(tzinfo=None)
        
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        
        print('Number of tweets downloaded till now: {}'.format(len(all_tweets)))
        
        #random sleep to avoid aggressive scraping
        time.sleep(random.uniform(0,2))
        
        #break loop when we get tweets older than the starting date
        if last_tweet_date.date() + timedelta(days = 1) < start_date.date():
            break
    
    #store results in a dataframe
    outtweets = [[tweet.id_str, 
                  tweet.created_at, 
                  tweet.favorite_count, 
                  tweet.retweet_count, 
                  tweet.full_text.encode("utf-8").decode("utf-8")] 
                 for idx,tweet in enumerate(all_tweets)]
    
    df = pd.DataFrame(outtweets, columns=["id", "created_at", "favorite_count", "retweet_count", "text"])
    
    #keep only data in the time of interest
    df['created_at'] = df['created_at'].apply(lambda r: r.replace(tzinfo=None))
    df = df[df['created_at'] >= start_date]
    df = df[df['created_at'] <= end_date]
    df['username'] = userID
    
    return df


users_to_scrape = ['nytimes', 'BBCNews', 'TIME', 'GBNEWS', 'AJEnglish', 'Reuters', 'thetimes', 'forbes']

#######################################
# run function for all users in the list above
df_final = []
for user in users_to_scrape:
    print('Started scraping f{user}')
    df = get_user_tweets(userID = user, start_date = start_week, ndays = 7)
    df_final.append(df)
df_final = pd.concat(df_final)


#store data
df_final.to_csv('%s_tweets_080121.csv' % users_to_scrape, index = False)

