import numpy as np
import pandas as pd
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def pearson(data, cluster):
    cluster_data = data.loc[cluster]
    correlation_matrix = np.corrcoef(cluster_data)
    return correlation_matrix

def plot_heatmap(correlation_matrix):
    fig, ax = plt.subplots()
    cax = ax.matshow(correlation_matrix, cmap='coolwarm')
    fig.colorbar(cax)
    plt.show()

n_clusters = 2
data_cluster = pd.read_csv(f'./results/cluster/clustered_results(k={n_clusters}).csv')

cluster = []
for col in data_cluster.columns:
    stocks = data_cluster[col].dropna()
    stocks_code = stocks.apply(lambda x: list(mapping_dict.keys())[list(mapping_dict.values()).index(x)])
    cluster.append(stocks_code.tolist())

# print(cluster)
# correlation_matrix = pearson(data_close, cluster[0])
# plot_heatmap(correlation_matrix)
datasets = [data_open, data_close, data_max, data_min, data_num]
for i in datasets:
    for j in range(n_clusters):
        correlation_matrix = pearson(i, cluster[j])
        plot_heatmap(correlation_matrix)