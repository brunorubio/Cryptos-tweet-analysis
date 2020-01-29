# Run in python console
import nltk; nltk.download('stopwords')

# Save list objects
import pickle

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

# Read terms that should be added to the stopwords list
stopwords_path = os.path.join(os.getcwd(), "stopwords", "crypto_terms.csv")
infile = open(stopwords_path, 'r', encoding="utf8")

crypto_terms = []
for line in infile:
	lsts = line.split("\n")
	for terms in lsts:
		if terms == '':
			pass
		else:
			crypto_terms.append(terms)
infile.close()

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(crypto_terms)

# Import Dataset
import os
alltweets_path = os.path.join(os.getcwd(), "processing", "cryptos_alltweets_with_time.csv")
infile2 = open(alltweets_path, 'r')


# For Output
output_path = "C:\\mallet-2.0.8\\mydata"

crypto_groups = {	
					"Privacy": "privacy",
					"Faster transactions": "fastert",
					"Smart Contracts": "sc"					
				}

# Read big file
alltweets = []
for line in infile:
	lsts = line.split("\n")
	for block in lsts:
		item = block.split(',', maxsplit=3)
		if block == '':
			pass
		else:
			info = (item[0], item[2], item[3])
			alltweets.append(info) 


# Process everything for each crypto group			
for name, abrev in crypto_groups.items():
	tweets = []
	for line in alltweets:
		if line[1] == str(name):
			tweets.append((line[0], line[2]))

	def sent_to_words(sentences):
		for sentence in sentences:
			yield((sentence[0], gensim.utils.simple_preprocess(str(sentence[1]), deacc=True)))  # deacc=True removes punctuations

	tweet_words = list(sent_to_words(tweets))


	# Define functions for stopwords and lemmatization
	stop_words_group = [] # Use of specific stopword list for each group
	def remove_stopwords(texts):
		aux = [[word for word in simple_preprocess(str(doc[1])) if word not in stop_words_group] for doc in texts]
		k = 0
		doc = []
		for lst in aux:
			 doc.append((texts[k][0], lst))
			 k += 1
		return doc
	
	def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
		texts_out = []
		for sent in texts:
			doc = nlp(" ".join(sent[1])) 
			texts_out.append((sent[0],[token.lemma_ for token in doc if token.pos_ in allowed_postags]))
		return texts_out
		
	# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
	# If needed: python3 -m spacy download en
	nlp = spacy.load('en', disable=['parser', 'ner'])

	# Do lemmatization keeping only noun, adj, vb, adv
	tweet_lemmatized = lemmatization(tweet_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
	
	# Counting words
	allwords = []			# all words
	uniquewords = set()		# unique words
	for pair in tweet_lemmatized:
		for word in pair[1]:
			allwords.append(word)
			uniquewords.add(word)
	wordcount = Counter(allwords)
	
	print('%s all words: %g' % (name, len(allwords)))
	print('%s unique words: %g' % (name, len(uniquewords)))
	

	# Mark words with low frequency = lower than the 50% of the mean of the total amount of words per total unique words
	lowfrequency = []
	for k, l in wordcount.items():
		if l < int(0.5 * (len(allwords) / len(uniquewords))):	
			lowfrequency.append(k)
	print('%s low frequency words: %g' % (name, len(lowfrequency)))

	# Add low frequency terms to the stopword list
	stop_words_group.extend(stop_words)
	stop_words_group.extend(lowfrequency)
	
	# Remove Stop Words
	tweet_words_nostops = remove_stopwords(tweet_lemmatized)
	texts = tweet_words_nostops

	# Create and save Dictionary
	output_dict_file = 'tweet-dict-' + abrev + '.dict'
	id2word = corpora.Dictionary(texts)
	id2word.save(output_dict_file)

	# Create Corpus
	pickle.dump(texts, open('tweet-texts-' + abrev + '.pkl', 'wb'))

	# Term Document Frequency
	output_corpus_file = 'tweet-corpus-' + abrev + '.pkl'
	corpus = [id2word.doc2bow(text) for text in texts]
	pickle.dump(corpus, open(output_corpus_file, 'wb'))
