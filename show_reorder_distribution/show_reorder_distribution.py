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
    ax.imshow(matrix, cmap='Reds')
    ax.set_title(title)

    # 添加图像右侧的文本信息
    text = f"Graph Information:\nNumber of Nodes: {num_nodes}\nNumber of Edges: {num_edges}\nMax Degree: {max_degree}\nMin Degree: {min_degree}\nAvg Degree: {avg_degree:.2f}"
    ax.annotate(text, xy=(180, 40), xycoords='axes points', ha='right', va='center', fontsize=10)
    #上面的代码作用是在图像右侧添加文本信息，其中xy=(1.2, 0.5)表示文本信息的位置，xycoords='axes fraction'表示文本信息的位置是相对于图像的，ha='left'表示文本信息的水平对齐方式为左对齐，va='center'表示文本信息的垂直对齐方式为居中对齐，fontsize=10表示文本信息的字体大小为10
    #xy=(0.2, 0.5)表示文本距离图像左边的距离为0.2，距离图像下边的距离为0.5，0.2的单位是图像的宽度，0.5的单位是图像的高度，如果想让文本距图像一个固定的距离，可以将xycoords='axes fraction'改为xycoords='axes points'，然后将0.2和0.5改为固定的数值，如20和20，表示文本距离图像左边的距离为20，距离图像下边的距离为20

fig, axes = plt.subplots(1, 3, figsize=(18, 8), gridspec_kw={'width_ratios': [len(edges1), len(edges2), len(edges3)]})
#上面的代码作用是创建一个1行3列的图像，每个图像的宽度比例为edges1,edges2,edges3的长度比例
plot_edges(edges1, threshold1, '前10%的稠密子图', axes[0])
plot_edges(edges2, threshold2, '前5%的稠密子图', axes[1])
plot_edges(edges3, threshold3, '前1%的稠密子图', axes[2])

# 调整图像之间的间距和图像右侧的距离
plt.subplots_adjust(wspace=0.6, right=0.85)

plt.savefig('E:\华科实验室论文\MyPythonCode\dataset\Social networks\Wiki-Vote_reorder.png', dpi=300)