from collections import defaultdict

class Graph():
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def DFS_util(self, s, visited):
        visited[s] = True
        print(s)

        for i in self.graph[s]:
            if visited[i] == False:
                self.DFS_util(i, visited)


    def depth_first_search(self, s):
        visited = [False] * len(self.graph)
        self.DFS_util(s, visited)


graph = Graph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 2)
graph.add_edge(2, 0)
graph.add_edge(2, 3)
graph.add_edge(3, 3)

if __name__ == '__main__':
    graph.depth_first_search(2)
