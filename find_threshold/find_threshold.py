import numpy as np
import matplotlib.pyplot as plt


def read_graph_data(file_path):
    """
    读取图数据文件并返回边的列表
    """
    edges = np.loadtxt(file_path, dtype=int)
    return edges


def compute_degrees(edges):
    """
    统计每个点的度数并返回度数字典
    """
    degrees = {}
    for edge in edges:
        degrees[edge[0]] = degrees.get(edge[0], 0) + 1
        degrees[edge[1]] = degrees.get(edge[1], 0) + 1
    return degrees


def select_threshold(sorted_degrees, edges, degrees):
    """
    选择最佳阈值，并计算稠密子图的平均度数和顶点数量
    """
    # 定义参数
    num_samples = 1000  # 随机采样的次数

    # 初始化最佳阈值和最大平均度数
    best_threshold = None
    max_avg_degree = 0
    dense_edges_count = 0
    dense_vertexs_count = 0

    # 记录每次采样的阈值和稠密子图平均度数
    thresholds = []
    avg_degrees = []

    # 进行随机采样
    for _ in range(num_samples):
        # 随机选择一个阈值
        random_index = np.random.randint(len(sorted_degrees))
        threshold = sorted_degrees[random_index][1]
        edge_count = 0
        vertex_set = set()
        # 筛选边的数量
        for edge in edges:
            if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
                vertex_set.add(edge[0])
                vertex_set.add(edge[1])
                edge_count += 1

        if len(vertex_set) == 0:
            continue
        # 更新最大平均度数和阈值
        avg_degree = edge_count / len(vertex_set)
        if avg_degree > max_avg_degree:
            max_avg_degree = avg_degree
            best_threshold = threshold
            dense_edges_count = edge_count
            dense_vertexs_count = len(vertex_set)

        # 记录阈值和稠密子图平均度数
        thresholds.append(threshold)
        avg_degrees.append(avg_degree)

    return best_threshold, max_avg_degree, dense_edges_count, dense_vertexs_count, thresholds, avg_degrees


def filter_dense_edges(edges, degrees, threshold):
    """
    根据阈值筛选稠密子图的边
    """
    dense_edges = []
    for edge in edges:
        if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
            dense_edges.append(edge)
    return dense_edges


if __name__ == "__main__":
    # 读取图数据文件
    # edges = read_graph_data(r'C:\\Users\\huao\Desktop\\MyPythonCode\dataset\Social networks\Wiki-Vote.txt')
    # edges = read_graph_data(r'C:\\Users\\huao\Desktop\\MyPythonCode\dataset\Amazon  networks\Amazon0601.txt')
    edges = read_graph_data(r'C:\\Users\\huao\Desktop\\MyPythonCode\dataset\\Road  networks\\roadNet-CA.txt')

    # 统计每个点的度数
    degrees = compute_degrees(edges)

    # 按度数进行排列
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)

    # 选择最佳阈值，并计算稠密子图的平均度数和顶点数量
    best_threshold, max_avg_degree, dense_edges_count, dense_vertexs_count, thresholds, avg_degrees = select_threshold(
        sorted_degrees, edges, degrees
    )

    # 输出结果
    print("最大平均度数:", max_avg_degree)
    print("最佳阈值:", best_threshold)
    print("稠密子图的平均度数为:", dense_edges_count / dense_vertexs_count)
    print("稠密子图的边数量:", dense_edges_count)
    print("稠密子图的点数量:", dense_vertexs_count)

    # 绘制阈值和稠密子图平均度数的散点图
    plt.rcParams["font.sans-serif"] = "SimHei"
    plt.rcParams["axes.unicode_minus"] = False
    plt.scatter(thresholds, avg_degrees)
    plt.xlabel("阈值")
    plt.ylabel("稠密子图的平均度数")
    plt.title("不同阈值下稠密子图的平均度数的变化")

    # 添加结果标记
    annotations = [
        f"最大平均度数: {max_avg_degree:.2f}",
        f"最佳阈值: {best_threshold}",
        f"稠密子图的平均度数: {dense_edges_count / dense_vertexs_count:.2f}",
        f"稠密子图的边数量: {dense_edges_count}",
        f"稠密子图的点数量: {dense_vertexs_count}",
    ]
    for i, annotation in enumerate(annotations):
        plt.annotate(
            annotation,
            xy=(best_threshold, max_avg_degree),
            xytext=(0.95, 0.95 - i * 0.05),
            textcoords="axes fraction",
            horizontalalignment="right",
            verticalalignment="top",
            color="red",
        )

    # 绘制与 x 轴和 y 轴的射线
    plt.axvline(x=best_threshold, color="red", linestyle="--")
    plt.axhline(y=max_avg_degree, color="red", linestyle="--")

    # 绘制红色的点
    plt.plot(best_threshold, max_avg_degree, marker="o", markersize=8, color="red")

    # 手动设置坐标轴范围从 0 开始
    plt.xlim(0, plt.xlim()[1])
    plt.ylim(0, plt.ylim()[1])

    plt.savefig(r"C:\\Users\\huao\Desktop\\MyPythonCode\\find_threshold\\find_threshold_2.png")
