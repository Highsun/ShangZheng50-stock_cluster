import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

n_clusters = 2
clusters = pd.read_csv(f'./results/cluster/clustered_stocks(k={n_clusters}).csv')

# Plot by clusters
def plot_cluster(clusters, dataset, cnt):
    for i in range(n_clusters):
        stock_codes =  clusters[clusters.columns[i]].dropna().values
        data = dataset.loc[stock_codes]
        dates = pd.to_datetime(data.columns)

        plt.figure(figsize=(14, 8))
        for code in stock_codes:
            plt.plot(dates, data.loc[code], label=mapping_dict.get(code, code))
        plt.xlabel('日期')
        plt.ylabel('价格/数量')
        plt.title(f'dataset_{cnt}，cluster_{i} 分类数据走势图')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=9)
        plt.grid(True)
        plt.tight_layout()
        # plt.show()
        output_path = f'./results/cluster/cluster_display(k={n_clusters})/cluster_{i}_dataset_{cnt}.png'
        plt.savefig(output_path, dpi=300)

if not os.path.exists(f'./results/cluster/cluster_display(k={n_clusters})'):
    os.makedirs(f'./results/cluster/cluster_display(k={n_clusters})')

datasets = [data_open, data_close, data_max, data_min, data_num]
cnt = 1
for dataset in datasets:
    plot_cluster(clusters, dataset, cnt)
    cnt += 1