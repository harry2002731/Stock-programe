import sys

import tkinter
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

from UIeilson2 import Ui_MainWindow
from Data_convert import *
import config
import fuzzyfinder
from utility import *
from Gain_lose import *
from Earning_compare import Earning_compare
from Fetch_stock_data import Fetch_stock_data
from CandlestickItem import CandlestickItem
from AmountstickItem import AmountstickItem
from MA_chart import MA_chart


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        global ui
        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.setMouseTracking(True)
        ui.custom_edit.textChanged.connect(self.custom_edit_textChanged)
        ui.listWidget.itemClicked.connect(self.listWidget_selectionChange)
        ui.listWidget.itemSelectionChanged.connect(self.listWidget_selectionChange)
        ui.listWidget_2.itemClicked.connect(self.listWidget2_selectionChange)
        ui.listWidget_2.itemSelectionChanged.connect(self.listWidget_selectionChange)

        ui.pushButton.clicked.connect(self.appendToInteringStockList)  #添加到自选股
        ui.pushButton_2.clicked.connect(self.moveFromInteringStockList)  #移除自选股

        ui.pushButton_3.clicked.connect(self.recommendStockCal)  #荐股计算

        # self.region = pg.LinearRegionItem()
        # self.region.setZValue(10)
        # self.region.sigRegionChanged.connect(self.update)
        
        #添加自选股    
        ui.listWidget_2.clear()
        rec=config.interestingStockList
        if rec:
            for i in range(len(rec)):
                ui.listWidget_2.addItem(list(rec.keys())[i])

        #添加股票代码
        rec=config.Stock_list
        if rec:
            for i in range(len(rec)):
                ui.listWidget.addItem(list(rec.keys())[i])

        root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
        root.withdraw()  # 将Tkinter.Tk()实例隐藏

        """header 表头  stock_data 数据类型 int(t), str(trade_date), float(open), float(close), float(low),
        float(high), float(vol), float(change), float(pct_chg)) """
    def recommendStockCal(self):
        ec = Earning_compare()
        # ec = Earning_compare.



    def appendToInteringStockList(self):
        text = ui.listWidget.currentItem().text()
        ui.listWidget_2.addItem(text)
        #保存自选股名单

    def moveFromInteringStockList(self):
        text = ui.listWidget_2.currentItem().text()
      
        for i in range(ui.listWidget_2.count()):            
            item = ui.listWidget_2.item(i).text()
            if text==item:
                ui.listWidget_2.takeItem(i)

    def custom_edit_textChanged(self,event):
        # if event != '':
        try:

            rec=fuzzyfinder.fuzzyfinder(event, config.Stock_list.keys())
            ui.listWidget.clear()
            if rec:
                for i in range(len(rec)):
                    ui.listWidget.addItem(rec[i])
            else:
                self.setText(event)
        except Exception:
            pass

    def listWidget2_selectionChange(self):
        text = ui.listWidget_2.currentItem().text()
        self.stockclick(text)

    def stockclick(self,text):
        Datalist = Fetch_stock_data()
        Datalist.ini(config.Stock_list[text])

        if ui.verticalLayout.count()==0:

            Moving_data = Datalist.Data_form_list.Moving_datum
            cdst = CandlestickItem(Datalist.Data_form_list.Candle_datum, Moving_data, 400)
            cdst1 = AmountstickItem(Datalist.Data_form_list.Amount_datum, 400)
            ui.verticalLayout.addWidget(cdst.plt)
            ui.verticalLayout.addWidget(cdst1.plt)
            list = Calculation(Moving_data)


            d=Mat_picture(list.earning_x, list.earning_y)
            ui.verticalLayout_2.addWidget(cdst.plt)
            ui.verticalLayout_2.addWidget(d.win)
        else:
            for i in range(ui.verticalLayout.count()):
                ui.verticalLayout.itemAt(i).widget().deleteLater()
            for i in range(ui.verticalLayout_2.count()):
                ui.verticalLayout_2.itemAt(i).widget().deleteLater()
            Moving_data = Datalist.Data_form_list.Moving_datum
            cdst = CandlestickItem(Datalist.Data_form_list.Candle_datum, Moving_data, 400)
            cdst1 = AmountstickItem(Datalist.Data_form_list.Amount_datum, 400)
            ui.verticalLayout.addWidget(cdst.plt)
            ui.verticalLayout.addWidget(cdst1.plt)
            list = Calculation(Moving_data)
            d = Mat_picture(list.earning_x, list.earning_y)
            ui.verticalLayout_2.addWidget(cdst.plt)
            ui.verticalLayout_2.addWidget(d.win)


    def listWidget_selectionChange(self):
        text = ui.listWidget.currentItem().text()
        self.stockclick(text)
        




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
