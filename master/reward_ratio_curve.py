import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def calculate_returns(data_close):
    returns = {}
    for stock_code in data_close.index:
        close_prices = data_close.loc[stock_code].values
        returns[stock_code] = (close_prices[1:] - close_prices[:-1]) / close_prices[:-1]
    return returns

def plot_returns(returns, stock_code):
    plt.figure(figsize=(10, 6))
    plt.plot(returns[stock_code], label=f'区间回报率 ({mapping_dict.get(stock_code, stock_code)})', color='purple')
    plt.xlabel('时间 (天)')
    plt.ylabel('区间回报率')
    plt.title(f'{mapping_dict.get(stock_code, stock_code)} 的区间回报率曲线')
    plt.legend()
    plt.grid(True)
    # plt.show()

returns = calculate_returns(data_close)

if not os.path.exists('./results/reward_ratio/returns'):
    os.makedirs('./results/reward_ratio/returns')

data_returns = np.zeros((len(data_close.index), len(data_close.columns) - 1))
for stock_code in data_close.index:
    plot_returns(returns, stock_code)
    plt.savefig(f'./results/reward_ratio/returns/returns_{stock_code}.png', dpi=300)
    plt.close()
    data_returns[data_close.index.get_loc(stock_code)] = returns[stock_code]

data_returns = pd.DataFrame(data_returns, index=data_close.index, columns=data_close.columns[1:])
data_returns.to_csv('./results/reward_ratio/returns/returns_raw.csv')