# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.models.wrappers import LdaMallet 

# Plotting tools
import matplotlib.pyplot as plt

# Load and Save objects and models
import os
import csv
import pickle

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# spacy for lemmatization
import spacy

import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

crypto_groups = {	
					"Faster transactions": "fastert",
					"Smart Contracts": "sc",
					"Privacy": "privacy"
				}

lines_cv = []
lines_um = []

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

scores = []		

# Process everything for each crypto group
for i, j in crypto_groups.items():
		

	# Loading dictionary, corpus and text data
	dict_name = "tweet-dict-" + j + ".dict"
	texts_name = "tweet-texts-" + j + ".pkl"
	corpus_name = "tweet-corpus-" + j + ".pkl"
	
	loaded_dict = os.path.join("D:\\UTA\\Thesis\\data\\processing\\dictionary_corpus", dict_name)
	loaded_texts = os.path.join("D:\\UTA\\Thesis\\data\\processing\\dictionary_corpus", texts_name)
	loaded_corpus = os.path.join("D:\\UTA\\Thesis\\data\\processing\\dictionary_corpus", corpus_name)

	id2word = corpora.Dictionary.load(loaded_dict)
	texts = pickle.load(open(loaded_texts, 'rb'))
	corpus = pickle.load(open(loaded_corpus, 'rb'))
	
	print(i)
	
	if __name__ ==  '__main__':
		
		def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3):
			"""
			Compute c_v coherence for various number of topics

			Parameters:
			----------
			dictionary : Gensim dictionary
			corpus : Gensim corpus
			texts : List of input texts
			limit : Max num of topics

			Returns:
			-------
			model_list : List of LDA topic models
			coherence_values : Coherence values corresponding to the LDA model with respective number of topics
			"""
			coherence_values = []
			model_list = []
			log_likelihood = []
			u_mass = []
			perplexity = []
			os.environ.update({'MALLET_HOME': r'c:/mallet-2.0.8/'})
			mallet_path = "c:/mallet-2.0.8/bin/mallet"
			for num_topics in range(start, limit, step):
				model = gensim.models.wrappers.LdaMallet(mallet_path, corpus=corpus, num_topics=num_topics, id2word=id2word)
				model_list.append(model)
				# Compute Coherence Score using c_v
				coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
				coherence_values.append(coherencemodel.get_coherence())
				# Compute Coherence Score using UMass
				coherencemodel2 = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='u_mass')
				u_mass.append(coherencemodel2.get_coherence())
			return model_list, coherence_values, u_mass
		
		# Can take a long time to run.
		model_list, coherence_values, u_mass = compute_coherence_values(dictionary=id2word, corpus=corpus, texts=texts, start=2, limit=40, step=4)

		# Save list objects
		pickle.dump(model_list, open('model_list_' + j + '.pkl', 'wb'))
		
		# Show graph
		limit=40; start=2; step=4;
		x = range(start, limit, step)
		
		font = {
				'color':  'black',
				'weight': 'normal',
				'size': 12,
				}
		
		lines_cv += ax1.plot(x, coherence_values, label=i)
		lines_um += ax2.plot(x, u_mass, label=i)
		
		# Print all the scores
		print(i)
		for m, cv in zip(x, coherence_values):
			print("Num Topics =", m, " has Coherence Value of", round(cv, 4))
			info = (i, m, 'Coherence c_v', round(cv,4))
			scores.append(info)
		for m, um in zip(x, u_mass):
			print("Num Topics =", m, " has UMass of", round(um, 4))
			info = (i, m, 'Coherence u_m', round(um,4))
			scores.append(info)			
						

labels = [l.get_label() for l in lines_cv]
ax1.set_title('Optimal number of topics according to Coherence Scores - c_v')
ax1.set_xlabel("Num Topics")
ax1.set_ylabel("Coherence Score - c_v")
ax1.legend(lines_cv, labels)
fig1.savefig('optimal_model_cv.png')
plt.close(fig1)

labels = [l.get_label() for l in lines_um]
ax2.set_title('Optimal number of topics according to Coherence Scores - UMass')
ax2.set_xlabel("Num Topics")
ax2.set_ylabel("Coherence Score - u_mass")
ax2.legend(lines_cv, labels)
fig2.savefig('optimal_model_um.png')
plt.close(fig2)

# Save computed scores
outfile = open('all_scores.csv', 'w+', newline='') 
csvWriter = csv.writer(outfile)
for info in scores:
	csvWriter.writerow(info)
	
