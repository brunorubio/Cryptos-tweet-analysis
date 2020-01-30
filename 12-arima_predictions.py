import os
import csv
import pickle
import pandas as pd
import warnings
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

crypto_groups = {						
					"Faster transactions": "fastert",
					"Smart Contracts": "sc",
					"Privacy": "privacy"
				}

# load dataset
base_dir = "D:\\UTA\\Thesis\\data\\processing\\model"

# Process the entire thing for each crypto group
for i, j in crypto_groups.items():	

	# Parameters file
	parameters_name = os.path.join(os.getcwd(), 'Best_ARIMA_parameters_per_theme_' + j + '.pkl')

	arima_param = pickle.load(open(parameters_name, 'rb'))

	# Weights file
	file_name = os.path.join(base_dir, 'time_series', 'themes', 'TS_themes_' + j + '.pkl')

	df = pd.read_pickle(file_name)

	df.date = pd.to_datetime(df.date)

	df_theme = df.drop_duplicates(['theme_id','theme'])[['theme_id','theme']]
	
	all_info = []

	for row in df_theme.itertuples(index=True, name='Pandas'):
		idt = getattr(row, "theme_id")
		series = df.loc[df.theme_id == idt, 'average_weight']
		theme = df_theme.iloc[idt-1][1]
		params = arima_param[int(idt)-1][1]
		print(i, idt, theme, params)
		X = series.values
		size = int(len(X) * 0.66)
		train, test = X[0:size], X[size:len(X)]
		history = [x for x in train]
		predictions = list()
		for t in range(len(test)):
			model = ARIMA(history, order=params)
			try:
				model_fit = model.fit(disp=0)
				output = model_fit.forecast()
				yhat = output[0]
				predictions.append(yhat)
			except:
				print("error:", idt, t)
				print(test)
				predictions.append(test[t])
			obs = test[t]
			history.append(obs)
		error = mean_squared_error(test, predictions)
		print('Test MSE: %.6f' % error)
		all_info.append((idt, theme, train, test, predictions))

	pickle.dump(all_info, open('arima_prediction_values_' + j + '.pkl', 'wb'))
		
	# Plot
	plt.rcdefaults()
	fig = plt.figure()
		
	for k in range(1, len(df_theme)+1):
		if i == "Privacy":
			ax = fig.add_subplot(5, 2, k)
		else:
			ax = fig.add_subplot(4, 2, k)
		values = []
		for item in all_info:
			if item[0] == k:
				values.append((item[2], item[3], item[4]))
			else:
				pass
		train = [x[0] for x in values] 		
		test = [x[1] for x in values]
		predictions = [x[2] for x in values]
		theme = df_theme.iloc[k-1][1]
	
		ax.plot(train[0])
		ax.plot([None for i in train[0]] + [x for x in test[0]], color='black')
		ax.plot([None for i in train[0]] + [x for x in predictions[0]], color='red')
		ax.set_title(theme, fontsize=16)
		ax.legend(('train set','expected (test set)', 'predicted'), loc='upper left', shadow=True)
		
	plt.show()
	plt.close(fig)
		
			
