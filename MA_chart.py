class MA_chart:

    @staticmethod
    def Week_chart(stock_data):
        open = 0.0
        close = 0.0
        low = 0.0
        high = 0.0
        t = 0
        trade_date = stock_data[0][1]
        stock_MA_data = []
        for i in stock_data:
            open += i[2]
            close += i[3]
            low += i[4]
            high += i[5]
            if (i[0] + 1) % 5 == 0:
                datum = (int(t), str(trade_date), float(open / 5), float(close / 5), float(low / 5), float(high / 5))
                t += 1
                open = 0.0
                close = 0.0
                low = 0.0
                high = 0.0
                trade_date = i[1]
                stock_MA_data.append(datum)
        return stock_MA_data

    # 月k线
    @staticmethod
    def Month_chart(stock_data):
        pass