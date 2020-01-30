import os
import csv
import pickle
import pandas as pd

crypto_groups = {	
					"Privacy": ["privacy","darkred"],
					"Faster transactions": ["fastert", "slateblue"],
					"Smart Contracts": ["sc","gold"]
				}

colors = 	[	"#A9F5F2","#FF8000","#D7DF01","#00FF00","#00FFBF","#00BFFF",
				"#0000FF","#BF00FF","#FF0080","#848484","#000000","#868A08",
				"#81DAF5","#F3E2A9","#086A87","#F5A9A9","#F7819F","#FF0000"
			]

# Process everything for each crypto group
for i, j in crypto_groups.items():	
	def compile_dataframe(labels, weights):
		# Combines a series of dataframes to create a large composit dataframe.
		df = weights.merge(labels, on="topic_id", how="left")
		
		return df

	labels_filename = os.path.join(os.getcwd(), 'topiclabels' + j[0] + '.csv')
	weights_filename = os.path.join(os.getcwd(), 'topicweight' + j[0] + '.csv')

	labels = pd.read_csv(labels_filename, usecols=['topic_id', 'topic_words'])
	weights = pd.read_csv(weights_filename, usecols=['doc_id', 'topic_id','date', 'topic_weight'])

	df = compile_dataframe(labels, weights)
	
	df['topic_id_words'] = df.topic_id.map(str) + " - " + df.topic_words

	# Graphs
	import seaborn as sns
	import matplotlib.pyplot as plt

	
	# Scatterplot of Topic Weights
	p = sns.FacetGrid(df, col='topic_id_words', col_wrap=2,
					   height=4, aspect=2)
	p.map(plt.scatter, "date", "topic_weight", color=j[1], alpha=0.1,s=10)
	p.fig.subplots_adjust(top=0.95, hspace=.5)
	p.fig.suptitle("Scatterplot of Daily Topic Weights by Topic from May/18 to Aug/18 - " + i, fontsize=8)
	plt.show()
	p.fig.savefig('weights_graph_transp_' + j[0] + '.png')
	plt.close(p.fig)


	# Get number of docs per day
	total_docs = df.groupby('date')['doc_id'].apply(lambda x: len(x.unique())).reset_index()
	total_docs.columns = ['date', 'total_docs']

	# Group by day and topic id
	df_avg = df.groupby(['date', 'topic_id']).agg({'topic_weight': 'sum'}).reset_index()

	# Merge dataframes
	df_avg = df_avg.merge(total_docs, on="date", how="left")

	# Compute the mean per topic
	df_avg['average_weight'] = df_avg['topic_weight'] / df_avg['total_docs']

	# Merge the dataframes
	df_avg = df_avg.merge(labels, on='topic_id')
	
	df_avg.to_pickle('TS_topics_avg_' + j[0] + '.pkl')
	
	df_avg['topic_id_words'] = df_avg.topic_id.map(str) + " - " + df_avg.topic_words
	
	# Topic Average Graph
	def create_pointplot(df, y_value, hue=None, col=None, wrap=None, height=5, aspect=1.5, title=""):
		p = sns.catplot(x="date", y=y_value, kind='point', hue=hue, col=col, col_wrap=wrap, 
							height=height, aspect=aspect, data=df, palette=colors, scale=0.5, legend=False )
		p.fig.subplots_adjust(top=0.9)
		p.fig.suptitle(title, fontsize=14)
		plt.setp(p.ax.lines,linewidth=1)
		plt.yticks(fontsize=6)
		plt.xticks(fontsize=5, rotation=90)
		plt.legend(loc='upper right', fontsize=6)
		return p

	create_pointplot(df_avg, 'average_weight', hue="topic_id_words",
					title="Daily Average of Weights per Topic from May/18 to Aug/18 - " + i)
	
	# See graph result and save manually 				
	plt.show()
	plt.close()
