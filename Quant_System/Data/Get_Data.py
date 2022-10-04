#-*-coding:utf-8-*-
import tushare as ts
import json
from chinese_calendar import is_workday
import datetime
import time
import os
import pandas as pd

os.chdir('D:\Quant_System\Data')
delta = datetime.timedelta(days=1)
cur = datetime.datetime.now().date()-delta

ts.set_token('7cc44d29a128bad59dbd055c75cdf07bab5e9ef3cb3f1aef9bab9cf2')
stock_info = json.load(open('D:\Quant_System\Json\stock_info.json', 'r'))
pro = ts.pro_api()

def getworkday(cur):
    if is_workday(cur):
        return cur
    while not is_workday(cur):
        cur -= delta
        if is_workday(cur):
            return cur

workday = getworkday(cur)


def get_tick_data():
    df = ts.get_tick_data(code=stock_info['ts_code'], src='tt', date=str(workday))
    df.to_excel('tick.xlsx')
    return df


def get_trade_data():
    df = pro.query('daily', ts_code=(stock_info['ts_code']+".sh"), start_date=stock_info['start_date'],
                   end_date=stock_info['end_date'])
    df['trade_date'] = pd.to_datetime(df['trade_date'],format="%Y-%m-%d")
    df.sort_values(by='trade_date', inplace=True)
    df.to_csv('stock.csv',index=False)
get_trade_data()

import core.model

def get_pre_data():
    get_trade_data()
    pre_data = core.model.get_pre()
    pre_data.to_csv('pre_data.csv',index=False)

def data_process():
    df = pd.read_csv('stock.csv')
    pre_data = pd.read_csv('pre_data.csv')
    pre_data['change'] = pre_data['close'].diff()
    pre_data['change'][0] = pre_data['close'][0]-df.iloc[-1]['close']
    df['trade_date'] = df['trade_date'].apply(lambda x: pd.to_datetime(str(x)).strftime("%Y-%m-%d"))
    df.to_csv('stock.csv', index=False)
    pre_data.to_csv('pre_data.csv', index=False)

if __name__ == '__main__':
    get_pre_data()
    get_tick_data()
    data_process()









