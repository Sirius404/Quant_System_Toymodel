from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import pandas as pd
from pandas import DataFrame

class KLineThread(QtCore.QThread):
    _signal = pyqtSignal(DataFrame)

    def __init__(self):
        super(KLineThread, self).__init__()

    def setValue(self, shareNumber):
        self.share_num = shareNumber

    def run(self):
        df = pd.read_csv("D:\Quant_System\Data\stock.csv")
        self._signal.emit(df)
