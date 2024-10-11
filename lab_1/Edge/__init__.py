from Node import Node


class Edge:
    def __init__(self, startNode: Node, endNode: Node, label):
        self.startNode = startNode
        self.endNode = endNode
        self.label = label
        self.used = False