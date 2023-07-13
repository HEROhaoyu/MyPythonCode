#!/bin/bash

#该脚本用来测试pagerank性能
# 定义变量
dateset_name="MyGenerateData_15_1024.edgelist"
node_num=15
edge_num=1024
directory_name="pagerank_10_15_1024"
run_num=10

# # 第一步：生成数据集
/home/hedonghao/generate_graph/g500KronGenerator/yche-bin/yche_generator_omp ${node_num} -e ${edge_num} -o /home/hedonghao/generate_graph/MyGenerateData/${dateset_name}
# 展示数据集文件大小
echo "顶点数量为：2^$node_num，平均度数为:$edge_num的数据集的大小为："
du -h /home/hedonghao/generate_graph/MyGenerateData/${dateset_name}
# 第二步：数据集格式转化
mkdir -p /home/hedonghao/graph/dataset/${directory_name}/CPU
mkdir -p /home/hedonghao/graph/dataset/${directory_name}/NPU
mkdir -p /home/hedonghao/graph/output/${directory_name}/
mkdir -p /home/hedonghao/graph/output/${directory_name}/Mylog/
/home/hedonghao/graph/build/tools/graph-convert/graph-convert --edgelist2gr --edgeType=void /home/hedonghao/generate_graph/MyGenerateData/${dateset_name} /home/hedonghao/graph/dataset/${directory_name}/CPU/dataset.gr
echo "wx1186405"|sudo chmod 777 "/home/hedonghao/graph/dataset/${directory_name}/CPU/dataset.gr"
# 运行代码
# 执行CPU代码
/home/hedonghao/graph/build/lonestar/analytics/distributed/pagerank/pagerank-pull-dist /home/hedonghao/graph/dataset/${directory_name}/CPU/dataset.gr -tolerance=0.000001 -damping_factor=0.85 -maxIterations=4294967295 -runs=10 -output=true -outputLocation=/home/hedonghao/graph/output/${directory_name}/ 1>>/home/hedonghao/graph/output/${directory_name}/Mylog/cpu_pagerank_log.txt
# 执行NPU代码
cp -i /home/hedonghao/generate_graph/MyGenerateData/${dateset_name} /home/hedonghao/graph/dataset/${directory_name}/NPU/dataset.txt
echo "wx1186405"|sudo chmod 777 "/home/hedonghao/graph/dataset/${directory_name}/NPU/dataset.txt"
echo "wx1186405"|sudo python /home/hedonghao/graph/python_code/pagerank_with_mindspore.py --name=${directory_name} --runs=${run_num} 1>>/home/hedonghao/graph/output/${directory_name}/Mylog/npu_pagerank_log.txt
echo "wx1186405"|sudo chmod 777 -R /home/hedonghao/graph/output/${directory_name}/profiler/profiler/
