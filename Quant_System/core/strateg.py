import pandas as pd
import talib
import numpy as np
import ffn
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys
sys.path.append(r"D:\Quant_System\core")
# from core.FengKong import tmp_if_send_email

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus']=False
xx = (talib)



class Strategy():

    def turtle_strategy(self, df):

        # 读取数据
        df.index = pd.to_datetime(df.trade_date, format='%Y-%m-%d')  # 设置日期索引

        T = 24
        atr1 = talib.ATR(df['high'].values, df['low'].values, df['close'].values, timeperiod=T)
        atr = pd.DataFrame(atr1)
        atr = atr.sort_index()
        atr.index = pd.to_datetime(df['trade_date'], format='%Y-%m-%d')  # 设置日期索引
        atr = atr.fillna(0)
        mv = talib.MA(np.array(df.close), timeperiod=T)
        close10 = mv + 0.5 * atr1
        close100 = mv + atr1
        close1000 = mv + 1.5 * atr1
        unit = 10000 / (100 * atr1[-1])
        close10_ = mv - 0.5 * atr1
        close100_ = mv - atr1
        close1000_ = mv - 1.5 * atr1
        unit = 10000 / (100 * atr1[-1])
        # 收市股价
        close = df.close
        # 每天的股价变动百分率
        ret = df['change'] / df['close']

        SmaSignal = pd.Series(0, index=close.index)
        s = 0
        k = 0
        for i in range(T, len(close)):
            if all([close[i] > close10[i], SmaSignal[i - 1] < 100, close[i] < close100[i]]):
                SmaSignal[i] = 1 + SmaSignal[i - 1]

            elif all([close[i] > close100[i], SmaSignal[i - 1] <= 96, close[i] < close1000[i]]):
                SmaSignal[i] = 4 + SmaSignal[i - 1]
            elif all([close[i] > close100[i], SmaSignal[i - 1] <= 100, close[i] < close1000[i]]):
                SmaSignal[i] = 100
            elif all([close[i] > close1000[i], SmaSignal[i - 1] <= 100]):
                SmaSignal[i] = 100
            elif all([close[i] < close10_[i], SmaSignal[i - 1] > 0, close[i] > close100_[i]]):
                SmaSignal[i] = SmaSignal[i - 1] - 1
            elif all([close[i] < close100_[i], SmaSignal[i - 1] >= 4, close[i] < close1000_[i]]):
                SmaSignal[i] = SmaSignal[i - 1] - 4
            elif all([close[i] < close100_[i], SmaSignal[i - 1] >= 0, close[i] < close1000_[i]]):
                SmaSignal[i] = 0
            elif all([close[i] < close1000_[i], SmaSignal[i - 1] <= 100]):
                SmaSignal[i] = 0
            else:
                SmaSignal[i] = SmaSignal[i - 1]

        SmaTrade = SmaSignal.shift(1).dropna() / 100  # shift(1)整体下移一行
        # SmaBuy=SmaTrade[SmaTrade==1]
        # SmaSell=SmaTrade[SmaTrade==-1]
        SmaRet = ret * SmaTrade.dropna()

        cumStock = np.cumprod(1 + ret[SmaRet.index[0:]]) - 1
        # 策略累积收益率
        cumTrade = np.cumprod(1 + SmaRet) - 1

        f = cumTrade[-2] * 250 / len(close)
        f1 = 100 * f #f1为年化收益率

        # tmp_if_send_email;
        return cumTrade, cumStock

    def KDJ_Strategy(self, df):
        def trade(signal, price):
            ret = ((price - price.shift(1)) / price.shift(1))[1:]  # 变化量
            ret.name = 'ret'
            signal = signal.shift(1)[1:]
            tradeRet = ret * signal + 0
            tradeRet.name = 'tradeRet'
            Returns = pd.merge(pd.DataFrame(ret), pd.DataFrame(tradeRet), left_index=True,
                               right_index=True).dropna()
            return (Returns)

        def backtest(ret, tradeRet):
            def performance(x):
                winpct = len(x[x > 0]) / len(x[x != 0])
                annRet = (1 + x).cumprod() ** (245 / len(x)) - 1
                sharpe = ffn.calc_risk_return_ratio(x)
                maxDD = ffn.calc_max_drawdown((1 + x).cumprod())
                perfo = pd.Series([winpct, annRet, sharpe, maxDD],
                                  index=['win rate', 'annualized                          return', 'sharpe ratio',
                                         'maximum drawdown'])
                return (perfo)

            BuyAndHold = performance(ret)
            Trade = performance(tradeRet)
            return (pd.DataFrame({ret.name: BuyAndHold, tradeRet.name: Trade}))

        df.index = pd.to_datetime(df.trade_date, format='%Y-%m-%d')  # 设置日期索引

        # 收市股价
        close = df['close']
        highPrice = df['high']
        lowPrice = df['low']
        # 每天的股价变动百分率
        ret = df['change'] / 100
        # 调用talib计算MACD指标
        df['k'], df['d'] = talib.STOCH(np.array(highPrice), np.array(lowPrice), np.array(close),
                                       fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        # money = 10000
        # num = 0
        sig_k = df.k
        sig_d = df.d
        sig_j = df.k * 3 - df.d * 2

        KSignal = sig_k.apply(lambda x: -1 if x > 85 else 1 if x < 20 else 0)
        DSignal = sig_d.apply(lambda x: -1 if x > 80 else 1 if x < 20 else 0)
        JSignal = sig_j.apply(lambda x: -1 if x > 100 else 1 if x < 0 else 0)

        KDJSignal = KSignal + DSignal + JSignal
        KDJSignal = KDJSignal.apply(lambda x: 1 if x >= 2 else -1 if x <= -2 else 0)

        KDJtrade = trade(KDJSignal, df['close'])
        KDJtrade.rename(columns={'ret': 'Ret', 'tradeRet': 'KDJtradeRet'}, inplace=True)
        backtest(KDJtrade.Ret, KDJtrade.KDJtradeRet)

        KDJCumRet = (1 + KDJtrade).cumprod()

        # 对KDJ交易策略进行回测

        # plt.figure(figsize=(10, 6))
        #
        # plt.plot(KDJCumRet.Ret, label='Ret')
        # plt.plot(KDJCumRet.KDJtradeRet, '--', label='KDJtradeRet')
        #
        # plt.title('KDJ指标交易策略绩效表现')
        # plt.legend(loc='upper left')
        # plt.show()


        # tmp_if_send_email;
        return KDJCumRet.Ret, KDJCumRet.KDJtradeRet

    # def Trend_momentum_Strategy(self):
    #     ts.set_token('7cc44d29a128bad59dbd055c75cdf07bab5e9ef3cb3f1aef9bab9cf2')  # 这里的token已改成我们自己的了
    #     pro = ts.pro_api()
    #     stock_info = json.load(open('../JSON/stock_info.json', 'r'))
    #     dsc1 = pro.index_daily(ts_code=stock_info['ts_code'], start_date=stock_info['start_date'],
    #                            end_date=stock_info['end_date'])
    #     dc = dsc1.set_index(dsc1.trade_date).sort_index(ascending=True)
    #     dc.index = pd.to_datetime(dc.index, format="%Y-%m-%d")
    #     ret = (dc.close - dc.close.shift(1)) / dc.close.shift(1)
    #     ret = ret.sort_index(ascending=True)
    #
    #     T = 55
    #
    #     ###信号判断#####
    #     sig = pd.Series(0, index=dc.index)
    #     for i in range(math.floor(len(ret) / T) - 2):
    #         if dc.close[(1 + i) * T] > dc.close[i * T] + 50:
    #             for j in range((i + 1) * T + 1, (i + 2) * T + 1):
    #                 sig[j] = 1
    #     sig = sig.tail(len(sig) - T)
    #     RET = ret * sig
    #     cum = np.cumprod(RET + 1).dropna()
    #
    #     ############################################################################
    #
    #     def Tongji(cum):
    #         cum = cum.sort_index()
    #         NH = (cum[-1] - 1) * 100 * 252 / len(cum.index)
    #         BD = np.std(np.log(cum / cum.shift(-1))) * np.sqrt(252) * 100
    #         SR = (NH - 4) / BD
    #         return_list = cum
    #         MHC = ((np.maximum.accumulate(return_list) - return_list) / np.maximum.accumulate(return_list)).max() * 100
    #         print("年化收益率：{:.2f}%:，年化夏普率：{:.2f},波动率为：{:.2f}%,最大回撤：{:.2f}%".format(NH, SR, BD, MHC))
    #
    #     JZ = dc.close.tail(len(cum)) / dc.close.tail(len(cum))[0]  # 上证指数净值\
    #     print("组合策略：")
    #     Tongji(cum)
    #     print("直接持有：")
    #     Tongji(JZ)
    #     plt.plot(JZ, label="000001.SH", color='b', linestyle='-')
    #     plt.plot(cum, label="策略", color='r', linestyle='-')
    #     plt.title("净值走势")
    #     plt.legend()
    #     plt.show()

    def Moving_Average_Strategy(self,df):
        df.index = pd.to_datetime(df.trade_date, format='%Y-%m-%d')
        #####如果有其他数据库，可以直接从这开始####
        # 收市股价
        close = df.close
        # 每天的股价变动百分率
        ret = df.change / df.close

        # 8日的移动均线
        df1 = talib.MA(np.array(close), timeperiod=8)  # 调用talib的移动平均函数
        close8 = df1

        # 处理
        SmaSignal = pd.Series(0, index=close.index)
        s = 0
        k = 0
        for i in range(8, len(close)):
            if all([close[i] > close8[i], close[i - 1] < close8[i - 1]]):  # 买入条件
                SmaSignal[i] = 1
                k += 1

            elif all([close[i] < close8[i], close[i - 1] > close8[i - 1]]):  # 卖出
                SmaSignal[i] = 0
                k += 1
            else:
                SmaSignal[i] = SmaSignal[i - 1]
            s = s + SmaSignal[i]
            ds = len(close) - s

        SmaTrade = SmaSignal.shift(1).dropna()  # shift(1)表示整体下移一行  ，dropna表示删除NAN数据
        SmaBuy = SmaTrade[SmaTrade == 1]  # 这行没啥卵用，解释作用，注释掉一样的
        SmaSell = SmaTrade[SmaTrade == -1]  # 也没啥用
        SmaRet = ret * SmaTrade.dropna()  # 关键一行，将股价变动×信号序列，信号序列只有0  或 1 ，对应做多，做空。

        # 股票累积收益率
        cumStock = np.cumprod(1 + ret[SmaRet.index[0:]]) - 1
        # 策略累积收益率
        cumTrade = np.cumprod(1 + SmaRet) - 1
        # plt.rcParams['font.sans-serif']=['SimHei']
        # plt.plot(cumTrade, label="cumTrade", color='r', linestyle=':')
        # plt.plot(cumStock, label="cumStock", color='k')
        # plt.title("股票累积收益率与8日平均策略收益率")
        # plt.legend()
        # plt.show()
        # print("组合年化收益率：{}".format(cumTrade[-2] * 250 / len(close)))
        # print("操作{}次,,空头天数{},多头天数{}".format(k, s, ds))

        return cumStock, cumTrade

    def MACD_strategy(self, df):

        def indicators(df):
            # 取历史数据，取到上市首日
            data = df

            # 将数据转化为dataframe格式
            # data['bob'] = data['bob'].apply(lambda x: x.strftime('%Y-%m-%d')).tolist()

            # 计算EMA(12)和EMA(16)
            data['EMA12'] = data['close'].ewm(alpha=2 / 13, adjust=False).mean()
            data['EMA26'] = data['close'].ewm(alpha=2 / 27, adjust=False).mean()

            # 计算DIFF、DEA、MACD
            data['DIFF'] = data['EMA12'] - data['EMA26']
            data['DEA'] = data['DIFF'].ewm(alpha=2 / 10, adjust=False).mean()
            data['MACD'] = 2 * (data['DIFF'] - data['DEA'])

            # 上市首日，DIFF、DEA、MACD均为0
            data['DIFF'].iloc[0] = 0
            data['DEA'].iloc[0] = 0
            data['MACD'].iloc[0] = 0

            # 按照起止时间筛选
            indictitors = data

            return indictitors

        indicator = indicators(df)

        DIFF = indicator['DIFF'].astype(float)
        DEA = indicator['DEA'].astype(float)
        MACD = indicator['MACD'].astype(float)
        close = indicator['close'].astype(float)
        ret = indicator.change / 100
        Trade_Ret = ret


        indicator['Signal'] = 0
        indicator['ret'] = 0
        indicator.ret = close / close.shift(1) - 1.0
        for i in range(len(indicator)):
            if DIFF[i] > DEA[i] and DEA[i] < 0 and DIFF[i] - DEA[i] < 0.2 :
                indicator['Signal'][i] = 1
            if DIFF[i] >= DEA[i] and DEA[i] > 0 and DIFF[i] - DEA[i] < 0.2 :
                indicator['Signal'][i] = 1
            if DIFF[i] <= DEA[i] and DEA[i] > 0 and DEA[i] - DIFF[i] > 0.6:
                indicator['Signal'][i] = -1
        #     ret.append(money)
        # ret[i] = ret.apply(lambda ret[i-1]:)

        # plt.plot(Trade_Ret, label='Trade', color='r',linestyle=':')
        # plt.legend()
        # plt.show()
        indicator['income'] = indicator['ret'] * indicator['Signal'].shift(1)
        # plt.plot(indicator['income'], color='r', label='日收益率')
        # plt.plot(indicator['income'].cumsum(), color='g', label='累计收益率')
        #
        # # plt.plot(ret, label='stock', color='k')
        # plt.legend()
        # plt.show()
        #
        # tmp_if_send_email;
        return indicator['income'], indicator['income'].cumsum()

