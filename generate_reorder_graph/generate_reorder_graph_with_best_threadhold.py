import numpy as np

def read_graph_data(file_path):
    """
    读取图数据文件并返回边的列表
    """
    # 载入数据，每行数据表示一条边，两个数字分别表示边的两个顶点，如果每行有超出两个数字，则只取前两个数字
    # edges = []
    # with open(file_path, "r") as f:
    #     for line in f.readlines():
    #         # edge = line.strip().split(',')#如果数据文件中的数据是用逗号分隔的，则用这行代码
    #         edge = line.strip().split()
    #         edges.append((int(edge[0]), int(edge[1])))
    edges = np.loadtxt(file_path,int)
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

def find_best_threshold(sorted_degrees, edges, degrees, coarse_ratio=0.1, medium_ratio=0.01, fine_ratio=0.001):
    """
    根据粗粒度、中粒度和细粒度搜索的比例找到数据集的最佳阈值

    参数：
    - sorted_degrees: 按度数从大到小排序的度数列表
    - edges: 边的列表
    - degrees: 度数字典，记录每个点的度数
    - coarse_ratio: 粗粒度搜索的比例，相对于度数最大值的比例
    - medium_ratio: 中粒度搜索的比例，相对于粗粒度搜索的阈值区间的比例
    - fine_ratio: 细粒度搜索的比例，相对于中粒度搜索的阈值区间的比例

    返回值：
    - best_fine_threshold: 最佳阈值
    - max_fine_avg_degree: 稠密子图的平均度数
    - dense_edges_count: 稠密子图的边的数量
    - dense_vertex_set: 稠密子图的顶点数量
    """
    # 粗粒度搜索
    max_degree = sorted_degrees[0][1]
    coarse_threshold_range = coarse_ratio * max_degree#粗粒度搜索的阈值区间,[0,coarse_threshold_range]
    coarse_thresholds = set(np.arange(0, max_degree, coarse_threshold_range))#np.arange(0, max_degree, coarse_threshold_range)返回一个数组，数组中的元素为0,coarse_threshold_range,2*coarse_threshold_range,...,max_degree
    best_coarse_threshold = None
    max_coarse_avg_degree = 0

    for threshold in coarse_thresholds:
        edge_count = 0
        vertex_set = set()

        for edge in edges:
            if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
                vertex_set.add(edge[0])
                vertex_set.add(edge[1])
                edge_count += 1

        if len(vertex_set) > 0:
            avg_degree = edge_count / len(vertex_set)
            if avg_degree > max_coarse_avg_degree:
                max_coarse_avg_degree = avg_degree
                best_coarse_threshold = threshold

    # 中粒度搜索
    medium_threshold_range = medium_ratio * coarse_threshold_range#中粒度搜索的阈值区间,[best_coarse_threshold - medium_threshold_range, best_coarse_threshold + medium_threshold_range]
    medium_thresholds = np.arange(best_coarse_threshold - medium_threshold_range, best_coarse_threshold + medium_threshold_range, medium_threshold_range)
    best_medium_threshold = None
    max_medium_avg_degree = 0

    for threshold in medium_thresholds:
        edge_count = 0
        vertex_set = set()

        for edge in edges:
            if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
                vertex_set.add(edge[0])
                vertex_set.add(edge[1])
                edge_count += 1

        if len(vertex_set) > 0:
            avg_degree = edge_count / len(vertex_set)
            if avg_degree > max_medium_avg_degree:
                max_medium_avg_degree = avg_degree
                best_medium_threshold = threshold

    # 细粒度搜索
    fine_threshold_range = fine_ratio * medium_threshold_range
    fine_thresholds = np.arange(best_medium_threshold - fine_threshold_range, best_medium_threshold + fine_threshold_range, fine_threshold_range)
    best_fine_threshold = None
    max_fine_avg_degree = 0
    best_fine_threshold_edge_count = 0
    best_fine_threshold_vertex_count = 0
    for threshold in fine_thresholds:
        edge_count = 0
        vertex_set = set()

        for edge in edges:
            if degrees[edge[0]] > threshold and degrees[edge[1]] > threshold:
                vertex_set.add(edge[0])
                vertex_set.add(edge[1])
                edge_count += 1

        if len(vertex_set) > 0:
            avg_degree = edge_count / len(vertex_set)
            if avg_degree > max_fine_avg_degree:
                max_fine_avg_degree = avg_degree
                best_fine_threshold = threshold
                best_fine_threshold_edge_count = edge_count
                best_fine_threshold_vertex_count = len(vertex_set)
                

    # 返回结果
    return best_fine_threshold, max_fine_avg_degree, best_fine_threshold_edge_count, best_fine_threshold_vertex_count

def generate_edgelist_txt(edges,best_fine_threshold,output_path):
    sparse_edgelist=[]
    with open(output_path,"w") as f:
        for edge in edges:
            if(edge[0]<best_fine_threshold or edge[1]<best_fine_threshold):
                sparse_edgelist.append(edge)
            else:
                f.write(f"{edge[0]} {edge[1]}\n")
        for edge in sparse_edgelist:
            f.write(f"{edge[0]} {edge[1]}\n")
    f.close()

    
if __name__ == "__main__":
    # 读取图数据文件
    # input_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\find_threshold\bio-DM-HT.edges"#复杂生物网络
    # input_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\find_threshold\\cit-DBLP.edges"#论文引用网络
    input_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\generate_reorder_graph\\Wiki-Vote.txt"#社交网络
    # input_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\find_threshold\\road-euroroad.edges"#道路网络
    # input_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\find_threshold\\petster-friendships-hamster.edges"#社会网络
    output_path=r"C:\\Users\\huao\Desktop\\MyPythonCode\\generate_reorder_graph\\Wiki-Vote_reorder_graph.txt"
    edges = read_graph_data(input_path)
    # dateset_name="petster-friendships-hamster社会网络"
    dateset_name="Wiki-Vote社交网络"
    # dateset_name="cit-DBLP论文引用网络"
    # dateset_name="bio-DM-HT复杂生物网络"
    # 定义参数
    # num_samples = 1000  # 随机采样的次数

    # 统计每个点的度数
    degrees = compute_degrees(edges)

    # 按度数进行排列
    sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)#按照度数从大到小排序

    # 找到最佳阈值
    best_fine_threshold, max_fine_avg_degree, best_fine_threshold_edge_count, best_fine_threshold_vertex_count = find_best_threshold(sorted_degrees, edges, degrees)
    
    #打印全部结果
    print("数据集名称：",dateset_name)
    print("最佳阈值：",best_fine_threshold)
    print("最佳阈值的平均度数：",max_fine_avg_degree)
    print("最佳阈值的边的数量：",best_fine_threshold_edge_count)
    print("最佳阈值的顶点的数量：",best_fine_threshold_vertex_count)

    #生成重排序边文件
    generate_edgelist_txt(edges,best_fine_threshold,output_path)