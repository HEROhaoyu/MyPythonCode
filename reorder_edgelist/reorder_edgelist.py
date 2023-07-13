import numpy as np


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


def select_threshold(edges, degrees):
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


def generator_reorder_edgelist(edges, threshold,filename):
    """
    根据阈值筛选稠密子图的边
    """
    dense_edges = ""
    orther_edges = ""
    for edge in edges:
        if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
            dense_edges+=edge[0]+" "+edge[1]+"\n"
        else:
            orther_edges+=edge[0]+" "+edge[1]+"\n"
    with open(filename, 'w') as file:
        file.write(dense_edges)
        file.write(orther_edges)

if __name__ == "__main__":
    #设置文件路径
    # input_path="C:\\Users\\huao\Desktop\\MyPythonCode\dataset\\Road  networks\\roadNet-CA.txt"
    # output_path="E:\华科实验室论文\MyPythonCode\\reorder_edgelist\\dataset_reorder.txt"
    input_path="C:\Users\huao\Desktop\MyPythonCode\reorder_edgelist\Wiki-Vote.txt"
    output_path="C:\Users\huao\Desktop\MyPythonCode\reorder_edgelist\Wiki-Vote_reorder.txt"
    
    # 读取图数据文件
    # edges = read_graph_data(r'C:\\Users\\huao\Desktop\\MyPythonCode\dataset\Social networks\Wiki-Vote.txt')
    # edges = read_graph_data(r'C:\\Users\\huao\Desktop\\MyPythonCode\dataset\Amazon  networks\Amazon0601.txt')
    edges = read_graph_data(input_path)

    # 统计每个点的度数
    degrees = compute_degrees(edges)

    # 选择最佳阈值，并统计稠密子图的顶点集
    threshold = select_threshold(edges, degrees)

    #生成重排序后的edgelist文件
    generator_reorder_edgelist(edges,threshold,output_path)

