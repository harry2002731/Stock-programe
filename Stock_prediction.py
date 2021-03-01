from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import paddle
import paddle.fluid as fluid

SAVE_DIRNAME = 'model'

f = open('training_data/五粮液.txt')
df = f.readlines()
f.close()

data = []
for line in df:
    data_raw = line.strip('\n').strip('\r').split('\t')  # 这里data_raw是列表形式，代表一行数据样本
    data.append(data_raw)  # data为二维列表形式
data = np.array(data, dtype='float32')
ratio = 0.8
DATA_NUM = len(data)

train_len = int(DATA_NUM * ratio)
test_len = DATA_NUM - train_len
test_data = data[test_len:]

avg = np.mean(test_data, axis=0)
max_ = np.max(test_data, axis=0)
min_ = np.min(test_data, axis=0)
shape=np.shape(test_data)
print(shape)

def normalization(data, avg, max_, min_):
    result_data = (data - avg) / (max_ - min_)
    return result_data


test_data = normalization(test_data, avg, max_, min_)


def my_test_reader():
    def reader():
        for temp in test_data:
            yield temp[:-1], temp[-1]

    return reader


def convert2LODTensor(temp_arr, len_list):
    temp_arr = np.array(temp_arr)
    temp_arr = temp_arr.flatten().reshape((-1, 1))  # 把325个测试样本的array平坦化到一维数据[1950,1]的格式
    print(temp_arr.shape)
    return fluid.create_lod_tensor(
        data=temp_arr,  # 对测试样本来说这里表示325个样本的平坦化数据列表，维度为[1950,1]
        recursive_seq_lens=[len_list],  # 对于测试样本来说这里全是6，所以为325 个6的列表
        place=fluid.CPUPlace()
    )  # 返回：A fluid LoDTensor object with tensor data and recursive_seq_lens info


def get_tensor_label(mini_batch):
    tensor = None
    labels = []

    temp_arr = []
    len_list = []
    for _ in mini_batch:  # mini_batch表示的大小为325个测试样本数据
        labels.append(_[1])  # 收集 label----y----------1维
        temp_arr.append(_[0])  # 收集序列本身--x---------6维
        len_list.append(len(_[0]))  # 收集每个序列x的长度,和上边x的维度对应，这里全为6
    tensor = convert2LODTensor(temp_arr, len_list)
    return tensor, labels


my_tensor = None
labels = None

# 定义batch
test_reader = paddle.batch(
    my_test_reader(),
    batch_size=482)  # 一次性把样本取完

for mini_batch in test_reader():
    my_tensor, labels = get_tensor_label(mini_batch)  # 其实就是变成tensor格式的x和y
    break
print(labels)
# place = fluid.CPUPlace()
place = fluid.CPUPlace()
exe = fluid.Executor(place)
inference_scope = fluid.core.Scope()
with fluid.scope_guard(inference_scope):  # 更改全局/默认作用域实例。运行时的所有变量将分配给新的作用域。
    [inference_program, feed_target_names, fetch_targets] = (
        fluid.io.load_inference_model(SAVE_DIRNAME, exe))
    results = exe.run(inference_program,
                      feed={'x': my_tensor},  # {feed_target_names[0]:my_tensor },和上面保存模型时统一
                      fetch_list=fetch_targets)

result_print = results[0].flatten()
result_print=result_print*(np.array(max_[7]-min_[7]))+np.array(avg[7])
labels=labels*(np.array(max_[7]-min_[7]))+np.array(avg[7])
plt.figure()
plt.plot(list(range(len(labels))), labels, color='r')  # 红线为真实值
plt.plot(list(range(len(result_print))), result_print, color='g')  # 绿线为预测值
plt.show()
