import networkx as nx
import matplotlib.pyplot as plt
import heapq


def dijkstra(graph, start):
    # Словарь для хранения кратчайших путей
    shortest_paths = {node: float('inf') for node in graph}
    shortest_paths[start] = 0
    # Очередь приоритетов для хранения вершин
    priority_queue = [(0, start)]
    # Словарь для хранения предыдущих вершин на пути
    previous_nodes = {start: None}

    while priority_queue:
        # Извлекаем минимальный элемент
        current_distance, current_node = heapq.heappop(priority_queue)

        # Проверяем соседей текущей вершины
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # Если найден новый кратчайший путь
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return shortest_paths, previous_nodes


def get_shortest_path(previous_nodes, start, end):
    # Восстановление кратчайшего пути
    path = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()

    return path


def visualize_graph(graph, path=None):
    G = nx.Graph()

    # Добавляем рёбра и веса в граф
    for node, edges in graph.items():
        for neighbor, weight in edges.items():
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')

    # Рисуем граф
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=16)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    if path:
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)

    plt.title("Граф с весами и кратчайшим путем")
    plt.show()


# Пример графа с весами
graph1 = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Поиск кратчайшего пути
start_node = 'A'
end_node = 'D'
shortest_paths, previous_nodes = dijkstra(graph1, start_node)
shortest_path = get_shortest_path(previous_nodes, start_node, end_node)

print(f"Кратчайший путь из {start_node} в {end_node}: {shortest_path}")

# Визуализация графа и кратчайшего пути
visualize_graph(graph1, shortest_path)