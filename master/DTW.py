import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def calculate_dtw(stock_code1, stock_code2, data_close):
    series1 = data_close.loc[stock_code1].values.reshape(-1, 1)
    series2 = data_close.loc[stock_code2].values.reshape(-1, 1)
    
    dtw_distance, _ = fastdtw(series1, series2, dist=euclidean)
    
    return dtw_distance

def make_dtw_matrix(data_close, calculate_dtw):
    dtw = np.zeros((len(data_close.index), len(data_close.index)))
    for stock_code1 in data_close.index:
        for stock_code2 in data_close.index:
            dtw_distance = calculate_dtw(stock_code1, stock_code2, data_close)
            dtw[data_close.index.get_loc(stock_code1), data_close.index.get_loc(stock_code2)] = dtw_distance
    return dtw

## data source:
# dtw = make_dtw_matrix(data_close, calculate_dtw)

# data_obv = pd.read_csv('./results/OBV/OBV_raw.csv', index_col=0)
# dtw = make_dtw_matrix(data_obv, calculate_dtw)

# data_rsi = pd.read_csv('./results/RSI/RSI_raw.csv', index_col=0)
# dtw = make_dtw_matrix(data_rsi, calculate_dtw)

data_returns = pd.read_csv('./results/reward_ratio/returns/returns_raw.csv', index_col=0)
dtw = make_dtw_matrix(data_returns, calculate_dtw)

# print(dtw)
if not os.path.exists('./results/DTW'):
    os.mkdir('./results/DTW')

dtw = pd.DataFrame(dtw, index=data_close.index, columns=data_close.index)
dtw.to_csv('./results/DTW/DTW_returns.csv')