'''
Twitter bot program using Twitter APIs that tweets quotes every six hours by Oikawa Tooru,
a fictional character from the sports anime series "Haikyuu!!". Will also auto-reply to
mentions with fun fact about Oikawa.

Made By: Katherine Wong
Date: July 23rd - July 25th, 2022

Resources used and modified for this project: tutorials by Top Code and freeCodeCamp.org.
'''

import tweepy
import time
import random

# variables that contain user credentials to access Twitter API
consumer_key = 'XXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXX'
access_secret = 'XXXXXXXXXXXXXXX'

# log into twitter account api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# variables for file names
quoteFileName = 'quotes.txt'
repliesFileName = 'replies.txt'
lastseenFileName = 'last_seen.txt'

# function to transfer contents of text file into a list
def createList(fileName):
    txtFile = open(fileName, "r")
    txtContent = txtFile.read()

    contentList = txtContent.split("\n")
    txtFile.close()

    return contentList

# function to return random
def randomQuote(contentList):
    randomQuote = random.choice(contentList)
    return randomQuote

# functions to read and store last seen id
def readLastSeen(filename):
    fileRead = open(filename, 'r')
    id = int(fileRead.read().strip())
    fileRead.close()
    return id

def writeLastSeen(filename, id):
    fileWrite = open(filename, 'w')
    fileWrite.write(str(id))
    fileWrite.close()
    return

# create lists of quotes and replies
quotesList = createList(quoteFileName) # list of quotes
repliesList = createList(repliesFileName)

# function to reply to mentions
def reply():
    tweets = api.mentions_timeline(since_id=readLastSeen(lastseenFileName))

    for tweet in reversed(tweets):
        id = tweet.id
        api.update_status(status=randomQuote(repliesList), in_reply_to_status_id=id, auto_populate_reply_metadata=True)  # tweet reply
        writeLastSeen(lastseenFileName, id)  # store id of last seen tweet

# main program - replies to mentions with a fun fact
while True:
    reply()
    time.sleep(2)

# main program - tweet quotes every six hours
while True:
    try:
        api.update_status(randomQuote(quotesList)) # tweet random quote
        time.sleep(60 * 60 * 6) # sleep for 6 hours

    except StopIteration:
        break