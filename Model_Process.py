# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 20:03:35 2023

@author: gusta
"""
import os
path_raw_data = r'C:\Users\gusta\Desktop\Personal_Projects\Nixtla_Forecast\Raw_Data'
path_processed_data = r'C:\Users\gusta\Desktop\Personal_Projects\Nixtla_Forecast\Processed_Data'
path_final_data = r'C:\Users\gusta\Desktop\Personal_Projects\Nixtla_Forecast\Final_Data'

import numpy as np
import pandas as pd


from hierarchicalforecast.utils import aggregate
from statsforecast.core import StatsForecast


from statsforecast.models import AutoARIMA
from statsforecast.models import SeasonalWindowAverage

from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import   OptimalCombination
from hierarchicalforecast.methods import  BottomUp, TopDown, MiddleOut, MinTrace, BottomUpSparse





#Load Tourism BR and set data to Model
df_br = pd.read_csv(os.path.join(path_processed_data, 'processed_data.csv'), sep = ';', index_col=0)

#Cut data before Covid
df_br = df_br[df_br['ds'] <'2020-01-01']
hierarchy_levels = [['top_level'],
                    ['top_level', 'middle_level'],
                    ['top_level', 'middle_level', 'bottom_level']]
Y_df, S, tags = aggregate(df=df_br, spec=hierarchy_levels)

Y_df = Y_df.reset_index()
###Data Is ALL GOOD


# Split train/test sets
Y_test_df  = Y_df.groupby('unique_id').tail(12)
Y_test_df_aux = Y_test_df.copy()
Y_test_df_aux['ds'] = pd.to_datetime(Y_test_df_aux['ds'])

Y_train_df = Y_df.drop(Y_test_df.index)
# Y_train_df = Y_train_df[Y_train_df['ds'] <'2020-01-01']



fcst = StatsForecast(df=Y_train_df,
                     models=[ 
                             SeasonalWindowAverage(season_length=12, window_size=4)
                             ],
                     freq='MS', n_jobs=-1)

Y_hat_df = fcst.forecast(h=12)
Y_hat_df = Y_hat_df.fillna(0)

Y_eval = pd.merge(Y_hat_df, Y_test_df_aux, on = ['ds', 'unique_id'], how = 'left')#.reset_index()
Y_eval = Y_eval.fillna(0)
Y_eval_gp = Y_eval.groupby('unique_id').sum() 
Y_eval_gp['MAPE'] = 1 - (abs(Y_eval_gp['y']-Y_eval_gp['SeasWA']  )/ Y_eval_gp['y'])
# col_reverse = [x for x in Y_hat_df if 'ds' not in x]
# Y_hat_df[col_reverse] = np.exp(Y_hat_df[col_reverse])

reconcilers = [
    BottomUp(),
    TopDown(method='forecast_proportions'),
    MinTrace(method='ols'),
    MinTrace(method='wls_struct'),  #ols

              ] 

hrec = HierarchicalReconciliation(reconcilers=reconcilers)
Y_rec_df = hrec.reconcile(Y_hat_df=Y_hat_df, Y_df=Y_train_df,
                          S=S, tags=tags)

#append real values


Y_eval_final = pd.merge(Y_rec_df, Y_test_df_aux, on = ['ds', 'unique_id'])
Y_eval_final.columns = ['Date', 'unique_id', 'Singular_Models_SeasWA', 'Reconcile_BottomUp',
       'Reconcile_TopDown_method-forecast_proportions',
       'Reconcile_MinTrace_method-ols', 'Reconcile_MinTrace_method-wls_struct', 'Real_Value']

Y_eval_final_gp = Y_eval_final.groupby('unique_id').sum() 

#Save Output Data
Y_eval_final.to_csv(os.path.join(path_final_data, 'final_results.csv'), sep = ';', decimal = '.', encoding = 'UTF-8')
Y_eval_final_gp.to_csv(os.path.join(path_final_data, 'final_results_groupby_id.csv'), sep = ';', decimal = '.',  encoding = 'UTF-8')




    
    