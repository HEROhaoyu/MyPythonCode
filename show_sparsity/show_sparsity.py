edges = []
vertices = set()
with open('E:\华科实验室论文\MyPythonCode\dataset\Amazon  networks\Amazon0601.txt', 'r') as f:
    for line in f:
        edge = tuple(map(int, line.strip().split()))
        edges.append(edge)
        vertices.update(edge)
num_edges = len(edges)
num_vertices = len(vertices)
sparsity = num_edges / (num_vertices ** 2)
print(f'Number of edges: {num_edges}')
print(f'Number of vertices: {num_vertices}')
print(f'Sparsity: {sparsity}')