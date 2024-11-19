import numpy as np
import pandas as pd
import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def pearson(data, cluster):
    cluster_data = data.loc[cluster]
    correlation_matrix = np.corrcoef(cluster_data)
    return correlation_matrix

def plot_heatmap(correlation_matrix, cnt, j):
    fig, ax = plt.subplots()
    cax = ax.matshow(correlation_matrix, cmap='coolwarm')
    fig.colorbar(cax)
    plt.title(f'Pearson相关系数热力图（dataset_{cnt}，cluster_{j}）')
    # plt.show()
    plt.savefig(f'./results/cluster/Pearson_heatmap(k={n_clusters})/Ph_{cnt}_{j}.png', dpi=300)

n_clusters = 3
data_cluster = pd.read_csv(f'./results/cluster/clustered_results(k={n_clusters}).csv')

cluster = []
for col in data_cluster.columns:
    stocks = data_cluster[col].dropna()
    stocks_code = stocks.apply(lambda x: list(mapping_dict.keys())[list(mapping_dict.values()).index(x)])
    cluster.append(stocks_code.tolist())

# cluster_df = pd.DataFrame(cluster).transpose()
# cluster_df.to_csv(f'./results/cluster/clustered_stocks(k={n_clusters}).csv', index=False)

# print(cluster)
# correlation_matrix = pearson(data_close, cluster[0])
# plot_heatmap(correlation_matrix)

if not os.path.exists(f'./results/cluster/Pearson_heatmap(k={n_clusters})'):
    os.makedirs(f'./results/cluster/Pearson_heatmap(k={n_clusters})')

datasets = [data_open, data_close, data_max, data_min, data_num]
cnt = 1
for i in datasets:
    for j in range(n_clusters):
        correlation_matrix = pearson(i, cluster[j])
        plot_heatmap(correlation_matrix, cnt, j)
    cnt += 1