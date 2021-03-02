import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import config

class AmountstickItem(pg.GraphicsObject):
    """绘制交易量的图表"""

    def __init__(self, data, days):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.data = data
        # self.days=config.StockDataDays
        # if len(self.data)>self.days:
        self.days=len(self.data)      
        # self.days = days
        self.plt = pg.PlotWidget()
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.generatePicture_amount()

        self.X_axis()
        self.Y_axis_Amount()
        # self.plt.addItem(self.vLine, ignoreBounds=True)
        # self.plt.addItem(self.hLine, ignoreBounds=True)
        # 只重画部分图形，大大提高界面更新速度
        self.setFlag(self.ItemUsesExtendedStyleOption)

    def X_axis(self):
        xdict = []
        # self.days=config.StockDataDays
        # if len(self.data)>self.days:
        self.days=len(self.data)
        for i in range(self.days):
            dt = self.data[i][1]
            dt = f"{dt[0:4]}-{dt[4:6]}-{dt[6:]}"
            if i % (int(self.days / 20)) == 0 or i == range(self.days):
                xdict.append((self.data[i][0], dt))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict])
        self.plt = pg.PlotWidget(axisItems={'bottom': stringaxis}, enableMenu=True)
        return self.plt

    def Y_axis_Amount(self):
        item = self
        self.plt.addItem(item)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', '成交量', "十手")
        self.plt.setLabel('bottom', '日 期')
        return self.plt

    def generatePicture_amount(self):
        p = QtGui.QPainter(self.picture)
        p.setBrush(pg.mkBrush('r'))
        p.setPen(pg.mkPen('r'))
        if len(self.data)<self.days:
            self.days=len(self.data)
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, trade_date, open, close, vol) in self.data:
            if t == self.days:
                break
            if open > close:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
            if open < close:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))
            p.drawRect(QtCore.QRectF(t - w, 0, w * 2, vol / 10))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
