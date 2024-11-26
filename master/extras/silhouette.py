import pandas as pd
from sklearn.metrics import silhouette_score

def load_classification(dtw_matrix, cluster_file):
    cluster = []
    codes = dtw_matrix.index.tolist()
    for code in codes:
        for cluster_id in cluster_file.columns:
            cluster_codes = cluster_file[cluster_id].dropna().values
            if code in cluster_codes:
                cluster.append(cluster_id)
                break
    return cluster

weighted_dtw_matrix = pd.read_csv('./results/cluster/weighted_dtw.csv', index_col=0)
cluster_file = pd.read_csv('./results/cluster/cluster_results.csv', header=None)

clusters = load_classification(weighted_dtw_matrix, cluster_file)
sil_score = silhouette_score(weighted_dtw_matrix, clusters, metric='precomputed')
print(f"轮廓系数: {sil_score}")