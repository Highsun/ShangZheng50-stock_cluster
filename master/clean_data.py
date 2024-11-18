import numpy as np
import pandas as pd
import json

data = pd.read_csv('./dataset/上证50成分股交易数据.csv', index_col='code',encoding='utf-8')

print(data.head(5))
# data.info() # check!

## mapping code to name
mapping = data.reset_index().iloc[:, :2]
mapping = mapping.iloc[::5]
mapping.columns = ['code', 'code_name']
mapping_dict = mapping.set_index('code')['code_name'].to_dict()
print(mapping_dict)

with open('./dataset/mapping_dict.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_dict, f, ensure_ascii=False, indent=4)

## Process the data
data_numeric = data.select_dtypes(include=[np.number])

data_numeric.columns = pd.to_datetime(data_numeric.columns)
# print(data_numeric.columns)

data_numeric.head(5)
# print(data_numeric.info()) # check!
data_numeric.isnull().sum() # check!
data_numeric.T.describe() # check!

data_numeric.to_csv('./dataset/cleaned_data.csv', encoding='utf-8')