# -*- coding: UTF-8 -*-
import tweepy
import os
import json
from sseclient import SSEClient as EventSource
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

# init tweepy
auth = tweepy.OAuthHandler(os.getenv("API_KEY"), os.getenv("API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
twitter = tweepy.API(auth)

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
for event in EventSource(url):
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            if change['user'].startswith("130.83."):
                if 'revision' in change:
                    if 'old' in change['revision']:
                        diff_link = "{}/w/index.php?diff={}&oldid={}".format(change['server_url'], change['revision']['new'], change['revision']['old'])
                        tweet_message = '"{}" wurde anonym aus dem Netz der TU Darmstadt bearbeitet:\n{}'.format(change['title'], diff_link)
                    else:
                        article_link = change['meta']['uri']
                        tweet_message = '"{}" wurde anonym aus dem Netz der TU Darmstadt angelegt:\n{}'.format(change['title'], article_link)
                    print(tweet_message)
                    print()               
                    twitter.update_status(tweet_message)