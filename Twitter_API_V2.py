import requests
import os
import pandas as pd
import json
from pandas.io.json import json_normalize

def tweetsNext(handler, StartTime, EndTime):  # basic starter function
    tweets = []
    try:
        url = 'https://api.twitter.com/2/users/' + handler + '/tweets?start_time=' + StartTime + '&end_time=' + EndTime + '&max_results=100&tweet.fields=attachments,author_id,id,text,entities&user.fields=id,name,profile_image_url,url,username&expansions=referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,in_reply_to_user_id,attachments.media_keys&media.fields=preview_image_url,type,url'
        payload = {}
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOXTSAEAAAAAHi6oQIL1l8yY%2BCVlbWcw%2F3WYdew%3DqrTCKZ30KK8Kwvp4779eNswGkLiCeJWzF7xOdwcYUnqnD5mB5v'}
        response = requests.request("GET", url, headers=headers, data=payload)
        response = json.loads(response.text)
        for i in range(len(response['data'])):
            tweets.append(response['data'][i])
        next_token = response['meta']['next_token']
        print("nextToken---------------------------->>" + next_token)

        while (next_token):
            url = 'https://api.twitter.com/2/users/' + handler + '/tweets?start_time=' + StartTime + '&end_time=' + EndTime + '&max_results=100&tweet.fields=attachments,author_id,id,text,entities&user.fields=id,name,profile_image_url,url,username&expansions=referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,in_reply_to_user_id,attachments.media_keys&media.fields=preview_image_url,type,url&pagination_token=' + next_token
            payload = {}
            headers = {
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOXTSAEAAAAAHi6oQIL1l8yY%2BCVlbWcw%2F3WYdew%3DqrTCKZ30KK8Kwvp4779eNswGkLiCeJWzF7xOdwcYUnqnD5mB5v'}
            response = requests.request("GET", url, headers=headers, data=payload)
            response = json.loads(response.text)
            for i in range(len(response['data'])):
                tweets.append(response['data'][i])
            next_token = response['meta']['next_token']
            print("nextToken---------------------------->>" + next_token)

    except KeyError:
        print("no Next Token-------------------------------------------------------------------------------")
        print("These are all tweets", tweets)
        print(response)
    CSV = json_normalize(tweets)
    return CSV


def toDataFrame(AccountID, StartTime, EndTime):  # put account id as argument and returns you full tweets of account
    try:
        x = '1'
        tweetsjson = tweetsNextTokens(x, AccountID, StartTime, EndTime)
        Final_CSV = json_normalize(tweetsjson['data'])
        return Final_CSV
    except KeyError:
        return tweetsjson


def tweetsInfo(
        id):  # this function requires and id of tweet as argument and return you include part of retweet full text

    try:
        url = "https://api.twitter.com/2/tweets/" + id + "?expansions=attachments.media_keys,referenced_tweets.id,author_id"

        payload = {}
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAOXTSAEAAAAAHi6oQIL1l8yY%2BCVlbWcw%2F3WYdew%3DqrTCKZ30KK8Kwvp4779eNswGkLiCeJWzF7xOdwcYUnqnD5mB5v'}

        response = requests.request("GET", url, headers=headers, data=payload)

        res = json.loads(response.text)
        result = res['includes']['tweets'][0]
    except KeyError:
        return "NaN"

    return result


def GetRetweetText(CDU_vals):  # accepts array of ids of half text retweets and returns you retweets
    CDU_Retweets = []
    for i in range(len(CDU_vals)):
        print(i + 1, " / ", len(CDU_vals), " id: ", CDU_vals[i])
        result = tweetsInfo(CDU_vals[i])
        CDU_Retweets.append(result)
    return CDU_Retweets


def finalCSV(df, retweetsJson):
    tweettxt = []
    Rtweets = []
    for i in range(len(retweetsJson)):
        try:
            Rtweets.append(retweetsJson[i]['id'])
            tweettxt.append(retweetsJson[i]['text'])
        except TypeError:
            tweettxt.append('NaN')
            Rtweets.append('NaN')
    df['Retweeted Ids'] = Rtweets
    df['Retweeted texts'] = tweettxt

    return df


if __name__ == '__main__':
    StartTime = "2021-07-28T19:03:12Z"  # time Stamp YYYY-MM-DDTHH:MM-SSZ please follow exact time format
    EndTime = "2021-09-28T19:03:12Z"  # time Stamp YYYY-MM-DDTHH:MM-SSZ please follow exact time format
    AccountID = "21107582"  # valid account id

    # for example
    alltweets = tweetsNext(AccountID, StartTime=StartTime,EndTime=EndTime)  # Enter UserID and StartTime, EndTime to get dataframe of tweets in betweet

    tweetIds = alltweets['id'].values  # convert id to values from dataframe

    fulltextRetweets = GetRetweetText(tweetIds)  # get full text of retweeets

    DF_Final = finalCSV(alltweets, fulltextRetweets)  # pass dataframe and fulltextRetweets

    DF_Final.to_csv('./CSU_tweets.csv')


