# MASTER branch of ShangZheng50-stock_cluster

This is the final version of our project, fully structured and tested. You can use our project with the guidance below.

## Environment
- Python: Latest version of python (python 3.12.2 or later version)
  - pandas: 2.2.2
  - numpy: 1.26.4
  - json5: 0.9.25
  - matplotlib: 3.9.2
  - scipy: 1.13.1
  - scikit-learn: 1.5.1
  - mplfinance: 0.12.10b0
  - fastdtw: 0.3.4

## Structure
```
.
├── README.md
└── master
    ├── DTW.py
    ├── K_line.py
    ├── OBV.py
    ├── RSI.py
    ├── __pycache__
    │   └── std_setup.cpython-312.pyc
    ├── basic_display.py
    ├── best_weight_clustering.py
    ├── clean_data.py
    ├── cluster_plot.py
    ├── dataset
    │   ├── cleaned_data.csv
    │   ├── mapping_dict.json
    │   └── 上证50成分股交易数据.csv
    ├── extras
    │   ├── clustering.py
    │   ├── exp_results.zip
    │   └── silhouette.py
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
    └── std_setup.py

13 directories, 19 files

```

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

### 'best_weight_clustering.py'
Use the grid point method to search for the optimal weight distribution of each DTW matrix under the condition of applying the contour coefficient evaluation results.

After our experiment, the recommended weight allocation and distance thresholds are as follows:

+ Weights
  + (0.5, 0.2, 0.2, 0.1)
  + (0.5, 0.1, 0.3, 0.1)
+ Distance-threshold
  + 8
  + 10
  + 12

The above $ 2 \times 3 = 6 $ combinations can show a good classification effect.

You can also apply your own weight allocation method with these two individual clustering programs. We also provide the experimental results under the recommended parameter settings under the `\extras` folder.

> Notes: Before using, copy these two under the `\extras` folder to the `\master` directory.

#### 'clustering.py'
Use hierarchical clustering algorithm to cluster stocks, distance:

$$ L_{\text{all}} = w_1 \times L_{\text{RAW}} + w_2 \times L_{\text{RSI}} + w_3 \times L_{\text{OBV}} + w_4 \times L_{\text{RR}} $$

Where:
- $RR$: Return Rate.
- $w_i$: Weight of each distance term, initially defined as $w_1 = 0.2$, $w_2 = 0.3$, $w_3 = 0.25$, $w_4 = 0.25$.

#### 'silhouette.py''
Use the contour coefficient method to evaluate the quality of clustering results.

### 'cluster_plot.py'
Draw the results of clustering.

## Folders
### dataset
Contains raw data, cleaned data and mapping dictionary json file.
> Put your raw data downloaded from web in this folder and modify the raw data path in 'clean_data.py' and 'std_setup.py'.

### results
All the results (plots and output files) are stored in this folder.

---

Created and edited by Highsun, any question: highsun910@gmail.com

**Last update**: 2024.11.26
