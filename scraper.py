# -*- coding: utf-8 -*-
import tweepy
import numpy as np
import pandas as pd
import sys

class Twitter_Scraper(object):
    def __init__(self, query=None, delimiter=200):
        """
        Inputs: Query, delimiter
        Query format: pass a tuple containing two lists. first list is your words
        second list is emojis. this ANDs every combination of emoji and words,
        and ORs the combinations. Or pass one list containing words, this will and all
        emojis with words
        Delimiter: Top k emojis, default 200.
        """
        self.scraperListener = MyStreamListener()
        self.authorization = ""
        self.api = ""
        self.scraperListener = MyStreamListener()
        self.hashtags = np.array
        self.data = pd.read_csv('/Users/Matthew_Findlay/Desktop/Documents/Personal/TweetSentiment/Emoji_Sentiment_Data_v1.0.csv')
        self.top_emoji = self.data['Emoji'][:delimiter]

        if query is None:
            self.query = self.top_emoji
            self.query = [i for i in self.query]
            self.query = [','.join(self.query)]
        else:
            if query.count(list) ==2 :
                words, emojis = query
            else:
                words = query
                emojis = self.top_emoji
            self.query = emojis
            self.query = [i + "  "+ w for i in self.query for w in words]
            self.query = [','.join(self.query)]
        print(self.query[0])
        print(len(str(self.query[0]).encode('utf-8')))
        self.connect()
        self.stream_tweets()

    def connect(self):
        try:
            self.authorization = tweepy.OAuthHandler('S7JBDnDRaKEmJXKvKtFagL1mP', 'RJc2mEI5lKWijTteLMa8RO0Jxl0jwb9VNF7n5p0UlDkYSWdDaO')
            self.authorization.set_access_token('851901972437377024-iqlj68E7dXvGRbBfY3cQenKVznhO0nn', 'ZFTipPlxlmDRFaGxsVQ7w34ej6yijJisJeFeKGsUFk7jk')
            self.api = tweepy.API(self.authorization)
        except:
            sys.stdout.write("Authorization failed, check keys and tokens")
            sys.exit()

    def stream_tweets(self):
        try:
            stream = tweepy.Stream(self.authorization, self.scraperListener)
            stream.filter(track=self.query, languages=["en"])
        except KeyboardInterrupt:
            sys.stdout.write("\n\nGoodnight Sweet Prince")
            sys.exit()

    def get_trending_hashtags(self):
        top_hashtags = self.api.trends_place(1)
        data = top_hashtags[0]
        trend_data= data['trends']
        names = [trend['name'] for trend in trend_data]
        for tag in names:
            print(tag)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        pass
        #print(status._json)
        #Parser.process_tweet(status)
