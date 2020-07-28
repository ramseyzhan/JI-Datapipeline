import sys 
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL

import joblib
import keras
import sklearn

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	n_vars = 1 if type(data) is list else data.shape[1]
	dff = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(dff.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(dff.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

def predicPowerUsage(model_path,data_path):

	Power_model_clstm = keras.models.load_model(model_path+"Power_model_clstm")
	Power_model_traditional = keras.models.load_model(model_path+"Power_model_traditional")
	Power_FCL = keras.models.load_model(model_path+"Power_FCL")


	df = pd.read_csv(data_path+'household_power_consumption.csv', sep=',', parse_dates={'time' : ['dt']},
	                 infer_datetime_format=True, low_memory=False, na_values=['nan','?'], index_col='time')

	values = df.values 
	scaler = joblib.load(model_path+'Powerscaler.gz')
	scaled = scaler.transform(values)
	reframed = series_to_supervised(scaled, 1, 1)
	reframed.drop(reframed.columns[[8,9,10,11,12,13]], axis=1, inplace=True)
	values = reframed.values
	n_train_time = 60*24

	train = values[:n_train_time, :]
	test_X, test_y = train[:, :-1], train[:, -1]
	test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
	test_X_t = test_X.reshape((test_X.shape[0], 7))


	yhat_FCL = Power_FCL.predict(test_X)

	inv_yhat_FCL = np.concatenate((yhat_FCL, test_X_t[:, -6:]), axis=1)
	inv_yhat_FCL = scaler.inverse_transform(inv_yhat_FCL)[:,0]

	yhat_traditional = Power_model_traditional.predict(test_X)
	inv_yhat_traditional = np.concatenate((yhat_traditional, test_X_t[:, -6:]), axis=1)
	inv_yhat_traditional = scaler.inverse_transform(inv_yhat_traditional)[:,0]



	test_X = test_X.reshape(test_X.shape[0],7,1)
	yhat_clstm = Power_model_clstm.predict(test_X)

	test_X = test_X.reshape((test_X.shape[0], 7))
	inv_yhat_clstm = np.concatenate((yhat_clstm, test_X[:, -6:]), axis=1)
	inv_yhat_clstm = scaler.inverse_transform(inv_yhat_clstm)[:,0]

	test_y = test_y.reshape((len(test_y), 1))
	inv_y = np.concatenate((test_y, test_X[:, -6:]), axis=1)
	inv_y = scaler.inverse_transform(inv_y)[:,0]

	return [df.index[30*24:],inv_y[30*24:],inv_yhat_clstm[30*24:],inv_yhat_traditional[30*24:],inv_yhat_FCL[30*24:]]

