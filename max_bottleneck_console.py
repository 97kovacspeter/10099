def read_file():
    graphs = {}
    index = 0
    while True:
        data = input().split(' ')
        vertex = int(data[0])
        edge = int(data[1])
        if vertex == 0 or edge == 0:
            return graphs
        matrix = [ [ 0 for i in range(vertex+1)] for j in range(vertex+1)]
        for _ in range(edge):
            data = input().split(' ')
            start = int(data[0])
            end = int(data[1])
            weight = int(data[2])
            matrix[start][end] = weight
            matrix[end][start] = weight
        data = input().split(' ')
        graphs[index] = {}
        graphs[index]['vertex'] = vertex
        graphs[index]['edge'] = edge
        graphs[index]['start'] = int(data[0])
        graphs[index]['end'] = int(data[1])
        graphs[index]['tourists'] = int(data[2])
        graphs[index]['matrix'] = matrix
        index += 1

def solve_max_bottleneck(graph):
    dp = graph['matrix']
    for k in range(graph['vertex']+1):
        for i in range(graph['vertex']+1):
            for j in range(graph['vertex']+1):
                dp[i][j] = max(dp[i][j], min(dp[i][k], dp[k][j]))
    weight = dp[graph['start']][graph['end']]
    i = 0
    while True:
        if i*(weight - 1) >= graph['tourists']:
            return i
        i += 1

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
