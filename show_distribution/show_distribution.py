import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib import colors
# 读取图数据集
with open('E:\华科实验室论文\MyPythonCode\dataset\Social networks\soc-Epinions1.txt', 'r') as f:
    edges = [tuple(map(int, line.strip().split())) for line in f]

# 获取节点数量
n = max(max(u, v) for u, v in edges) + 1

# 初始化矩阵
matrix = np.zeros((n, n),bool)

# 填充矩阵
for u, v in edges:
    matrix[u][v] = 1



# 将matrix绘制成图像,值为1的点为蓝色，值为0的点为白色
plt.imshow(matrix,cmap='Reds')
plt.savefig('E:\华科实验室论文\MyPythonCode\dataset\Social networks\soc-Epinions1.txt.png')
