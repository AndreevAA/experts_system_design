from typing import List
from Edge import Edge
from Node import Node
from Queue import Queue
from Stack import Stack

class Graph:

    def __init__(self, edgeLst: List[Edge]):
        self.edgeLst = edgeLst  # Список рёбер графа
        self.closed = []  # Посещённые узлы
        self.goal = None  # Целевой узел
        self.isSolutionNotFound = 1  # Флаг, указывающий на отсутствие решения
        self.childCounter = 1  # Счётчик для поиска потомков

    def bfs(self, start: int, goal: int):
        self.opened = Queue()  # Очередь для хранения узлов
        self.resPWD = {}  # Словарь для хранения пути к узлам

        self.opened.put(Node(start))
        self.goal = goal

        while self.childCounter and self.isSolutionNotFound:
            print("Очередь: ", end="")
            self.opened.print()

            self.__bfs_sample_search()
            if self.isSolutionNotFound == 0:
                break

            currentNode = self.opened.get()  # Извлечение текущего узла из очереди
            self.closed.append(currentNode.number)  # Посещение узла

            if self.opened.length() != 0:  # Если есть ещё узлы
                self.childCounter = 1

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

    def dfs(self, start: int, goal: int):
        self.opened = Stack()  # Стек для хранения узлов
        self.opened.push(Node(start))  # Начальный узел в стек
        self.goal = goal  # Установка целевого узла

        while self.childCounter and self.isSolutionNotFound:
            print("Стек: ", end="")
            self.opened.print()

            self.__dfs__sample_search()
            if self.isSolutionNotFound == 0:
                break
            if self.childCounter == 0 and self.opened.length() > 1:  # Нет потомков
                currentNode = self.opened.pop()
                self.closed.append(currentNode.number)
                self.childCounter = 1

        if self.isSolutionNotFound == 1:
            return None
        return self.opened

    def __dfs__sample_search(self):
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

            if edge.endNode.number == self.goal:
                self.isSolutionNotFound = 0
                return

    def __get_res_pwd(self, start: int):
        current = self.goal  # Начинаем с целевого узла
        result = [current]
        while current != start:  # Пока не достигнем стартового узла
            current = self.resPWD[current]  # Переход к родительскому узлу
            result.append(current)  # Добавляем узел в результат
        return result