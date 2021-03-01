convert_data_form 将股票数据变为训练用数据格式（labels 为未来第五天的平均成交价）
config 为配置文件

UI0 --有表格界面
UI1 为界面 --无表格界面
UI2


stockmain 主程序 负责从数据库获取数据，和绘制k线图像
    -Data_convert  用以转换数据格式（依赖）