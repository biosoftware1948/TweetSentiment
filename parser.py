import tweepy
import sys
import re


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
    def on_status(self, status):
        # print(status.author.location)
        states = ['IA', 'KS', 'UT', 'VA', 'NC', 'NE', 'SD', 'AL', 'ID', 'FM', 'DE', 'AK', 'CT', 'PR', 'NM', 'MS', 'PW', 'CO', 'NJ', 'FL', 'MN', 'VI', 'NV', 'AZ', 'WI', 'ND', 'PA', 'OK', 'KY', 'RI', 'NH', 'MO', 'ME', 'VT', 'GA', 'GU', 'AS', 'NY', 'CA', 'HI', 'IL', 'TN', 'MA', 'OH', 'MD', 'MI', 'WY', 'WA', 'OR', 'MH', 'SC', 'IN', 'LA', 'MP', 'DC', 'MT', 'AR', 'WV', 'TX']
        statesFull = ['Alabama','Alaska','American Samoa','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Federated States of Micronesia','Florida','Georgia','Guam','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Marshall Islands','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Northern Mariana Islands','Ohio','Oklahoma','Oregon','Palau','Pennsylvania','Puerto Rico','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virgin Island','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
        regex = re.compile(r'\b(' + '|'.join(states + statesFull) + r')\b')
        if not status.author.location is None:
            # print(status.author.location)
            st = regex.search(status.author.location)
            if st:
                print(st.group(0))





def main():
    try:
        with open(sys.argv[1]) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        Spider = Twitter_Scraper(content[0], content[1], content[2], content[3])
        Spider.connect()
        Spider.stream_tweets(['Trump'])
    except:
        sys.exit(1)

if __name__ == "__main__":
	main()
