#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 21:34:56 2018

@author: jennifernghinguyen
"""

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd
"""
helpers 
"""
def hex_to_decimal(row):
    return int(row['Hex (24 bit)'].replace("#",""), 16)

def get_color_name(row, data):
    return data['Name'][row[1]]
   
def find_color_hex(row):
    return hex(row[0])
  
def get_hex_color_from_name(row, data):
    return data['Hex (24 bit)'][row[1]]


def random_forest_training(X_train, X_test, y_train, y_test):
    """
    random forest classifier
    :param X_train: ﻿numpy.ndarray
    :param X_test: ﻿numpy.ndarray
    :param y_train:﻿ numpy.ndarray
    :param y_test:﻿ numpy.ndarray
    :return: train_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
             test_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
    """
    rnd_clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=2, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=500, n_jobs=-1,
            oob_score=False, random_state=0, verbose=0, warm_start=False)
    
    rnd_clf.fit(X_train, y_train.ravel())
    y_pred_rf = rnd_clf.predict(X_test)
    y_pred_rf= y_pred_rf.reshape(len(y_pred_rf),1)
    
    test_result = np.concatenate((X_test, y_pred_rf),axis =1)
    

    y_pred_rf_train = rnd_clf.predict(X_train)
    y_pred_rf_train = y_pred_rf_train.reshape(len(y_pred_rf_train),1)
    
    train_result = np.concatenate((X_train, y_pred_rf_train),axis =1)
    
    print("accuracy_score random forest  on test set")
    print(accuracy_score(y_test, y_pred_rf))

    print("accuracy_score random forest  on train set")
    print(accuracy_score(y_train, y_pred_rf_train))
    return train_result, test_result



def k_mean_classifier(X_train, X_test, y_train, y_test):
    """
       k mean classifier
       :param X_train: ﻿numpy.ndarray
       :param X_test: ﻿numpy.ndarray
       :param y_train:﻿ numpy.ndarray
       :param y_test:﻿ numpy.ndarray
       :return: train_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
                test_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
       """
    k_mean = KNeighborsClassifier(n_neighbors=2, n_jobs=-1)
    k_mean.fit(X_train, y_train.ravel())

    y_pred_k = k_mean.predict(X_test)
    y_pred_k= y_pred_k.reshape(len(y_pred_k),1)
    
    test_result = np.concatenate((X_test, y_pred_k),axis =1)
    

    y_pred_k_train = k_mean.predict(X_train)
    y_pred_k_train = y_pred_k_train.reshape(len(y_pred_k_train),1)
    
    train_result = np.concatenate((X_train, y_pred_k_train),axis =1)
    
    print("accuracy_score k mean  on test set")
    print(accuracy_score(y_test, y_pred_k))

    print("accuracy_score k mean  on train set")
    print(accuracy_score(y_train, y_pred_k_train))
    return train_result, test_result 



def gradient_boosting_classifier(X_train, X_test, y_train, y_test):
    """
       gradient boosting classifier
       :param X_train: ﻿numpy.ndarray
       :param X_test: ﻿numpy.ndarray
       :param y_train:﻿ numpy.ndarray
       :param y_test:﻿ numpy.ndarray
       :return: train_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
                test_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
       """
    g_boost = GradientBoostingClassifier(loss='deviance', learning_rate=0.1, 
                                        n_estimators=100, subsample=1.0,
                                        criterion='friedman_mse', min_samples_split=2, 
                                        min_samples_leaf=1, min_weight_fraction_leaf=0.0, 
                                        max_depth=3, min_impurity_decrease=0.0, 
                                        min_impurity_split=None, init=None, 
                                        random_state=None, max_features=None, 
                                        verbose=0, max_leaf_nodes=None, 
                                        warm_start=False, presort='auto', 
                                       )
    g_boost.fit(X_train, y_train.ravel())

    y_pred_k = g_boost.predict(X_test)
    y_pred_k= y_pred_k.reshape(len(y_pred_k),1)
    
    test_result = np.concatenate((X_test, y_pred_k),axis =1)
    

    y_pred_k_train = g_boost.predict(X_train)
    y_pred_k_train = y_pred_k_train.reshape(len(y_pred_k_train),1)
    
    train_result = np.concatenate((X_train, y_pred_k_train),axis =1)
    
    print("accuracy_score gradient boosting  on test set")
    print(accuracy_score(y_test, y_pred_k))

    print("accuracy_score gradient boosting  on train set")
    print(accuracy_score(y_train, y_pred_k_train))
    return train_result, test_result 


def adaboosting_classifier(X_train, X_test, y_train, y_test):
    """
       ada boosting classifier
       :param X_train: ﻿numpy.ndarray
       :param X_test: ﻿numpy.ndarray
       :param y_train:﻿ numpy.ndarray
       :param y_test:﻿ numpy.ndarray
       :return: train_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
                test_result: ﻿numpy.ndarray - 2 cols decimal and prediction color id
       """
    ada_clf = AdaBoostClassifier(
            DecisionTreeClassifier(max_depth=1), 
            n_estimators=200, algorithm="SAMME.R", 
            learning_rate=0.5, random_state=42)
    ada_clf.fit(X_train, y_train.ravel())

    y_pred_ada = ada_clf.predict(X_test)
    y_pred_ada= y_pred_ada.reshape(len(y_pred_ada),1)
    
    test_result = np.concatenate((X_test, y_pred_ada),axis =1)
    

    y_pred_ada_train = ada_clf.predict(X_train)
    y_pred_ada_train = y_pred_ada_train.reshape(len(y_pred_ada_train),1)
    
    train_result = np.concatenate((X_train, y_pred_ada_train),axis =1)
    
    print("accuracy_score ada boosting  on test set")
    print(accuracy_score(y_test, y_pred_ada))

    print("accuracy_score ada boosting  on train set")
    print(accuracy_score(y_train, y_pred_ada_train))
    return train_result, test_result 