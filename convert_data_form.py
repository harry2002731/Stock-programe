import sqlite3
import time

from stockmain import Fetch_stock_data
from testing_data_form import testing
from log import log as logger
from config import Stock_list

stock_code = Stock_list


def Avg_price(value):
    header, stock = Fetch_stock_data.Connecting_database(value)
    avg_list, avg_list_5day, avg_list_10day, avg_list_20day, avg_list_60day = [0 for i in range(len(stock))], [0 for i
                                                                                                               in range(
            len(stock))], [0 for i in range(len(stock))], [0 for i in range(len(stock))], [0 for i in range(len(stock))]
    i, f_day, ten_day, t_day, s_day = 0, 0, 0, 0, 0
    sql = "SELECT \"temp\".* FROM \"temp\" ORDER BY \"temp\".trade_date ASC"
    curs.execute(sql)

    for (t, trade_date, open, close, low, high, vol, change, pct_chg, pre_close, amount) in stock:
        avg_list[i] = float(format(amount * 10 / vol, '.3f'))
        if i < 5:
            # avg_list_5day[i] = ''
            f_day += avg_list[i]
        else:
            f_day = f_day + avg_list[i] - avg_list[i - 5]
            avg_list_5day[i] = float(format((f_day) / 5, '.3f'))
        if i < 10:
            # avg_list_10day[i] = ''
            ten_day += avg_list[i]
        else:
            ten_day = ten_day + avg_list[i] - avg_list[i - 10]
            avg_list_10day[i] = float(format(ten_day / 10, '.2f'))
        if i < 20:
            # avg_list_20day[i] = ''
            t_day += avg_list[i]
        else:
            t_day = t_day + avg_list[i] - avg_list[i - 20]
            avg_list_20day[i] = float(format((t_day) / 20, '.3f'))
        if i < 60:
            # avg_list_60day[i] = ''
            s_day += avg_list[i]
        else:
            s_day = s_day + avg_list[i] - avg_list[i - 60]
            avg_list_60day[i] = float(format((s_day) / 60, '.3f'))
        try:
            sql = f"""update stock set avgprice = {avg_list[i]} , avg_price_5day = {avg_list_5day[i]} , avg_price_10day = {avg_list_10day[i]} , avg_price_20day = {avg_list_20day[i]},avg_price_60day = {avg_list_60day[i]} where trade_date = \'{trade_date}\' and ts_code = \'{t}\'; """
            print(sql)
            curs.execute(sql)

        except Exception:
            logger.logerror(f"{t}-{trade_date}未被添加！")
        i += 1
    connection.commit()


def Build_txt_file(value, txt_file):
    """将数据转换为测试用数据格式"""
    header, stock = Fetch_stock_data.Connecting_database(value)
    stock.reverse()
    str_text = []
    pre_average_list = [0, 0, 0, 0, 0]
    i = 0
    j = 0
    line_num = 0
    for (t, trade_date, open, close, low, high, vol, change, pct_chg, pre_close, amount) in stock:
        if j < 5:
            pre_average_list[j] = amount * 10 / vol
            j += 1
            continue
        if i == 5:
            i = 0
        if line_num == len(stock) - j - 1:
            txt_file.writelines(" ")
        pre_average = pre_average_list[i]

        if line_num == 0:
            text = f"{format(open, '.2f')}\t{format(close, '.2f')}\t{format(low, '.2f')}\t{format(high, '.2f')}\t{format(vol, '.2f')}\t{format(amount, '.2f')}\t{format(change, '.2f')}\t{format(pre_average, '.2f')} "
        else:
            text = f"{format(open, '.2f')}\t{format(close, '.2f')}\t{format(low, '.2f')}\t{format(high, '.2f')}\t{format(vol, '.2f')}\t{format(amount, '.2f')}\t{format(change, '.2f')}\t{format(pre_average, '.2f')}\n "
        pre_average_list[i] = amount * 10 / vol
        str_text.append(text)
        i += 1
        line_num += 1
    str_text.reverse()
    for text in str_text:
        txt_file.write(text)
    if not testing(txt_file):
        logger.logerror(f"{value}不符合数据格式！")
    txt_file.close()


if __name__ == '__main__':
    logger = logger()
    count = 0
    line_count = len(Stock_list)
    connection = sqlite3.connect(r'C:\Users\Harry2002\Desktop\数据库文件\database.db')  # 连接数据库
    curs = connection.cursor()  # 返回连接的游标对象
    for key in stock_code.keys():
        if key == "浙商中拓":
            try:
                logger.loginfo(f"{key} start!")
                start = time.perf_counter()
                Avg_price(stock_code[key])
                end = time.perf_counter()
                logger.loginfo(f"用时{start - end}")
                print(f"还剩{line_count - count}支股票...")
                count += 1
                # txt_file = open(f"training_data/{key}.txt", 'w+')
                # Build_txt_file(stock_code[key],txt_file)
                # logger.loginfo(f"{key} 已成功转换")
            except Exception as e:
                logger.logerror(e)
