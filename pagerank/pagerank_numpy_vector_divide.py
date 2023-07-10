import numpy as np
import time
'''
问题记录:
1,遍历矩阵找非零元素的方法太慢了,可以考虑用稀疏矩阵的方法,后面发觉可以直接用边表
2,为了减少矩阵转置的次数,提前对矩阵进行转置,导致很多变量的含义都变了,导致后面的代码很难看懂
3,没有注意数组矩阵的类型,导致后面的计算出现了问题
4,忽略了一点,如果某个点的residual值小于tolerance,它的delta也应该置为0
5,注意不同的地方用不同的变量名,重名变量会导致奇奇怪怪的问题
6,最最愚蠢的错误,delta的计算方式写错了

'''
def read_edges(filename):
    vertices_orginal = set()
    id_map={}
    edges_reorder = []
    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            vertices_orginal.add(start)
            vertices_orginal.add(end)
            if start not in id_map:
                id_map[start]=len(id_map)
            if end not in id_map:
                id_map[end]=len(id_map)
            start=id_map[start]
            end=id_map[end]
            edges_reorder.append((start, end))

    return vertices_orginal,edges_reorder,id_map

def pagerank_incremental(vertices_len,edges_reorder, damping_factor=0.85, tolerance=1e-6, max_iterations=100):
    
    pagerank = np.zeros(vertices_len,np.float64)
    delta = np.zeros(vertices_len,np.float64)
    residual = np.ones(vertices_len,np.float64) * (1 - damping_factor)
    outdegree=np.zeros(vertices_len)
    #统计outdegree
    for src,dst in edges_reorder:
        outdegree[src]+=1

    #限制精度
    # dtype=np.float64
    # precision=np.finfo(dtype).precision

    record=set()
    for iter in range(max_iterations):
        #添加增量
        pagerank=np.add(pagerank,residual)
        #计算增量
        delta=np.zeros(vertices_len,float)
        # delta=np.round(np.divide(residual,outdegree)*damping_factor,precision)
        delta=np.divide(residual,outdegree,out=delta,where=(outdegree!=0))*damping_factor
        residual=np.zeros(vertices_len,np.float64)


        #增量值累加  
        for src,dst in edges_reorder:
            residual[dst]+=delta[src]
        residual[residual<tolerance]=0
        if np.sum(np.greater(residual, tolerance)) == 0:
            print('Converged after %d iterations.' % (iter + 1))
            break

    return pagerank


def write_pagerank(pagerank, output,vertices_orginal,id_map):
    with open(output, 'w') as file:
        for v in vertices_orginal:
            file.write('{}\t{}\n'.format(v, format(pagerank[id_map[v]], '.6f').rstrip('0').rstrip('.')))


if __name__ == '__main__':
    input_file = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote.txt"
    output_file = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote-pagerank_numpy_vector_divide.txt"
    #读图
    t1=time.time()
    vertices_orginal,edges_reorder,id_map = read_edges(input_file)
    t2=time.time()
    print(f"读图时间: {t2-t1}秒")
    vertices_len=len(vertices_orginal)
    # Calculate pagerank using incremental method
    pagerank = pagerank_incremental(vertices_len,edges_reorder,damping_factor=0.85, tolerance=1e-6, max_iterations=100)
    t3=time.time()
    print(f"计算PageRank时间: {t3-t2}秒")
    # Write pagerank values to file
    write_pagerank(pagerank, output_file,vertices_orginal,id_map)
    t4=time.time()
    print(f"写入PageRank计算结果时间: {t4-t3}秒")
