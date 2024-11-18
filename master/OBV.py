import numpy as np
import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def calculate_obv(data_close, data_num, stock_code):
    close_prices = data_close.loc[stock_code].values
    volumes = data_num.loc[stock_code].values

    obv_values = np.zeros(len(close_prices))
    
    for i in range(1, len(close_prices)):
        if close_prices[i] > close_prices[i - 1]:
            obv_values[i] = obv_values[i - 1] + volumes[i]
        elif close_prices[i] < close_prices[i - 1]:
            obv_values[i] = obv_values[i - 1] - volumes[i]
        else:
            obv_values[i] = obv_values[i - 1]
    
    return obv_values

def plot_obv(stock_code):
    obv_values = calculate_obv(data_close, data_num, stock_code)
    stock_name = mapping_dict.get(stock_code, stock_code)
    
    plt.figure(figsize=(10, 6))
    plt.plot(obv_values, label=f'OBV - {stock_name}', color='blue')
    plt.xlabel('时间 (天)')
    plt.ylabel('OBV 值')
    plt.title(f'{stock_name}的OBV曲线')
    plt.legend()
    plt.grid(True)
    # plt.show()

if not os.path.exists('./results/OBV'):
    os.mkdir('./results/OBV')

data_obv = np.zeros((len(data_close.index), len(data_close.columns)))
for stock_code in data_close.index:
    # plot_obv(stock_code)
    # plt.savefig(f'./results/OBV/OBV_{stock_code}.png', dpi=300)
    # plt.close()
    obv = calculate_obv(data_close, data_num, stock_code)
    data_obv[data_close.index.get_loc(stock_code)] = obv

data_obv = pd.DataFrame(data_obv, index=data_close.index, columns=data_close.columns)
data_obv.to_csv('./results/OBV/OBV_raw.csv')