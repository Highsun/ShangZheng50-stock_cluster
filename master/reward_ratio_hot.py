import numpy as np
import matplotlib.pyplot as plt
import os
from std_setup import *

plot_setup()
data_open, data_close, data_max, data_min, data_num, mapping_dict = load_data()

def calculate_reward_matrix(data_open, data_close):
    A = np.zeros((49, 49))
    for k in range(48):
        p1 = (data_open.iloc[k, :] / data_close.iloc[k, :] - 1).values
        for t in range(k+1, 49):
            p2 = (data_open.iloc[t, :] / data_close.iloc[t, :] - 1).values
            Q1 = np.where(p2 * p1 > 0, 1, 0)
            Q2 = np.where(np.abs(p2 - p1) < 0.001, 0.95,
                      np.where(np.abs(p2 - p1) < 0.005, 0.85,
                               np.where(np.abs(p2 - p1) < 0.01, 0.75,
                                        np.where(np.abs(p2 - p1) < 0.02, 0.65, 0.55))))
            A[k, t] = (Q1.mean() + Q2.mean()) / 2
    return A

A = calculate_reward_matrix(data_open, data_close)
A = A + A.T + np.eye(49)

plt.imshow(A, cmap='jet', interpolation='nearest')
plt.colorbar()
plt.title('上证50成分股每日区间回报率热力图')
plt.xlabel('股票')
plt.ylabel('股票')
# plt.show()

if not os.path.exists('./results/reward_ratio'):
    os.mkdir('./results/reward_ratio')

plt.savefig('./results/reward_ratio/上证50成分股每日区间回报率热力图.png', dpi=300)