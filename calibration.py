# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 19:47:34 2024

@author: boomelage
"""

def clear_all():
    globals_ = globals().copy()
    for name in globals_:
        if not name.startswith('_') and name not in ['clear_all']:
            del globals()[name]
clear_all()
import time
from datetime import datetime
start_time = time.time()
start_datetime = datetime.fromtimestamp(start_time)
start_tag = start_datetime.strftime("%c")
print(f"\n{start_tag}")
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append('term_structure')



import QuantLib as ql
import numpy as np
import pandas as pd

from settings import model_settings
ms = model_settings()
settings = ms.import_model_settings()
security_settings = settings[0]['security_settings']
s = security_settings[5]
day_count = settings[0]['day_count']
calendar = settings[0]['calendar']
calculation_date = settings[0]['calculation_date']


from calibration_generation import features

dataset = features.copy()

s = float(dataset['spot_price'].unique()[0])
S_handle = ql.QuoteHandle(ql.SimpleQuote(s))

risk_free_rate = 0.055
dividend_rate = 0.01312
flat_ts = ms.make_ts_object(risk_free_rate)
dividend_ts = ms.make_ts_object(dividend_rate)

grouped = dataset.groupby(by='days_to_maturity')
T = dataset['days_to_maturity'].unique()

heston_parameters_np = np.zeros((len(T),6),dtype=object)
heston_parameters = pd.DataFrame(heston_parameters_np)
heston_parameters[f's = {int(s)}'] = T.astype(int)
heston_parameters = heston_parameters.set_index(f's = {int(s)}')
heston_parameters.columns = ['theta', 'kappa', 'sigma', 'rho', 'v0', 'error']


for t_idx, t in enumerate(T):
    calibration_dataset = grouped.get_group(t).reset_index(drop=True)
    
    v0 = 0.01; kappa = 0.2; theta = 0.02; rho = -0.75; sigma = 0.5; 
    process = ql.HestonProcess(
        flat_ts,                
        dividend_ts,            
        S_handle,               
        v0,                # Initial volatility
        kappa,             # Mean reversion speed
        theta,             # Long-run variance (volatility squared)
        sigma,             # Volatility of the volatility
        rho                # Correlation between asset and volatility
    )
    
    model = ql.HestonModel(process)
    engine = ql.AnalyticHestonEngine(model)
    heston_helpers = []
    date = calculation_date + ql.Period(int(t),ql.Days)
    dt = (date - calculation_date)
    p = ql.Period(dt, ql.Days)
    
    for row_idx, row in calibration_dataset.iterrows():
        risk_free_rate = row['risk_free_rate']
        dividend_rate = row['dividend_rate']
        flat_ts = ms.make_ts_object(risk_free_rate)
        dividend_ts = ms.make_ts_object(dividend_rate)
        volatility = row['volatility']
        k = row['strike_price']
        helper = ql.HestonModelHelper(
            p,
            calendar,
            float(s),
            k,
            ql.QuoteHandle(ql.SimpleQuote(volatility)),
            flat_ts,
            dividend_ts)
        helper.setPricingEngine(engine)
        heston_helpers.append(helper)
    
    lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
    model.calibrate(heston_helpers, lm,
                      ql.EndCriteria(500, 50, 1.0e-8,1.0e-8, 1.0e-8))
    
    theta, kappa, sigma, rho, v0 = model.params()
    
    avg = 0.0
    
    for i in range(min(len(heston_helpers), calibration_dataset.shape[0])):
        opt = heston_helpers[i]
        err = (opt.modelValue() / max(opt.marketValue(),0.0000000000001)) - 1.0
        avg += abs(err)
        
    avg = avg*100/len(heston_helpers)
    
    heston_parameters.loc[t,'theta'] = theta
    heston_parameters.loc[t,'kappa'] = kappa
    heston_parameters.loc[t,'sigma'] = sigma
    heston_parameters.loc[t,'rho'] = rho
    heston_parameters.loc[t,'v0'] = v0
    heston_parameters.loc[t,'error'] = avg/100
    
    error_string = "Total Average Abs Error (%%) : %5.3f" % (avg)
    print("-"*len(error_string))
    print(error_string)
    print(f"for {int(t)} day maturity")
    print("-"*len(error_string))

heston_parameters = heston_parameters[~(heston_parameters['error']>5)]
print(f"\n{heston_parameters}")


end_time = time.time()
end_datetime = datetime.fromtimestamp(end_time)
end_tag = end_datetime.strftime("%c")
print(f"\n{end_tag}")


runtime = end_time - start_time
print(f"\ntotal time elapsed: {int(runtime)} seconds")


