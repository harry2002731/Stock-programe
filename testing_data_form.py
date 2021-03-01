import numpy as np


def testing(f) -> bool:
    try:
        df = f.readlines()
        f.close()
        data = []
        for line in df:
            data_raw = line.strip('\n').strip('\r').split('\t')  # 这里data_raw是列表形式，代表一行数据样本
            data.append(data_raw)  # data为二维列表形式
        np.array(data, dtype='float32')
        return True
    except Exception:
        return False
