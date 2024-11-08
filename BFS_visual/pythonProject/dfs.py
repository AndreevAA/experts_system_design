from typing import List, Deque, Optional
from collections import deque

import enum
import typing
import dataclasses

import networkx as nx
import matplotlib.pyplot as plt
import models
from typing import Optional, List, Dict

def _convert_edges(edges: List[models.Edge]) -> List[tuple]:
    return [
        (edge.start.number, edge.end.number)
        for edge in edges
    ]

def _convert_path(path: List[models.Node]) -> List[tuple]:
    if not path:
        return

    prev = path[0]
    edges = []
    for vert in path[1:]:
        edges.append((prev.number, vert.number))
        prev = vert
    return edges

def print_path(path: Optional[List[models.Node]]):
    if not path:
        print("no path")
    else:
        print(" -> ".join(map(lambda v: str(v.number), path)))

NODE_COLOR_MAP = {
    models.NodeState.WHITE: 'white',
    models.NodeState.GRAY: 'gray',
    models.NodeState.BLACK: 'blue',
}

def show_graph(
        graph: models.Graph,
        path: Optional[List[models.Node]] = None,
        node_color_map: Dict[int, str] = None,
    ) -> None:
    node_options = {"edgecolors": "tab:gray", "node_size": 500, "alpha": 0.9}
    edge_options = {"arrows": True, "arrowsize": 20, "alpha": 0.9}

    G = nx.DiGraph(directed=True)
    G.add_edges_from(_convert_edges(graph.edges()))

    if not node_color_map:
        node_color_map = {}
    for vert in graph.nodees():
        if vert.number not in node_color_map:
            node_color_map[vert.number] = NODE_COLOR_MAP[vert.state]

    if not path:
        path_edges = []
    else:
        path_edges = _convert_path(path)
    values = [node_color_map.get(node) for node in G.nodes()]

    red_edges = []
    black_edges = []
    for edge in G.edges():
        if edge not in path_edges:
            black_edges.append(edge)
        else:
            red_edges.append(edge)

    # Need to create a layout when doing
    # separate calls to draw nodes and edges
    # pos = nx.spring_layout(G)
    pos = nx.circular_layout(G)

    #  cmap=plt.get_cmap('jet'),
    nx.draw_networkx_nodes(G, pos, node_color=values, **node_options)
    nx.draw_networkx_labels(G, pos)

    nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='red', **edge_options)
    nx.draw_networkx_edges(G, pos, edgelist=black_edges, edge_color='black', **edge_options)

    plt.tight_layout()
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    from models import *
    graph = Graph(
        Edge(Node(1), Node(2)),
        Edge(Node(1), Node(4)),
        Edge(Node(2), Node(3)),
        Edge(Node(3), Node(4)),
    )
    path = [Node(1), Node(2), Node(3)]
    print_path(path)
    show_graph(graph, path)

class NodeState(enum.Enum):
    BLACK = 1
    GRAY = 2
    WHITE = 3


@dataclasses.dataclass(unsafe_hash=True)
class Node:
    """Вершина"""
    number: int
    state: NodeState = dataclasses.field(default=NodeState.WHITE, compare=False)


class EdgeState(enum.Enum):
    TRAVERSED = 1
    FREE = 2
    FORBIDDEN = 3


@dataclasses.dataclass
class Edge:
    """Ребро"""
    start: Node
    end: Node
    label: EdgeState = EdgeState.FREE


class Graph:
    """Граф"""

    def __init__(self, *edges: Edge):
        self._edges = list(edges)

    def edges(self) -> typing.List[Edge]:
        """Список рёбер"""
        return self._edges

    def nodees(self) -> typing.List[Node]:
        """Список вершин"""
        set_node = set()
        for edge in self._edges:
            set_node.add(edge.start)
            set_node.add(edge.end)
        return list(set_node)


class AlgorithmDFS:
    def __init__(self, graph: models.Graph):
        self._graph: models.Graph = graph

    def search(
            self,
            source: models.Node,
            target: models.Node
    ) -> Optional[List[models.Node]]:
        stack: Deque[models.Node] = deque()
        open_nodees: List[models.Node] = self._graph.nodees()
        close_nodees: List[models.Node] = list()

        stack.append(source)
        while stack:
            source = stack[-1]  # Stack.peek()
            edge = self._search_edge(source)
            if edge:
                edge.label = EdgeState.TRAVERSED
                stack.append(edge.end)

                if edge.end == target:
                    return list(stack)
            else:
                stack.pop()
                open_nodees.remove(source)
                close_nodees.append(source)

        return None

    def _search_edge(
            self,
            source: models.Graph
    ) -> Optional[models.Edge]:
        for edge in self._graph.edges():
            if edge.start == source \
                    and edge.label == models.EdgeState.FREE:
                return edge
        return None



graph = Graph(
    Edge(Node(1), Node(2)),
    Edge(Node(2), Node(3)),
    Edge(Node(3), Node(4)),

    Edge(Node(3), Node(6)),
    # Edge(node(6), node(3)),

    Edge(Node(5), Node(6)),
    Edge(Node(6), Node(7)),
    Edge(Node(6), Node(8)),
)

alg = AlgorithmDFS(graph)
source = Node(1)
target = Node(8)

path = alg.search(source, target)

utils.print_path(path)
utils.show_graph(graph, path, node_color_map={
    source.number: 'red',
    target.number: 'red',
})