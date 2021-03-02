import datetime

import pandas as pd

from utility import *
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pyqtgraph as pg
import config
from SQLserver import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

Interchange_fees = 0.003
QtySale = 1

# 连接数据库 获取股票的表头信息和表内数据
server = DataServer_Sqlite3()
server.Sql_execution(sql="DELETE FROM \"temp\"")
server.Sql_execution(
    f"""INSERT INTO temp({config.tushare["Column"]}) SELECT {config.tushare["Column"]} FROM "stock" where stock.ts_code == '000005.SZ' """)
server.Sql_execution("select * from temp")
server.Fetch_data()
data = server.data  # 获取表内数据
Data = Data_convert()
Data.Transfer_data_form(data)
datum = Data.Moving_datum


class Calculation():
    def __init__(self, datum):
        # self.amount
        self.datum=datum
        self.hold_vol = 0
        self.final_amount = 0
        self.hold_amount = 100000
        self.vol_x, self.vol_y = [], []
        self.amount_x, self.amount_y = [], []
        self.earning_x, self.earning_y = [], []
        self.trade_datum = []
        self.Buy_rec, self.Sale_rec = [], []
        des = Descison()
        s = selectedStock()
        des.selectStock_avg(datum)
        self.stocklist = des.selectedStockList
        self.iterator()

        # self.lose=[]
        # self.trade=[]

        # trade_datum = [str(t), str(trade_date), float(avgprice), float(avg5day), float(avg10day)]

    def iterator(self):
        selectIndex = 0
        while selectIndex < len(self.stocklist):
            self.Stocklist = self.stocklist[selectIndex]
            self.Decision()
            if selectIndex == len(self.stocklist) - 1:
                print(int(self.Final_amount())) # 打印最终总收益  类型--int
            selectIndex += 1

    def Decision(self):
        # self.gainlose=[]    #ID,stock,stockcode,buydate，price，qty,amount，saledate ，qty，price,amount ，gainlose$, %
        stock_inf = [self.Stocklist.ID, self.Stocklist.Name, self.Stocklist.code]
        if self.Stocklist.Decision == 'buy':
            self.Buying()
            self.Buy_rec = [self.Stocklist.DateToBuy, self.Stocklist.PriceBuy, self.Stocklist.QtyBuy,
                            self.Stocklist.AmountBuy]
            # rec = [self.Stocklist.ID, self.Stocklist.Name, self.Stocklist.DateToBuy, self.Stocklist.PriceBuy, self.Stocklist.QtyBuy,
            #        self.Stocklist.AmountBuy, self.Stocklist.DateToSale, self.Stocklist.QtySale,
            #        self.Stocklist.PriceSale,
            #        self.Stocklist.AmountSale, 0, 0]
            # self.trade_datum.append(rec)

        if self.Stocklist.Decision == "sale":
            self.Selling()
            if self.Stocklist.ID != 1:
                gainlose = self.Stocklist.AmountSale - self.Buy_rec[3] # AmountBuy
                if self.Stocklist.AmountBuy == 0:
                    self.Stocklist.AmountBuy = 1

                self.Sale_rec = [self.Stocklist.DateToSale, self.Stocklist.PriceSale,self.Stocklist.QtySale,
                                     self.Stocklist.AmountSale, gainlose, round(gainlose*100 / self.Buy_rec[3],2)]
                    # rec = [self.Stocklist.ID, self.Stocklist.Name, self.Stocklist.DateToBuy, self.Stocklist.PriceBuy, self.Stocklist.QtyBuy,
                    #        self.Stocklist.AmountBuy, self.Stocklist.DateToSale, self.Stocklist.QtySale,
                    #        self.Stocklist.PriceSale, self.Stocklist.AmountSale, gainlose, gainlose / self.Stocklist.AmountBuy]
                rec = stock_inf + self.Buy_rec + self.Sale_rec
                self.trade_datum.append(rec)

    def Buying(self):
        trade_date = self.Stocklist.DateToBuy
        self.avg_price = self.Stocklist.PriceBuy
        vol=self.Stocklist.QtyBuy
        # vol = int(self.hold_amount / (self.avg_price * 1.003))
        # cost = -(self.avg_price * 1.003) * vol
        cost=-self.Stocklist.AmountBuy
        self.Hold_amount(trade_date, cost)
        self.Hold_vol(trade_date, vol)
        self.Earning(trade_date)

    def Selling(self):
        trade_date = self.Stocklist.DateToSale
        self.avg_price = self.Stocklist.PriceSale
        vol=-self.Stocklist.QtySale
        # vol = -int(self.hold_vol * QtySale)
        # cost = (self.avg_price * 0.997) * -vol
        cost=self.Stocklist.AmountSale
        self.Hold_amount(trade_date, cost)
        self.Hold_vol(trade_date, vol)
        self.Earning(trade_date)

    def Hold_amount(self, trade_date, cost):  # 手中持有的金额
        self.hold_amount += cost
        self.amount_x.append(trade_date)
        self.amount_y.append(self.hold_amount)

    def Hold_vol(self, trade_date, vol):  # 持有量
        self.hold_vol += vol
        self.vol_x.append(trade_date)
        self.vol_y.append(self.hold_vol)

    def Earning(self, trade_date):
        self.earning_x.append(trade_date)
        self.earning_y.append(self.hold_amount + (self.hold_vol * self.avg_price))

    def Final_amount(self):  # 最终总计金额，包括未被抛出的股票。
        self.final_amount = self.hold_amount + (self.hold_vol * self.avg_price)
        return self.final_amount


