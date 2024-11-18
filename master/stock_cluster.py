import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import os
from std_setup import plot_setup, load_data

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

# 0. Load DTW results
data_dtw1 = pd.read_csv('./results/DTW/DTW_raw.csv', index_col=0)
data_dtw2 = pd.read_csv('./results/DTW/DTW_obv.csv', index_col=0)
data_dtw3 = pd.read_csv('./results/DTW/DTW_rsi.csv', index_col=0)
data_dtw4 = pd.read_csv('./results/DTW/DTW_returns.csv', index_col=0)

# 1. Data preprocessing, normalization
def normalize_dtw(dtw_matrix):
    scaler = MinMaxScaler()
    return scaler.fit_transform(dtw_matrix)

# 2. Convert these matrices to similarity
def calculate_similarity(dtw_matrix):
    dtw_matrix = normalize_dtw(dtw_matrix)
    return 1 / (1 + dtw_matrix)

dtw1 = data_dtw1.values
dtw2 = data_dtw2.values
dtw3 = data_dtw3.values
dtw4 = data_dtw4.values

similarity1 = calculate_similarity(dtw1)
similarity2 = calculate_similarity(dtw2)
similarity3 = calculate_similarity(dtw3)
similarity4 = calculate_similarity(dtw4)

# 3. Weighted sum
def weighted_similarity(similarity1, similarity2, similarity3, similarity4, w1=0.20, w2=0.25, w3=0.30, w4=0.25):
    return w1 * similarity1 + w2 * similarity2 + w3 * similarity3 + w4 * similarity4

similarity_matrix = weighted_similarity(similarity1, similarity2, similarity3, similarity4)

# 4. K-means clustering
def cluster_stocks(similarity_matrix, n_clusters=5):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(1 - similarity_matrix)
    return clusters

n_clusters = 3
clusters = cluster_stocks(similarity_matrix, n_clusters)

stock_codes = list(mapping_dict.keys())
stock_names = [mapping_dict[stock_code] for stock_code in stock_codes]
clustered_stocks = pd.DataFrame({'Stock': stock_names, 'Cluster': clusters})

print(clustered_stocks)

# Visualize clustering results
def plot_cluster(n_clusters, clustered_stocks):
    plt.figure(figsize=(10, 6))
    plt.scatter(clustered_stocks['Stock'], clustered_stocks['Cluster'], c=clustered_stocks['Cluster'], cmap='viridis')
    plt.xlabel('股票代码')
    plt.ylabel('类别')
    plt.title(f'股票分类结果（类别数：{n_clusters}）')
    plt.xticks(rotation=90)
    # plt.show()
    plt.savefig(f'./results/cluster/stock_cluster(k={n_clusters}).png', dpi=300)

# Determine the optimal number of clusters using the elbow method
def plot_elbow_method(similarity_matrix, max_k=10):
    distortions = []
    K = range(1, max_k + 1)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(1 - similarity_matrix)
        distortions.append(kmeans.inertia_)
    
    plt.figure(figsize=(10, 6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    # plt.show()
    plt.savefig(f'./results/cluster/elbow_method(k={n_clusters}).png', dpi=300)

if not os.path.exists('./results/cluster'):
    os.makedirs('./results/cluster')

plot_cluster(n_clusters, clustered_stocks)
plot_elbow_method(similarity_matrix)