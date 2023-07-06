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
    vertices = set()
    vertices1 = set()
    id_map = {}
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            vertices1.add(start)
            vertices1.add(end)            
            #顶点重映射
            if start not in id_map:
                id_map[start] = len(id_map)
            if end not in id_map:
                id_map[end] = len(id_map)
            start = id_map[start]
            end = id_map[end]
            edges.append((start, end))
            vertices.add(start)
            vertices.add(end)
    return edges, vertices, vertices1,id_map

def build_adjacency_matrix(edges, vertices):
    """
    根据边列表和顶点集合构建邻接矩阵，并返回邻接矩阵和顶点ID映射。

    Args:
        edges (list): 边列表。
        vertices (set): 顶点集合。

    Returns:
        tuple: 包含邻接矩阵和顶点ID映射的元组。
    """
    n = len(vertices)
    matrix = np.zeros((n, n))
    for edge in edges:
        start, end = edge
        matrix[start][end] = 1
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
    n = adjacency_matrix.shape[0]
    deg_out = np.sum(adjacency_matrix, axis=1)#计算每个节点的出度，axis=1表示按行求和
    transfer_matrix = np.zeros_like(adjacency_matrix)

    for i in range(n):
        if deg_out[i] != 0:
            transfer_matrix[i] = adjacency_matrix[i] / deg_out[i]

    pagerank = np.ones(n) / n
    iter = 0

    # while True:
    for i in range(2):
        new_pagerank = np.zeros_like(pagerank)

        for i in range(n):
            for j in range(n):
                if adjacency_matrix[j][i] != 0:
                    new_pagerank[i] += damping_factor * pagerank[j] / deg_out[j]

        new_pagerank += (1 - damping_factor) / n

        if np.linalg.norm(new_pagerank - pagerank, ord=1) < epsilon:
            break

        pagerank = new_pagerank
        iter += 1
        print("第{}次迭代".format(iter))

    return pagerank

def write_pagerank(pagerank_vector, vertex,id_map, output):
    with open(output, 'w') as file:
        for v in vertex:
            file.write('{}\t{}\n'.format(v, format(pagerank_vector[id_map[v]], '.6f').rstrip('0').rstrip('.')))

# 输入边文件名
edge_filename = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote.txt"

# 读取边数据和顶点集合
edges, vertices, vertices1,id_map = read_edges(edge_filename)

# 构建邻接矩阵和顶点ID映射
matrix = build_adjacency_matrix(edges, vertices)

# 计算PageRank
pagerank = calculate_pagerank(matrix)

# 写入结果文件
result_filename = "E:\华科实验室论文\MyPythonCode\pagerank\pagerank19.txt"
write_pagerank(pagerank, vertices1,id_map,result_filename)

print("PageRank计算完成，结果已写入pagerank.txt文件。")
