#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 18:27:15 2018

@author: jennifernghinguyen
"""

import helper

colors_file = '../dataset/color_names_rgb_output.csv'
data = helper.read_csv(colors_file)

id_file = '../dataset/color_names_id.csv'
data_id = helper.read_csv(id_file)

colors_numerical = data

def get_color_id(row):
    return data_id.loc[data_id['Name']==row[0], 'id'].item()

colors_numerical['hex_color'] = colors_numerical.apply(lambda row:  helper.hex_to_decimal(row), axis =1)

colors_numerical['id'] = colors_numerical.apply(lambda row:  get_color_id(row), axis =1)

X = colors_numerical.drop(['Name', 'Hex (24 bit)', 'Red (8 bit)', 'Green (8 bit)', 'Blue (8 bit)', 'id'], axis =1)
X = X.values.reshape(len(X),1)


Y = colors_numerical['id'] # label represent for the string
Y = Y.values.reshape(len(Y),1)



X_train, X_test, y_train, y_test = helper.train_test_split(X, Y, test_size=0.20) 

#### random forest
rdf_train_result, rdf_test_result = helper.random_forest_training(X_train, X_test, y_train, y_test)

#train results df
df_train_rf =  helper.pd.DataFrame(rdf_train_result)
df_train_rf['Actual_hex_of_X'] = df_train_rf.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_train_rf['Predicted_Name'] = df_train_rf.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_rf['Predicted_hex_of_Name'] = df_train_rf.apply(lambda row:  helper.get_hex_color_from_name(row, data), axis =1)

#test results df
df_test_rf =  helper.pd.DataFrame(rdf_test_result)
df_test_rf['Actual_hex_of_X'] = df_test_rf.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_test_rf['Predicted_Name'] = df_test_rf.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_rf['Predicted_hex_of_Name'] = df_test_rf.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)



#### k-mean classifier
k_train_result, k_test_result =  helper.k_mean_classifier(X_train, X_test, y_train, y_test)

#train results df
df_train_k =  helper.pd.DataFrame(k_train_result)
df_train_k['Actual_hex_of_X'] = df_train_k.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_train_k['Predicted_Name'] = df_train_k.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_k['Predicted_hex_of_Name'] = df_train_k.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

#test results df
df_test_k =  helper.pd.DataFrame(rdf_test_result)
df_test_k['Actual_hex_of_X'] = df_test_k.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_test_k['Predicted_Name'] = df_test_k.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_k['Predicted_hex_of_Name'] = df_test_k.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)


####ada Boosting classifier

ada_boosting_train_result, ada_boosting_test_result =  helper.adaboosting_classifier(X_train, X_test, y_train, y_test)

#train results df
df_train_ada_boosting =  helper.pd.DataFrame(ada_boosting_train_result)
df_train_ada_boosting['Actual_hex_of_X'] = df_train_ada_boosting.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_train_ada_boosting['Predicted_Name'] = df_train_ada_boosting.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_train_ada_boosting['Predicted_hex_of_Name'] = df_train_ada_boosting.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

#test results df
df_test_ada_boosting =  helper.pd.DataFrame(ada_boosting_test_result)
df_test_ada_boosting['Actual_hex_of_X'] = df_test_ada_boosting.apply(lambda row:  helper.find_color_hex(row), axis =1)
df_test_ada_boosting['Predicted_Name'] = df_test_ada_boosting.apply(lambda row:  helper.get_color_name(row,data), axis =1)
df_test_ada_boosting['Predicted_hex_of_Name'] = df_test_ada_boosting.apply(lambda row:  helper.get_hex_color_from_name(row,data), axis =1)

