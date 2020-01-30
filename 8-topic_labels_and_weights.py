import os
import csv
import pickle

crypto_groups = {	
					"Faster transactions": "fastert",
					"Smart Contracts": "sc",
					"Privacy": "privacy"
				}
				
# Process everything for each crypto group
for i, j in crypto_groups.items():				

	# Create topic labels file
	load_wordtopics = 'wordtopics_' + j + '.pkl'
	wordtopics = pickle.load(open(load_wordtopics, 'rb'))

	topic_labels = []
	for topic_num in range(1, 19):
		label = str()
		k = 1
		for line in wordtopics:
			if k > 7:
				k = 1
			if line[0] == topic_num and k < 7:
				label += line[1] + ', '
			elif line[0] == topic_num and k == 7:
				label += line[1]
			else:
				pass
			k += 1	
		info = (topic_num, label)
		topic_labels.append(info)
	
	outfile = open('topiclabels' + j + '.csv', 'w+', newline='')
	fieldnames = ['topic_id', 'topic_words'] 
	csvWriter = csv.writer(outfile)
	csvWriter.writerow(fieldnames)
	for info in topic_labels:
		csvWriter.writerow(info)
	outfile.close()

	# Create file with topic weights
	infile = open(j + 'composition.csv', 'r', encoding="utf8")
	topic_weights = []
	for line in infile:
		lsts = line.split("\n")
		for block in lsts:
			item = block.split(';')
			#print(item)
			if block == '':
				pass
			else:
				topic_weights.append(item) 	

	
	topic_weights_final = []
	for w in range(0, len(topic_weights)):
		for z in range(0, len(topic_weights[w][2:])):
			info = (int(topic_weights[w][0]), z+1, topic_weights[w][1], float(topic_weights[w][z+2]))
			topic_weights_final.append(info)
		
	# Save topic weights
	outfile = open('topicweight' + j + '.csv', 'w+', newline='')
	fieldnames = ['doc_id', 'topic_id', 'date', 'topic_weight'] 
	csvWriter = csv.writer(outfile)
	csvWriter.writerow(fieldnames)
	for info in topic_weights_final:
		csvWriter.writerow(info)
