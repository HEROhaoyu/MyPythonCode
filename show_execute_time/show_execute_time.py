import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False

# 输入数据
x = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
y_cpu = [486, 775, 1484, 2902, 5730, 11321, 22449, 45032, 89509]
y_npu = [50.213, 47.259, 52.396, 56.129, 58.916, 45.718, 46.509, 46.509, 47.013]

# 绘制图表
plt.plot(x, y_cpu, marker='o', label='CPU执行时间(us)')
plt.plot(x, y_npu, marker='o', label='NPU执行时间(ms)')

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('数据集平均度数与执行时间')
plt.xlabel('数据集平均度数(顶点数量固定为2^15）')
plt.ylabel('执行时间')

# 显示图表
plt.show()
