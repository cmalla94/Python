#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2
from sklearn.decomposition import PCA
import sys


# In[2]:



def main():
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output = sys.argv[3]
    train = pd.read_csv(file1)
    test = pd.read_csv(file2).drop(['city', 'year'], axis=1)
    X = train.drop(['city', 'year'], axis=1)
    y = train.city
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)
    pipe = Pipeline([
    # normalize data
    ('scale', StandardScaler()),
    ('reduce_dim', PCA()),
    ('classify', SVC())
    ])
    N_FEATURES_OPTIONS = np.arange(3, 15)
    C_OPTIONS = np.arange(1.0,10.0)
    SVM_KERNELS = ['linear', 'rbf']

    param_grid = [
        {
            'reduce_dim__n_components': N_FEATURES_OPTIONS,
            'classify__kernel': SVM_KERNELS,
            'classify__C': C_OPTIONS,
            'classify__gamma': ['auto', 'scale'],
            'classify__random_state': [4]
        }
    ]

    grid = GridSearchCV(pipe, param_grid=param_grid, iid=False, cv=3, n_jobs=1)
    grid.fit(X_train, y_train)
    kernel = grid.best_params_['classify__kernel']
    C = grid.best_params_['classify__C']
    n = grid.best_params_['reduce_dim__n_components']

    # read the unlabelled data set and make predictions
    predictions = grid.predict(test)
    pd.DataFrame(predictions).to_csv(output, index=False, header=False)
    # print(grid.score(X_train, y_train))
    print("Model: SVM, StandardScaler, PCA({}), {} kernel with C={}. Score: {}"          .format(n, kernel, C, grid.score(X_valid, y_valid)))

if __name__ == '__main__':
    main()

