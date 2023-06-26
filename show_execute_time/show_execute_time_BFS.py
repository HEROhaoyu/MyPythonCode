import matplotlib.pyplot as plt
import math
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False

# 输入数据
x = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
y_cpu = [486, 775, 1484, 2902, 5730, 11321, 22449, 45032, 89509]

y_npu = [50.213, 47.259, 52.396, 56.129, 58.916, 45.718, 46.509, 46.509, 47.013]




# 绘制图表
plt.xscale('log',base=2)
plt.plot(x, y_cpu, marker='o', label='CPU执行时间')
plt.plot(x, y_npu, marker='o', label='NPU执行时间')

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('固定顶点数目情况下，BFS算法执行时间与边数目关系')
plt.xlabel('数据集中每个顶点的平均度数(顶点数量固定为2^15）')
plt.ylabel('执行时间(ms)')

# 显示图表
plt.show()
