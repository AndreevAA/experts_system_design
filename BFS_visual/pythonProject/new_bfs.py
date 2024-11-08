from typing import List, Deque, Optional
from collections import deque
import enum
import typing
import dataclasses
import networkx as nx
import matplotlib.pyplot as plt


class NodeState(enum.Enum):
    """Состояние узла (вершины)"""
    BLACK = 1  # Обработанный узел
    GRAY = 2   # Узел в процессе обработки
    WHITE = 3  # Необработанный узел


@dataclasses.dataclass(unsafe_hash=True)
class Node:
    """Класс, представляющий узел (вершину) графа"""
    number: int  # Идентификатор узла
    state: NodeState = dataclasses.field(default=NodeState.WHITE, compare=False)  # Состояние узла


class EdgeState(enum.Enum):
    """Состояние ребра"""
    TRAVERSED = 1  # Ребро, по которому уже прошли
    FREE = 2       # Свободное ребро
    FORBIDDEN = 3  # Запрещённое ребро


@dataclasses.dataclass
class Edge:
    """Класс, представляющий ребро между двумя узлами"""
    start: Node  # Начальный узел
    end: Node    # Конечный узел
    label: EdgeState = EdgeState.FREE  # Состояние ребра


class Graph:
    """Класс, представляющий граф"""

    def __init__(self, *edges: Edge):
        self._edges = list(edges)  # Список рёбер графа
        self._nodes = self._create_nodes()  # Создаём узлы графа

    def _create_nodes(self):
        """Создаёт уникальные узлы из рёбер"""
        node_set = set()
        for edge in self._edges:
            node_set.add(edge.start)
            node_set.add(edge.end)
        return list(node_set)

    def edges(self) -> typing.List[Edge]:
        """Возвращает список рёбер графа"""
        return self._edges

    def nodes(self) -> typing.List[Node]:
        """Возвращает список уникальных узлов (вершин) графа"""
        return self._nodes

class AlgorithmBFS:
    """Класс для реализации алгоритма поиска в ширину (BFS)"""

    def __init__(self, graph: Graph):
        self._graph: Graph = graph  # Храним граф для поиска

    def search(self, source: Node, target: Node) -> Optional[List[Node]]:
        """Ищет путь от исходного узла к целевому узлу с помощью BFS"""
        queue: Deque[Node] = deque([source])  # Очередь для хранения узлов для обработки
        source.state = NodeState.GRAY  # Помечаем исходный узел как обрабатываемый
        parent_map = {source: None}  # Словарь для хранения предшественников узлов

        while queue:
            current_node = queue.popleft()  # Извлекаем узел из очереди

            # Если достигли целевого узла, возвращаем путь
            if current_node == target:
                return self._reconstruct_path(parent_map, target)

            # Обрабатываем все соседние узлы
            for edge in self._graph.edges():
                if edge.start == current_node and edge.end.state == NodeState.WHITE:
                    edge.end.state = NodeState.GRAY  # Помечаем как обрабатываемый
                    queue.append(edge.end)  # Добавляем в очередь
                    parent_map[edge.end] = current_node  # Сохраняем предшественника
                    edge.label = EdgeState.TRAVERSED  # Помечаем ребро как пройденное

            current_node.state = NodeState.BLACK  # Помечаем текущий узел как обработанный

        return None  # Если путь не найден, возвращаем None

    def _reconstruct_path(self, parent_map: dict, target: Node) -> List[Node]:
        """Восстанавливает путь до целевого узла"""
        path = []
        while target is not None:
            path.append(target)
            target = parent_map[target]
        return path[::-1]  # Возвращаем путь в обратном порядке

import matplotlib.pyplot as plt
import networkx as nx

def show_graph(graph: Graph, path: Optional[List[Node]]):
    """Отображает граф с отмеченным путём."""
    # Создаем граф networkx
    G = nx.Graph()

    # Добавляем узлы и их состояния
    for node in graph.nodes():
        G.add_node(node.number)

    # Добавляем рёбра
    for edge in graph.edges():
        G.add_edge(edge.start.number, edge.end.number)

    # Настройки для отображения
    pos = nx.spring_layout(G, seed=42)  # Определяем позиции узлов с фиксированным началом
    plt.figure(figsize=(10, 8))

    # Рисуем рёбра
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')

    # Если путь найден, визуализируем его отдельно
    if path:
        path_edges = [(path[i].number, path[i + 1].number) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='blue', style='solid')

    # Определяем цвета для узлов в зависимости от состояния
    node_color_map = []
    for node in graph.nodes():
        if node.state == NodeState.BLACK:
            node_color_map.append('red')  # Обработанный
        elif node.state == NodeState.GRAY:
            node_color_map.append('yellow')  # В процессе обработки
        else:
            node_color_map.append('lightgreen')  # Необработанный

    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_color=node_color_map, node_size=800)

    # Рисуем метки узлов
    nx.draw_networkx_labels(G, pos, font_size=14, font_color='black', font_family='sans-serif')

    plt.title("Граф с отмеченным путём (BFS)", fontsize=18)
    plt.axis('off')  # Отключаем оси
    plt.show()  # Показываем график

if __name__ == '__main__':
    graph = Graph(
        Edge(Node(1), Node(2)),
        Edge(Node(1), Node(3)),
        Edge(Node(2), Node(4)),
        Edge(Node(2), Node(5)),
        Edge(Node(3), Node(6)),
        Edge(Node(4), Node(7)),
        Edge(Node(5), Node(8)),
        Edge(Node(6), Node(9)),
        Edge(Node(6), Node(10)),
        Edge(Node(7), Node(10)),  # Добавлено новое ребро
        Edge(Node(8), Node(9)),  # Добавлено новое ребро
        Edge(Node(1), Node(5)),  # Добавлено новое ребро
        Edge(Node(3), Node(4))  # Добавлено новое ребро
    )

    bfs_alg = AlgorithmBFS(graph)
    source_node = graph.nodes()[0]  # Как пример, начнём с первого узла
    target_node = graph.nodes()[2]  # Ищем путь к шестому узлу
    path = bfs_alg.search(source_node, target_node)

    print("Путь:", ' -> '.join(str(node.number) for node in path) if path else "Путь не найден")
    show_graph(graph, path)