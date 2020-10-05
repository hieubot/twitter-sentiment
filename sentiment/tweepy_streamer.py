# CODE TO STREAM IN TWEETS USING TWEEPY API

from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import numpy as np
import pandas as pd
import re
import csv
import json

# # # # TWITTER CLIENT # # # #


class TwitterClient:
    """
    Class to use Cursor module to extract tweets from user timelines
    """

    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client


# # # # TWITTER AUTHENTICATOR # # # #

class TwitterAuthenticator:
    def authenticate_twitter_app(self):
        auth = OAuthHandler(
            twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET
        )
        auth.set_access_token(
            twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET
        )

        return auth


class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
        self.twitter_client = TwitterClient()

    def search_hashtags(self, fname, hashtag_list, n_tweets):
        api = self.twitter_client.get_twitter_client_api()

        # open the spreadsheet we will write to
        with open('%s.csv' % (fname), 'wb') as file:

            w = csv.writer(file)

            # write header row to spreadsheet
            w.writerow(['timestamp', 'tweet_text', 'username',
                        'all_hashtags', 'followers_count', 'likes', 'retweets'])

            # for each tweet matching our hashtags, write relevant info to the spreadsheet
            for tweet in Cursor(api.search, q=hashtag_list+' -filter:retweets', lang="en", tweet_mode='extended').items(n_tweets):
                w.writerow([tweet.created_at, tweet.full_text.replace('\n', ' ').encode('utf-8'), tweet.user.screen_name.encode(
                    'utf-8'), [e['text'] for e in tweet._json['entities']['hashtags']], tweet.user.followers_count, tweet.favorite_count, tweet.retweet_count])


class TweetAnalyzer():
    """
    Analyze and categorize content from tweets.
    """

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def tweets_to_data_frame(self, tweets):
        """
        Creates dataframe with data of interest extracted from tweets.
        This can be customized-- use following line to display extractable elements:
            `print(dir(tweets[0]))`
        """
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=['tweets'])
        df['length'] = np.array([len(tweet.text) for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == "__main__":

    # twitter_client = TwitterClient()
    # tweet_analyzer = TweetAnalyzer()

    # api = twitter_client.get_twitter_client_api()
    # tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)

    # df = tweet_analyzer.tweets_to_data_frame(tweets)

    search_terms = "snowflake"

    tweet_streamer = TwitterStreamer()
    tweet_streamer.search_hashtags(
        fname="hashtag_search", hashtag_list=search_terms, n_tweets=100)
