# -*- coding: utf-8 -*-
import re
import tweepy
import nltk
import sys
import textblob
import json
import csv
import os

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
			sys.stdout.write("\n\nGoodnight Sweet Prince")
			sys.exit()

	def get_trending_hashtags(self):
		top_hashtags = self.api.trends_place(1)
		data = top_hashtags[0]
		trend_data= data['trends']
		names = [trend['name'] for trend in trend_data]
		for tag in names:
			print tag

class MyStreamListener(tweepy.StreamListener):
	def on_status(self, status):
		self.process_tweet(status)

	def process_tweet(self, unprocessedTweet):
		jsonTweet = json.dumps(unprocessedTweet._json)
		parsedTweet = json.loads(jsonTweet)
		try:
			fullTweet = str(parsedTweet['extended_tweet']['full_text'].encode('utf-8'))
		except:
			try:
				fullTweet = str(parsedTweet['quoted_status']['extended_tweet']['full_text'].encode('utf-8'))
			except:
				try:
					fullTweet = str(parsedTweet['retweeted_status']['extended_tweet']['full_text'].encode('utf-8'))
				except:
					fullTweet = str(parsedTweet['text'].encode('utf-8'))

		polarity, subjectivity = self.analyze_sentiment(fullTweet)
		sys.stdout.write("Tweet: " + fullTweet + "\nPolarity: " + str(polarity) + "\nSubjectivity: " + str(subjectivity) + "\n")

		highpoints = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
		tweetEmojis = highpoints.findall(fullTweet.decode('utf-8'))

		if not len(tweetEmojis) == 0:
			emojiList = list(''.join(x) for x in tweetEmojis if x != '')
			searchList = list(x.encode('utf-8') for x in emojiList)
			print("Emojis Used: " + ' '.join(emojiList))
			sentiment_database = fetch_data()
			emojiNums = emoji_analyze(searchList, sentiment_database)
			print(emojiNums)
			print("\n\n")

	def analyze_sentiment(self, tweet):
		#returns a tuple containing polarity and subjectivity
		cleanTweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
		testimonial = textblob.TextBlob(cleanTweet)
		return testimonial.sentiment

def fetch_data():
	#Fetch directory and open
	dir_path = os.path.dirname(os.path.realpath(__file__))
	emoji_data_path = os.path.join(dir_path, "Emoji_Sentiment_Ranking_1.0/Emoji_Sentiment_Data_v1.0.csv")
	#organize into dictionary
	data = csv.DictReader(open(emoji_data_path, 'r'))
	emoji_sentiment_data = {}
	for row in data:
		key = row.pop('Emoji')
		emoji_sentiment_data[key] = row
	#print_database(emoji_sentiment_data)
	return emoji_sentiment_data

def print_database(obj):
    if type(obj) == dict:
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print "\n" + k
                print_database(v)
            else:
                print '%s : %s' % (k, v)
    elif type(obj) == list:
        for v in obj:
            if hasattr(v, '__iter__'):
                print_database(v)
            else:
                print v
    else:
        print obj + "\n"

def emoji_analyze(emojis, database):
	sentiments = []
	#Use laplace estimate to calculate probabilities
	class_count = 3
	for emoji in emojis:
		try:
			proba_pos = (float(database[emoji].get("Positive"))+1)/(float(database[emoji].get("Occurrences"))+class_count)
			proba_neut = (float(database[emoji].get("Neutral"))+1)/(float(database[emoji].get("Occurrences"))+class_count)
			proba_neg = (float(database[emoji].get("Negative"))+1)/(float(database[emoji].get("Occurrences"))+class_count)
			sentiments.append(1*proba_pos + 0*proba_neut + (-1)*proba_neg)
		except:
			sentiments.append(-20)	#-20 means there was a failure with that emoji
	return sentiments

def hashtag_analyze(hashtag, sentiments):
	hashtag_sentiments = {}
	avg_sentiment = sum(sentiments)/len(sentiments)
	hashtag_sentiments[hashtag] = avg_sentiment


