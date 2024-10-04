import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def bfs(graph, start):
    # Создаем очередь для хранения вершин, которые нужно исследовать
    queue = deque([start])
    # Множество для хранения посещенных вершин
    visited = set([start])
    # Список для хранения порядка посещения вершин
    order_of_visit = []

    # Пока в очереди есть вершины
    while queue:
        # Извлекаем вершину из очереди
        vertex = queue.popleft()
        # Добавляем ее в список посещенных
        order_of_visit.append(vertex)

        # Получаем всех соседей текущей вершины
        for neighbor in graph[vertex]:
            # Если сосед еще не был посещен
            if neighbor not in visited:
                # Добавляем его в очередь и помечаем как посещенный
                queue.append(neighbor)
                visited.add(neighbor)

    return order_of_visit


def visualize_graph(graph, start):
    # Визуализация графа
    G = nx.Graph()

    # Добавляем ребра в граф
    for vertex in graph:
        for neighbor in graph[vertex]:
            G.add_edge(vertex, neighbor)

    # Задаем позицию узлов для визуализации
    pos = nx.spring_layout(G)

    # Рисуем граф
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=800, font_size=16, font_weight='bold')
    plt.title("Граф")
    plt.show()

    # Выполняем BFS и выводим порядок посещения
    order_of_visit = bfs(graph, start)
    print("Порядок посещения вершин (BFS):", order_of_visit)


# Пример графа в виде словаря
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

# Выбираем начальную вершину для BFS
start_vertex = 'A'

# Визуализируем граф и выполняем BFS
visualize_graph(graph, start_vertex)