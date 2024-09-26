# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 17:13:18 2024

"""
import os
import sys
import time
from datetime import datetime

os.chdir(os.path.dirname(os.path.abspath(__file__)))
from mlop import mlop
from data_query import dirdatacsv
csvs = dirdatacsv()
sys.path.append(os.path.join('train_data','barriers'))
sys.path.append(os.path.join('train_data','vanillas'))

train_start = time.time()
train_start_datetime = datetime.fromtimestamp(train_start)
train_start_tag = train_start_datetime.strftime('%c')
print(f"\n{train_start_tag}\n")

"""
# =============================================================================
                                importing data
"""

# from train_generation_barriers import training_data, title

# from train_generation_vanillas import training_data, title

from train_data_barrier_collector import training_data
title = 'barrier options'

"""
# =============================================================================
"""

mlop = mlop(user_dataset = training_data)
print('\ntraining...')

"""
# =============================================================================
                            preprocessing data
"""
train_data, train_X, train_y, \
    test_data, test_X, test_y = mlop.split_user_data()

preprocessor = mlop.preprocess()

"""
# =============================================================================
                              model selection                
"""
"""
single layer network
"""

model_name = "Single Layer Network"
print(model_name)
model_fit, runtime = mlop.run_nnet(preprocessor, train_X, train_y)

"""
deep neural network
"""

# model_name = "Deep Neural Network"
# print(model_name)
# model_fit, runtime = mlop.run_dnn(preprocessor,train_X,train_y)

"""
random forest
"""

# model_name = "Random Forest"
# print(model_name)
# model_fit, runtime = mlop.run_rf(preprocessor,train_X,train_y)

"""
lasso regression
"""

# model_name = "Lasso Regression"
# print(model_name)
# model_fit, runtime = mlop.run_lm(train_X,train_y)

"""
# ============================================================================
                                model testing
"""

df = mlop.test_model(test_X,test_y,model_fit)

predictive_performance_plot = mlop.plot_model_performance(df,runtime,title)

"""
# =============================================================================
"""

train_end = time.time()
train_time = train_end - train_start

print(f"\nruntime: {int(train_time)} seconds")

