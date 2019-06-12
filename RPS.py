# https://zhuanlan.zhihu.com/p/59867869 如何利用欧奈尔的RPS寻找强势股
# https://zhuanlan.zhihu.com/p/55425806 Python量化策略风险指标

import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt

from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

token = '629a5fc9090b600286d4335136057650352d031dbb6d18e8d934adaf'
ts.set_token(token)
pro = ts.pro_api()

df = pro.stock_basic(exchange='', list_status='L',
                     fields='ts_code,symbol,name,area,industry,list_date')
print(len(df))

df = df[df['list_date'].apply(int).values < 20170101]
print(len(df))