def main():
	#Get arguments
	try:
		with open(sys.argv[1]) as f:
			content = f.readlines()
			content = [x.strip() for x in content]
		Spider = Twitter_Scraper(content[0], content[1], content[2], content[3])
	except:
		usage()
		sys.exit(1)
	sentiment_database = fetch_data()
	hashtag_of_interest = "#trump"
	filterStream = '😀,😃,😄,😁,😆,😅,😂,🤣,😊,😇,🙂,🙃,😉,😌,😍,😘,😗,😙,😚,😋,😜,😝,😛,🤑,🤗,🤓,😎,🤡,🤠,😏,😒,😞,😔,😟,😕,🙁,☹️,😣,😖,😫,😩,😤,😠,😡,😶,😐,😑,😯,😦,😧,😮,😲,😵,😳,😱,😨,😰,😢,😥,🤤,😭,😓,😪,😴,🙄,🤔,🤥,😬,🤐,🤢,🤧,😷,🤒,🤕,😈,👿,👹,👺,💩,👻,💀,☠️,👽,👾,🤖,🎃,😺,😸,😹,😻,😼,😽,🙀,😿,😾,👐,🙌,👏,🙏,🤝,👍,👎,👊,✊,🤛,🤜,🤞,✌️,🤘,👌,👈,👉,👆,👇,☝️,✋,🤚,🖐,🖖,👋,🤙,💪,🖕,✍️,🤳,💅,🖖,💄,💋,👄,👅,👂,👃,👣,👁,👀,🗣,👤,👥,👶,👦,👧,👨,👩,👱‍,👱,👴,👵,👲,👳‍,👳,👮‍,👷‍,👷,💂‍,💂,🕵️️,👩‍,👨‍,👩‍🌾,👨‍🌾,👩‍🍳,👨‍🍳,👩‍🎓,👨‍🎓,👩‍🎤,👨‍🎤,👩‍🏫,👨‍🏫,👩‍🏭,👨‍🏭,👩‍💻,👨‍💻,👩‍💼,👨‍💼,👩‍🔧,👨‍🔧,👩‍🔬,👨‍🔬,👩‍🎨,👨‍🎨,👩‍🚒,👨‍🚒,👩,‍✈️,👩‍🚀,👨‍🚀,⚖️,🤶,🎅,👸,🤴,👰,🤵,👼,🤰,💁,💁‍,🙅,🙆,🙆‍,🙋,🙋‍,🤦‍,🤷‍,🤷‍,🙎,🙎‍,🙍,🙍‍,💇,💇‍,💆,💆‍,🕴,💃,🕺,👯,👯‍,🚶‍,🚶,🏃‍,🏃,👫,👭,👬,💑,👩‍❤️‍👩,👨‍❤️‍👨,💏,👩‍❤️‍💋‍👩,👨‍❤️‍💋‍👨,👪,👨‍👩‍👧,👨‍👩‍👧‍👦,👨‍👩‍👦‍👦,👨‍👩‍👧‍👧,👩‍👩‍👦,👩‍👩‍👧,👩‍👩‍👧‍👦,👩‍👩‍👦‍👦,👩‍👩‍👧‍👧,👨‍👨‍👦,👨‍👨‍👧,👨‍👨‍👧‍👦,👨‍👨‍👦‍👦,👨‍👨‍👧‍👧,👩‍👦,👩‍👧,👩‍👧‍👦,👩‍👦‍👦,👩‍👧‍👧,👨‍👦,👨‍👧,👨‍👧‍👦,👨‍👦‍👦,👨‍👧‍👧,👚,👕,👖,👔,👗,👙,👘,👠,👡,👢,👞,👟,👒,🎩,🎓,👑,⛑,🎒,👝,👛,👜,💼,👓,🕶,🌂,☂️,❤️,💛,💚,💙,💜,🖤,💔,❣️,💕,💞,💓,💗,💖,💘,💝,💟,🐵,🙊,🙉,🎉,💯,💀,☠️,👑,🎁,🎈,🎂,🏆'

	steam_list = filterStream.split(',')
	steam_list = [i.decode('utf-8') for i in steam_list]
	steam_list = [i + "  "+hashtag_of_interest for i in steam_list]
	for i in steam_list:
		filterStream = ','.join(steam_list)

	print filterStream
	Spider.connect()
	Spider.stream_tweets(['trump'])

def usage():
	usg = """
	PASS A TEXT FILE CONTAINING THE FOLLOWING A AN ARGUMENT:
	Consumer Key
	Consumer Secret
	Access Token
	Access Token Secret \n"""
	sys.stdout.write(usg)

if __name__ == "__main__":
	main()
