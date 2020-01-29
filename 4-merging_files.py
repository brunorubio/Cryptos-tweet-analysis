import os
import csv
import datetime
from datetime import timedelta

# Writing csv files
outfile = open('cryptos_alltweets_with_time.csv', 'w+', newline='')
csvWriter = csv.writer(outfile)

# Define range according to first and last date of files 
for d in range(2, 122):
	
	# Merge all files from May to August 
	months = ['08','07','06','05']
	
	today_string = (datetime.datetime.today() - timedelta(days=d)).strftime('%Y-%m-%d')
	month_string = (datetime.datetime.today() - timedelta(days=d)).strftime('%m')
	
	if month_string not in months:
		pass
	else:
		# Reading text files
		infile = open('cryptos_validtweets_with_time_' + today_string + '.csv', 'r')
		infile2 = open('crypto_groups.csv', 'r', encoding="utf8")

		# List of the crypto groups
		groups = []
		for line in infile2:
			lsts = line.split("\n")
			for block in lsts:
				item = block.split(',')
				if block == '':
					pass
				else:
					info = (item[0].lower(), item[1], item[2])
					groups.append(info)
		infile2.close()	

		# Reading file for one day and adding info of the crypto group
		tweets = set()
		for line in infile:
			lsts = line.split("\n")
			for block in lsts:
				item = block.split(',', maxsplit=1)
				if block == '':
					pass
				else:
					for coin in groups:
						if coin[0] not in item[1]:
							pass
						else:
							info = (item[0], coin[1], coin[2], item[1])
							tweets.add(info)
		
		for i in tweets:
			csvWriter.writerow(i)

		print(today_string, len(tweets))
