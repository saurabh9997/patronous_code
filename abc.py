import tweepy  # https://github.com/tweepy/tweepy
import csv
import re
import pandas as pd
from csv_file import mentioned

# Twitter API credentials
consumer_key = "52uxnTb1VxqI6by7w8Gvp7QmC"
consumer_secret = "ZpU2yKY40lJ77V2FlBxDPXfWdh7XfgmzVnbBQEX4J4jvvLkJau"
access_key = "1368485797544873990-zcLQ8OYi56OTLB7L2FhjzwpPqTb0Z8"
access_secret = "VGL8L094KHRpGMA3Pb7O7xbXNhb9ZWN8AcCI9OcU3tfPm"


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print(f"...{len(alltweets)} tweets downloaded so far")

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]

    # write the csv
    with open(f'new_{screen_name}_tweets.csv', 'w', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)
    return tweets_analysis(screen_name)


def tweets_analysis(screen_name):
    df = pd.read_csv(f'new_{screen_name}_tweets.csv')
    mentiondf = mentioned(df)
    mentiondf.to_csv('mentions.csv', ignore_index=True)


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("@AngelList")
    # print(c)
