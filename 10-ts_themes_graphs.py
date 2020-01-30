import pandas as pd 
import os
import csv
import pickle

# Graphs
import seaborn as sns
import matplotlib.pyplot as plt

base_dir = "C:\\Users\\Bruno Rubio\\Dropbox\\UTA\\Thesis\\data\\processing\\model"

crypto_groups = {	
					"Privacy": ["privacy","RdGy"],
					"Faster transactions": ["fastert", "PRGn"],
					"Smart Contracts": ["sc","PuOr"]
				}

colors = ["#000000", "#ff0000", "#cccc00", "#3333ff", "#ff007f", "#009999", "#ff6666", "#9999ff", "#006400", "#800080"]

# Process everything for each crypto group
for i, j in crypto_groups.items():	
	def compile_dataframe(themes, weights):
		"""
		Combines a series of dataframes to create a large composit dataframe.
		"""
		df = weights.merge(themes, on="topic_id", how="left")
		
		return df

	themes_filename = os.path.join(os.getcwd(), 'themes_' + j[0] + '.csv')
	weights_filename = os.path.join(base_dir, 'time_series', 'topicweight' + j[0] + '.csv')

	themes = pd.read_csv(themes_filename, usecols=['topic_id', 'theme_id', 'theme'])
	weights = pd.read_csv(weights_filename, usecols=['doc_id', 'topic_id','date', 'topic_weight'])

	df = compile_dataframe(themes, weights)
	
	

	# Get dataframe with weights by theme
	df_theme = df.groupby(['doc_id', 'date', 'theme_id', 'theme']).agg({'topic_weight': 'sum'}).reset_index()
	
	# Get just theme and description
	df_theme_table = df.drop_duplicates(['theme_id', 'theme'])[['theme_id', 'theme']]
	
	print(df_theme_table)

	# Get number of docs per day
	total_docs = df_theme.groupby('date')['doc_id'].apply(lambda x: len(x.unique())).reset_index()
	total_docs.columns = ['date', 'total_docs']

	# Group by day and topic id
	df_avg = df_theme.groupby(['date', 'theme_id']).agg({'topic_weight': 'sum'}).reset_index()

	# Merge dataframes
	df_avg = df_avg.merge(total_docs, on="date", how="left")

	# Compute the mean per topic
	df_avg['average_weight'] = df_avg['topic_weight'] / df_avg['total_docs']
	
	# Merge the dataframes
	df_avg = df_avg.merge(df_theme_table, on='theme_id')
	
	print(df_avg[:20])
	
	df_avg.to_pickle('TS_themes_' + j[0] + '.pkl')
	

	# Theme Average Graph
	def create_pointplot(df, y_value, hue=None, col=None, wrap=None, height=5, aspect=1.5, title=""):	
		p = sns.catplot(x="date", y=y_value, kind='point', hue=hue, col=col, col_wrap=wrap,
							height=height, aspect=aspect, data=df, palette=colors, legend=False )
		p.fig.subplots_adjust(top=0.9)
		p.fig.suptitle(title, fontsize=14)
		plt.setp(p.ax.lines,linewidth=1)
		plt.yticks(fontsize=6)
		plt.xticks(fontsize=5,rotation=90)
		plt.legend(loc='upper right', fontsize=16)
		return p

	create_pointplot(df_avg, 'average_weight', hue="theme",
					title="Daily Average of Weights per Theme from May/18 to Aug/18 - " + i)
					
	# See graph result and save manually 				
	plt.show()
	plt.close()
