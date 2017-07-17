# -*- coding: utf-8 -*-
import tweepy
import sys
import re
import json
import emoji
import numpy as np
import pandas as pd


class Tweet():
    def __init__(self, location, emojis, urls, hashtags, cleanText, text):
        self.location = location
        self.emojis = emojis
        self.urls = urls
        self.hashtags = hashtags
        self.cleanText = cleanText
        self.text = text


class parser():
    def __init__(self):
        self.tweet = None
        self.location = "None1"
        self.emojis = []
        self.urls = []
        self.hashtags = []
        self.cleanText = ""
        self.text = ""

        self.tweetJSON = ""
        self.stateDict = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AS": "American Samoa",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "DC": "District Of Columbia",
            "FM": "Federated States Of Micronesia",
            "FL": "Florida",
            "GA": "Georgia",
            "GU": "Guam",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MH": "Marshall Islands",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "MP": "Northern Mariana Islands",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PW": "Palau",
            "PA": "Pennsylvania",
            "PR": "Puerto Rico",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "UT": "Utah",
            "VT": "Vermont",
            "VI": "Virgin Islands",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming"
        }
        states = ['IA', 'KS', 'UT', 'VA', 'NC', 'NE', 'SD', 'AL', 'ID', 'FM', 'DE', 'AK', 'CT', 'PR', 'NM', 'MS', 'PW', 'CO', 'NJ', 'FL', 'MN', 'VI', 'NV', 'AZ', 'WI', 'ND', 'PA', 'OK', 'KY', 'RI', 'NH', 'MO', 'ME', 'VT', 'GA', 'GU', 'AS', 'NY', 'CA', 'HI', 'IL', 'TN', 'MA', 'OH', 'MD', 'MI', 'WY', 'WA', 'OR', 'MH', 'SC', 'IN', 'LA', 'MP', 'DC', 'MT', 'AR', 'WV', 'TX']
        statesFull = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virgin Island','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
        self.statesRegex = re.compile(r'\b(' + '|'.join(states + statesFull) + r')\b')
        self.urlRegex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        data = pd.read_csv('Emoji_Sentiment_Data_v1.0.csv')
        top_emoji = data['Emoji']
        pattern = '[' + ''.join(top_emoji) + ']'
        self.emojiRegex = re.compile(pattern, flags=re.UNICODE)


    def parseTweet(self, toParse, location=None):
        try:
            self.tweet = toParse
            jsonString = json.dumps(self.tweet._json)
            self.tweetJSON = jsonString
            self.tweet = json.loads(jsonString)

            if location:
                if location == "ALL":
                    if(self.getLocation() and self.getText() and self.getHashtags()):
                        if(self.getURLS() and self.getEmojis() and (not self.location == "None")):
                            return Tweet(self.location, self.emojis, self.urls, self.hashtags, self.cleanText, self.text)
                    return False
                else:
                    if(self.getLocation() and self.getText() and self.getHashtags()):
                        if(self.getURLS() and self.getEmojis() and self.location == location):
                            return Tweet(self.location, self.emojis, self.urls, self.hashtags, self.cleanText, self.text)
                    return False
            else:
                if(self.getLocation() and self.getText() and self.getHashtags()):
                    if(self.getURLS() and self.getEmojis()):
                        return Tweet(self.location, self.emojis, self.urls, self.hashtags, self.cleanText, self.text)
                return False

        except:
            print("There was an error parsing the tweet")
            return False

    def getLocation(self):
        try:
            if not self.tweet["user"]["location"] is None:
                st = self.statesRegex.search(self.tweet["user"]["location"])
                if st:
                    if (len(st.group(0))) == 2:
                        self.location = self.stateDict[st.group(0)]
                        return True
                    else:
                        self.location = st.group(0)
                        return True

            self.location = "None"
            return True
        except:
            print("Error occured parsing location data for Tweet")
            return False

    def getText(self):
        try:
            if "retweeted_status" in self.tweet:
                if "extended_tweet" in self.tweet["retweeted_status"]:
                    self.text = ("RT:: " + self.tweet["retweeted_status"]["extended_tweet"]["full_text"])
                    return True
                else:
                    self.text = ("RT::" + self.tweet["retweeted_status"]["text"])
                    return True
            else:
                if "extended_tweet" in self.tweet:
                    self.text = (self.tweet["extended_tweet"]["full_text"])
                    return True
                else:
                    self.text = (self.tweet["text"])
                    return True
            return False
        except:
            print('Error occured when parsing text of tweet.\n')
            return False

    def getHashtags(self):
        try:
            self.hashtags = []
            if "retweeted_status" in self.tweet:
                if "extended_tweet" in self.tweet["retweeted_status"]:
                    for tag in self.tweet["retweeted_status"]["extended_tweet"]["entities"]["hashtags"]:
                        self.hashtags.append(tag["text"])
                        return True
                else:
                    for tag in self.tweet["retweeted_status"]["entities"]["hashtags"]:
                        self.hashtags.append(tag["text"])
                        return True
            else:
                if "extended_tweet" in self.tweet:
                    for tag in self.tweet["extended_tweet"]["entities"]["hashtags"]:
                        self.hashtags.append(tag["text"])
                        return True
                else:
                    for tag in self.tweet["entities"]["hashtags"]:
                        self.hashtags.append(tag["text"])
                        return True

            return True
        except:
            print('Error occured when parsing hashtags of tweet.\n')
            return False

    def getURLS(self):
        try:
            self.urls = self.urlRegex.findall(self.text)
            self.cleanText = self.urlRegex.sub("", self.text)
            return True
        except:
            print('Error occured when parsing URLs of tweet. \n')
            return False

    def getEmojis(self):
        try:
            matches = self.emojiRegex.findall(self.text)
            self.emojis = matches
            #matching regex cannot catch all updated UNICODE Emojis - use 'emoji' lib to remove all
            for c in self.text:
                if c in emoji.UNICODE_EMOJI:
                    self.cleanText = self.cleanText.replace(c,'')
            return (len(self.emojis) > 0)
        except:
            print('Error occured when parsing Emojis of tweet. \n')
            return False

