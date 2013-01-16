#!/usr/bin/env python
"""Little attempt of a Twitter Client in python, only for read the tweets through a text file."""
__author__ = "B4rret"

import json
import const
import os
import codecs
import twitter
import threading
import time
import sys
import urllib2

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

def yes_no_question(question, defaultAnswer = None):
    #yn = ""
    #da = ""
    if defaultAnswer == True:
        yn = ' [Y/n]'
        da = 'y'
    elif defaultAnswer == False:
        yn = ' [y/N]'
        da = 'n'
    else:
        yn = ' [y/n]'
        da = ''
    while True:
        answer = raw_input(question + yn).strip().lower()

        if answer == '':
            answer = da
        else:
            answer = answer[1]

        if answer in 'yn':
            break

    return answer == 'y'

def read_config_file():

    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret

    if not os.path.exists(const.CONFIG_FILE):
        return False

    f = open(const.CONFIG_FILE)
    cfgDict = json.load(f)
    f.close()

    if "ConsumerKey" in cfgDict:
        consumer_key = cfgDict["ConsumerKey"]
    if "ConsumerSecret" in cfgDict:
        consumer_secret = cfgDict["ConsumerSecret"]
    if "AccessToken" in cfgDict:
        access_token = cfgDict["AccessToken"]
    if "AccessTokenSecret" in cfgDict:
        access_token_secret = cfgDict["AccessTokenSecret"]

    if consumer_key == "" or consumer_secret == "" or access_token == "" or access_token_secret == "":
        print "Keys missing in config file :/ ..."
        answer = yes_no_question("Do you want to introduce again the keys? ", True)
        if answer == True:
            print "Leave the fieds empty to keep old key..."
            return False
        #else:
        #   sys.exit(0)
    return True

def create_config_file():

    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret

    f = open(const.CONFIG_FILE, "w")
    f.write('{\n')

    txt = raw_input("Write Consumer Key:").strip()
    if txt != '':
        consumer_key = txt
    else:
        txt = consumer_key
    f.write('\t"ConsumerKey":"' + txt + '",\n')

    txt = raw_input("Write Consumer Secret:").strip()
    if txt != '':
        consumer_secret = txt
    else:
        txt = consumer_secret
    f.write('\t"ConsumerSecret":"' + txt + '",\n')

    txt = raw_input("Write Access Token:").strip()
    if txt != '':
        access_token = txt
    else:
        txt = access_token
    f.write('\t"AccessToken":"' + txt + '",\n')

    txt = raw_input("Write Access Token Secret:").strip()
    if txt != '':
        access_token_secret = txt
    else:
        txt = access_token_secret
    f.write('\t"AccessTokenSecret":"' + txt + '"\n')

    f.write('}')
    f.close()

def write_tweets(id):

    global fileOutputName
    global twitterApi

    while True:

        # f = open(fileOutputName, 'w')
        f = codecs.open(fileOutputName, encoding='utf-8', mode='a+')

        if id != 0: 
            statuses = twitterApi.GetFriendsTimeline(None, None, None, id, True, True)
        else:
            f.write("START\n------\n")
            statuses = twitterApi.GetFriendsTimeline(None, None, None, None, True, True)

        for s in reversed(statuses):
            id = s.id
            line = s.created_at + ' | @' + s.user.screen_name + ' (' + s.user.name + '):\n' + s.GetText() + '\nhttps://twitter.com/#!/' + s.user.screen_name + '/status/' + str(id) + '\n--------------------------------------------------------------------------------------------------------------------------------------------'
            
            #if s.urls is not None:
            for u in s.urls :
                line = line.replace(u.url, u.expanded_url)
                #f.write(str(u.expanded_url) + "\n")                  
            #else:            
                #f.write("urls:" + str(s.urls) + "\n")
            
            f.write(line + "\n")
            #print line.encode('ascii','ignore')
        f.flush()
        f.close()
        time.sleep(15) # Twitter lets only 350 petitions per hour. This time wouldn't be less than 10


def main():

    global fileOutputName

    global consumer_key
    global consumer_secret
    global access_token
    global access_token_secret

    global twitterApi

    if not read_config_file():
        #print "Oops -.- , config file doesn't exist... Creating..."
        create_config_file()

    twitterApi = twitter.Api(consumer_key, consumer_secret, access_token, access_token_secret)

    #print consumer_key
    #print consumer_secret
    #print access_token
    #print access_token_secret

    u = twitterApi.VerifyCredentials() 

    if u is None:
        print "Keys wrong"
        return 1
    elif u.GetName() is None:
        print "Keys wrong"
        return 1
    #else:
    #    print "Keys ok"
    #    print u.GetName()

    auxDriveTail = os.path.splitdrive(__file__)
    driveLetter = auxDriveTail[0]

    fileOutputName = os.path.join(driveLetter, 'tws.txt')

    t = threading.Thread(target=write_tweets, args=(0,))  
    t.start()  
    t.join()
    return 0
    
######################################################

if __name__ == "__main__":
    sys.exit(main())
