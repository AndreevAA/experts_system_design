from typing import List

from Edge import Edge
from Node import Node
from Queue import Queue
from Stack import Stack


class Graph:

    def __init__(self, edgeLst: List[Edge]):
        self.edgeLst = edgeLst
        self.closed = []
        self.goal = None
        self.isSolutionNotFound = 1
        self.childCounter = 1

    def bfs(self, start: int, goal: int):
        self.opened = Queue()
        self.resPWD = {}

        self.opened.put(Node(start))
        self.goal = goal

        while self.childCounter and self.isSolutionNotFound:
            print("Очередь: ", end="")
            self.opened.print()

            self.__bfs_sample_search()  # метод потомков
            if self.isSolutionNotFound == 0:  # решение найдено
                break

            currentNode = self.opened.get()
            self.closed.append(currentNode.number)

            if self.opened.length() != 0:
                self.childCounter = 1

        if self.isSolutionNotFound == 1:
            return None
        return self.__get_res_pwd(start)

    # Поиск по образцу (метод, находящий потомка для текущей подцели)
    def __bfs_sample_search(self):
        self.childCounter = 0

        for edge in self.edgeLst:
            currentNode = self.opened.top()

            if edge.startNode.number != currentNode.number:
                continue
            if edge.used:
                continue
            if self.opened.isExist(edge.endNode.number) or edge.endNode.number in self.closed:
                continue

            edge.used = True
            self.opened.put(edge.endNode)
            self.resPWD[edge.endNode.number] = edge.startNode.number
            self.childCounter = 1

            if edge.endNode.number == self.goal:
                self.isSolutionNotFound = 0
                return


    def dfs(self, start: int, goal: int):
        self.opened = Stack()
        self.opened.push(Node(start))
        self.goal = goal

        while self.childCounter and self.isSolutionNotFound:
            print("Стек: ", end="")
            self.opened.print()

            self.__dfs__sample_search()
            if self.isSolutionNotFound == 0:
                break
            if self.childCounter == 0 and self.opened.length() > 1:
                currentNode = self.opened.pop()
                self.closed.append(currentNode.number)
                self.childCounter = 1
        if self.isSolutionNotFound == 1:
            return None
        return self.opened

    # Поиск по образцу (метод, находящий потомка для текущей подцели)
    def __dfs__sample_search(self):
        self.childCounter = 0

        for edge in self.edgeLst:
            currentNode = self.opened.peek()

            if edge.startNode.number != currentNode.number:
                continue
            if edge.used:
                continue
            if self.opened.isExist(edge.endNode.number) or edge.endNode.number in self.closed:
                continue

            edge.used = True
            self.opened.push(edge.endNode)
            self.childCounter = 1

            if edge.endNode.number == self.goal:
                self.isSolutionNotFound = 0
            return

    def __get_res_pwd(self, start: int):
        current = self.goal
        result = [current]
        while current != start:
            current = self.resPWD[current]
            result.append(current)
        return result

