import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import config

from utility import Descison, selectedStock


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data, datum, days):
        pg.GraphicsObject.__init__(self)
        self.picture = QtGui.QPicture()
        self.data = data
        self.days=config.StockDataDays
        if len(self.data)>self.days:
            self.days=len(self.data)
        # self.days = days
        self.plt = pg.PlotWidget()
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        des = Descison()
        s = selectedStock()
        des.selectStock_avg(datum)
        # for s in des.selectedStockList:
        #     print(s.DateToBuy, s.DateToSale, s.Decision)

        self.generatePicture(des.selectedStockList)
        self.X_axis()
        self.Y_axis_Candle()
        self.plt.addItem(self.vLine, ignoreBounds=True)
        self.plt.addItem(self.hLine, ignoreBounds=True)
        # 只重画部分图形，大大提高界面更新速度
        self.setFlag(self.ItemUsesExtendedStyleOption)
        self.label = pg.TextItem(text='', color=(255, 255, 255))
        self.plt.addItem(self.label)

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

    def Y_axis_Candle(self):

        item = self
        self.plt.addItem(item)
        self.plt.setLabel('left', '股 价')
        self.plt.setLabel('bottom', '日 期')

        # plt.showGrid(x=True, y=True)
        return self.plt
    def generatePicture(self, stocklist):
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        if len(self.data)<self.days:
            self.days=len(self.data)

        w = (self.data[1][0] - self.data[0][0]) / 3.
        prema5 = 0
        prema10 = 0
        prema = 0
        selectIndex = 0
        for (t, trade_date, open, close, low, high, ma, ma5, ma10, ma20, ma60) in self.data:
            if t == self.days:
                break
            if open > close:
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, high))
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
            if prema5 != 0:
                p.setPen(pg.mkPen('w'))
                p.setBrush(pg.mkBrush('w'))
                p.drawLine(QtCore.QPointF(t - 1, prema5), QtCore.QPointF(t, ma5))
            prema5 = ma5
            if prema10 != 0:
                p.setPen(pg.mkPen('c'))
                p.setBrush(pg.mkBrush('c'))
                p.drawLine(QtCore.QPointF(t - 1, prema10), QtCore.QPointF(t, ma10))
            prema10 = ma10
            if prema != 0:
                p.setPen(pg.mkPen('b'))
                p.setBrush(pg.mkBrush('b'))
                p.drawLine(QtCore.QPointF(t - 1, prema), QtCore.QPointF(t, ma))
            prema = ma
            

        p.end()
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

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

    # def mouseReleaseEvent(self, event):
    #     print()
    # 鼠标左单击
    # ----------------------------------------------------------------------
    def onLClick(self, pos):
        x = pos.x()
        y = pos.y()
        self.vLine.setPos(pos.x())
        self.hLine.setPos(pos.y())

    def mouseMoveEvent(self, event):
        pos = event.pos()
        index = int(pos.x())
        y = self.data[index][2]
        # print(y)
        lastPos = event.lastPos()
        dif = pos - lastPos
        # label = pg.LabelItem(justify='left')
        # self.plt.addItem(label)
        # label.setText(
        #     "<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>" % (
        #         mousePoint.x(), self.data[index]))
        if index > 0 and index < self.days:
            # dt = f"{dt[0:4]}-{dt[4:6]}-{dt[6:]}"
            # ui.label.setText(f"日期={self.data[index][1]}  开盘={self.data[index][2]}  收盘={self.data[index][3]}")
            a = f"日期={self.data[index][1]}  开盘={self.data[index][2]}  收盘={self.data[index][3]}"
            self.label.setText(a)

        self.vLine.setPos(pos.x())
        self.hLine.setPos(y)
