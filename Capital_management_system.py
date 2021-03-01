import datetime
import config
from SQLserver import *



def Connecting_database(self):
    # 连接数据库 获取股票的表头信息和表内数据
    server = DataServer_Sqlite3.SQLserver()
    server.Sql_execution(sql="DELETE FROM \"temp\"")
    server.Sql_execution(
        f"""INSERT INTO temp({config.tushare["Column"]}) SELECT {config.tushare["Column"]} FROM "stock" where stock.ts_code == '{self}' """)
    server.Sql_execution("select * from temp")
    server.Fetch_data()
    data = server.data  # 获取表内数据

def DEMO_SG(self):
    """
    买入信号：周线MACD零轴下方底部金叉，即周线的DIF>DEA金叉时买入
    卖出信号：日线级别 跌破 20日均线

    参数：
    week_macd_n1：周线dif窗口
    week_macd_n2: 周线dea窗口
    week_macd_n3: 周线macd平滑窗口
    day_n: 日均线窗口
    """
    k = self.to
    if (len(k) == 0):
        return

    stk = k.get_stock()

    # -----------------------------
    # 计算日线级别的卖出信号
    # -----------------------------
    day_c = CLOSE(k)
    day_ma = MA(day_c, self.get_param("day_n"))
    day_x = day_c < day_ma  # 收盘价小于均线
    for i in range(day_x.discard, len(day_x)):
        if day_x[i] >= 1.0:
            self._add_sell_signal(k[i].datetime)

    # -----------------------------
    # 计算周线级别的买入信号
    # -----------------------------
    week_q = Query(k[0].datetime, k[-1].datetime.next_day(), ktype=Query.WEEK)
    week_k = k.get_stock().get_kdata(week_q)

    n1 = self.get_param("week_macd_n1")
    n2 = self.get_param("week_macd_n2")
    n3 = self.get_param("week_macd_n3")
    m = MACD(CLOSE(week_k), n1, n2, n3)
    fast = m.get_result(0)
    slow = m.get_result(1)

    discard = m.discard if m.discard > 1 else 1
    for i in range(discard, len(m)):
        if (fast[i - 1] < slow[i - 1] and fast[i] > slow[i]):
            # 当周计算的结果，只能作为下周一的信号
            self._add_buy_signal(week_k[i].datetime.next_week())




class DEMO_MM(MoneyManagerBase):
    """
    买入：30% （不明确，暂且当做当前现金的30%）
    卖出：已持仓股票数的50%
    """

    def __init__(self):
        super(DEMO_MM, self).__init__("MACD_MM")

    def _reset(self):
        pass

    def _clone(self):
        return DEMO_MM()

    def _get_buy_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        cash = tm.current_cash

        # 可以不用考虑最小交易单位的问题，已经自动处理
        # num = int((cash * 0.3 // price // stk.atom) * stk.atom)
        return int(cash * 0.3 / price)  # 返回类型必须是int

    def _get_sell_num(self, datetime, stk, price, risk, part_from):
        tm = self.tm
        position = tm.get_position(stk)
        total_num = position.number
        num = int(total_num * 0.5)
        return num if num >= 100 else 0