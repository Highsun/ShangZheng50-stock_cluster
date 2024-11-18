import pandas as pd
import matplotlib.pyplot as plt
import os
from std_setup import plot_setup, load_data

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

## Display the data
def plot_stock_prices(data, title):
    stock_codes = data.index
    dates = pd.to_datetime(data.columns)

    plt.figure(figsize=(14, 8))
    for code in stock_codes:
        plt.plot(dates, data.loc[code], label=mapping_dict.get(code, code))

    plt.xlabel('日期')
    plt.ylabel('价格/数量')
    plt.title(title + '走势图')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=9)
    plt.grid(True)
    plt.tight_layout()
    # plt.show()
    output_path = './results/overall/' + title + '走势图' + '.png'
    plt.savefig(output_path, dpi=300)

if not os.path.exists('./results/overall'):
    os.makedirs('./results/overall')

plot_stock_prices(data_open, '开盘价')
plot_stock_prices(data_close, '收盘价')
plot_stock_prices(data_max, '最高价')
plot_stock_prices(data_min, '最低价')
plot_stock_prices(data_num, '成交量')