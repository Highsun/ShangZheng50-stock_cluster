import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from std_setup import plot_setup, load_data

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def calculate_rsi(data_close, stock_code, period=14):
    if stock_code not in data_close.index:
        raise ValueError(f"股票代码 {stock_code} 不在数据中")

    close_prices = data_close.loc[stock_code].values
    rsi_values = []
    
    for t in range(period, len(close_prices)):
        gains = 0
        losses = 0
        for i in range(1, period + 1):
            change = close_prices[t - i + 1] - close_prices[t - i]
            if change > 0:
                gains += change
            else:
                losses -= change
        
        avg_gain = gains / period
        avg_loss = losses / period if losses != 0 else 0
        
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
        rsi_values.append(rsi)
    
    return rsi_values

def plot_rsi_curve(stock_code):
    rsi_values = calculate_rsi(data_close, stock_code, period)

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(rsi_values)), rsi_values, label=f'RSI ({mapping_dict.get(stock_code, stock_code)})', color='purple')
    plt.axhline(y=70, color='red', linestyle='--', label='超买 (70)')
    plt.axhline(y=30, color='green', linestyle='--', label='超卖 (30)')
    plt.xlabel('时间 (天)')
    plt.ylabel('RSI 值')
    plt.title(f'{mapping_dict.get(stock_code, stock_code)}的RSI曲线')
    plt.legend()
    plt.grid(True)
    # plt.show()
    plt.savefig(f'./results/RSI/RSI_{mapping_dict.get(stock_code, stock_code)}.png', dpi=300)

if not os.path.exists('./results/RSI'):
    os.makedirs('./results/RSI')

period = 14
data_rsi = np.zeros((len(data_close.index), len(data_close.columns) - period))
for stock_code in data_close.index:
    # plot_rsi_curve(stock_code)
    rsi = calculate_rsi(data_close, stock_code, period)
    data_rsi[data_close.index.get_loc(stock_code)] = rsi

data_rsi = pd.DataFrame(data_rsi, index=data_close.index, columns=data_close.columns[period:])
data_rsi.to_csv('./results/RSI/RSI_raw.csv')