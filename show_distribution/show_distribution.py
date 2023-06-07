import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# 读取图数据集
with open('graph.txt', 'r') as f:
    edges = [tuple(map(int, line.strip().split())) for line in f]

# 获取节点数量
n = max(max(u, v) for u, v in edges) + 1

# 初始化矩阵
matrix = np.zeros((n, n))

# 填充矩阵
for u, v in edges:
    matrix[u][v] = 1

# 创建自定义颜色映射
color_list = ListedColormap(['white','red'],2);

# 绘制图像
plt.imshow(matrix,cmap=[plt.cm.gray,                 )
plt.savefig('graph.png')
