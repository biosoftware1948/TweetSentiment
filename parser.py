import tweepy
import sys


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



class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status)





def main():
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        Spider = Twitter_Scraper(content[0], content[1], content[2], content[3])
        Spider.connect()
        Spider.stream_tweets(['Spicer'])
    except:
        sys.exit(1)

if __name__ == "__main__":
	main()
