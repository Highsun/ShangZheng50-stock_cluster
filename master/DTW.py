import numpy as np
import pandas as pd
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import os
from sklearn.preprocessing import MinMaxScaler
import time
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def normalize_data(data):
    scaler = MinMaxScaler()
    normalized_data = pd.DataFrame(scaler.fit_transform(data), index=data.index, columns=data.columns)
    return normalized_data

def calculate_dtw(stock_code1, stock_code2, data):
    data = normalize_data(data)
    series1 = data.loc[stock_code1].values.reshape(-1, 1)
    series2 = data.loc[stock_code2].values.reshape(-1, 1) 
    dtw_distance, _ = fastdtw(series1, series2, dist=euclidean)
    return dtw_distance

def make_dtw_matrix(data, calculate_dtw):
    dtw = np.zeros((len(data.index), len(data.index)))
    for stock_code1 in data.index:
        for stock_code2 in data.index:
            dtw_distance = calculate_dtw(stock_code1, stock_code2, data)
            dtw[data.index.get_loc(stock_code1), data.index.get_loc(stock_code2)] = dtw_distance
    return dtw

def save_dtw(dtw, i, path_list):
    dtw = pd.DataFrame(dtw, index=data_close.index, columns=data_close.index)
    path = './results/DTW'
    file_name = 'DTW_' + path_list[i] + '.csv'
    output_path = os.path.join(path, file_name)
    dtw.to_csv(output_path)

def process_and_time(data, data_name, calculate_dtw):
    start_time = time.time()
    dtw_matrix = make_dtw_matrix(data, calculate_dtw)
    elapsed_time = time.time() - start_time
    print(f"DTW matrix for {data_name} took {elapsed_time:.2f} s.")
    return dtw_matrix

if not os.path.exists('./results/DTW'):
    os.mkdir('./results/DTW')

## main()
data_sources = {
    'raw': data_close,
    'obv': pd.read_csv('./results/OBV/OBV_raw.csv', index_col=0),
    'rsi': pd.read_csv('./results/RSI/RSI_raw.csv', index_col=0),
    'returns': pd.read_csv('./results/reward_ratio/returns/returns_raw.csv', index_col=0)
}

path_list = list(data_sources.keys())

for i, (data_name, data) in enumerate(data_sources.items()):
    dtw_matrix = process_and_time(data, data_name, calculate_dtw)
    save_dtw(dtw_matrix, i, path_list)
    print(f'File: DTW_{data_name}.csv saved.')