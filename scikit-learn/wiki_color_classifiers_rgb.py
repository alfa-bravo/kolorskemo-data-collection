#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:34:17 2018

@author: jennifernghinguyen
"""

import helper

colors_file = '../dataset/color_names_rgb_output.csv'
data = helper.read_csv(colors_file)

id_file = '../dataset/color_names_id.csv'
data_id = helper.read_csv(id_file)
colors_numerical = data

colors_numerical['id'] = colors_numerical.apply(lambda row:  helper.get_color_id(row), axis =1)

X = colors_numerical.drop(['Name', 'Hex (24 bit)','id'], axis =1)
X = X.values.reshape(len(X),3)


Y = colors_numerical['id'] # label represent for the string
Y = Y.values.reshape(len(Y),1)


X_train, X_test, y_train, y_test = helper.train_test_split(X, Y, test_size=0.20) 



#### random forest
rdf_train_result, rdf_test_result = helper.random_forest_training(X_train, X_test, y_train, y_test)





#### k-mean classifier
k_train_result, k_test_result =  helper.k_mean_classifier(X_train, X_test, y_train, y_test)



####ada Boosting classifier

ada_boosting_train_result, ada_boosting_test_result =  helper.adaboosting_classifier(X_train, X_test, y_train, y_test)

