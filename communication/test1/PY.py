# coding=utf-8
import os
import time

def read_edges(filename):
    vertices = set()
    vertices_outdegree = {}
    vertices_in_neighbor = {}

    with open(filename, 'r') as file:
        for line in file:
            start, end = map(int, line.strip().split())
            if start not in vertices_outdegree:
                vertices_outdegree[start] = 1
            else:
                vertices_outdegree[start] += 1
            if end not in vertices_in_neighbor:
                vertices_in_neighbor[end] = set()
            vertices_in_neighbor[end].add(start)
            vertices.add(start)
            vertices.add(end)

    return vertices, vertices_outdegree, vertices_in_neighbor


def pagerank_incremental(vertices, vertices_outdegree, vertices_in_neighbor, damping_factor=0.85, tolerance=1e-6, max_iterations=100000):
    n = len(vertices)
    pagerank = {v: 0 for v in vertices}
    delta = {v: 0 for v in vertices}
    residual = {v: 1 - damping_factor for v in vertices}

    for i in range(max_iterations):
        changed = False

        for src in vertices:
            delta[src] = 0
            if residual[src] > tolerance:
                old_residual = residual[src]
                pagerank[src] += old_residual
                residual[src] = 0.0
                if src in vertices_outdegree:
                    delta[src] = old_residual * damping_factor / vertices_outdegree[src]
                    changed = True

        for src in vertices:
            sum_delta = 0
            if src in vertices_in_neighbor: 
                for n in vertices_in_neighbor[src]:
                    if delta[n] > 0:
                        sum_delta += delta[n]
                if sum_delta > 0:
                    residual[src] = sum_delta

        # 检查residual是否全部小于tolerance，如果是则跳出循环
        if all(residual[src] <= tolerance for src in vertices):
            print('Converged after %d iterations.' % (i + 1))
            break

        if not changed:
            print('Converged after %d iterations.' % (i + 1))
            break

    return pagerank


def write_pagerank_to_pipe(pagerank):
    # 获取管道文件描述符
    pipe_fd = int(os.getenv("PIPE_FD"))

    # 创建管道文件对象
    pipe_out = os.fdopen(pipe_fd, "wb")

    # 将字典数据序列化为字符串
    data=""
    for key in pagerank:
        data += str(key) + " " + str(pagerank[key]) + "\n"
    
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

    vertices, vertices_outdegree, vertices_in_neighbor = read_edges(input_file)

    # Calculate pagerank using incremental method
    pagerank = pagerank_incremental(vertices, vertices_outdegree, vertices_in_neighbor, damping_factor=0.85, tolerance=1e-6, max_iterations=1000)

    # Write pagerank values to file
    write_pagerank_to_pipe(pagerank)