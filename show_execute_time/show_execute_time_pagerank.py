import matplotlib.pyplot as plt
import math
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False

# 输入数据

x = [8,16, 32, 64, 128, 256, 512, 1024]
y_cpu = [16293,30243,56442,134004,282575,480556,991700,1978296]
y_npu = [383.821,517.631,630.72,733.085,850.841,964.045,993.435,1017.113]


# 绘制图表

#将横坐标刻度值改为以2为底的对数坐标
plt.xscale('log',base=2)
plt.plot(x, y_cpu, marker='o', label='CPU执行时间')
plt.plot(x, y_npu, marker='o', label='NPU执行时间')

# 添加图例
plt.legend()

# 添加标题和标签
plt.title('固定顶点数目情况下，pagerank算法执行时间与边数目的关系')
plt.xlabel('数据集中每个顶点的平均度数(顶点数量固定为2^15）')
plt.ylabel('执行时间(ms)')

# 显示图表
plt.show()
