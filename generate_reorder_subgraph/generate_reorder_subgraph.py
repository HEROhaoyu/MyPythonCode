import numpy as np
import matplotlib.pyplot as plt

# 读取图数据文件
edges = np.loadtxt('E:\华科实验室论文\MyPythonCode\dataset\Social networks\\twitter_combined.txt', dtype=int)

# 统计每个点的度数
degrees = {}
for edge in edges:
    degrees[edge[0]] = degrees.get(edge[0], 0) + 1
    degrees[edge[1]] = degrees.get(edge[1], 0) + 1

# 按度数进行排列
sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

# 计算阈值
threshold = sorted_degrees[int(len(sorted_degrees) * 0.1)][1]

# 筛选边
dense_edges = []
for edge in edges:
    if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
        dense_edges.append(edge)

#稠密子图的平均度数
print("稠密子图的平均度数为：", len(dense_edges) / len(degrees))

# 将边信息保存到txt文件
with open('E:\华科实验室论文\MyPythonCode\dataset\Social networks\\twitter_combined_subgraph.txt', 'w') as f:
    for edge in dense_edges:
        f.write(f"{edge[0]} {edge[1]}\n")

# 输出提示信息
print("稠密子图边信息已保存到文件。")
