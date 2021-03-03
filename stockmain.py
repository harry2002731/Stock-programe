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
from earning_Compare import earning_Compare
from Fetch_stock_data import Fetch_stock_data
from CandlestickItem import CandlestickItem
from AmountstickItem import AmountstickItem
from MA_chart import MA_chart


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        global ui
        # global custom_edit

        ui = Ui_MainWindow()
        ui.setupUi(self)

        self.setMouseTracking(True)
        ui.custom_edit.textChanged.connect(self.custom_edit_textChanged)
        ui.listWidget.itemClicked.connect(self.listWidget_selectionChange)
        ui.listWidget.itemSelectionChanged.connect(self.listWidget_selectionChange)
        ui.listWidget_2.itemClicked.connect(self.listWidget2_selectionChange)
        ui.listWidget_2.itemSelectionChanged.connect(self.listWidget2_selectionChange)

        ui.pushButton.clicked.connect(self.appendToInteringStockList)  # 添加到自选股
        ui.pushButton_2.clicked.connect(self.moveFromInteringStockList)  # 移除自选股
        ui.pushButton_3.clicked.connect(self.recommendStockCal)  # 荐股计算
        ui.pushButton_4.clicked.connect(self.pushButton_4_gainloseCal)  # 自选股收益计算


        # self.region = pg.LinearRegionItem()
        # self.region.setZValue(10)
        # self.region.sigRegionChanged.connect(self.update)

        # 添加自选股
        ui.listWidget_2.clear()
        rec = config.interestingStockList
        if rec:
            for i in range(len(rec)):
                ui.listWidget_2.addItem(list(rec.keys())[i])

        # 添加股票代码
        rec = config.Stock_list
        if rec:
            for i in range(len(rec)):
                ui.listWidget.addItem(list(rec.keys())[i])

        root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
        root.withdraw()  # 将Tkinter.Tk()实例隐藏

        """header 表头  stock_data 数据类型 int(t), str(trade_date), float(open), float(close), float(low),
        float(high), float(vol), float(change), float(pct_chg)) """

    def MymouseEvent(self, event):
        pos=event.pos()
        self.d.vLine.setPos(int(pos.x()))
        self.cdst.vLine.setPos(int(pos.x()))




    def pushButton_4_gainloseCal(self):
        # 自选股收益计算
        ec = earning_Compare()
        key, value = [], []
        for i in range(ui.listWidget_2.count()):
            item = ui.listWidget_2.item(i).text()
            key.append(item)
            value.append(config.Stock_list[item])
        list = dict(zip(key, value))

        # list = {'宏大爆破': '002683.SZ',
        #         '晶方科技': '603005.SH',
        #         '双塔食品': '002481.SZ',
        #         '亿纬锂能': '300014.SZ'}

        db = ec.CalculateForspecStock(list)
        wg = ui.listWidget_5
        wg.clear()
        for i in range(len(db)):
            sumlist = db[i][0]
            detail = db[i][1]
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"{detail[1][1]} {detail[1][1]}")
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"总收益:{db[i][0] - 100000}  {(int(db[i][0] - 100000) / 100000) * 100}%")
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"--{detail[0][3:6]}")
            wg.addItem(f"--{detail[len(detail) - 1][7:10]}")
            wg.addItem(f"-----------------------------------")
            amount = 0
            for c in range(len(detail)):
                amount = amount + detail[c][11]
                wg.addItem(f"{detail[c][0] - 1}： 累计收益:{amount} : {detail[c][3:]}")
    def recommendStockCal(self):
        ec = earning_Compare()
        # list = {'宏大爆破': '002683.SZ',
        #         '晶方科技': '603005.SH',
        #         '双塔食品': '002481.SZ',
        #         '亿纬锂能': '300014.SZ'}
        db = ec.CalculateForspecStock(config.recommendStock)
        ui.listWidget_3.clear()
        for i in range(len(db)):
            sumlist = db[i][0]
            detail = db[i][1]
            ui.listWidget_3.addItem(f"-----------------------------------")
            ui.listWidget_3.addItem(f"{detail[1][1]} {detail[1][1]}")
            ui.listWidget_3.addItem(f"-----------------------------------")
            ui.listWidget_3.addItem(f"总收益:{db[i][0] - 100000}  {(int(db[i][0] - 100000) / 100000) * 100}%")
            ui.listWidget_3.addItem(f"-----------------------------------")
            ui.listWidget_3.addItem(f"--{detail[0][3:6]}")
            ui.listWidget_3.addItem(f"--{detail[len(detail) - 1][7:10]}")
            ui.listWidget_3.addItem(f"-----------------------------------")
            amount = 0
            for c in range(len(detail)):
                amount = amount + detail[c][11]
                ui.listWidget_3.addItem(f"{detail[c][0] - 1}： 累计收益:{amount} : {detail[c][3:]}")
    def appendToInteringStockList(self):
        text = ui.listWidget.currentItem().text()
        ui.listWidget_2.addItem(text)

        # 保存自选股名单
    def moveFromInteringStockList(self):
        text = ui.listWidget_2.currentItem().text()

        for i in range(ui.listWidget_2.count()):
            item = ui.listWidget_2.item(i).text()
            if text == item:
                ui.listWidget_2.takeItem(i)
    def custom_edit_textChanged(self, event):
        # if event != '':
        try:

            rec = fuzzyfinder.fuzzyfinder(event, config.Stock_list.keys())
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
    def stockclick(self, text):
        Datalist = Fetch_stock_data()
        Datalist.ini(config.Stock_list[text])

        Moving_data = Datalist.Data_form_list.Moving_datum
        
        self.cdst = CandlestickItem(Datalist.Data_form_list.Candle_datum, Moving_data, 400)
    
        self.cdst1 = AmountstickItem(Datalist.Data_form_list.Amount_datum, 400)
        
        list = Calculation(Moving_data)

        self.d = Mat_picture(list.earning_x, list.earning_y, Datalist.Data_form_list.Candle_datum)
        self.cdst.sigMouseMoveChanged.connect(self.MymouseEvent)  # K线图鼠标同步事件
        self.d.sigMouseMoveChanged.connect(self.MymouseEvent)  # K线图鼠标同步事件

        if ui.verticalLayout.count() == 0:
            ui.verticalLayout.addWidget(self.cdst.plt)
            ui.verticalLayout.addWidget(self.cdst1.plt)
            ui.verticalLayout_2.addWidget(self.cdst.plt)
            ui.verticalLayout_2.addWidget(self.d.plt)
        else:
            for i in range(ui.verticalLayout.count()):
                ui.verticalLayout.itemAt(i).widget().deleteLater()
            for i in range(ui.verticalLayout_2.count()):
                ui.verticalLayout_2.itemAt(i).widget().deleteLater()
            Moving_data = Datalist.Data_form_list.Moving_datum
            # cdst = CandlestickItem(Datalist.Data_form_list.Candle_datum, Moving_data, 400)
            #         self.cdst1 = AmountstickItem(Datalist.Data_form_list.Amount_datum, 400)
            ui.verticalLayout.addWidget(self.cdst.plt)
            ui.verticalLayout.addWidget(self.cdst1.plt)
            # list = Calculation(Moving_data)
            # d = Mat_picture(list.earning_x, list.earning_y,Datalist.Data_form_list.Candle_datum)
            ui.verticalLayout_2.addWidget(self.cdst.plt)
            ui.verticalLayout_2.addWidget(self.d.plt)

        self.singleStockGainLoseCal(text)

    def singleStockGainLoseCal(self: 'spam', stockcode: str):
        ec = earning_Compare()
        key, value = [], []
        key.append(stockcode)
        value.append(config.Stock_list[stockcode])
        list = dict(zip(key, value))

        # list = {'宏大爆破': '002683.SZ',
        #         '晶方科技': '603005.SH',
        #         '双塔食品': '002481.SZ',
        #         '亿纬锂能': '300014.SZ'}

        db = ec.CalculateForspecStock(list)
        wg = ui.listWidget_5
        wg.clear()
        for i in range(len(db)):
            sumlist = db[i][0]
            detail = db[i][1]
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"{detail[1][1]} {detail[1][1]}")
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"总收益:{db[i][0] - 100000}  {(int(db[i][0] - 100000) / 100000) * 100}%")
            wg.addItem(f"-----------------------------------")
            wg.addItem(f"--{detail[0][3:6]}")
            wg.addItem(f"--{detail[len(detail) - 1][7:10]}")
            wg.addItem(f"-----------------------------------")
            amount = 0
            for c in range(len(detail)):
                amount = amount + detail[c][11]
                wg.addItem(f"{detail[c][0] - 1}： 累计收益:{amount} : {detail[c][3:]}")
    def listWidget_selectionChange(self):
        text = ui.listWidget.currentItem().text()
        self.stockclick(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
