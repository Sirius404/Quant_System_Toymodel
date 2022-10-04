#coding:utf-8
import pandas as pd
import core.strateg as st
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.figsize'] = (15,8)
plt.rcParams['axes.unicode_minus']=False

pre = pd.read_csv('D:\Quant_System\Data\pre_data.csv')
df1 = pd.read_csv('D:\Quant_System\Data\stock.csv')
df1 = df1[int(len(df1)*0.9):]
df = pd.concat([df1,pre])

def turtle_plot(df, df1):
    cumStock, cumTrade = st.Strategy().turtle_strategy(df=df)
    # plt.figure(figsize=(20,10),dpi=80)


    plt.subplot(2,2,1)
    plt.plot(df['trade_date'][:len(df1)], cumStock[:len(df1)], label="直接持有", color='b')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("直接持有收益率")
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(df['trade_date'][:len(df1)], cumTrade[:len(df1)], label="海龟交易策略", color='r')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("海龟交易策略收益率")
    plt.legend()

    plt.subplot(2,2,3)
    plt.plot(df['trade_date'][len(df1):], cumStock[len(df1):], label="直接持有(预测)", color='k')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("海龟交易策略收益率(预测)")
    plt.legend()

    plt.subplot(2,2,4)
    plt.plot(df['trade_date'][len(df1):], cumTrade[len(df1):], label="海龟交易策略(预测)", color='g')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("直接持有收益率(预测)")
    plt.legend()

    plt.show()

def KDJ_plot(df,df1):
    ret, trade_ret = st.Strategy().KDJ_Strategy(df=df)
    # plt.figure(figsize=(20,10),dpi=80)


    plt.subplot(2,2,1)
    plt.plot(df['trade_date'][:len(df1)], ret[:len(df1)], label="直接持有", color='b')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("直接持有收益率")
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(df['trade_date'][:len(df1)], trade_ret[:len(df1)], label="KDJ策略", color='r')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("KDJ指标交易策略收益率")
    plt.legend()

    plt.subplot(2,2,3)
    plt.plot(df['trade_date'][len(df1):-1], ret[len(df1):], label="直接持有(预测)", color='k')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("直接持有收益率(预测)")
    plt.legend()

    plt.subplot(2,2,4)
    plt.plot(df['trade_date'][len(df1):-1], trade_ret[len(df1):], label="KDJ策略(预测)", color='g')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("KDJ指标交易策略收益率(预测)")
    plt.legend()


    plt.show()

def MA_plot(df,df1):
    cumStock, cumTrade = st.Strategy().Moving_Average_Strategy(df)
    # plt.figure(figsize=(20,10),dpi=80)


    plt.subplot(2,2,1)
    plt.plot(df['trade_date'][:len(df1)], cumStock[:len(df1)], label="直接持有", color='b')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("直接持有收益率")
    plt.legend()

    plt.subplot(2,2,2)
    plt.plot(df['trade_date'][:len(df1)], cumTrade[:len(df1)], label="移动平均策略", color='r')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=360))
    plt.title("移动平均策略收益率")
    plt.legend()

    plt.subplot(2,2,3)
    plt.plot(df['trade_date'][len(df1):], cumStock[len(df1):], label="直接持有(预测)", color='k')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("直接持有收益率(预测)")
    plt.legend()

    plt.subplot(2,2,4)
    plt.plot(df['trade_date'][len(df1):], cumTrade[len(df1):], label="移动平均策略(预测)", color='g')
    at = plt.gca()
    at.xaxis.set_major_locator(tick.MultipleLocator(base=10))
    plt.title("移动平均策略收益率(预测)")
    plt.legend()

    plt.show()














