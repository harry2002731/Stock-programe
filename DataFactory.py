import config
from Fetch_stock_data import *

class DataFacory():

    def __init__(self):
        self.stockName=''
        self.stockCode=''
        self.stockHistoryDatum_Webdata=[]    #网络爬取的数据
        self.stockHistoryDatum=[]             #转换后的股票历时交易数据，开收盘价、成交量等
        self.stockHistoryDatumHeader=[]       #数据表头
        self.stockTradingDatum=[]        #交易日期列表
        self.stockHistoryMovingDatum=[]          #移动平均线数据
        self.stockHistoryDesDatum=[]         #决策后数据 买卖点，日期，交易数量

        self.StockList_interesting=[]       #自选股列表
        self.StockList_SH=[]                 #A股列表
        self.StockList_SZ=[]                 #深圳股列表
        self.StockList_H=[]                 #H股列表 港股
        self.StockList_Ind=[]               #指数列表

                
        self.ChartCandleDatum=[]             #蜡烛图数据
        self.ChartAmountDatum=[]             #成交量数据
        self.ChartGainLoseDatum=[]           #收益图数据

    def setStockName(self,stockName):       #设置股票名称
        self.stockName=stockName
        self.stockCode=config.Stock_list[stockName]

    def setStockCode(self,stockCode):       #设置股票名称
        self.stockCode=stockCode       
        k=config.Stock_list.keys()
        v=config.Stock_list.values()
        new=dict(zip(v,k))
        self.stockName=new[stockCode]
        

    def fillSqlData(self):        #返回SQL数据，数据表头
        server = DataServer_Sqlite3()
        server.Connecting_database()
        server.Sql_execution(sql="DELETE FROM \"temp\"")
        server.Sql_execution(
            f"""INSERT INTO temp({config.tushare["Column"]}) SELECT {config.tushare["Column"]} FROM "stock" where stock.ts_code == '{self.stockCode}' """)
        server.Sql_execution("select * from temp")
        server.Fetch_data()
        self.stockHistoryDatum_Webdata = server.data  # 获取表内数据
        
        Header = []                           # 获取表头信息
        for index in server.header:
            Header.append(index[0])
        
        self.stockHistoryDatumHeader = Header  
            

    def FillAnalysisData(self):
        data=self.stockHistoryDatum_Webdata
        
        t = 0
        for (ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount, avgprice, avg5day,
                avg10day, avg20day, avg60day) in data:
            All_datum = (str(ts_code), str(trade_date), float(open), float(close), float(low), float(high),float(vol),float(change),float(pct_chg), float(pre_close), float(amount)), float(avgprice), float(avg5day), float(avg10day), float(avg20day), float(avg60day)
            Candle_datum = (int(t), str(trade_date), float(open), float(close), float(low), float(high),float(avgprice),float(avg5day), float(avg10day), float(avg20day), float(avg60day))
            Moving_datum = [str(ts_code), str(trade_date), float(avgprice), float(avg5day), float(avg10day)]
            Amount_datum = (int(t), str(trade_date), float(open), float(close), float(vol))

            self.stockHistoryDatum.append(All_datum)
            self.ChartCandleDatum.append(Candle_datum)
            self.stockHistoryMovingDatum.append(Moving_datum)
            self.ChartAmountDatum.append(Amount_datum)
            t += 1
    def FillDecisionData(self):
        pass



class Trading():                #交易类
    def __init__(self):
        self.stockName=''       #股票名称
        self.stockCode=''       #股票代码
        self.TradingList=[]     #交易记录 append TradingRec
    
    def Buy(self,stockName,price,qty):
        rec=TradingRec()
        rec.stockName=stockName
        rec.stockCode=config.Stock_list[stockName]
        rec.price=price
        rec.qty=qty
        self.TradingList.append(rec)
        return rec

    def Sale(stockName,price,qty):
        rec=TradingRec()
        rec.stockName=stockName
        rec.stockCode=config.Stock_list[stockName]
        rec.price=price
        rec.qty=qty
        self.TradingList.append(rec)
        return rec

    def TradingRecToList(Tradingrec):
        rec=Trading()
        rec=Tradingrec
        list=[
            rec.stockName,
            rec.stockCode,
            rec.tradingDate,
            rec.tradingName,
            rec.price,
            rec.qty,
            rec.amount,
            rec.status,
            rec.account,
            ]
        
        return list
class TradingRec():
    def __init__(self):
        self.stockName=''       #股票名称
        self.stockCode=''       #股票代码
        self.tradingDate=''     #交易日期
        self.tradingName=''     #'buy'   'sale'
        self.price=''           #交易金额
        self.qty=''             #交易数量
        self.amount=''          #交易金额
        self.status=''          #交易转态  ，申请，撤单，成交，取消
        self.account=''          #交易账户

        self.list=config.interestingStockList

class stockHistoryRec(list):

    def __init__(self):
        self.list=[]
   
    def filldata(stockcode):
        self.list= Fetch_stock_data.ini(stockcode)



        Moving_data = Datalist.Data_form_list.Moving_datum
        
        self.cdst = CandlestickItem(Datalist.Data_form_list.Candle_datum, Moving_data, 400)
    
        self.cdst1 = AmountstickItem(Datalist.Data_form_list.Amount_datum, 400)
        
        list = Calculation(Moving_data)

        self.d = Mat_picture(list.earning_x, list.earning_y, Datalist.Data_form_list.Candle_datum)
        self.cdst.sigMouseMoveChanged.connect(self.MymouseEvent)  # K线图鼠标同步事件
        self.d.sigMouseMoveChanged.connect(self.MymouseEvent)  # K线图鼠标同步事件

if __name__ == '__main__':
    df=DataFacory()
    df.stockName='东山精密'
    df.stockCode=config.Stock_list[df.stockName]
    df.fillSqlData()
    df.FillAnalysisData()
    df.setStockCode('002384.SZ')
    df.FillDecisionData()


    da=Fetch_stock_data()
    name='东山精密'
    da.Connecting_database()
    da.Get_header()
    da.Transfer_data()
    

    # app = QtWidgets.QApplication(sys.argv)
    # window = Main()
    # window.show()
    # sys.exit(app.exec_())