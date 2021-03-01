import sqlite3
import config

class DataServer_Sqlite3():
    def __init__(self):
        self.curs = ''
        self.connection = ''
        self.header = ''
        self.data = ''
        self.Connecting_database()

    def Connecting_database(self):
        self.connection = sqlite3.connect(config.dbPath)  # 连接数据库
        self.curs = self.connection.cursor()

    def Sql_execution(self, sql: str):
        self.curs = self.curs.execute(sql)
        self.connection.commit()

    def Fetch_data(self):
        self.header = self.curs.description
        self.data = self.curs.fetchall()
        print("")

    def Create_table(self,name:str,input_header:str):
        """sample: input_header =int primary key,ts_code,symbol,name,area,industry,market,list_date"""
        self.Sql_execution(f"create table {name}({input_header})")
