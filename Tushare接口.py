# -*- coding: utf-8 -*-
import tushare as t1
from config import *
from log import log as logger
import time
from SQLserver import *

# 股票字典
stock_code = Stock_list


# 爬取股票的数据
class Append_Data():
    """input_code股票代码 input_csv_name要存取的csv文件名 sd开始日期 ed结束日期"""

    def __init__(self, code, start_data, end_data):
        self.code = code
        self.start_data = start_data
        self.end_data = end_data
        # self.csv_name = "csv_data/" + csv_name + ".csv"

    def web_spider(self):  # 网络爬虫tushare接口
        try:
            df = ts.daily(ts_code=self.code, start_date=self.start_data, end_date=self.end_data)  # 爬取数据--dataframe格式
            # df.to_csv(self.csv_name) # 转换为csv文件
            return df  # 返回数据
        except Exception as e:
            # logger.error(e, exc_info=True)
            logger.logerror(e)  # 将出错信息写入log内


# 存储到数据库
class Sql_Data_Handle():
    def __init__(self, df, connect, curs):
        self.df = df
        self.connect = connect
        self.curs = curs

    def character(self):
        # df = pandas.read_csv(self.csv_name, encoding='gbk') # 用pandas库读取csv文件
        line_num = self.line_num
        # pandas的iloc函数读取每行对应数据
        ts_code = self.df.iloc[line_num]["ts_code"]
        trade_date = self.df.iloc[line_num]["trade_date"]
        open = self.df.iloc[line_num]["open"]
        high = self.df.iloc[line_num]["high"]
        low = self.df.iloc[line_num]["low"]
        close = self.df.iloc[line_num]["close"]
        pre_close = self.df.iloc[line_num]["pre_close"]
        change = self.df.iloc[line_num]["change"]
        pct_chg = self.df.iloc[line_num]["pct_chg"]
        vol = self.df.iloc[line_num]["vol"]
        amount = self.df.iloc[line_num]["amount"]
        # 将数据转换为元祖tuple格式
        values = (
            ts_code, trade_date, float(open), float(high), float(low), float(close), float(pre_close),
            float(change), float(pct_chg), float(vol), float(amount))
        return values

    def add_data(self):

        self.line_num = len(self.df) - 1
        # 将avg_list, avg_list_5day, avg_list_10day, avg_list_20day, avg_list_60day 进行初始化
        avg_list, avg_list_5day, avg_list_10day, avg_list_20day, avg_list_60day = [0 for i in
                                                                                   range(self.line_num + 1)], [0 for i
                                                                                                               in range(
                self.line_num + 1)], [0 for i in range(self.line_num + 1)], [0 for i in range(self.line_num + 1)], [0
                                                                                                                    for
                                                                                                                    i in
                                                                                                                    range(self.line_num + 1)]
        # f_day 五日平均线，ten_day 十日平均线，t_day 二十日平均线，s_day 六十日平均线
        i, f_day, ten_day, t_day, s_day = 0, 0, 0, 0, 0
        # 循环调用character()函数-读取每行数据
        while self.line_num >= 0:
            value_list = self.character()
            vol = value_list[9]  # 交易量
            amount = value_list[10]  # 交易额
            avg_list[i] = float(format(amount * 10 / vol, '.3f'))  # 保留三位小数
            # 计算移动平均线
            if i < 5:
                f_day += avg_list[i]
            else:
                f_day = f_day + avg_list[i] - avg_list[i - 5]
                avg_list_5day[i] = float(format(f_day / 5, '.3f'))
            if i < 10:
                ten_day += avg_list[i]
            else:
                ten_day = ten_day + avg_list[i] - avg_list[i - 10]
                avg_list_10day[i] = float(format(ten_day / 10, '.2f'))
            if i < 20:
                t_day += avg_list[i]
            else:
                t_day = t_day + avg_list[i] - avg_list[i - 20]
                avg_list_20day[i] = float(format(t_day / 20, '.3f'))
            if i < 60:
                s_day += avg_list[i]
            else:
                s_day = s_day + avg_list[i] - avg_list[i - 60]
                avg_list_60day[i] = float(format(s_day / 60, '.3f'))
            try:
                # 插入数据库
                Sql.Sql_execution(
                    f"""insert into stock ({tushare["Column"]}) values """ + f"(\'{value_list[0]}\',\'{value_list[1]}\',\'{value_list[2]}\',\'{value_list[3]}\',\'{value_list[4]}\',\'{value_list[5]}\',\'{value_list[6]}\',\'{value_list[7]}\',\'{value_list[8]}\',\'{value_list[9]}\',\'{value_list[10]}\',\'{avg_list[i]}\',\'{avg_list_5day[i]}\',\'{avg_list_10day[i]}\',\'{avg_list_20day[i]}\',\'{avg_list_60day[i]}\')")
            except Exception:
                # 出错信息
                logger.logerror(f"{value_list[0]}-{value_list[1]}未被添加！")
            self.line_num -= 1
            i += 1
        print(f"The data has been added to the stock database")
        return i


if __name__ == '__main__':
    logger = logger()
    count = 0
    line_count = len(Stock_list)
    logger.loginfo("连接数据库")
    Sql = DataServer_Sqlite3("stock")  # 连接数据库
    logger.loginfo("连接数据库成功")
    Sql.Empty_database("stock")  # 清空数据库
    logger.loginfo("清空数据库")
    Sql.Zero_Id()  # 将ID归零
    logger.loginfo("将ID归零")
for key in stock_code:
    try:
        column = tushare["column"]
        t1.set_token(tushare["token"])  # token值
        ts = t1.pro_api()  # 初始化pro接口
        logger.loginfo("初始化pro接口成功")
        input_code = stock_code[key]
        sd, ed = "20181231", "20201231"  # 起始日期，结束日期
        logger.loginfo(f"抓取{key}股票数据")
        start = time.perf_counter()  # 开始时间
        df = Append_Data(input_code, sd, ed).web_spider()  # dataframe格式股票数据
        line_num = Sql_Data_Handle(df, Sql.connection, Sql.curs).add_data()
        end = time.perf_counter()  # 结束时间
        # 记录用时
        logger.loginfo(f"添加{key}股票数据到数据库--成功,用时{start - end}")
        # 记录添加的数据条数
        logger.loginfo(f"{key} 共{line_num}条数据已添加到数据库！")
    except Exception as e:
        logger.logerror(e)
    count += 1
    print(f"还剩{line_count - count}支股票...")

Sql.connection.close()  # 关闭数据库
