# coding=utf-8
import numpy as np
import os
import time

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

def write_pagerank_to_pipe(pagerank,vertices_orginal,id_map):
    # 将字典数据序列化为字符串
    data=""
    for v in vertices_orginal:
        data += str(v) + " " + str(pagerank[id_map[v]]) + "\n"
    
    # 获取管道文件描述符
    pipe_fd = int(os.getenv("PIPE_FD"))

    # 创建管道文件对象
    pipe_out = os.fdopen(pipe_fd, "wb")
    
    # 分块大小
    chunk_size = 1024

    # 数据长度和分块大小写入管道
    pipe_out.write(str(len(data)).zfill(16).encode())
    pipe_out.write(str(chunk_size).zfill(16).encode())
    pipe_out.flush()

    # 循环写入数据分块
    total_bytes_sent = 0
    while total_bytes_sent < len(data):
        # 获取当前分块的数据
        chunk = data[total_bytes_sent:total_bytes_sent + chunk_size]

        # 尝试写入数据到管道
        while True:
            try:
                pipe_out.write(chunk.encode())
                pipe_out.flush()
                break
            except BlockingIOError:
                # 管道已满，等待管道可写
                print("管道已满，等待管道可写")
                time.sleep(0.1)

        total_bytes_sent += len(chunk)

    # 关闭管道写入端
    pipe_out.close()



if __name__ == '__main__':
    input_file = "/home/liaoyj/project/Myproject/communication/Wiki-Vote.txt"

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
    write_pagerank_to_pipe(pagerank,vertices_orginal,id_map)
    t4=time.time()
    print(f"写入PageRank计算结果时间: {t4-t3}秒")    