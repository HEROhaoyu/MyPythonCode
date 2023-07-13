import numpy as np
import time
import os
import argparse
import mindspore
from mindspore import Tensor
from mindspore import numpy
from mindspore import dtype as mstype
import mindspore.ops as ops
from mindspore import Profiler
def read_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default = None)
    
def read_edges(filename):
    print("执行mind_graph.py代码，生成图数据")
    t1 = time.time()#统计程序耗时
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
    t2 = time.time()
    print("read graph finished in time:",t2-t1)
    return vertices_orginal,edges_reorder,id_map


def BFSMatmul(x,y,eye):
    # matmul = ops.MatMul()
    # x = matmul(x, eye)
    add = ops.Add() 
    sum = add(x, y)                
    op = ops.ReduceMin(keep_dims=True)        
    output = op(sum,0)
    return output

def process_graph(vertices_orginal,edges_reorder,source_node):
    print("执行Matrix_BFS.py代码，使用mindspore进行计算")
    vertex_num=len(vertices_orginal)
    matrix = Tensor(shape=(vertex_num,vertex_num),dtype=mstype.float16,init='zeros')
    
    eye = Tensor(np.eye(vertex_num),mstype.float16)#np.eye用于生成对角阵
    V = np.ones([vertex_num,vertex_num], dtype=np.int16) * 100#np.ones用于生成单位阵
    V[source_node] = 0
    V = Tensor(V,mstype.int16)
    finished = False
    itr = 0
    t1 = time.time()
    while(not finished):
        res = BFSMatmul(matrix, V, eye)
        transpose = ops.Transpose()
        res_perm = (1,0) 
        V1 = transpose(res,res_perm)
        finished = numpy.array_equal(V,V1)
        if finished == False:
            V = V1
        print("itr",itr,"finished")
        itr=itr+1
    t2 = time.time()
    V = V.asnumpy()
    print("BFS finished in:",t2-t1)
    return V;
    

if __name__ == "__main__":
    #读取参数
    source_node=read_argument()
    #开启Profiler
    mindspore.set_context(mode=mindspore.GRAPH_MODE, device_target="Ascend")
    profiler = Profiler(output_path="/home/hedonghao/graph/output/"+directory_name+"/profiler",profile_memory=True,aicore_metrics=1,l2_cache=True)#初始化分析器
    # 检查文件
    check_file()
    #读图
    ID,matrix,table=read_graph()
    # 处理图
    process_graph(ID,matrix,table,directory_name,source_node)
    profiler.analyse()#关闭分析器
