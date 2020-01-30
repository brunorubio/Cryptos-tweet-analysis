import os
import csv
import pickle
import pandas as pd
import warnings
from pprint import pprint
from pandas import datetime
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error


crypto_groups = {	
					"Faster transactions": "fastert",
					"Smart Contracts": "sc",
					"Privacy": "privacy"
				}

# load dataset
base_dir = "C:\\Users\\Bruno Rubio\\Dropbox\\UTA\\Thesis\\data\\processing\\model"

# Process the entire thing for each crypto group
for i, j in crypto_groups.items():	

	file_name = os.path.join(base_dir, 'time_series', 'themes', 'TS_themes_' + j + '.pkl')

	df = pd.read_pickle(file_name)
	df.date = pd.to_datetime(df.date)

	df_theme = df.drop_duplicates(['theme_id'])[['theme_id']]

	arima_param = []

	for row in df_theme.itertuples(index=True, name='Pandas'):

		# evaluate an ARIMA model for a given order (p,d,q)
		def evaluate_arima_model(X, arima_order):
			# prepare training dataset
			train_size = int(len(X) * 0.66)
			train, test = X[0:train_size], X[train_size:]
			history = [x for x in train]
			# make predictions
			predictions = list()
			for t in range(len(test)):
				# fit model
				model = ARIMA(history, order=arima_order)
				model_fit = model.fit(disp=0)
				# one step forecast
				yhat = model_fit.forecast()[0]
				# store forecast and ob
				predictions.append(yhat)
				history.append(test[t])
			# calculate out of sample error
			error = mean_squared_error(test, predictions)
			return error

		idt = getattr(row, "theme_id")
		
		# evaluate combinations of p, d and q values for an ARIMA model
		def evaluate_models(dataset, p_values, d_values, q_values):
			dataset = dataset.astype('float32')
			best_score, best_cfg = float("inf"), None
			for p in p_values:
				for d in d_values:
					for q in q_values:
						order = (p,d,q)
						try:
							mse = evaluate_arima_model(dataset, order)
							if mse < best_score and order != (0, 0, 0):
								best_score, best_cfg = mse, order
							print('ARIMA%s MSE=%.6f' % (order,mse))
						except:
							continue
			arima_param.append((idt, best_cfg, best_score))				
			print('Best ARIMA%s MSE=%.6f' % (best_cfg, best_score))

		series = df.loc[df.theme_id == idt, 'average_weight']

		# evaluate parameters
		p_values = [0, 1, 2, 4, 6, 8, 10]
		d_values = range(0, 3)
		q_values = range(0, 3)
		warnings.filterwarnings("ignore")
		evaluate_models(series.values, p_values, d_values, q_values)

	pickle.dump(arima_param, open('Best_ARIMA_parameters_per_theme_' + j + '.pkl', 'wb'))
	pprint(arima_param)
