import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False

# 读取图数据文件
edges = np.loadtxt('E:\华科实验室论文\MyPythonCode\show_reorder_distribution\graph.txt', dtype=int)

# 统计每个点的度数
degrees = {}
for edge in edges:
    degrees[edge[0]] = degrees.get(edge[0], 0) + 1
    degrees[edge[1]] = degrees.get(edge[1], 0) + 1

# 按度数进行排列
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

# 计算三个阈值
threshold1 = sorted_degrees[int(len(sorted_degrees) * 0.1)][1]
threshold2 = sorted_degrees[int(len(sorted_degrees) * 0.05)][1]
threshold3 = sorted_degrees[int(len(sorted_degrees) * 0.01)][1]

# 筛选边
edges1 = []
edges2 = []
edges3 = []
for edge in edges:
    if degrees[edge[0]] > threshold1 and degrees[edge[1]] > threshold1:
        edges1.append(edge)
    if degrees[edge[0]] > threshold2 and degrees[edge[1]] > threshold2:
        edges2.append(edge)
    if degrees[edge[0]] > threshold3 and degrees[edge[1]] > threshold3:
        edges3.append(edge)

# 将边转换为矩阵并绘制
def plot_edges(edges, threshold, title):
    max_node = max(max(edge) for edge in edges)
    matrix = np.zeros((max_node + 1, max_node + 1))
    for edge in edges:
        matrix[edge[0], edge[1]] = 1

    # 绘制图像并添加标题
    plt.imshow(matrix, cmap='Reds')
    plt.title(title)

plt.figure(figsize=(15, 5))
plt.subplot(131)
plot_edges(edges1, threshold1, '前10%的稠密子图')
plt.subplot(132)
plot_edges(edges2, threshold2, '前5%的稠密子图')
plt.subplot(133)
plot_edges(edges3, threshold3, '前1%的稠密子图')
plt.show()