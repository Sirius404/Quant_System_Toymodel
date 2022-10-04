import sys
sys.path.append(r'D:\Quant_System')
import PyQt5
import qdarkstyle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import json
import core.Plot
from UI.k_tab.kLineThread import KLineThread
from UI.k_tab.k_line_pic import KMplCanvas
from UI.tab_widget.mianThread import MainPlotThread
from UI.tab_widget.plateThread import plateThread
from UI.tab_widget.shareThread import ShareThread
from UI.tab_widget.stock_day_pic import StockMplCanvas
import matplotlib
import pandas as pd
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets
import os


pre = pd.read_csv('D:\Quant_System\Data\pre_data.csv')
df1 = pd.read_csv('D:\Quant_System\Data\stock.csv')
df = pd.concat([df1, pre])

class MyFigure(FigureCanvas):
    def __init__(self,width=5,height=4,dpi=100):
        self.fig = Figure(figsize=(width,height),dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.ax = self.fig.add_subplot(1,1,1)



class MyFrom(QMainWindow):
    def __init__(self):
        super(MyFrom, self).__init__()
        self.setWindowTitle('量化交易系统')
        self.resize(1100, 700)
        self.isListView = True

        self.init()

    def init(self):
        self.qTableWidget = QTabWidget()
        self.homeTab = QWidget()
        self.kTab2 = QWidget()
        self.strategyTab = QWidget()
        # self.nchTab = QWidget()
        self.qTableWidget.addTab(self.homeTab, "主页")
        self.qTableWidget.addTab(self.kTab2, "K线图")
        self.qTableWidget.addTab(self.strategyTab, "策略收益")
        # self.qTableWidget.addTab(self.nchTab, "北向资金")

        self.init_hometab()
        self.init_kTab()
        self.init_strategyTab()

        # self.init_nch()
        self.setCentralWidget(self.qTableWidget)
        # self.setupUi(self)

    # K线模块
    def init_kTab(self):
        self.grid_k = QGridLayout()
        self.grid_k.setSpacing(5)
        k_text = ['十字星', '两只乌鸦', '三只乌鸦']
        self.k_content = ['预示着当前趋势反转', '预示股价下跌', '预示股价下跌']
        self.K_method = ['CDLDOJISTAR', 'CDL2CROWS', 'CDL3BLACKCROWS']
        self.cb = QComboBox()
        self.cb.addItems(k_text)
        self.cb.currentIndexChanged.connect(self.selectionchange)
        self.cb_label = QLabel("预示着当前趋势反转")
        self.k_label = QLabel("选择K线图的形态：")
        self.grid_k.addWidget(self.k_label, 0, 0, 1, 1)
        self.grid_k.addWidget(self.cb, 0, 2, 1, 2)
        self.grid_k.addWidget(self.cb_label, 0, 5, 1, 5)
        self.kTab2.setLayout(self.grid_k)
        self.kLineThread = KLineThread()
        self.kLineThread.setValue("sh600690")
        self.kLineThread._signal.connect(self.kLineThread_callbacklog)
        self.kLineThread.start()

    def kLineThread_callbacklog(self, df):
        self.df = df
        self.mplK = KMplCanvas(self, width=5, height=4, dpi=100)
        self.mplK.start_staict_plot(df)
        mpl_ntb = NavigationToolbar(self.mplK, self)
        mpl_ntb.setStyleSheet("background-color:white;color:black")

        self.grid_k.addWidget(self.mplK, 2, 0, 13, 12)
        self.grid_k.addWidget(mpl_ntb, 2, 0, 1, 5)

    def selectionchange(self, i):
        self.cb_label.setText(self.k_content[i])
        self.mplK.start_staict_plot(self.df, self.K_method[i], i)

        # #

    def init_strategyTab(self):
        self.pushButton = QtWidgets.QPushButton(self.strategyTab)
        self.pushButton.setGeometry(QtCore.QRect(720, 90, 251, 101))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.strategyTab)
        self.label.setGeometry(QtCore.QRect(100, 80, 541, 91))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.strategyTab)
        self.pushButton_2.setGeometry(QtCore.QRect(720, 270, 251, 101))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_2 = QtWidgets.QLabel(self.strategyTab)
        self.label_2.setGeometry(QtCore.QRect(100, 250, 541, 141))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.strategyTab)
        self.pushButton_3.setGeometry(QtCore.QRect(720, 450, 251, 101))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_3 = QtWidgets.QLabel(self.strategyTab)
        self.label_3.setGeometry(QtCore.QRect(100, 450, 541, 91))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    # #这一部分是预留的触发，参考文献：https://blog.csdn.net/weixin_42267309/article/details/103517140
        self.pushButton.clicked.connect(self.turtle)
        self.pushButton_2.clicked.connect(self.KDJ)
        self.pushButton_3.clicked.connect(self.MA)
    #
    def turtle(self):
        core.Plot.turtle_plot(df,df1)  # 运行main.py模块里的主函数

    def KDJ(self):
        core.Plot.KDJ_plot(df,df1)  # 运行main.py模块里的主函数

    def MA(self):
        core.Plot.MA_plot(df,df1) # 运行main.py模块里的主函数
    # # 这一部分是预留的触发，参考文献：https://blog.csdn.net/weixin_42267309/article/details/103517140

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.pushButton.setText(_translate("MainWindow", "海龟交易策略"))
        self.label.setText(_translate("MainWindow", "海龟交易策略：利用唐安奇通道来跟踪趋势产生买卖信号，利用ATR（真实波幅均值）分批加仓或者减仓，并且动态进行止盈和止损。"))
        self.pushButton_2.setText(_translate("MainWindow", "KDJ交易策略"))
        self.label_2.setText(_translate("MainWindow", "KDJ交易策略：KDJ指标主要是研究最高价、最低价和收盘价之间的关系，同时也融合了动量观念、强弱指标和移动平均线的一些优点，能够比较迅速、快捷、直观地研判行情。"))
        self.pushButton_3.setText(_translate("MainWindow", "移动平均策略"))
        self.label_3.setText(_translate("MainWindow", "移动平均策略：能够反映价格趋势走向，可以帮助交易者确认现有趋势、判断将出现的趋势、发现过度延生即将反转的趋势。"))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))

    # 主页模块
    def init_hometab(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        ft = QFont()
        ft.setPointSize(26)
        ft.setBold(True)
        self.share_params = [QLabel() for x in range(10)]
        self.grid.addWidget(self.share_params[0], 0, 0, 2, 3)
        self.share_params[0].setFont(ft)
        self.share_params[0].setStyleSheet("color:yellow")
        self.grid.addWidget(self.share_params[1], 0, 3, 1, 2)
        self.share_params[1].setFont(ft)
        self.grid.addWidget(self.share_params[2], 0, 5)
        self.grid.addWidget(self.share_params[3], 0, 6)
        self.grid.addWidget(self.share_params[4], 0, 7)
        self.grid.addWidget(self.share_params[5], 1, 3)
        self.grid.addWidget(self.share_params[6], 1, 4)
        self.grid.addWidget(self.share_params[7], 1, 5)
        self.grid.addWidget(self.share_params[8], 1, 6)
        self.grid.addWidget(self.share_params[9], 1, 7)
        self.shareThread = ShareThread()
        self.shareThread.setValue()
        self.shareThread._signal.connect(self.shareThread_callbacklog)
        self.shareThread.start()

        self.qListOne = ['上证指数', '深证成指', '创业板指', '科创50', '上证50', '中证500', '沪深300']  # 添加的数组数据
        self.plateThread = plateThread()
        self.plateThread._signal.connect(self.plateThread_callbacklog)
        self.plateThread.start()
        self.homeTab.setLayout(self.grid)

        self.mainThread = MainPlotThread()
        self.mainThread.setValue("sh600690")
        self.mainThread._signal.connect(self.mianThread_callbacklog)
        self.mainThread._orderList.connect(self.orderThread_callbacklog)
        self.mainThread.start()

    def mianThread_callbacklog(self, df):
        mpl = StockMplCanvas(self, width=5, height=4, dpi=100)
        mpl.start_staict_plot(df)
        mpl_ntb = NavigationToolbar(mpl, self)
        mpl_ntb.setStyleSheet("background-color:white;color:black")

        self.grid.addWidget(mpl, 2, 0, 12, 12)
        self.grid.addWidget(mpl_ntb, 2, 0, 1, 5)

    def shareThread_callbacklog(self, shareList):
        isloss = float(shareList[5])
        i = 0
        for share_label, qlist in zip(self.share_params, shareList):
            if i == 1:
                share_label.setText(str(qlist))
                if isloss >= 0:
                    share_label.setStyleSheet("color:red")
                else:
                    share_label.setStyleSheet("color:rgb(0, 255, 0)")
            else:
                share_label.setText(str(qlist))
            i += 1

    def plateThread_callbacklog(self, urlList):
        i = 0
        one_QLabel = [QLabel() for x in range(7)]
        two_QLabel = [QLabel() for x in range(7)]
        for o_label, t_label, qlist, m_name in zip(one_QLabel, two_QLabel, urlList, self.qListOne):
            temp = qlist.split('"')[1].split(',')
            isloss = float(str(round(float(temp[2]), 2)))
            if isloss >= 0:
                o_label.setStyleSheet("color:red;font-size:14px")
                t_label.setStyleSheet("color:red;font-size:14px")
            else:
                o_label.setStyleSheet("color:rgb(0, 255, 0);font-size:14px")
                t_label.setStyleSheet("color:rgb(0, 255, 0);font-size:14px")
            o_label.setText(m_name)
            self.grid.addWidget(o_label, 0, 8 + i, 1, 1)
            t_label.setText(str(round(float(temp[1]), 2)))
            self.grid.addWidget(t_label, 1, 8 + i, 1, 1)
            i += 1

    # 指数显示模块
    def tableWidget_connect(self, item):
        QMessageBox.information(self, "QTableWidget", "你选择了" + item.text())

    def orderThread_callbacklog(self, urlList):
        ft = QFont()
        ft.setPointSize(10)
        ft.setBold(True)
        m_color = None
        j = 0
        if not self.isListView:
            self.tableWidget.clear()
            self.tableWidget.setHorizontalHeaderLabels(['性质', '成交量(手)', '成交额(元)'])
            for qlist in urlList:
                for index, m_dict in enumerate(qlist):
                    if index == 0:
                        if str(m_dict).strip() == "买盘":
                            m_color = QColor(255, 0, 0)
                        elif str(m_dict).strip() == "卖盘":
                            m_color = QColor(0, 255, 0)
                        else:
                            m_color = QColor(255, 255, 255)
                    newItem = QTableWidgetItem(str(m_dict))
                    newItem.setFont(ft)
                    newItem.setForeground(QBrush(m_color))
                    self.tableWidget.setItem(j, index, newItem)
                j += 1
        else:
            # 各个板块指数
            self.tableWidget = QTableWidget(len(urlList), 3)
            self.tableWidget.setHorizontalHeaderLabels(['性质', '成交量(手)', '成交额(元)'])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不可编辑
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # 禁止拖拽
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 只能选中一行
            self.tableWidget.itemClicked.connect(self.tableWidget_connect)
            self.tableWidget.verticalHeader().setVisible(False)
            self.tableWidget.setShowGrid(False)  # 不显示子线条
            self.tableWidget.setColumnWidth(0, 70)  # 设置第一列宽
            self.tableWidget.setColumnWidth(1, 70)  # 设置第二列宽
            self.tableWidget.setColumnWidth(2, 70)  # 设置第三列宽
            for qlist in urlList:
                for index, m_dict in enumerate(qlist):
                    if index == 0:
                        if str(m_dict).strip() == "买盘":
                            m_color = QColor(255, 0, 0)
                        elif str(m_dict).strip() == "卖盘":
                            m_color = QColor(0, 255, 0)
                        else:
                            m_color = QColor(255, 255, 255)
                    newItem = QTableWidgetItem(str(m_dict))
                    newItem.setFont(ft)
                    newItem.setForeground(QBrush(m_color))
                    self.tableWidget.setItem(j, index, newItem)
                j += 1
            self.grid.addWidget(self.tableWidget, 2, 12, 12, 4)
            self.isListView = False
        self.tableWidget.scrollToBottom()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    myUI = MyFrom()
    myUI.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)  # 禁止放大界面
    myUI.setFixedSize(myUI.width(), myUI.height())  # 静止拖拽放大界面
    myUI.show()
    sys.exit(app.exec_())
