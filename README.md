# MASTER branch of ShangZhen50-stock_cluster

This is the final version of our project, fully structured and tested. You can use our project with the guidance below.

## Environment
- Python: Latest version of python (python 3.12.2 or later version)
  - pandas: 2.2.2
  - numpy: 1.26.4
  - json5: 0.9.25
  - matplotlib: 3.9.2
  - scikit-learn: 1.5.1
  - mplfinance: 0.12.10b0

## Structure
```
.
└── master
    ├── DTW.py
    ├── K_line.py
    ├── OBV.py
    ├── Pearson.py
    ├── RSI.py
    ├── __pycache__
    │   └── std_setup.cpython-312.pyc
    ├── basic_display.py
    ├── clean_data.py
    ├── cluster_plot.py
    ├── dataset
    │   ├── cleaned_data.csv
    │   ├── mapping_dict.json
    │   └── 上证50成分股交易数据.csv
    ├── extras
    │   └── entropy_weight.py
    ├── results
    │   ├── DTW
    │   ├── K_line
    │   ├── OBV
    │   ├── RSI
    │   ├── cluster
    │   ├── overall
    │   └── reward_ratio
    ├── reward_ratio_curve.py
    ├── reward_ratio_hot.py
    ├── std_setup.py
    └── stock_cluster.py
```

13 directories, 17 files

## Files
> Note: These files are listed in order.
### 'clean_data.py'
Load raw data, clean and format it.

### 'std_setup.py'
Load cleaned data and divide it into opening price, closing price, highest price, lowest price and trading volume.
Create a mapping of stock name and code for subsequent programming.

### 'basic_display.py'
Display the whole picture of the original data.

### 'K_line.py'
Draw a stock Candlestick chart to show the information and change laws of each stock in an all-round way.

### 'RSI.py'
Calculate and plot the RSI curve of stocks, using closing price.

### 'OBV.py'
Calculate and plot the OBV curve of stocks, using closing price and trading volume.

### 'reward_ratio_curve.py'
Calculate and plot the return rate curve of stocks, using closing price.

### 'reward_ratio_hot.py'
Draw the heat-map of the stock return rate, aiming at better display the return rate.

### 'DTW.py'
Realize the DTW algorithm, and apply it to measure the similarity between raw data, RSI, OBV and return rate curve.

### 'stock_cluster.py'
Use hierarchical clustering algorithm to cluster stocks, distance:

$$
\mathcal{L}_{\text{all}} = w_1 \times \mathcal{L}_{\text{RAW}} + w_2 \times \mathcal{L}_{\text{RSI}} + w_3 \times \mathcal{L}_{\text{OBV}} + w_4 \times \mathcal{L}_{\text{RR}}
$$

Where:
- $RR$: Return Rate.
- $w_i$: Weight of each distance term, initially defined as $w_1 = 0.2$, $w_2 = 0.3$, $w_3 = 0.25$, $w_4 = 0.25$.

### 'cluster_plot.py'
Draw the results of clustering.

### 'Pearson.py''
Apply Pearson correlation coefficient to measure the quality of the clustering results.

## Folders
### dataset
Contains raw data, cleaned data and mapping dictionary json file.
> Put your raw data downloaded from web in this folder and modify the raw data path in 'clean_data.py' and 'std_setup.py'.

### results
All the results (plots and output files) are stored in this folder.

---

Created and edited by Highsun, any question: highsun910@gmail.com

**Last update**: 2024.11.26
