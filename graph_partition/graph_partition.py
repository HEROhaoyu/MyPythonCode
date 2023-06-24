import networkx as nx

def extract_dense_subgraph(input_file, output_file, method, target_vertex_count):
    # 读取原始数据集文件
    graph = nx.DiGraph()
    edges = set()  # 用于去重边
    
    with open(input_file, 'r') as file:
        for line in file:
            # 每一行表示一条边，包含起始点和终点
            source, target = map(int, line.strip().split())
            edges.add((source, target))
    
    # 添加边到图中
    graph.add_edges_from(edges)
    
    # 打印原始图数据集的信息
    print("原始图数据集信息:")
    print("顶点数:", graph.number_of_nodes())
    print("边数:", graph.number_of_edges())
    print("平均度数:", 2 * graph.number_of_edges() / graph.number_of_nodes())
    
    # 根据不同的方式进行稠密子图划分
    if method == ' ':
        # 图划分方式
        
        # 使用弱连通组件算法找到原始图中的连通分量
        components = nx.weakly_connected_components(graph)
        
        # 计算每个连通分量的平均度数
        avg_degrees = []
        for component in components:
            subgraph = graph.subgraph(component)
            avg_degree = 2 * subgraph.number_of_edges() / subgraph.number_of_nodes()
            avg_degrees.append((list(component), avg_degree))
        
        # 按照平均度数从高到低排序
        sorted_components = sorted(avg_degrees, key=lambda x: x[1], reverse=True)
        
        # 获取最稠密的连通分量，使得总顶点数小于等于 target_vertex_count
        selected_components = []
        total_vertex_count = 0
        for component, avg_degree in sorted_components:
            if total_vertex_count + len(component) > target_vertex_count:
                remaining_vertices = target_vertex_count - total_vertex_count
                selected_components.append(component[:remaining_vertices])
                break
            selected_components.append(component)
            total_vertex_count += len(component)
        
        # 构建最终的稠密子图
        subgraph = graph.subgraph([v for component in selected_components for v in component])
    elif method == 'clustering':
        # 图聚类方式
        
        # 将有向图转换为无向图
        undirected_graph = graph.to_undirected()
        
        # 使用图聚类算法计算每个节点的聚类系数
        clustering = nx.clustering(undirected_graph)
        
        # 根据聚类系数对节点进行排序
        sorted_nodes = sorted(clustering, key=clustering.get, reverse=True)
        
        # 选择排名靠前的节点作为稠密子图的顶点
        dense_subgraph = sorted_nodes[:target_vertex_count]
        
        #将稠密顶点加入到稠密子图中
        subgraph = nx.DiGraph()
        subgraph.add_nodes_from(dense_subgraph)
        # #遍历dense_subgraph
        # for i in dense_subgraph:
        #     print(i)


        #遍历原始图，如果边的两个顶点都在稠密子图中，则将该边添加到稠密子图中
        for edge in graph.edges():
            source, target = edge  
            if source in dense_subgraph and target in dense_subgraph:
                # print(source, target)
                subgraph.add_edge(source, target)
        
        
    else:
        print("无效的方法选择")
        return
    
    # 打印稠密子图数据集的信息
    print("\n稠密子图数据集信息:")
    print("顶点数:", subgraph.number_of_nodes())
    print("边数:", subgraph.number_of_edges())
    print("平均度数:", 2 * subgraph.number_of_edges() / subgraph.number_of_nodes())
    
    # 输出稠密子图到文件
    with open(output_file, 'w') as file:
        for edge in subgraph.edges():
            file.write(str(edge[0]) + '\t' + str(edge[1]) + '\n')

# 使用示例：
input_file = 'E:\华科实验室论文\MyPythonCode\graph_partition\\twitter_combined.txt'
output_file = 'E:\华科实验室论文\MyPythonCode\graph_partition\dense_subgraph.txt'
# method = 'partition'
method = 'clustering'
target_vertex_count = 40000
extract_dense_subgraph(input_file, output_file, method, target_vertex_count)
