import numpy as np

def read_edges(filename):
    vertices = set()
    vertices1 = set()
    edges = []
    id_map = {}
    outdegree = {}
    inneighbour = {}
    outneighbour = {}
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
            #统计顶点出度
            if start not in outdegree:
                outdegree[start] = 1
            else:
                outdegree[start] += 1
            #统计入边邻居
            if end not in inneighbour:
                inneighbour[end] = [start]
            else:
                inneighbour[end].append(start)
            #统计出边邻居
            if start not in outneighbour:
                outneighbour[start] = [end]
            else:
                outneighbour[start].append(end)

    return vertices, vertices1,edges, id_map, outdegree, inneighbour,outneighbour
    
def pagerank_point(vertices, outdegree, inneighbour,outneighbour, damping_factor=0.85, convergence_threshold=1e-6, max_iterations=100000):
    n = len(vertices)
    # Create initial pagerank vector
    pagerank_vector = np.ones(n) / n
    #迭代运算
    for i in range(max_iterations):
        new_pagerank_vector = np.zeros(n)
        for v in vertices:
            if v not in inneighbour:
                continue
            for u in inneighbour[v]:
                new_pagerank_vector[v] += damping_factor * pagerank_vector[u] / outdegree[u]
            # if v not in outneighbour:
            #     continue
            # for u in outneighbour[v]:
            #     new_pagerank_vector[u] += damping_factor * pagerank_vector[v] / outdegree[v]
        new_pagerank_vector += (1 - damping_factor) / n
        # Check convergence using L1 norm
        if np.linalg.norm(new_pagerank_vector - pagerank_vector, ord=1) < convergence_threshold:
            break
        pagerank_vector = new_pagerank_vector
        print("第{}次迭代".format(i))
    return pagerank_vector

def write_pagerank(pagerank_vector, vertex,id_map, output):
    with open(output, 'w') as file:
        for v in vertex:
            file.write('{}\t{}\n'.format(v, format(pagerank_vector[id_map[v]], '.6f').rstrip('0').rstrip('.')))

if __name__ == '__main__':
    input_file = r"E:\\华科实验室论文\\MyPythonCode\\pagerank\\Wiki-Vote.txt"
    output_file = r"E:\\华科实验室论文\\MyPythonCode\\pagerank\\\Wiki-Vote-pagerank-point-1.txt"

    vertices, vertices1,edges, id_map, outdegree, inneighbour ,outneighbour= read_edges(input_file)

    # Calculate pagerank using point-wise multiplication method
    pagerank_vector = pagerank_point(vertices, outdegree, inneighbour, outneighbour,damping_factor=0.85, convergence_threshold=1e-6, max_iterations=1000)

    # Write pagerank values to file
    write_pagerank(pagerank_vector, vertices1,id_map, output_file)
