import json
import const
import os


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


######################################################



if not read_config_file():
    #print "Oops -.- , config file doesn't exist... Creating..."
    create_config_file()

