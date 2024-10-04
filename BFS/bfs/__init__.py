class BFS:
    def __init__(self, graph):
        self.visited = []
        self.queue = []
        self.graph = graph

    def run(self, node):
        self.visited.append(node)
        self.queue.append(node)

        while self.queue:
            _ = self.queue.pop(0)

            print(_, end=" ")

            for neighbour in self.graph.nodes[_]:
                if neighbour not in self.visited:
                    self.visited.append(neighbour)
                    self.queue.append(neighbour)
