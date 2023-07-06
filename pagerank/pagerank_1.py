import numpy as np

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
    max_id = 0
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            edges.append((start, end))
            vertices.add(start)
            vertices.add(end)
            max_id = max(max_id, start, end)
    return edges, vertices,max_id

def build_adjacency_matrix(edges, vertices):
    """
    根据边列表和顶点集合构建邻接矩阵，并返回邻接矩阵和顶点ID映射。

    Args:
        edges (list): 边列表。
        vertices (set): 顶点集合。

    Returns:
        tuple: 包含邻接矩阵和顶点ID映射的元组。
    """
    # id_map = {v: i for i, v in enumerate(sorted(vertices))}
    n = max_vertex_num
    matrix = np.zeros((n, n),float)
    for edge in edges:
        start, end = edge
        matrix[start,end] = 1
    return matrix

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
    n = max_vertex_num
    deg_out = np.sum(adjacency_matrix, axis=1)
    transfer_matrix = adjacency_matrix / np.where(deg_out[:, np.newaxis] != 0, deg_out[:, np.newaxis], 1)
    pagerank = np.ones(n,float)/n
    # pagerank = np.ones(n) / n
    iter=0
    while True:
        new_pagerank = (1 - damping_factor) / n + damping_factor * np.dot(transfer_matrix.T, pagerank)
        # if (new_pagerank - pagerank).all < epsilon:
        # diff = np.max(np.abs(new_pagerank - pagerank))  # 计算新旧PageRank值之间的最大差异
        # if(diff<epsilon):
        # if np.linalg.norm(new_pagerank - pagerank) < epsilon:
        #     break
        # if sum(abs(new_pagerank - pagerank)) < epsilon:
        #     break
        if iter>100:
            break
        iter=iter+1
        pagerank = new_pagerank
    return pagerank

def write_pagerank(filename, pagerank):
    """
    将PageRank结果写入文件。

    Args:
        filename (str): 结果文件名。
        pagerank (numpy.ndarray): 包含每个节点的PageRank值的数组。
        id_map (dict): 顶点ID映射。

    Returns:
        None
    """
    with open(filename, 'w') as file:
        # for v, pr in id_map.items():
        #     file.write(f"{v} {pagerank[pr]}\n")
        for i in range(max_vertex_num):
            file.write(f"{i} {pagerank[i]}\n")



# 输入边文件名
edge_filename = "E:\华科实验室论文\MyPythonCode\pagerank\\barabasi-20000.txt"

# 读取边数据和顶点集合
edges, vertices, max_id = read_edges(edge_filename)
max_vertex_num = max_id+1
# 构建邻接矩阵和顶点ID映射
adjacency_matrix = build_adjacency_matrix(edges, vertices)

# 计算PageRank
pagerank = calculate_pagerank(adjacency_matrix)

# 写入结果文件
result_filename = "E:\华科实验室论文\MyPythonCode\pagerank\pagerank22.txt"
write_pagerank(result_filename, pagerank)

print("PageRank计算完成，结果已写入pagerank.txt文件。")
