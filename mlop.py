#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:24:36 2024

"""

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MaxAbsScaler,\
    MinMaxScaler, RobustScaler, Normalizer, PowerTransformer, \
        SplineTransformer, PolynomialFeatures, KernelCenterer, \
            QuantileTransformer
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from plotnine import ggplot, aes, geom_point, facet_wrap, labs, theme
import matplotlib.pyplot as plt
import time

class mlop:
    
    '''
    Machine Learning Option Pricing with sklearn
    
    '''
    def __init__(self):
        self.user_dataset = None
        self.random_state = None
        self.test_size = 0.01
        self.max_iter = int(1e3)
        self.hidden_layer_sizes = (100,100,100)
        self.solver = [
                    "lbfgs",
                    # "sgd", 
                    # "adam"
                    ]
        
        self.alpha = 0.0001
        self.learning_rate = [
            
            'adaptive',
            # 'constant'
            
            ]
        
        self.activation_function = [  
            
            # 'identity',
            # 'logistic',
            'tanh',
            # 'relu',
            
            ]
        
        
        self.rf_n_estimators = 50
        self.rf_min_samples_leaf = 2000
        
        self.target_name = 'observed_price'
        self.feature_set = [
            
            'spot_price', 
            'strike_price', 
            'days_to_maturity',
            
            'barrierType',
            'outin',
            'updown',
            
            'w'
            
            ]
        
        self.numerical_features = [
            
            'spot_price', 
            'strike_price', 
            'days_to_maturity', 
            
            ]
        
        self.categorical_features = [
            
            'barrierType',
            'outin',
            'updown',
            
            'w'
            
            ]
        
        # self.security_tag = 'vanilla options'
        self.security_tag = 'barrier options'
        
        self.transformers = [
            ("scale1",StandardScaler(),self.numerical_features),
            # ("scale2",QuantileTransformer(),self.numerical_features),
            ("encode", OneHotEncoder(),self.categorical_features)
            ]   

        self.activation_function = self.activation_function[0]
        self.learning_rate = self.learning_rate[0]
        self.solver = self.solver[0]
        print(f"\n{self.security_tag}")
        print(f"\ntransformers:\n{self.transformers}")
        print(f"\nactivation: {self.activation_function}")
        print(f"solver: {self.solver}")
        print(f"learning rate: {self.learning_rate}")
        print(f"hidden layers: {self.hidden_layer_sizes}")
        print(f"\nfeatures:\n{self.feature_set}")
# =============================================================================
                                                                # Preprocessing

    def split_user_data(self):
        train_data, test_data = train_test_split(
            self.user_dataset, 
            test_size=self.test_size, 
            random_state=self.random_state)
         
        train_X = train_data[self.feature_set]
        test_X = test_data[self.feature_set]
        
        train_y = train_data[self.target_name]
        test_y = test_data[self.target_name]
        
        return train_data, train_X, train_y, \
            test_data, test_X, test_y
            
    def preprocess(self):
        preprocessor = ColumnTransformer(transformers=self.transformers)
        return preprocessor
    
# =============================================================================
                                                             # Model Estimation

    def run_nnet(self, preprocessor, train_X, train_y):
        nnet_start = time.time()
        nnet_model = MLPRegressor(
            hidden_layer_sizes=self.hidden_layer_sizes,
            activation=self.activation_function, 
            solver=self.solver, 
            max_iter=self.max_iter,
            random_state=self.random_state
            )
            
        nnet_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", nnet_model)
            ])
        
        model_fit = nnet_pipeline.fit(train_X, train_y)
        nnet_end = time.time()
        nnet_runtime = int(nnet_end - nnet_start)
        return model_fit, nnet_runtime
    
    def run_dnn(self, preprocessor,train_X,train_y):
        dnn_start = time.time()
        deepnnet_model = MLPRegressor(
            hidden_layer_sizes= self.hidden_layer_sizes,
            activation = self.activation_function, 
            solver= self.solver,
            alpha = self.alpha,
            learning_rate = self.learning_rate,
            max_iter = self.max_iter, 
            random_state = self.random_state
            )
                                  
        deepnnet_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", deepnnet_model)
        ])
        dnn_fit = deepnnet_pipeline.fit(train_X,train_y)
        dnn_end = time.time()
        dnn_runtime = int(dnn_end - dnn_start)
        return dnn_fit, dnn_runtime
    
    def run_rf(self, preprocessor, train_X, train_y):
        rf_start = time.time()
        rf_model = RandomForestRegressor(
        n_estimators=self.rf_n_estimators, 
        min_samples_leaf=self.rf_min_samples_leaf, 
        random_state=self.random_state)
        
        rf_pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("regressor", rf_model)])
        rf_fit = rf_pipeline.fit(train_X, train_y)
        rf_end = time.time()
        rf_runtime = rf_end - rf_start
        return rf_fit, rf_runtime
    
    def run_lm(self, train_X, train_y):
        lm_start = time.time()
        lm_pipeline = Pipeline([
            ("polynomial", PolynomialFeatures(degree=5, 
                                    interaction_only=False, 
                                    include_bias=True)),
            ("scaler", StandardScaler()),
            ("regressor", Lasso(alpha=0.01))])

        lm_fit = lm_pipeline.fit(train_X, train_y)
        lm_end = time.time()
        lm_runtime = lm_end - lm_start
        return lm_fit, lm_runtime

# =============================================================================
                                                                # Model Testing

    def test_model(self,test_X,test_y,model_fit):
        training_results = test_X.copy()
        training_results.loc[
            training_results['w'] == 'call', 'moneyness'
            ] = training_results['spot_price'] / training_results['strike_price'] - 1
        training_results.loc[
            training_results['w'] == 'put', 'moneyness'
            ] = training_results['strike_price'] / training_results['spot_price'] - 1
        training_results['target'] = test_y
        training_results['prediciton'] = model_fit.predict(test_X)
        training_results['absRelError'] = abs(training_results['prediciton']/training_results['target']-1)
        return training_results

    def plot_model_performance(self,predictive_performance, runtime):
        predictive_performance_plot = (
            ggplot(predictive_performance, 
                   aes(x="moneyness", y="absRelError")) + 
            geom_point(alpha=0.05) + 
            labs(x="Percentage moneyness (S/K)", 
                 y=f"Absolute percentage error ({round(runtime,4)} second runtime)",
                 title=f'Prediction error for {self.security_tag}') + 
            theme(legend_position="")
            )
        predictive_performance_plot.show()
        plt.cla()
        plt.clf()
        return predictive_performance_plot    



    