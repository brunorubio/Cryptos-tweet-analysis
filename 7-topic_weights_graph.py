import pickle

crypto_groups = {	
					"Faster transactions": ["fastert","slateblue"],
					"Smart Contracts": ["sc","gold"],
					"Privacy": ["privacy","darkred"]
				}

# Process the entire thing for each crypto group
for i, j in crypto_groups.items():

	# Import word weights obtained from MALLET processing
	import os
	filename = j[0] + 'wordweight.txt'
	file_path = os.path.join(os.getcwd(), filename)
	infile = open(file_path, 'r')

	# Read big file
	topic_word = []
	for line in infile:
		lsts = line.split("\n")
		for block in lsts:
			item = block.split('\t')
			if block == '':
				pass
			else:
				info = (int(item[0])+1, item[1], float(item[2]))
				topic_word.append(info) 
				
	# Add empty line just to stop the procedure
	topic_word.append((19, '', 0))

	# Calculate sum of weights for all words in every topic
	weight = 0
	id = 1
	topic_max_weight = []
	for topic in sorted(topic_word, key=lambda x: x[0]):
		if id == topic[0]:
			weight += topic[2]
		else:
			topic_max_weight.append((id, weight))
			weight = 0
			weight += topic[2]
			id += 1
			

	# Normalize the weights for for all words in every topic		
	topic_word_normalized = []
	for topics in topic_word:
		for id in topic_max_weight:
			if topics[0] == id[0]:
				norm = round(topics[2]/id[1], 6)
				topic_word_normalized.append((topics[0], topics[1], norm))
			else:
				pass

	#print(topic_word_normalized[:10])

	# Selecting final topics
	print(sorted(topic_word_normalized, key=lambda x: (x[0], -x[2]))[:10])

	topic_word_final = []
	for k in range(1, 19):
		count = 0
		for item in sorted(topic_word_normalized, key=lambda x: (x[0], -x[2])):
			if item[0] == k and count < 7:
				count += 1
				topic_word_final.append(item)
			else:
				pass
				
	pprint(topic_word_final)
	pickle.dump(topic_word_final, open('wordtopics_' + j[0] + '.pkl', 'wb'))

	# Plot graph for all topics
	import matplotlib.pyplot as plt
	import numpy as np

	plt.rcdefaults()
	fig = plt.figure()
	st = fig.suptitle('Topics for ' + i, fontsize=36)

	for k in range(1, 19):
		ax = fig.add_subplot(3, 6, k)
		values = []
		for item in topic_word_final:
			if item[0] == k:
				values.append((item[1], item[2]))
			else:
				pass
		y_val = [x[0] for x in values]
		x_val = [x[1] for x in values]
		y_pos = np.arange(len(y_val))
				
		ax.barh(y_pos, x_val, color=j[1])
		ax.set_yticks(y_pos)
		ax.set_yticklabels(y_val, fontsize=14)
		ax.invert_yaxis()  # labels read top-to-bottom
		ax.set_title(k, fontsize=16)
		
	plt.show()
	fig.savefig('topics_' + j[0] + '.png')
	plt.close(fig)			
	
			


			

				
