import re
import os
import csv
import datetime
from datetime import timedelta
from difflib import SequenceMatcher as sm
 
today_string = (datetime.datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')

# Reading text files
input_text = 'cryptos_cleaned_noRTs_' + today_string + '.csv'
cleaned_path = os.path.join(os.getcwd(), "files", "cleaned_noRTs", input_text)
infile = open(cleaned_path, 'r')

bypasslist_path = os.path.join(os.getcwd(), "blacklist", "important_users.csv")
infile2 = open(bypasslist_path, 'r', encoding="utf8")

# Writing csv files
output_text = 'cryptos_validtweets_' + today_string + '.csv'
validtweets_path = os.path.join(os.getcwd(), "valid_tweets", output_text)
outfile2 = open(validtweets_path, 'w+', newline='')

#Use csv Writer
csvWriter2 = csv.writer(outfile2)


# First cleaning of tweets
info = ()
tweets = []
for line in infile:
	lsts = line.split("\n")
	for block in lsts:
		item = block.split(',', maxsplit=2)
		if block == '':
			pass
		else:
			# Remove distracting single and double quotes
			text = re.sub("\'|\"", '', item[2])
			# Remove URLs from tweets and the annoying 'b' at front 
			text = re.sub(r'http\S+','',text[1:])
			# Remove new line characters
			text = re.sub('\s+', ' ', text)
			# Remove remaining \n
			text = re.sub('\\n', '', text)
			# Create tuple with date, username and tweet text
			info = (item[0][:10], item[1], text)
			tweets.append(info)
infile.close()

# Reads users that can't be blacklisted
bypasslist = []
for line in infile2:
	lsts = line.split("\n")
	for users in lsts:
		if users == '':
			pass
		else:
			bypasslist.append(users)
infile2.close()		

# Add users to the blacklist
count = 0
prev_sm = 0
blacklist = set()
for i in sorted(tweets, key = lambda x: x[2]):
	count += 1
	date_text = ()
	if count == 1:
		# Just reads the first line and username
		line1 = i[2][:60]
		user1 = i[1]
	else:
		# Reads the line to be compared with the previous one
		line2 = i[2][:60]
		user2 = i[1]
		dif = sm(None, line1, line2)
		# Users which tweets are too similar are flagged
		if float(dif.ratio()) >= 0.75:
			# Only users not on bypass list are added
			if any(user in user1 for user in bypasslist):
				pass
			else:
				blacklist.add(user1)
			if any(user in user2 for user in bypasslist):
				pass
			else:
				blacklist.add(user2)
		line1 = line2
		user1 = user2
		prev_sm = float(dif.ratio())

# Creating a file for the blacklisted users
file_name3 = 'blacklist_' + today_string + '.csv'
blacklist_path = os.path.join(os.getcwd(), "blacklist", file_name3)	
outfile3 = open(blacklist_path, 'w+', newline='')
for username in sorted(blacklist):
	outfile3.write(username + '\n')	

# Final list of tweets, ignoring users flagged on blacklist
for i in tweets:
	if any(user in i[1] for user in blacklist):
		pass
	else:
		csvWriter2.writerow([i[0], i[2]])

print (today_string, len(blacklist))
