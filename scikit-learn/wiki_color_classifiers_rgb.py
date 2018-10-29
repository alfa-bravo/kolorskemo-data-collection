#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:34:17 2018

@author: jennifernghinguyen
"""

import helper

filename = '../dataset/wikipedia_color_names.csv'
data = helper.read_csv(filename)



colors_numerical = data.drop(['Hue (degrees)', 'HSL.S (%)', 'HSL.L (%), HSV.S (%), HSV.V (%)'], axis =1)
colors_numerical['name_numerical_label'] = data.index

X = colors_numerical.drop(['Name', 'Hex (24 bit)','name_numerical_label'], axis =1)
X = X.values.reshape(len(X),3)

Y = colors_numerical['name_numerical_label'] # label represent for the string
Y = Y.values.reshape(len(Y),1)


X_train, X_test, y_train, y_test = helper.train_test_split(X, Y, test_size=0.20) 



#### random forest
rdf_train_result, rdf_test_result = helper.random_forest_training(X_train, X_test, y_train, y_test)


#train results df
df_train_rf =  helper.pd.DataFrame(rdf_train_result)
df_train_rf['Predicted_Name'] = df_train_rf.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_rf['Predicted_hex_of_Name'] = df_train_rf.apply(lambda row:  helper.get_hex_color_from_name(row, data), axis =1)

#test results df
df_test_rf =  helper.pd.DataFrame(rdf_test_result)
df_test_rf['Predicted_Name'] = df_test_rf.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_rf['Predicted_hex_of_Name'] = df_test_rf.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)




#### k-mean classifier
k_train_result, k_test_result =  helper.k_mean_classifier(X_train, X_test, y_train, y_test)

#train results df
df_train_k =  helper.pd.DataFrame(k_train_result)
df_train_k['Predicted_Name'] = df_train_k.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_k['Predicted_hex_of_Name'] = df_train_k.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

#test results df
df_test_k =  helper.pd.DataFrame(rdf_test_result)
df_test_k['Predicted_Name'] = df_test_k.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_k['Predicted_hex_of_Name'] = df_test_k.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)




####ada Boosting classifier

ada_boosting_train_result, ada_boosting_test_result =  helper.adaboosting_classifier(X_train, X_test, y_train, y_test)

#train results df
df_train_ada_boosting =  helper.pd.DataFrame(ada_boosting_train_result)
df_train_ada_boosting['Predicted_Name'] = df_train_ada_boosting.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_ada_boosting['Predicted_hex_of_Name'] = df_train_ada_boosting.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

#test results df
df_test_ada_boosting =  helper.pd.DataFrame(ada_boosting_test_result)
df_test_ada_boosting['Predicted_Name'] = df_test_ada_boosting.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_ada_boosting['Predicted_hex_of_Name'] = df_test_ada_boosting.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

