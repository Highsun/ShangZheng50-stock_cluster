import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import mplfinance as mpf
import os
from std_setup import plot_setup, load_data

def set_chinese_font():
    font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
    prop = font_manager.FontProperties(fname=font_path)
    return prop

def create_mpf_style(font_prop):
    return mpf.make_mpf_style(base_mpf_style='charles',
                              rc={'font.sans-serif': font_prop.get_name(),
                                  'axes.unicode_minus': False})

def plot_k_line(stock_code, data_open, data_close, data_max, data_min, mapping_dict, font_prop):
    stock_name = mapping_dict.get(stock_code, stock_code)
    
    ohlc_data = pd.DataFrame({
        'Open': data_open.loc[stock_code],
        'High': data_max.loc[stock_code],
        'Low': data_min.loc[stock_code],
        'Close': data_close.loc[stock_code]
    })
    
    ohlc_data.index = pd.to_datetime(ohlc_data.index)
    
    style = create_mpf_style(font_prop)
    mpf.plot(ohlc_data, type='candle', style=style,
             title=f"K线图（{stock_name}）", ylabel='价格',
             volume=False, mav=(5, 10), figsize=(10, 6),
             savefig={'fname': f"./results/K_line/K_line_{stock_code}.png", 'dpi': 300})

plot_setup()
font_prop = set_chinese_font()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

if not os.path.exists("./results/K_line"):
    os.makedirs("./results/K_line")

for stock_code in data_open.index:
    plot_k_line(stock_code, data_open, data_close, data_max, data_min, mapping_dict, font_prop)