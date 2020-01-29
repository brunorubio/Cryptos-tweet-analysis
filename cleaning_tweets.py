import os
import csv
import datetime
from datetime import timedelta
 
today_string = (datetime.datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')

# Open/Create a file to append data
infile = open('cryptos_' + today_string + '.csv', 'r')

file_name = 'cryptos_cleaned_noRTs_' + today_string + '.csv'
cleaned_path = os.path.join(os.getcwd(), "files", "cleaned_noRTs", file_name)
outfile = open(cleaned_path, 'w+', newline='')


cryptos = (
			# Faster transactions
				'Ripple','$XRP','#XRP',
				'#XEM','$NEM','$XEM',
				'$Steem','#Steem',
				"Bitcoin Cash",'$BCH','#BCH','#Bcash',
				'Litecoin','#LTC','$LTC',
				'$Dash','#Dash',
				'Bitshares','$BTS',
				'IOTA','MIOTA',
				'#Stellar','#XLM','$XLM',
				# Smart Contracts
				'#ARK','$ARK',
				'Cardano','#ADA','$ADA',
				'#Chainlink','$LINK',
				'$EOS','#EOS',
				'Ethereum','$ETH','#ETH',
				"Ethereum Classic",'$ETC','#ETC',
				'#NEO','$NEO',
				'Qtum',
				# Privacy
				'#Verge','#XVG','$XVG', 
				'Bytecoin','$BCN','#BCN', 
				'#Komodo','#KMD','$KMD', 
				'MaidSafeCoin','#MAID','$MAID', 
				'Monero','#XMR','$XMR',
				'PIVX', 
				'Zcoin','$XZC','#XZC',
				'Zcash','#ZEC','$ZEC'
			)

tweets = set()

for line in infile:
	lsts = line.split("\n")
	for item in lsts:
		j = 0
		for coins in cryptos:
			
			# Removing retweets and tweets that don't cointain cryptos
			if coins not in item or 'RT @' in item:
				pass
			else:
				# This prevents addition of repeated tweets
				j += 1
				if j > 1:
					pass
				else:
					print(item)
					tweets.add(item)
infile.close()

# Writing final list of tweets to a file
for tweet in tweets:
	outfile.write(tweet + '\n')
