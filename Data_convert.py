"""包含了 All_datum：全部数据
         Candle_datum：t,trade_date,open,close,low,high,avgprice,avg5day,avg10day,avg20day,avg60day
         Moving_datum:ts_code,trade_date,avgprice,avg5day,avg10day
         Amount_datum:t,trade_date,open,close,vol"""
class Data_convert:
    def __init__(self):
        self.All_datum = []
        self.Candle_datum = []
        self.Moving_datum = []
        self.Amount_datum = []

    def Transfer_data_form(self,data):

        t = 0
        for (
                ts_code, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount, avgprice, avg5day,
                avg10day, avg20day, avg60day) in data:
            All_datum = (str(ts_code), str(trade_date), float(open), float(close), float(low), float(high),float(vol),float(change),float(pct_chg), float(pre_close), float(amount)), float(avgprice), float(avg5day), float(avg10day), float(avg20day), float(avg60day)
            Candle_datum = (int(t), str(trade_date), float(open), float(close), float(low), float(high),float(avgprice),float(avg5day), float(avg10day), float(avg20day), float(avg60day))
            Moving_datum = [str(ts_code), str(trade_date), float(avgprice), float(avg5day), float(avg10day)]
            Amount_datum = (int(t), str(trade_date), float(open), float(close), float(vol))

            self.All_datum.append(All_datum)
            self.Candle_datum.append(Candle_datum)
            self.Moving_datum.append(Moving_datum)
            self.Amount_datum.append(Amount_datum)
            t += 1

