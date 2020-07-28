import sys
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL

import joblib
import keras


def predicIBM(model_path, data_path):
    regressor_clstm = keras.models.load_model(model_path + "IBM_model_clstm")
    sc = joblib.load(model_path + 'IBMscaler.gz')
    regressor = keras.models.load_model(model_path + "IBM_model_traditional")

    dataset = pd.read_csv(data_path + 'datasets_8388_11883_IBM_2006-01-01_to_2018-01-01.csv', index_col='Date',
                          parse_dates=['Date'])

    test_set = dataset['2017':].iloc[:, 1:2].values

    dataset_total = pd.concat((dataset["High"][:'2016'], dataset["High"]['2017':]), axis=0)

    inputs = dataset_total[len(dataset_total) - len(test_set) - 60:].values
    dates = dataset_total[len(dataset_total) - len(test_set):].index

    inputs = inputs.reshape(-1, 1)
    inputs = sc.transform(inputs)

    X_test = []
    for i in range(60, 311):
        X_test.append(inputs[i - 60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    predicted_stock_price_clstm = regressor_clstm.predict(X_test)
    predicted_stock_price_clstm = sc.inverse_transform(predicted_stock_price_clstm)

    X_test = []
    for i in range(60, 311):
        X_test.append(inputs[i - 60:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_stock_price = regressor.predict(X_test)
    predicted_stock_price = sc.inverse_transform(predicted_stock_price)

    test_set = test_set.reshape(len(test_set));
    predicted_stock_price_clstm = predicted_stock_price_clstm.reshape([len(predicted_stock_price_clstm), ]);
    predicted_stock_price = predicted_stock_price.reshape([len(predicted_stock_price), ]);

    return [dates, test_set, predicted_stock_price_clstm, predicted_stock_price]
