# https://zhuanlan.zhihu.com/p/59867869 如何利用欧奈尔的RPS寻找强势股
# https://zhuanlan.zhihu.com/p/55425806 Python量化策略风险指标

import datetime
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

token = '629a5fc9090b600286d4335136057650352d031dbb6d18e8d934adaf'
ts.set_token(token)
pro = ts.pro_api()


# 使用tushare获取上述股票周价格数据并转换为周收益率
# 设定默认起始日期为2018年1月5日，结束日期为2019年3月19日
# 日期可以根据需要自己改动
def get_data(code, start='20180101', end='20190319'):
    t_df = pro.daily(ts_code=code, start_date=start, end_date=end, fields='trade_date,close')
    # 将交易日期设置为索引值
    t_df.index = pd.to_datetime(t_df.trade_date)
    t_df = t_df.sort_index()
    # 计算收益率
    return t_df.close


# 计算收益率
def cal_ret(df, w=5):
    # w:周5;月20;半年：120; 一年250
    df = df / df.shift(w) - 1
    return df.iloc[w:, :].fillna(0)


# 计算RPS
def get_rps(ser):
    df = pd.DataFrame(ser.sort_values(ascending=False))
    df['n'] = range(1, len(df) + 1)
    df['rps'] = (1 - df['n'] / len(df)) * 100
    return df


# 计算每个交易日所有股票滚动w日的RPS
def all_rps(data):
    dates = (data.index).strftime('%Y%m%d')
    RPS = {}
    for i in range(len(data)):
        RPS[dates[i]] = pd.DataFrame(get_rps(data.iloc[i]).values, columns=['收益率', '排名', 'RPS'],
                                     index=get_rps(data.iloc[i]).index)
    return RPS


# 获取所有股票在某个期间的RPS值
def all_data(rps, ret):
    df = pd.DataFrame(np.NaN, columns=ret.columns, index=ret.index)
    for date in ret.index:
        date = date.strftime('%Y%m%d')
        d = rps[date]
        for c in d.index:
            df.loc[date, c] = d.loc[c, 'RPS']
    return df


def plot_rps(stock, df_new, data):
    plt.subplot(211)
    data[stock][120:].plot(figsize=(16, 16), color='r')
    plt.title(stock + '股价走势', fontsize=15)
    plt.yticks(fontsize=12)
    plt.xticks([])
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.subplot(212)
    df_new[stock].plot(figsize=(16, 8), color='b')
    plt.title(stock + 'RPS相对强度', fontsize=15)
    my_ticks = pd.date_range('2018-06-9', '2019-3-31', freq='m')
    plt.xticks(my_ticks, fontsize=12)
    plt.yticks(fontsize=12)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()


def stock_basic():
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    print(len(df))
    df = df[df['list_date'].apply(int).values < 20170101]
    print(len(df))

    # 获取当前所有非新股次新股代码和名称
    codes = df.ts_code.values
    names = df.name.values
    # 构建一个字典方便调用
    code_name = dict(zip(names, codes))
    # 构建一个空的dataframe用来装数据
    dataframe = pd.DataFrame()
    count = 0
    oldtime = datetime.datetime.now()
    for name, code in code_name.items():
        dataframe[name] = get_data(code)
        count = count + 1
        if count % 100 == 0:
            print('process ... : ' + str(count))
            newtime = datetime.datetime.now()
            print(u'相差：%s' % (newtime - oldtime))
            oldtime = datetime.datetime.now()
        # 有接口调用限制
        if count > 190:
            break
    # data.to_csv('daily_data.csv',encoding='gbk')
    # data=pd.read_csv('stock_data.csv',encoding='gbk',index_col='trade_date')
    # data.index=(pd.to_datetime(data.index)).strftime('%Y%m%d')
    ret120 = cal_ret(dataframe, w=120)
    rps120 = all_rps(ret120)
    # 构建一个以前面收益率为基础的空表
    df_new = pd.DataFrame(np.NaN, columns=ret120.columns, index=ret120.index)
    # 计算所有股票在每一个交易日的向前120日滚动RPS值。对股票价格走势和RPS进行可视化
    for date in df_new.index:
        date = date.strftime('%Y%m%d')
        d = rps120[date]
        for c in d.index:
            df_new.loc[date, c] = d.loc[c, 'RPS']
    # 查看2018年7月31日 - 2019年3月19日每月RPS情况。下面仅列出每个月RPS排名前十的股票，里面出现不少熟悉的“妖股”身影。
    dates = ['20180731', '20180831', '20180928', '20181031', '20181130', '20181228', '20190131', '20190228', '20190319']
    df_rps = pd.DataFrame()
    for date in dates:
        df_rps[date] = rps120[date].index[:50]

    plot_rps('东方通信', df_new, dataframe)


if __name__ == '__main__':
    stock_basic()
