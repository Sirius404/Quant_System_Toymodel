import akshare as ak
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from pandas import DataFrame


class MainPlotThread(QtCore.QThread):
    _signal = pyqtSignal(DataFrame)
    _orderList = pyqtSignal(list)
    def setValue(self, shareNumber):
        self.share_num = shareNumber

    def run(self):
        self.list = []
        df = pd.read_excel(r"D:\Quant_System\Data\tick.xlsx")
        self._signal.emit(df)
        self.list.clear()
        for index, row in df.iterrows():
            self.list.append([row['type'], row['volume'], row['amount']])
        self._orderList.emit(self.list)
