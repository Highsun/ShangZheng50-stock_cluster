import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram ,fcluster
from scipy.spatial.distance import squareform
from sklearn.metrics import silhouette_score
from itertools import product
import matplotlib.pyplot as plt
import os
from std_setup import plot_setup, load_data

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

if not os.path.exists('./results/cluster'):
    os.makedirs('./results/cluster')

data_dtw1 = pd.read_csv('./results/DTW/DTW_raw.csv', index_col=0).values
data_dtw2 = pd.read_csv('./results/DTW/DTW_obv.csv', index_col=0).values
data_dtw3 = pd.read_csv('./results/DTW/DTW_rsi.csv', index_col=0).values
data_dtw4 = pd.read_csv('./results/DTW/DTW_returns.csv', index_col=0).values

def weighted_similarity(dtw1, dtw2, dtw3, dtw4, w1, w2, w3, w4):
    weighted_dtw =  w1 * dtw1 + w2 * dtw2 + w3 * dtw3 + w4 * dtw4
    np.fill_diagonal(weighted_dtw, 0)
    return weighted_dtw

def cluster_stocks_hierarchical(dtw_matrix, threshold):
    Z = linkage(dtw_matrix, method='average')
    clusters = fcluster(Z, t=threshold, criterion='distance')
    return clusters, Z

def evaluate_clustering(dtw_matrix, clusters):
    return silhouette_score(dtw_matrix, clusters, metric='precomputed')

# Initialize
weights = np.arange(0.0, 1.05, 0.05).tolist()
distance_threshold = 10
best_score = -1
best_weights = None
best_clusters = None
best_Z = None

# Iterate over all possible weight combinations
for w1, w2, w3, w4 in product(weights, repeat=4):
    if np.isclose(w1 + w2 + w3 + w4, 1): # Make sure the sum of weights is 1
        weighted_dtw = weighted_similarity(data_dtw1, data_dtw2, data_dtw3, data_dtw4, w1, w2, w3, w4)
        try:
            condensed_dtw = squareform(weighted_dtw)
            clusters, Z = cluster_stocks_hierarchical(condensed_dtw, threshold=distance_threshold)
            score = evaluate_clustering(weighted_dtw, clusters)
            if score > best_score:
                best_score = score
                best_weights = (w1, w2, w3, w4)
                best_clusters = clusters
                best_Z = Z
        except Exception as e:
            print(f"评估失败，跳过权重组合 ({w1}, {w2}, {w3}, {w4}): {e}")

# 打印最佳结果
print(f"\n最佳权重组合: {best_weights}，轮廓系数: {best_score}")

# 保存最佳聚类结果
stock_codes = list(mapping_dict.keys())
stock_codes.remove('sh.600519')  # 去掉特定股票
stock_names = [mapping_dict[stock_code] for stock_code in stock_codes]
clustered_stocks = pd.DataFrame({'Stock': stock_names, 'Cluster': best_clusters})
n_clusters = len(np.unique(best_clusters))

print(f"在 distance_threshold 取 {distance_threshold} 的条件下，最佳聚类数目为: {n_clusters} 类")

cluster = []
for i in range(1, n_clusters + 1):
    cluster_stocks = clustered_stocks[clustered_stocks['Cluster'] == i]['Stock'].values
    cluster_codes = [list(mapping_dict.keys())[list(mapping_dict.values()).index(stock)] for stock in cluster_stocks]
    cluster.append(cluster_codes)
cluster = pd.DataFrame(cluster).T
cluster.to_csv('./results/cluster/cluster_results.csv', index=False)

# 保存最佳加权DTW矩阵
weighted_dtw = pd.DataFrame(
    weighted_similarity(data_dtw1, data_dtw2, data_dtw3, data_dtw4, *best_weights),
    index=pd.read_csv('./results/DTW/DTW_raw.csv', index_col=0).index,
    columns=pd.read_csv('./results/DTW/DTW_raw.csv', index_col=0).columns
)
weighted_dtw.to_csv('./results/cluster/weighted_dtw.csv', index=True)

# 绘制最佳树状图
def plot_dendrogram(Z, stock_names, threshold):
    plt.figure(figsize=(12, 8))
    dendrogram(Z, labels=stock_names, leaf_rotation=90, color_threshold=threshold)
    plt.title("最佳层次聚类树状图")
    plt.xlabel("股票")
    plt.ylabel("距离")
    plt.tight_layout()
    plt.savefig('./results/cluster/best_dendrogram.png', dpi=300)
    # plt.show()

plot_dendrogram(best_Z, stock_names, distance_threshold)