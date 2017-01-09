import os
import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
from peewee import *
import praw

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Twitter API
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_KEY = os.environ.get("ACCESS_KEY")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitter = tweepy.API(auth, wait_on_rate_limit=True)

# Database
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

database = PostgresqlDatabase(DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST,
                              port=DB_PORT)

# Reddit
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.environ.get("REDDIT_USERNAME")
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD")
REDDIT_SUBREDDIT = os.environ.get("REDDIT_SUBREDDIT")

reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent='UndeleteTwitter (by /u/jorda_n)',
                     username=REDDIT_USERNAME,
                     password=REDDIT_PASSWORD)
subreddit = reddit.subreddit(REDDIT_SUBREDDIT)
