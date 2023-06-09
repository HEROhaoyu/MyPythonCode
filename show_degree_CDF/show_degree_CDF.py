# CDF (cumulative distribution function) 累计分布函数
import matplotlib.pyplot as plt
import numpy as np


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

def plot_degree_distribution(degrees):
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

    # Calculate cumulative degree distribution
    cumulative_y = np.cumsum(y) / sum(y)

    # Plotting the cumulative degree distribution
    plt.figure(figsize=(10, 6))
    plt.plot(x, cumulative_y, 'bo-')
    plt.xlabel('Degree')
    plt.ylabel('Cumulative Distribution')
    plt.title('Degree Cumulative Distribution')
    plt.grid(True)

    plt.savefig('E:\华科实验室论文\MyPythonCode\show_degree_CDF\subgraph_cumulative_degree.png')
    plt.close()


if __name__ == "__main__":
    file_path = 'E:\华科实验室论文\MyPythonCode\generate_reorder_subgraph\dense_edges.txt'
    edges, degrees = read_graph_dataset(file_path)
    plot_degree_distribution(degrees)
