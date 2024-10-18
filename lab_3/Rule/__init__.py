from Node import Node
from typing import List
from Label import Label

class Rule:
    def __init__(self, number: int, out_node: Node, node_arr: List[Node], label=Label.OPEN):
        self.number = number
        self.out_node = out_node
        self.node_arr = node_arr  # массив входных вершин, связанных связкой И
        self.label = label  # открытое/закрытое/запрещенное

