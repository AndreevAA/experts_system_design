import matplotlib.pyplot as plt
import networkx as nx
from Graph import Graph
from Edge import Edge
from Node import Node


def show(arr: list):
    """
    Отображает путь в графе.

    :param arr: Список узлов, представляющий путь.
    """
    if arr is None:
        print("Не найдено")
        return
    for i in range(len(arr) - 1, -1, -1):
        if i != 0:
            print(f'{arr[i]} -> ', end='')
        else:
            print(f'{arr[i]}')


class Example:
    def edgeLst_1(self):
        """
        Возвращает первый набор рёбер графа.

        :return: Список рёбер.
        """
        edgeLst = [
            Edge(Node(1), Node(2), 101),
            Edge(Node(1), Node(3), 102),
            Edge(Node(1), Node(4), 103),
            Edge(Node(2), Node(5), 104),
            Edge(Node(3), Node(4), 105),
            Edge(Node(4), Node(6), 106)
        ]
        return edgeLst

    def edgeLst_2(self):
        """
        Возвращает второй набор рёбер графа.

        :return: Список рёбер.
        """
        edgeLst = [
            Edge(Node(0), Node(1), 101),
            Edge(Node(0), Node(2), 102),
            Edge(Node(0), Node(3), 103),
            Edge(Node(1), Node(4), 104),
            Edge(Node(2), Node(4), 105),
            Edge(Node(2), Node(5), 106),
            Edge(Node(3), Node(5), 107),
            Edge(Node(3), Node(6), 108),
            Edge(Node(4), Node(8), 109),
            Edge(Node(5), Node(4), 110),
            Edge(Node(5), Node(7), 112),
            Edge(Node(5), Node(9), 111),
            Edge(Node(6), Node(7), 113),
            Edge(Node(7), Node(9), 115),
            Edge(Node(9), Node(8), 114)
        ]
        return edgeLst


def visualize_graph(edges, filename='Graph.png'):
    """
    Визуализирует граф и сохраняет его в формате PNG.

    :param edges: Список рёбер для визуализации.
    :param filename: Имя файла для сохранения изображения.
    """
    G = nx.Graph()

    # Добавление рёбер в граф
    for tmp_edge in edges:
        G.add_edge(tmp_edge.startNode.number, tmp_edge.endNode.number, weight=tmp_edge.label)

    pos = nx.spring_layout(G)  # Определение позиции узлов
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10)
    labels = nx.get_edge_attributes(G, 'weight')  # Получение весов рёбер
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.title("Визуализация графа")
    plt.savefig(filename)  # Сохранение в файл
    plt.close()  # Закрытие графика


if __name__ == "__main__":
    print("Поиск в графе")

    edgeLst1 = Example().edgeLst_2()

    # Визуализируем граф
    visualize_graph(edgeLst1)

    print("Обход в глубину")
    print("Идем от 0 к 7")
    res = Graph(edgeLst1).dfs(0, 7)
    if res is None:
        print("Не найдено")
    else:
        res.show()

    print("-------------------------")

    print("Обход в ширину")
    print("Идем от 0 к 7")
    res = Graph(edgeLst1).bfs(0, 7)

    show(res)