import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = "SimHei"
plt.rcParams["axes.unicode_minus"] = False

# 读取图数据文件
edges = np.loadtxt('E:\华科实验室论文\MyPythonCode\dataset\Social networks\Wiki-Vote.txt', dtype=int)

# 统计每个点的度数
degrees = {}
for edge in edges:
    degrees[edge[0]] = degrees.get(edge[0], 0) + 1
    degrees[edge[1]] = degrees.get(edge[1], 0) + 1

# 按度数进行排列
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

# 计算三个阈值
threshold1 = sorted_degrees[int(len(sorted_degrees))-1][1]
threshold2 = sorted_degrees[int(len(sorted_degrees) * 0.5)][1]
threshold3 = sorted_degrees[int(len(sorted_degrees) * 0.25)][1]
threshold4 = sorted_degrees[int(len(sorted_degrees) * 0.10)][1]
threshold5 = sorted_degrees[int(len(sorted_degrees) * 0.05)][1]
threshold6 = sorted_degrees[int(len(sorted_degrees) * 0.01)][1]

# 筛选边
edges1 = []
edges2 = []
edges3 = []
edges4 = []
edges5 = []
edges6 = []
for edge in edges:
    if degrees[edge[0]] > threshold1 and degrees[edge[1]] > threshold1:
        edges1.append(edge)
    else:
        continue
    if degrees[edge[0]] > threshold2 and degrees[edge[1]] > threshold2:
        edges2.append(edge)
    else:
        continue
    if degrees[edge[0]] > threshold3 and degrees[edge[1]] > threshold3:
        edges3.append(edge)
    else:
        continue
    if degrees[edge[0]] > threshold3 and degrees[edge[1]] > threshold4:
        edges4.append(edge)
    else:
        continue
    if degrees[edge[0]] > threshold3 and degrees[edge[1]] > threshold5:
        edges5.append(edge)
    else:
        continue
    if degrees[edge[0]] > threshold3 and degrees[edge[1]] > threshold6:
        edges6.append(edge)
    else:
        continue
# 将边转换为矩阵并绘制
def plot_edges(edges, threshold, title, ax):
    max_node = max(max(edge) for edge in edges)
    matrix = np.zeros((max_node + 1, max_node + 1))
    for edge in edges:
        matrix[edge[0], edge[1]] = 1

    # 计算度数信息
    degrees = {}
    for edge in edges:
        degrees[edge[0]] = degrees.get(edge[0], 0) + 1
        degrees[edge[1]] = degrees.get(edge[1], 0) + 1
    max_degree = max(degrees.values())
    min_degree = min(degrees.values())
    avg_degree = sum(degrees.values()) / len(degrees)

    # 计算顶点数目和边数目
    num_nodes = len(set(node for edge in edges for node in edge))
    num_edges = len(edges)

    # 绘制图像并添加标题
    ax.imshow(matrix, cmap='Reds', aspect='equal', extent=[0, num_nodes, 0, num_nodes])
    ax.set_title(title)

    # 添加图像右侧的文本信息
    text = f"Graph Information:\nNumber of Nodes: {num_nodes}\nNumber of Edges: {num_edges}\nMax Degree: {max_degree}\nMin Degree: {min_degree}\nAvg Degree: {avg_degree:.2f}"
    ax.annotate(text, xy=(180, 40), xycoords='axes points', ha='right', va='center', fontsize=12)

fig, axes = plt.subplots(2, 3, figsize=(18,12))
plot_edges(edges1, threshold1, '原始图', axes[0][0])
plot_edges(edges2, threshold2, '前50%的稠密子图', axes[0][1])
plot_edges(edges3, threshold3, '前25%的稠密子图', axes[0][2])
plot_edges(edges4, threshold4, '前10%的稠密子图', axes[1][0])
plot_edges(edges5, threshold5, '前5%的稠密子图', axes[1][1])
plot_edges(edges6, threshold6, '前1%的稠密子图', axes[1][2])

# 调整图像之间的间距和图像右侧的距离
plt.subplots_adjust(wspace=0.6, right=0.85)

plt.savefig('E:\华科实验室论文\MyPythonCode\dataset\Social networks\Wiki-Vote_reorder.png', dpi=300)