class Mat_picture(pg.GraphicsObject):
    def __init__(self, x, y,data):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.data=data
        # self.days=config.StockDataDays
        # if len(self.data)>self.days:
        self.days=len(self.data)

        self.y = np.array(y)        
        self.plt = pg.PlotWidget()        
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        
        self.x = x      
        self.generate_picture()

        xdict = []
        for i in range(self.days):
            dt = self.data[i][1]
            dt = f"{dt[0:4]}-{dt[4:6]}-{dt[6:]}"
            if i % (int(self.days / 20)) == 0 or i == range(self.days):
                xdict.append((self.data[i][0], dt))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict])
        self.plt = pg.PlotWidget(axisItems={'bottom': stringaxis}, enableMenu=True)

        item = self
        self.plt.addItem(item)  

        self.plt.addItem(self.vLine, ignoreBounds=True)
        self.plt.addItem(self.hLine, ignoreBounds=True)  
           
        self.plt.setLabel('left', '收益(万)')
        self.plt.setLabel('bottom', '日 期')
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.label = pg.TextItem(text='', color=(255, 255, 255))
        self.plt.addItem(self.label)


    def generate_picture(self):        
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('g'))        
        prePoint = 0
        selectIndex = 0
        
        t = [i[0] for i in self.data] 
        trade_date=[i[1] for i in self.data] 
        list = dict(zip(trade_date, t))

        for i in range(len(self.x)):
            t=list[self.x[i]]
            
            if t == config.StockDataDays:
                break            
            if prePoint != 0:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
                p.drawLine(QtCore.QPointF(pre_t, prePoint), QtCore.QPointF(t, self.y[selectIndex]/10000))
            pre_t=t
            prePoint = self.y[selectIndex]/10000
            selectIndex =selectIndex+1
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
    def onLClick(self, pos):
        x = pos.x()
        y = pos.y()
        self.vLine.setPos(pos.x())
        self.hLine.setPos(pos.y())
# 手动重画
    # ----------------------------------------------------------------------
    def update(self):
        if not self.scene() is None:
            self.scene().update()

    def mousePressEvent(self, event):
        pos = event.scenePos()
        if event.button() == QtCore.Qt.RightButton:
            self.onRClick(event.pos())
        elif event.button() == QtCore.Qt.LeftButton:
            self.onLClick(event.pos())

    def mouseMoveEvent(self, event):
        pos = event.pos()
        index = int(pos.x())
        xdate = self.data[index][1]
        # print(xdate)
        
        if index > 0 and index < self.days:
            
            # dt = f"{dt[0:4]}-{dt[4:6]}-{dt[6:]}"
            # ui.label.setText(f"日期={self.data[index][1]}  开盘={self.data[index][2]}  收盘={self.data[index][3]}")
            # a = f"日期={self.data[index][1]}  开盘={self.data[index][2]}  收盘={self.data[index][3]}"
            # self.label.setText(a)
            pass

        self.vLine.setPos(pos.x())
        self.hLine.setPos(pos.y())


        # self.p1.plot(range(len(self.y)), self.y)

      
        # self.p1.show()


# if __name__ == '__main__':
#     list = Calculation(datum)
#     Mat_picture(list.earning_x, list.earning_y)
