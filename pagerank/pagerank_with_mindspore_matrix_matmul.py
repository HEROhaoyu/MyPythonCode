import time
import numpy as np
import mindspore
import mindspore.ops as ops
from mindspore import dtype as mstype
from mindspore import Tensor
from mindspore.profiler import Profiler
import argparse

print("执行pagerank_with_mindspore.py代码，使用mindspore进行计算\n")

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, default = None)
parser.add_argument('--runs', type=str, default = None)
directory_name=parser.parse_args().name
runs=int(parser.parse_args().runs)


def read_edges(filename):
    """
    从边文件中读取边数据，并返回边列表和顶点集合。
    Args:
        filename (str): 边文件名。
    Returns:
        tuple: 包含边列表和顶点集合的元组。
    """
    edges = []
    vertices = set()
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            edges.append((start, end))
            vertices.add(start)
            vertices.add(end)
    return edges, vertices

def build_adjacency_matrix(edges, vertices):
    """
    根据边列表和顶点集合构建邻接矩阵，并返回邻接矩阵和顶点ID映射。
    Args:
        edges (list): 边列表。
        vertices (set): 顶点集合。
    Returns:
        tuple: 包含邻接矩阵和顶点ID映射的元组。
    """
    id_map = {v: i for i, v in enumerate(sorted(vertices))}
    n = len(id_map)
    matrix = np.zeros((n, n), dtype=np.float32)
    for edge in edges:
        start, end = edge
        matrix[id_map[start], id_map[end]] = 1
    return matrix, id_map

def calculate_pagerank(adjacency_matrix, damping_factor=0.85, epsilon=1e-6):
    """
    计算PageRank值。
    Args:
        adjacency_matrix (numpy.ndarray): 邻接矩阵。
        damping_factor (float, optional): 阻尼因子，默认为0.85。
        epsilon (float, optional): 收敛阈值，默认为1e-6。
    Returns:
        numpy.ndarray: 包含每个节点的PageRank值的数组。
    """
    n = adjacency_matrix.shape[0]
    deg_out = np.sum(adjacency_matrix, axis=1)
    transfer_matrix = adjacency_matrix / np.where(deg_out[:, np.newaxis] != 0, deg_out[:, np.newaxis], 1)
    pagerank = np.ones(n, dtype=np.float32) / n
    pagerank = Tensor(pagerank, mstype.float32)
    transfer_matrix = Tensor(transfer_matrix, mstype.float32)

    start_time = time.time()
    itr = 0
    while True:
        new_pagerank = (1 - damping_factor) / n + damping_factor * ops.matmul(transfer_matrix, pagerank)
        norm_diff = ops.norm(new_pagerank - pagerank, 0)
        if norm_diff < epsilon:
            break
        pagerank = new_pagerank
        itr=itr+1
    print("本次运行",itr,"次迭代收敛")
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"PageRank计算时间: {elapsed_time}秒")

    return pagerank

def write_pagerank(filename, pagerank, id_map):
    """
    将PageRank结果写入文件。
    Args:
        filename (str): 结果文件名。
        pagerank (numpy.ndarray): 包含每个节点的PageRank值的数组。
        id_map (dict): 顶点ID映射。
        original_ids (dict): 映射前的原始ID映射。
    Returns:
        None
    """
    # 将PageRank结果写入文件
    pr_values = pagerank.asnumpy()  # 将Tensor转换为NumPy数组
    results = [f"{v} {pr_values[pr]}\n" for v, pr in id_map.items()]
    result_str = ''.join(results)

    with open(filename, 'w') as file:
        file.write(result_str)

if __name__ == "__main__":
    # 输入文件名
    # edge_filename = "/home/hedonghao/graph/dataset/"+directory_name+"/NPU/dataset.txt"  # 原始数据集文件
    # result_filename = "/home/hedonghao/graph/output/"+directory_name+"/NPU_pagerank_result.txt"  # 结果文件
    edge_filename = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote.txt"  # 原始数据集文件
    result_filename = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote-pagerank_with_mindspore_matrix_matmul.py.txt"  # 结果文件
    # 读取边数据和顶点集合
    start_time = time.time()
    edges, vertices = read_edges(edge_filename)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"读取边数据时间: {elapsed_time}秒")
    print(f"数据集顶点数: {len(vertices)}")
    print(f"数据集边数: {len(edges)}")

    # 构建邻接矩阵和顶点ID映射
    start_time = time.time()
    adjacency_matrix, id_map = build_adjacency_matrix(edges, vertices)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"构建邻接矩阵时间: {elapsed_time}秒")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #开启Profiler
    # mindspore.set_context(mode=mindspore.GRAPH_MODE, device_target="Ascend")
    # profiler = Profiler(output_path="/home/hedonghao/graph/output/"+directory_name+"/profiler",profile_memory=True,aicore_metrics=1,l2_cache=True)#初始化分析器
    # 计算PageRank
    start_time = time.time()
    for i in range(runs):
        pagerank = calculate_pagerank(adjacency_matrix)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"计算{runs}次PageRank: {elapsed_time}秒")
    # profiler.analyse()#关闭分析器
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # 写入结果文件
    start_time = time.time()
    write_pagerank(result_filename, pagerank, id_map)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"写入结果文件时间: {elapsed_time}秒")

    print("PageRank计算完成，结果已写入output目录。")
