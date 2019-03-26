from collections import defaultdict


class Graph():
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def breadth_first_search(self, s):
        visited = [False] * len(self.graph)

        queue = []  # create the queue for bfs
        queue.append(s)  # append the source element to queue
        visited[s] = True  # mark the source node as visited

        while queue:
            s = queue.pop(0)
            print(s)

            for i in self.graph[s]:
                if visited[i] == False:
                    visited[i] = True
                    queue.append(i)


graph = Graph()
graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(1, 2)
graph.add_edge(2, 0)
graph.add_edge(2, 3)
graph.add_edge(3, 3)

if __name__ == '__main__':
    graph.breadth_first_search(2)
