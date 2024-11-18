import pandas as pd
import json
import matplotlib.pyplot as plt

def plot_setup():
    plt.rcParams['font.sans-serif'] = ['Kaiti SC'] # other fonts: 'PingFang SC', 'Heiti SC', 'Songti SC'
    plt.rcParams['axes.unicode_minus'] = False

def load_data(data_path='./dataset/cleaned_data.csv', mapping_path='./dataset/mapping_dict.json'):
    # Load data with mapping
    data = pd.read_csv(data_path, index_col='code', encoding='utf-8')

    # Load mapping dictionary
    with open(mapping_path, 'r', encoding='utf-8') as f:
        mapping_dict = json.load(f)

    # Extract different classifications
    data_open = data.iloc[0::5]
    data_close = data.iloc[1::5]
    data_max = data.iloc[2::5]
    data_min = data.iloc[3::5]
    data_num = data.iloc[4::5]

    return data_open, data_close, data_max, data_min, data_num, mapping_dict