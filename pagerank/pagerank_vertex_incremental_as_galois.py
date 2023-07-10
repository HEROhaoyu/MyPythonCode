

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
        #检查residual是否全部小于tolerance,如果是则跳出循环
        for src in vertices:
            if residual[src] > tolerance:
                break

        if not changed:
            print('Converged after %d iterations.' % (i + 1))
            break

    return pagerank


def write_pagerank(pagerank, output):
    with open(output, 'w') as file:
        for v in pagerank:
            file.write('{}\t{}\n'.format(v, format(pagerank[v], '.6f').rstrip('0').rstrip('.')))


if __name__ == '__main__':
    # input_file = "C:\\Users\\huao\\Desktop\\MyPythonCode\\pagerank\\Wiki-Vote.txt"
    # output_file = "C:\\Users\\huao\\Desktop\\MyPythonCode\\pagerank\\Wiki-Vote-pagerank-matrix-vector-le6-1000-6.txt"
    input_file = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote.txt"
    output_file = "E:\华科实验室论文\MyPythonCode\pagerank\Wiki-Vote-pagerank_vertex_incremental_as_galois.txt"
    vertices, vertices_outdegree, vertices_in_neighbor = read_edges(input_file)

    # Calculate pagerank using incremental method
    pagerank = pagerank_incremental(vertices, vertices_outdegree, vertices_in_neighbor, damping_factor=0.85, tolerance=1e-6, max_iterations=1000)

    # Write pagerank values to file
    write_pagerank(pagerank, output_file)
