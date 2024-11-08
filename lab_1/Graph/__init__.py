import matplotlib.pyplot as plt
import networkx as nx
from typing import List
from Edge import Edge
from Node import Node
from Queue import Queue
from Stack import Stack

class Graph:
    def __init__(self, edgeLst: List[Edge], draw_flag: int = 0):
        self.edgeLst = edgeLst  # Список рёбер графа
        self.closed = []  # Посещённые узлы
        self.goal = None  # Целевой узел
        self.isSolutionNotFound = 1  # Флаг, указывающий на отсутствие решения
        self.childCounter = 1  # Счётчик для поиска потомков
        self.draw_flag = draw_flag  # Флаг для отрисовки графа

        self.G = nx.Graph()

        # Добавляем рёбра в граф и помечаем их
        for edge in self.edgeLst:
            self.G.add_edge(edge.startNode.number, edge.endNode.number, label=edge.label)

        # Вычисляем позиции узлов динамически
        self.pos = nx.spring_layout(self.G)

    def bfs(self, start: int, goal: int):
        self.opened = Queue()  # Очередь для хранения узлов
        self.resPWD = {}  # Словарь для хранения пути к узлам

        self.opened.put(Node(start))
        self.goal = goal

        self.plot_graph(is_bfs=True)

        while self.childCounter and self.isSolutionNotFound:
            print("\nОчередь (открытые узлы): ", end="")
            self.opened.print()
            print("Закрытые узлы:", self.closed)
            # print("Открытые узлы:", [node.number for node in self.opened.elements])  # Вывод открытых узлов

            self.__bfs_sample_search()
            if self.isSolutionNotFound == 0:
                break

            currentNode = self.opened.get()  # Извлечение текущего узла из очереди
            self.closed.append(currentNode.number)  # Посещение узла

            print("Текущий узел:", currentNode.number)

            if self.opened.length() != 0:  # Если есть ещё узлы
                self.childCounter = 1

            self.plot_graph(is_bfs=True)

        if self.isSolutionNotFound == 1:
            return None

        return self.__get_res_pwd(start)

    def __bfs_sample_search(self):
        self.childCounter = 0

        for edge in self.edgeLst:
            currentNode = self.opened.top()

            if edge.startNode.number != currentNode.number or edge.used:
                continue  # Пропускаем, если ребро не ведёт от текущего узла или уже использовано
            if self.opened.isExist(edge.endNode.number) or edge.endNode.number in self.closed:
                continue  # Пропускаем посещённые узлы

            edge.used = True
            self.opened.put(edge.endNode)
            self.resPWD[edge.endNode.number] = edge.startNode.number  # Запоминаем путь
            self.childCounter = 1

            if edge.endNode.number == self.goal:
                self.isSolutionNotFound = 0
                return

            self.plot_graph(is_bfs=True)

    def dfs(self, start: int, goal: int):
        self.opened = Stack()  # Стек для хранения узлов
        self.opened.push(Node(start))  # Начальный узел в стек
        self.goal = goal  # Установка целевого узла

        while self.childCounter and self.isSolutionNotFound:
            print("\nСтек (открытые узлы): ", end="")
            self.opened.print()
            print("Закрытые узлы:", self.closed)
            # print("Открытые узлы:", [node.number for node in self.opened.elements])  # Вывод открытых узлов

            self.__dfs_sample_search()
            if self.isSolutionNotFound == 0:
                break
            if self.childCounter == 0 and self.opened.length() > 1:  # Нет потомков
                currentNode = self.opened.pop()
                self.closed.append(currentNode.number)
                print("\nТекущий узел:", currentNode.number)
                print("Стек (открытые узлы): ", end="")
                self.opened.print()
                print("Закрытые узлы:", self.closed)
                self.childCounter = 1

            self.plot_graph(is_bfs=False)

        if self.isSolutionNotFound == 1:
            return None

        return self.opened

    def __dfs_sample_search(self):
        self.childCounter = 0

        for edge in self.edgeLst:
            currentNode = self.opened.peek()

            if edge.startNode.number != currentNode.number or edge.used:
                continue  # Пропускаем, если ребро не ведёт от текущего узла или уже использовано
            if self.opened.isExist(edge.endNode.number) or edge.endNode.number in self.closed:
                continue  # Пропускаем посещённые узлы

            edge.used = True
            self.opened.push(edge.endNode)
            self.childCounter = 1

            print()
            print("Текущий узел:", currentNode.number)
            print("\nСтек (открытые узлы): ", end="")
            self.opened.print()
            print("Закрытые узлы:", self.closed)

            if edge.endNode.number == self.goal:
                self.isSolutionNotFound = 0
                return

            self.plot_graph(is_bfs=False)

    def __get_res_pwd(self, start: int):
        current = self.goal  # Начинаем с целевого узла
        result = [current]
        while current != start:  # Пока не достигнем стартового узла
            current = self.resPWD[current]  # Переход к родительскому узлу
            result.append(current)  # Добавляем узел в результат
        return result

    def plot_graph(self, is_bfs):
        if self.draw_flag == 0:
            return  # Если флаг для отрисовки не установлен, выходим из метода

        # Устанавливаем цвет узлов
        color_map = []
        for node in self.G.nodes:
            if node in self.closed:
                color_map.append('red')  # Посещённые узлы
            elif node in [n.number for n in self.opened.elements]:  # Узлы в очереди/стеке
                color_map.append('green')
            else:
                color_map.append('blue')  # Не посещённые узлы

        # Рисуем граф
        nx.draw(self.G, self.pos, node_color=color_map, with_labels=True, node_size=700, font_size=10)
        edge_labels = nx.get_edge_attributes(self.G, 'label')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=edge_labels)

        plt.title('BFS' if is_bfs else 'DFS')
        plt.show()
