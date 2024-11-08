# Логическое следование
# Свойство невзвешенных графов: Алгоритм BFS гарантирует, что, если имеется путь от начальной вершины к целевой, найденный путь будет кратчайшим. Это связано с тем, что алгоритм последовательного обхода всех соседей минимизирует количество пройденных рёбер.
# Проверка наличия пути: Если граф соединён и существует путь между двумя вершинами, BFS обязательно его найдёт. Если же граф несоединён, то путь не будет найден.

import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs_shortest_path(graph, start, goal):

    queue = deque([(start, [start])])
    # Множество для отслеживания посещённых узлов
    visited = set()

    pos = nx.spring_layout(graph, k=10, iterations=50000)

    # Основной цикл обхода в ширину, продолжается, пока есть узлы в очереди
    while queue:
        # Извлечение текущего узла и пути к нему из очереди
        current_node, path = queue.popleft()
        # Добавление текущего узла в множество посещённых
        visited.add(current_node)

        # Визуализация текущего состояния графа с отмеченными посещёнными узлами и текущим путём
        visualize(graph, visited, path, pos)

        # Проверка, достигли ли мы целевого узла
        if current_node == goal:
            return path

        for neighbor in graph[current_node]:
            # Проверка, не посещали ли мы соседний узел и не находится ли он в очереди
            if neighbor not in visited and neighbor not in [p[0] for p in queue]:
                # Добавление соседнего узла в очередь с обновлённым путём
                queue.append((neighbor, path + [neighbor]))

    # Если цель не найдена, возвращаем None
    return None


def visualize(graph, visited, path, pos):
    plt.clf()  # Очистка предыдущего графика

    # Создание графа с NetworkX
    G = nx.Graph()
    for node in graph:
        G.add_node(node)
        for neighbor in graph[node]:
            G.add_edge(node, neighbor)

    # Определение цветов для вершин
    node_colors = ['lightblue' if node not in visited else 'lightgreen' for node in G.nodes()]
    edge_colors = ['gray' for _ in G.edges()]

    # Определяем цвет для рёбер, которые входят в текущий путь
    for i in range(len(path) - 1):
        edge = (path[i], path[i + 1])
        if edge in G.edges() or (edge[1], edge[0]) in G.edges():
            edge_index = list(G.edges()).index(edge) if edge in G.edges() else list(G.edges()).index((edge[1], edge[0]))
            edge_colors[edge_index] = 'orange'

    # Отображаем граф
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, node_size=800)

    plt.title("BFS Visualization")
    plt.pause(2)  # Пауза для обновления графика


#
# graph1 = {
#     'A': ['B', 'C'],
#     'B': ['A', 'D', 'E'],
#     'C': ['A', 'F'],
#     'D': ['B'],
#     'E': ['B', 'F'],
#     'F': ['C', 'E']
# }
#
# # Проверяем путь от A до F
# print(bfs_shortest_path(graph1, 'A', 'F'))  # Вывод: ['A', 'C', 'F'] или ['A', 'B', 'E', 'F']
#
# graph2 = {
#     'A': ['B', 'C'],
#     'B': ['A', 'D', 'E'],
#     'C': ['A', 'F', 'G'],
#     'D': ['B', 'H'],
#     'E': ['B', 'I'],
#     'F': ['C'],
#     'G': ['C', 'J', 'K'],
#     'H': ['D'],
#     'I': ['E'],
#     'J': ['G'],
#     'K': ['G']
# }
#
# # Проверяем путь от A до K
# print(bfs_shortest_path(graph2, 'A', 'K'))  # Вывод: ['A', 'C', 'G', 'K'] или аналогичный путь

graph3 = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'E', 'F'],
    'C': ['A', 'G', 'H'],
    'D': ['A', 'I'],
    'E': ['B', 'J'],
    'F': ['B', 'K'],
    'G': ['C'],
    'H': ['C', 'L'],
    'I': ['D'],
    'J': ['E'],
    'K': ['F'],
    'L': ['H'],
}



# Инициализация графика
plt.figure(figsize=(8, 6))
# Проверяем путь от A до J
print(bfs_shortest_path(graph3, 'A', 'J'))  # Вывод: ['A', 'B', 'E', 'J'] или аналогичный путь

plt.show()