import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import os
from std_setup import plot_setup, load_data

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

if not os.path.exists('./results/cluster'):
    os.makedirs('./results/cluster')

data_dtw1 = pd.read_csv('./results/DTW/DTW_raw.csv', index_col=0)
data_dtw2 = pd.read_csv('./results/DTW/DTW_obv.csv', index_col=0)
data_dtw3 = pd.read_csv('./results/DTW/DTW_rsi.csv', index_col=0)
data_dtw4 = pd.read_csv('./results/DTW/DTW_returns.csv', index_col=0)

dtw1 = data_dtw1.values
dtw2 = data_dtw2.values
dtw3 = data_dtw3.values
dtw4 = data_dtw4.values

def weighted_similarity(dtw1, dtw2, dtw3, dtw4, w1=0.25, w2=0.25, w3=0.25, w4=0.25):
    weighted_dtw = w1 * dtw1 + w2 * dtw2 + w3 * dtw3 + w4 * dtw4
    np.fill_diagonal(weighted_dtw, 0)
    return weighted_dtw

weighted_dtw = weighted_similarity(dtw1, dtw2, dtw3, dtw4)

def cluster_stocks_hierarchical(dtw_matrix, threshold=20):
    Z = linkage(dtw_matrix, method='average')
    clusters = fcluster(Z, t=threshold, criterion='distance')
    return clusters, Z

distance_threshold = 10 # Set the distance threshold

condensed_dtw = squareform(weighted_dtw)
clusters, Z = cluster_stocks_hierarchical(condensed_dtw, threshold=distance_threshold)

stock_codes = list(mapping_dict.keys())
stock_codes.remove('sh.600519') # Drop Guizhou Maotai if you need
stock_names = [mapping_dict[stock_code] for stock_code in stock_codes]
clustered_stocks = pd.DataFrame({'Stock': stock_names, 'Cluster': clusters})

# Get the number of clusters
n_clusters = len(np.unique(clusters))

def plot_dendrogram(Z, stock_names, threshold):
    plt.figure(figsize=(12, 8))
    dendrogram(Z, labels=stock_names, leaf_rotation=90, color_threshold=threshold)
    plt.title("层次聚类树状图")
    plt.xlabel("股票")
    plt.ylabel("距离")
    plt.tight_layout()
    plt.savefig('./results/cluster/dendrogram.png', dpi=300)
    # plt.show()

plot_dendrogram(Z, stock_names, distance_threshold)

# Get the cluster results
cluster = []
for i in range(1, n_clusters + 1):
    cluster_stocks = clustered_stocks[clustered_stocks['Cluster'] == i]['Stock'].values
    cluster_codes = [list(mapping_dict.keys())[list(mapping_dict.values()).index(stock)] for stock in cluster_stocks]
    cluster.append(cluster_codes)
cluster = pd.DataFrame(cluster).T
cluster.to_csv('./results/cluster/cluster_results.csv', index=False)

# Save the weighted DTW matrix
weighted_dtw = pd.DataFrame(weighted_dtw, index=data_dtw1.index, columns=data_dtw1.columns)
weighted_dtw.to_csv('./results/cluster/weighted_dtw.csv', index=True)