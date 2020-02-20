from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

consumer_key = "fkJ7hluYFsFXg8xXEmaUHFiiZ" #twitter app’s API Key
consumer_secret = "33P3DkdwPvhVlopbRUno2W32D3629qbFVQEpK1raMhtGgb12Fa" #twitter app’s API secret Key
access_token = "614519895-lmX8aaDCybG3fO23OB5hqU3RkCjTxZebVY5CEhBl" #twitter app’s Access token
access_token_secret = "r1XLlWTdUNJE9H3UNb2w9pRdAdJWMuBpKbminmIaNnu6D" #twitter app’s access token secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

trump_tweets = auth_api.user_timeline(screen_name = "Jennison", count = 600, include_rts = False, tweet_mode = "extended")

final_tweets = [each_tweet.full_text for each_tweet in trump_tweets]

with open("/dbfs/FileStore/tables/JennisonTweets2.txt", "w") as f:
 for item in final_tweets:
   f.write("%s\n" % item)
    
read_tweets = []
with open("/dbfs/FileStore/tables/JennisonTweets2.txt","r") as f:
 read_tweets.append(f.read())

for x in read_tweets:
  print(x)