from utility import *
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
import numpy as np
import pyqtgraph as pg
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
            # if selectIndex == len(self.stocklist) - 1:
            #     print(int(self.Final_amount())) # 打印最终总收益  类型--int
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


class Mat_picture():
    def __init__(self, x, y):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.p1 = self.win.addPlot(row=1, col=0)
        self.p1.setAutoVisible(y=True)
        self.y = np.array(y)
        self.x = np.array(np.arange(len(self.y)))

        self.generate_picture()

    def generate_picture(self):
        self.p1.plot(self.x, self.y)
        # self.p1.show()


if __name__ == '__main__':
    list = Calculation(datum)
    Mat_picture(list.earning_x, list.earning_y)
