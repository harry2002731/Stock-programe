import sqlite3
import config


class DataServer_Sqlite3():
    def __init__(self, db_name):
        self.curs = ''
        self.connection = ''
        self.header = ''
        self.data = ''
        self.db_name = db_name
        self.Connecting_database()

    def Connecting_database(self):
        self.connection = sqlite3.connect(config.dbPath)  # 连接数据库
        self.curs = self.connection.cursor()

    def Sql_execution(self, sql: str):
        self.curs = self.curs.execute(sql)
        self.connection.commit()

    def delete_data(self, key, data):
        self.curs = self.curs.execute(f"delete from " + key + " where trade_date=" + data)
        self.connection.commit()
        print("The data has been deleted")

    def Fetch_data(self):
        self.header = self.curs.description
        self.data = self.curs.fetchall()

    def Empty_database(self):
        self.curs = self.curs.execute(f"DELETE FROM \"{self.db_name}\"")
        self.connection.commit()

    def Zero_Id(self):
        self.curs = self.curs.execute(f"update sqlite_sequence set seq=0 where name='{self.db_name}'")
        self.connection.commit()

    def Create_table(self, name: str, input_header: str):
        """sample: input_header =int primary key,ts_code,symbol,name,area,industry,market,list_date"""
        self.Sql_execution(f"create table {name}({input_header})")
