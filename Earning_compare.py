from Gain_lose import *
import SQLserver
import config
import Data_convert
# from stockmain import *
from Fetch_stock_data import Fetch_stock_data

""" 
根据K线 移动平均线，确定买卖点，计算一个阶段股票的收益情况。

 """


class Earning_compare(Fetch_stock_data):
    def __init__(self):
        super(Earning_compare, self).__init__()
        self.length = 0
        self.Top_List, self.detal_list, self.summary_list = [], [], []

        self.datum = []
        self.ss = []
        # self.iterate()

    def CalculateForAllStock(self):
        i = 0
        self.length = len(config.Stock_list.keys())
        for code in config.Stock_list.values():
            self.ini(code)
            self.datum = self.Data_form_list.Moving_datum
            self.ss = Calculation(self.datum)
            self.Compare()
            i += 1
            # print(self.Top_List)
            print(f"还剩{self.length - i}")
        self.Write_to_txt()
        return self.Top_List

    def CalculateForspecStock(self, Stocklist):
        i = 0
        self.length = len(Stocklist)
        for code in Stocklist.values():
            self.ini(code)
            self.datum = self.Data_form_list.Moving_datum
            self.ss = Calculation(self.datum)
            self.Compare()
            i += 1
            # print(self.Top_List)
            print(f"还剩{self.length - i}")
        self.Write_to_txt()
        return self.Top_List

    def bubble_sort(self):

        length = len(self.Top_List)
        for i in range(length - 1):
            # i表示比较多少轮
            for j in range(length - i - 1):
                # j表示每轮比较的元素的范围，因为每比较一轮就会排序好一个元素的位置，
                # 所以在下一轮比较的时候就少比较了一个元素，所以要减去i
                if self.Top_List[j][0] < self.Top_List[j + 1][0]:
                    self.Top_List[j], self.Top_List[j + 1] = self.Top_List[j + 1], self.Top_List[j]

    def Compare(self):
        To_be_compare = [int(self.ss.final_amount), self.ss.trade_datum]
        if len(self.Top_List) < 10:
            self.Top_List.append(To_be_compare)
            if len(self.Top_List) == 10:
                self.bubble_sort()
        else:
            for top in self.Top_List:
                index = self.Top_List.index(top)
                if To_be_compare[0] > top[0]:
                    self.Top_List.insert(index, To_be_compare)
                    self.Top_List.pop()
                    break
                else:
                    pass

    def Detal_list(self):
        j = 0
        for List in self.Top_List:
            self.detal_list.append(List[j][1])
            j += 1

    def Summary_list(self):
        j = 0
        for List in self.Top_List:
            self.summary_list.append(List[j][0])
            j += 1

    def Write_to_txt(self):
        txt = open('toplist.txt', 'w')
        txt.write(f"{str(self.Top_List)}")
        txt.close()


if __name__ == '__main__':
    Earning_compare()
