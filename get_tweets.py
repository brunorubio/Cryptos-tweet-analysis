import tweepy
import csv
import datetime
import time
from tweepy import OAuthHandler
from datetime import timedelta
 
consumer_key = #password1
consumer_secret = #password2
access_token = #password3
access_secret = #password4
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)	
 
api = tweepy.API(auth, wait_on_rate_limit=True)

# Ideally get tweets from 2 days before query execution
d = 2

filename_string = (datetime.datetime.today() - timedelta(days = d)).strftime('%Y-%m-%d')
d1 = (datetime.datetime.today() - timedelta(days = d-1)).strftime("%Y-%m-%d")
d2 = (datetime.datetime.today() - timedelta(days = d)).strftime("%Y-%m-%d")

# Open/Create a file to append data
csvFile = open('cryptos_' + filename_string + '.csv', 'a', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)

query_list = [	
				# Faster transactions 
				'Ripple OR $XRP OR #XRP',
				'#XEM OR $NEM OR $XEM',
				'$Steem OR #Steem',
				'"Bitcoin Cash" OR $BCH OR #BCH OR #Bcash',
				'Litecoin OR #LTC OR $LTC',
				'$Dash OR #Dash',
				'Bitshares OR $BTS',
				'IOTA OR MIOTA',
				'#Stellar OR #XLM OR $XLM',
				# Smart Contracts
				'#ARK OR $ARK',
				'Cardano OR #ADA OR $ADA',
				'#Chainlink OR $LINK',
				'$EOS OR #EOS',
				'Ethereum OR $ETH OR #ETH',
				'"Ethereum Classic" OR $ETC OR #ETC',
				'#NEO OR $NEO',
				'Qtum',
				# Privacy
				'#Verge OR #XVG OR $XVG', 
				'Bytecoin OR $BCN OR #BCN', 
				'#Komodo OR #KMD OR $KMD', 
				'MaidSafeCoin OR #MAID OR $MAID', 
				'Monero OR #XMR OR $XMR',
				'PIVX', 
				'Zcoin OR $XZC OR #XZC',
				'Zcash OR #ZEC OR $ZEC'
				]

for query in query_list:
	for tweet in tweepy.Cursor(api.search,q=query, count=100,
                           since=d2, until=d1, lang="en", tweet_mode='extended').items():
		print (query, tweet.created_at, tweet.user.screen_name, tweet.full_text.encode('utf-8'))
		csvWriter.writerow([tweet.created_at, tweet.user.screen_name, tweet.full_text.encode('utf-8')])
csvFile.close()