class Twitter_Scraper(object):
	def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_token = access_token
		self.access_token_secret = access_token_secret
		self.authorization = ""
		self.api = ""
		self.scraperListener = MyStreamListener()

	def connect(self):
		try:
			self.authorization = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			self.authorization.set_access_token(self.access_token, self.access_token_secret)
			self.api = tweepy.API(self.authorization)
		except:
			sys.stdout.write("Authorization failed, check keys and tokens")
			sys.exit()

	def stream_tweets(self, tracker):
		try:
			stream = tweepy.Stream(self.authorization, self.scraperListener)
			stream.filter(track=tracker, languages=["en"])
		except KeyboardInterrupt:
			sys.stdout.write("\n\nGoodnight Sweet Prince\n")
			sys.exit()



class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        tweepy.StreamListener.__init__(self)
        self.parser = parser()
    def on_status(self, status):
        tweetFrame = (self.parser.parseTweet(status, "ALL"))
        if tweetFrame:
            print("\n\n********************")
            print("LOCATION: " + tweetFrame.location)
            print("TEXT: " + tweetFrame.text)
            print("CLEAN TEXT: " + tweetFrame.cleanText)
            print("EMOJIS: " + str(tweetFrame.emojis))
            print("URLS: " + str(tweetFrame.urls))
            print("********************\n\n")


def main():
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        Spider = Twitter_Scraper(content[0], content[1], content[2], content[3])
        Spider.connect()
        Spider.stream_tweets(['😂,❤,♥,😍,😭,😘,😊,👌,💕,👏,😁,☺,♡,👍,😩,🙏,✌,😏,😉,🙌,🙈,💪,😄,😒,💃,💖,😃,😔,😱,🎉,😜,☯,🌸,💜,💙,✨,😳,💗,★,█,☀,😡,😎,😢,💋,😋,🙊,😴,🎶,💞,😌,🔥,💯,🔫,💛,💁,💚,♫,😞,😆,😝,😪,😫,😅,👊,💀,😀,😚,😻,©,👀,💘,🐓,☕,👋,✋,🎊,🍕,❄,😥,😕,💥,💔,😤,😈,►,✈,🔝,😰,⚽,😑,👑,😹,👉,🍃,🎁,😠,🐧,☆,🍀,🎈,🎅,😓,😣,😐,✊,😨,😖,💤,💓,👎,💦,✔,😷,⚡,🙋'])
    except:
        print("main failed")
        sys.exit(1)

if __name__ == "__main__":
	main()
