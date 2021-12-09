import math
import timeit

def read_file():
    graphs = {}
    index = 0
    with open('input0.txt', 'r') as file:
        while True:
            graph = []
            data = file.readline().split(' ')
            vertex = int(data[0])
            edge = int(data[1])
            if vertex == 0 or edge == 0:
                return graphs            
            for _ in range(edge):
                data = file.readline().split(' ')
                start = int(data[0])
                end = int(data[1])
                weight = int(data[2])
                graph.append([start, end, weight])
                graph.append([end, start, weight])
            data = file.readline().split(' ')
            graphs[index] = {}
            graphs[index]['vertex'] = vertex
            graphs[index]['edge'] = edge
            graphs[index]['start'] = int(data[0])
            graphs[index]['end'] = int(data[1])
            graphs[index]['tourists'] = int(data[2])
            graphs[index]['graph'] = graph
            index += 1

def path_exists(start, prev, current, path):
    if prev[current] == -1:
        return [False, path]
    if prev[current] == start:
        return [True, path]
    path.append(prev[current])
    return path_exists(start, prev, prev[current], path)

def find_bottleneck(graph, path):
    bottleneck = {}
    path.reverse()
    bottleneck['path'] = []
    bottleneck['path'].append(graph['end'])
    if not path:
        path.append(graph['end'])
    curr = path.pop()
    bottleneck['path'].append(curr)
    for i in graph['graph']:
        if i[0] == curr and i[1] == graph['end']:
            bottleneck['weight'] = i[2]
    while path:
        curr = path.pop()   
        for i in graph['graph']:
            if i[0] == curr and i[1] == bottleneck['path'][-1]:
                if bottleneck['weight'] > i[2]:
                    bottleneck['weight'] = i[2]
        bottleneck['path'].append(curr)
    for i in graph['graph']:
        if i[0] == bottleneck['path'][-1] and i[1] == graph['start']:
            if bottleneck['weight'] > i[2]:
                bottleneck['weight'] = i[2]
    bottleneck['path'].append(graph['start'])
    return bottleneck

def find_path(prev, new_path, start, end):
    if prev[new_path[-1]] == start:
        return new_path
    tmp = prev[new_path[-1]]
    if tmp is not end:
        new_path.append(tmp)
    return find_path(prev, new_path, start, end)

def update_bottleneck(graph, prev):
    new_path = []
    new_path.append(graph['end'])
    new_path = find_path(prev, new_path, graph['start'], graph['end'])
    new_path.remove(graph['end'])
    return find_bottleneck(graph, new_path)

def solve_max_bottleneck(graph):
    sorted_edges = sorted(graph['graph'], key=lambda x:x[2], reverse=True)
    prio_queue = []
    for i in sorted_edges:
        if i[0] not in prio_queue:
            prio_queue.append(i[0])
    dist = {}
    prev = {}
    for i in range(graph['vertex']):
        if i+1 is not graph['start']:
            dist[i+1] = 1000
            prev[i+1] = -1
        else:
            dist[i+1] = 0
    prio_queue.reverse()
    exists_path = False
    bottleneck = {}
    bottleneck['weight'] = 0
    bottleneck['path'] = []
    while prio_queue:
        u = prio_queue.pop()
        for i in graph['graph']:
            if i[0] == u and i[1] in prio_queue:
                if i[2] > bottleneck['weight'] and i[0] in bottleneck['path']:
                    bottleneck = update_bottleneck(graph, prev)
                tmp = dist[u] + 1
                if tmp <= dist[i[1]]:
                    dist[i[1]] = tmp
                    prev[i[1]] = u
        if not exists_path:
            exists_path, path = path_exists(graph['start'], prev, graph['end'], [])
            if exists_path:
                bottleneck = find_bottleneck(graph, path)
    weight = bottleneck['weight'] #guide
    i = 1
    while True:
        if i*weight + i > graph['tourists']:
            return i
        i += 1
    #return math.ceil(graph['tourists'] / weight)

def main():
    graphs = read_file()

    for i,_ in enumerate(graphs):
        scenario_number = i+1
        solution = solve_max_bottleneck(graphs[i])
        print(f'Scenario #{scenario_number}')
        print(f'Minimum Number of Trips = {solution}\n')

if __name__ == '__main__':
    #timeit.timeit('main()', number=1)
    main()
