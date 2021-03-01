import config
from SQLserver import *
from Data_convert import *


class Descison():
    def __init__(self):
        self.selectedStockList = []
        self.QtyBuy = 0

    def selectStock_avg(self, datum):
        list = []
        self.hold_amount = 100000
        for i in range(len(datum)):
            if datum[i][4] == 0 or datum[i][3] == 0:
                continue
            if datum[i][4] - datum[i][3] == 0:
                gap = 1
            else:
                gap = abs(datum[i][4] - datum[i][3]) / (datum[i][4] - datum[i][
                    3])  # str(ts_code),str(trade_date),float(avgprice),float(avg5day),float(avg10day)
            list.append([gap, datum[i][0], datum[i][1], datum[i][2]])  # gap,ts_code,trade_date,avgprice

        # 选着跳变的点
        j = 1
        for i in range(len(list) - 1):
            if list[i][0] == 1 and list[i + 1][0] == -1:  # 5MA 上穿  10MA
                ss = selectedStock()
                # 第几次交易
                ss.code = datum[i][0]
                ss.Name = self.get_key(config.Stock_list, ss.code)  # 股票名称
                ss.DateToBuy = list[i][2]  # 买入日期
                ss.PriceBuy = list[i][3]  # 买入价格
                ss.QtyBuy = int(self.hold_amount / (list[i][3] * 1.003))  # 买入xxx股
                self.QtyBuy = ss.QtyBuy
                ss.AmountBuy = int(ss.PriceBuy * ss.QtyBuy*1.003)  # 买入金额
                ss.Decision = 'buy'  # 决策

                self.Hold_amount(cost=-self.hold_amount) # 计算手中还有多少钱
                self.selectedStockList.append(ss)
            elif list[i][0] == -1 and list[i + 1][0] == 1:
                ss = selectedStock()
                ss.ID = j  # 第几次交易
                ss.code = datum[i][0]
                ss.Name = self.get_key(config.Stock_list, ss.code)  # 股票名称
                ss.DateToSale = list[i][2]
                ss.PriceSale = list[i][3]
                ss.QtySale = self.QtyBuy
                ss.AmountSale = int(ss.PriceSale * ss.QtySale * 0.997)
                ss.Decision = 'sale'
                ss.GainloseAmount = ss.AmountSale - ss.AmountBuy
                if ss.GainloseAmount > 0:
                    ss.GainCount = ss.GainCount + 1
                else:
                    ss.LoseCount = ss.LoseCount + 1
                self.Hold_amount(cost=ss.AmountSale)
                self.selectedStockList.append(ss)  # 10MA 上穿  5MA
                j += 1

    def get_key(self, dict, value):
        for k, v in dict.items():
            if v == value:
                return k

    def Hold_amount(self, cost):  # 手中持有的金额
        self.hold_amount += cost


class selectedStock():
    def __init__(self):
        self.ID = ''
        self.Name = ''
        self.code = ''
        self.DateToBuy = ''
        self.PriceBuy = ''
        self.QtyBuy = 0
        self.AmountBuy = 0
        self.DateToSale = ''
        self.PriceSale = ''
        self.QtySale = 0
        self.AmountSale = 0
        self.GainloseAmount = 0
        self.GainCount = 0
        self.LoseCount = 0
        self.Decision = ''


def Connecting_database(self):
    # 连接数据库 获取股票的表头信息和表内数据
    server = SQLserver()
    server.Sql_execution(sql="DELETE FROM \"temp\"")
    server.Sql_execution(
        f"""INSERT INTO temp({config.tushare["Column"]}) SELECT {config.tushare["Column"]} FROM "stock" where stock.ts_code == '000001.SZ' """)
    server.Sql_execution("select * from temp")
    server.Fetch_data()
    data = server.data  # 获取表内数据
    datum = Data_convert(data).Moving_average_form()
    return datum
# if __name__ == '__main__':
#     datum=Connecting_database("000001.SZ")
#     des=Descison()
#     s = selectedStock()
#     des.selectStock_avg(datum)
#     for s in des.selectedStockList:
#         print(s.DateToBuy,s.DateToSale,s.Decision)
