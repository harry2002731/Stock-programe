from Data_convert import *
import config
from SQLserver import DataServer_Sqlite3
import fuzzyfinder


class Fetch_stock_data:
    def __init__(self):
        self.data = []
        self.Header = []
        self.Data_form_list = Data_convert()
        self.stock_code = ''

    def ini(self, stock_code):
        self.stock_code = stock_code

        self.Connecting_database()
        self.Get_header()
        self.Transfer_data()
        # return self.Data_form_list

    def Connecting_database(self):  # 连接数据库 获取股票的表头信息和表内数据
        server = DataServer_Sqlite3()
        server.Connecting_database()
        server.Sql_execution(sql="DELETE FROM \"temp\"")
        server.Sql_execution(
            f"""INSERT INTO temp({config.tushare["Column"]}) SELECT {config.tushare["Column"]} FROM "stock" where stock.ts_code == '{self.stock_code}' """)
        server.Sql_execution("select * from temp")
        server.Fetch_data()
        self.data = server.data  # 获取表内数据
        self.header_inf = server.header  # 获取表头信息

    def Get_header(self):
        self.Header = []
        for index in self.header_inf:
            self.Header.append(index[0])

    def Transfer_data(self):
        data_convert = Data_convert()
        data_convert.Transfer_data_form(self.data)
        self.Data_form_list = data_convert
