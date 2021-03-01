import pandas
import SQLserver

"""获取所有股票的名称和代码
ts_code--股票代码有SZ，SH
symbol--股票代码无SZ，SH
name--名称
area--所属区域
industry--行业
market--板块
list_date--上市日期"""


class Dataframe_reader():
    def __init__(self, df):
        self.df = df
        self.line_num = 0
        self.length = 0
        self.header_list = []

    def character(self):
        # self.df = pandas.read_csv("stock_basics.csv", encoding='utf-8')
        self.length = len(self.header_list)  # 列数
        values = [0 for j in range(self.length)]
        for i in range(self.length):
            values[i] = str(self.df.iloc[self.line_num][self.header_list[i]])
        return values

    def add_data(self):
        for text in self.df.columns:
            self.header_list.append(str(text))
        while self.line_num < len(self.df):
            value_list = self.character()
            server=SQLserver.DataServer_Sqlite3()
            val='\'%s\',' * (self.length - 2) + '\'%s\''
            # print("insert into stock_list " + f"({'%s,'*(self.length-2)+'%s'})" % tuple(self.header_list[1:]) + " values " + f"({'})" % tuple(value_list[1:]))
            try:
                server.Sql_execution("insert into stock_list " + f"({'%s,'*(self.length-2)+'%s'})" % tuple(self.header_list[1:]) + " values " + f"({val})" % tuple(value_list[1:]))
            except Exception:
                break
            self.line_num += 1


if __name__ == '__main__':
    Dataframe_reader(pandas.read_csv("stock_basics.csv", encoding='utf-8')).add_data()
