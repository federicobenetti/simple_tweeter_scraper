# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 10:46:19 2021

@author: Federico.Benetti
"""

import pandas as pd
import os
import re

path_to_folder = r'C:\Users\Federico.Benetti\OneDrive - Legatum Institute\Desktop\Tweets_Scrape'
os.chdir(path_to_folder)
os.listdir()

df1 = pd.read_csv("['nytimes', 'BBCNews', 'TIME', 'GBNEWS', 'AJEnglish', 'Reuters', 'thetimes', 'forbes']_tweets.csv")

df = df1.copy()


###clean data
df['text'] = df['text'].str.replace('\n', '')

df['tot_tweets'] = df.groupby('username')['id'].transform('size')
df['tweets_day'] = df.groupby('username')['id'].transform('size')/7
df['tweets_hour'] = df.groupby('username')['id'].transform('size')/168



#get link to the most liked tweet of the week
most_liked = df.sort_values('favorite_count', ascending = False).groupby('username').first()
most_liked['link'] = most_liked['text'].apply(lambda x: re.sub(r'^.*?https', 'https', x))

#get link to the most re-tweeted tweet of the week
most_retweet = df.sort_values('retweet_count', ascending = False).groupby('username').first()
most_retweet['link'] = most_retweet['text'].apply(lambda x: re.sub(r'^.*?https', 'https', x))


#remove links
df['text'] = df['text'].apply(lambda x: re.sub(r'https.*$', '', x)).str.strip()

#count number of words in tweet
df['nwords'] = df['text'].apply(lambda x: len(x.split()))

#count tweet length
df['tweet_length'] = df['text'].apply(lambda x: len(x))

#remove stopwords
#df['text_nostop'] = df['text'].apply(lambda y: [x for x in word_tokenize(y.lower()) if x not in stop_words])
#' '.join(df['text_nostop'][0])

# This returns a list of all words
def get_list_words(df):
    
    all_sentences = []
    for word in df['text']:
        all_sentences.append(word)

    lines = list()
    for line in all_sentences:    
        words = line.split()
        for w in words: 
            lines.append(w)
            
    return lines


# =============================================================================
# functions to be applied to each username
# =============================================================================

nytimes = df[df['username'] == 'nytimes']


nytimes2 = get_list_words(nytimes)

#remove punctuation
nytimes2 = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in nytimes2]

#make lowercase
nytimes2 = [x.lower() for x in nytimes2]

#non-lemmatize, lemmatize, or stem words

#lemmatize tokens
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 

nytimes_lem = [lemmatizer.lemmatize(x) for x in nytimes2]

#stem tokens
from nltk.stem import PorterStemmer
ps = PorterStemmer()

nytimes_stem = [ps.stem(x) for x in nytimes2]



#remove stopwords
#from nltk import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

nytime_nostop = [x for x in nytimes_lem if x not in stop_words]

nytime_nostop2 = [x for x in nytimes2 if x not in stop_words]

nytime_nostop3 = [x for x in nytimes_stem if x not in stop_words]


# =============================================================================
# Word clouds / Frequencies
# =============================================================================

from nltk.probability import FreqDist
fdist = FreqDist(nytime_nostop)
#can create a word cloud with this
fdistny = pd.DataFrame(fdist.items(), columns=['word', 'frequency'])

fdist2 = FreqDist(nytime_nostop2)
#can create a word cloud with this
fdistny2 = pd.DataFrame(fdist2.items(), columns=['word', 'frequency'])

fdist3 = FreqDist(nytime_nostop3)
#can create a word cloud with this
fdistny3 = pd.DataFrame(fdist3.items(), columns=['word', 'frequency'])


# =============================================================================
# Sentiment Analysis
# =============================================================================













# =============================================================================
# Topic modelling
# =============================================================================







#apply this to all usernames
words_lists = df.groupby('username').apply(get_list_words)

#remove punctuation
words_lists = words_lists.apply(lambda y: [re.sub(r'[^A-Za-z0-9]+', '', x) for x in y])

from nltk.stem.snowball import SnowballStemmer
# The Snowball Stemmer requires that you pass a language parameter
s_stemmer = SnowballStemmer(language='english')

stem = []
for word in lines2:
    stem.append(s_stemmer.stem(word))
    
stem

