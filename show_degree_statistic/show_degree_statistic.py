#代码功能：统计实际数据集中顶点的度数分布情况
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# plt.switch_backend('Agg')
import numpy as np
import argparse

def read_graph_dataset(file_path):
    edges = []
    degrees = {}
    with open(file_path, 'r') as file:
        for line in file:
            edge = line.strip().split()
            source_vertex = int(edge[0])
            target_vertex = int(edge[1])
            
            edges.append((source_vertex, target_vertex))

            # Update degrees dictionary for source vertex
            if source_vertex in degrees:
                degrees[source_vertex] += 1
            else:
                degrees[source_vertex] = 1

            # Update degrees dictionary for target vertex
            if target_vertex in degrees:
                degrees[target_vertex] += 1
            else:
                degrees[target_vertex] = 1

    return edges, degrees

def plot_degree_distribution(degrees,directory_name):
    degree_values = list(degrees.values())
    degree_counts = {}

    # Count the occurrences of each degree
    for degree in degree_values:
        if degree in degree_counts:
            degree_counts[degree] += 1
        else:
            degree_counts[degree] = 1

    # Sort the degrees in ascending order
    sorted_degrees = sorted(degree_counts.items())

    x = [degree[0] for degree in sorted_degrees]
    y = [degree[1] for degree in sorted_degrees]

    # Plotting the degree distribution
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'bo-')
    plt.xlabel('Degree')
    plt.ylabel('Count')
    plt.title('Degree Distribution')
    plt.grid(True)

    # Add text to the plot
    num_edges = len(edges)
    num_vertices = len(degrees)
    average_degree = num_edges *2 / num_vertices
    # average_degree = sum(degrees.values())/num_vertices
    max_degree = max(degrees.values())
    sorted_degrees = sorted(degrees.values())
    # sorted_degrees=degrees
    percentile_0 = np.percentile(sorted_degrees, 0)
    percentile_25 = np.percentile(sorted_degrees, 25)#np.percentile找到一组数的分位数值，如四分位数等(具体什么位置根据自己定义)，表示列表里有25%的数小于这个数
    percentile_50 = np.percentile(sorted_degrees, 50)
    percentile_75 = np.percentile(sorted_degrees, 75)
    percentile_80 = np.percentile(sorted_degrees, 80)
    percentile_90 = np.percentile(sorted_degrees, 90)
    percentile_95 = np.percentile(sorted_degrees, 95)
    percentile_99 = np.percentile(sorted_degrees, 99)
    percentile_100 = np.percentile(sorted_degrees, 100)
    text = f"Graph Information:\nNumber of edges: {num_edges}\nNumber of vertices: {num_vertices}\nAverage degree: {average_degree:.2f}\nMaximum degree: {max_degree}\nDegree of top 0% vertices: {percentile_0:.2f}\nDegree of top 25% vertices: {percentile_25:.2f}\nDegree of top 50% vertices: {percentile_50:.2f}\nDegree of top 75% vertices: {percentile_75:.2f}\nDegree of top 80% vertices: {percentile_80:.2f}\nDegree of top 90% vertices: {percentile_90:.2f}\nDegree of top 95% vertices: {percentile_95:.2f}\nDegree of top 99% vertices: {percentile_99:.2f}\nDegree of top 100% vertices: {percentile_100:.2f}"
    plt.text(0.5, 0.95, text, transform=plt.gca().transAxes, fontsize=14, verticalalignment='top',horizontalalignment='left')

    # plt.show() #没有图形界面的服务器好像用不了这个函数，需要把图像保存下来再查看
    # plt.savefig('/home/hedonghao/graph/dataset/'+directory_name+'/NPU/image.png')
    plt.savefig('E:\华科实验室论文\MyPythonCode\show_degree_statistic\graph.png')
    plt.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default = None)
    directory_name=parser.parse_args().name
    # file_path = '/home/hedonghao/graph/dataset/'+directory_name+'/NPU/dataset.txt'
    file_path = 'E:\华科实验室论文\MyPythonCode\show_degree_statistic\graph.txt'
    edges, degrees = read_graph_dataset(file_path)
    plot_degree_distribution(degrees,directory_name)