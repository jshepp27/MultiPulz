# Libraries
import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
import datetime, time
from twitter_credentials import consumer_key, consumer_secret, access_token, access_token_secret
import csv
from textblob import TextBlob

#Authenticate Twitter; Return API object. 
class TwitterAuthenticator():

    def twitter_auth(self):
        global auth
        global api

        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = API(auth)
        return api

# Extract input file 
class FileOps():

    def strip_file(self):
        global username
        username = []

        with open("user_list.txt", "r") as f:
            targets_list = f.readlines()

        for i in targets_list:
            username.append(i.strip('\n'))
        print(username)

# Download tweets
class PullTweets():
    
    # def sentiment(self, text):
    #     if TextBlob(text).sentiment == 0:
    #         print("Neutral")
        
    #     elif TextBlob(text).sentiment > 0:
    #         print("Positive")

    #     elif TextBlob(text).sentiment < 0:
    #         print("Negative")

    def get_tweets(self, screen_name): 

        print("downloading tweets ...")
        global tweets
        tweets = []

        fresh_tweets = api.user_timeline(screen_name, count=5)  
        oldest_id = fresh_tweets[-1].id

        while len(fresh_tweets) > 0:
            fresh_tweets = api.user_timeline(screen_name, count=5, since_id = oldest_id)  
            tweets.extend(fresh_tweets)
            oldest_id = tweets[-1].id
            print(f"{len(tweets)} tweets downloaded ...")

        out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), self.sentiment(tweet.text)] for tweet in tweets]
        
        with open(f'{screen_name} tweets.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["id","created_at","text","sentiment"])
            writer.writerows(out_tweets)



    def all_tweets(self):
        
        for i in username:
            self.get_tweets(i)

# Execution 

twitter_authenticator = TwitterAuthenticator()
twitter_authenticator.twitter_auth()

file_ops = FileOps()
file_ops.strip_file()

pull_tweets = PullTweets()
pull_tweets.all_tweets()





