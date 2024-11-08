from Rule import Rule
from Node import Node
from Label import Label
from Stack import Stack
import networkx as nx
import matplotlib.pyplot as plt


# Поиск в ширину от данных к целе
class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr  # Массив правил (база знаний)
        self.open_node_st = Stack()  # Стек для открытых узлов
        self.open_rule_lst = []  # Список открытых правил
        self.close_node_lst = []  # Список закрытых узлов
        self.close_rule_lst = []  # Список закрытых правил
        self.prohibited_node_lst = []  # Список запрещенных узлов
        self.prohibited_rule_lst = []  # Список запрещенных правил

        self.goal_node = None  # Целевой узел
        self.solution_flg = True  # Флаг для отслеживания, найденно ли решение
        self.no_solution_flg = True  # Флаг для отслеживания, нет ли решения

        self.node_positions = {}  # Словарь для хранения фиксированных позиций узлов

    # Функция для визуализации графа
    def draw_graph(self, rule_arr, closed_nodes, prohibited_nodes):
        G = nx.Graph()

        for rule in self.rule_arr:
            G.add_node(rule.out_node.number, label=str(rule.out_node.flag))
            for dependency in rule.node_arr:
                G.add_node(dependency.number, label=str(dependency.flag))
                G.add_edge(dependency.number, rule.out_node.number)

        # Определяем цвета для узлов
        color_map_nodes = []
        for node in G.nodes():
            if node in [n.number for n in self.open_node_st.elements]:
                color_map_nodes.append('lightgreen')  # Открытые
            elif node in [n.number for n in self.close_node_lst]:
                color_map_nodes.append('lightblue')  # Закрытые
            elif node in [n.number for n in self.prohibited_node_lst]:
                color_map_nodes.append('red')  # Запрещенные
            else:
                color_map_nodes.append('grey')  # Не помеченные узлы

        # Если позиции еще не заданы, вычисляем их
        if not self.node_positions:
            self.node_positions = nx.spring_layout(G)

        # Отрисовка узлов и рёбер с фиксированными позициями
        nx.draw(G, self.node_positions, node_color=color_map_nodes, with_labels=True,
                font_weight='bold')

        # Визуализация меток
        labels = {n: str(n) for n in G.nodes()}
        nx.draw_networkx_labels(G, self.node_positions, labels=labels)

        plt.title("Визуализация графа поиска")
        plt.show()

    def run(self, goal_node: Node, in_node_arr: [Node]):
        # Устанавливаем целевой узел и помещаем его в стек открытых узлов
        self.goal_node = goal_node
        self.open_node_st.push(goal_node)
        self.close_node_lst = in_node_arr  # Заполняем закрытые узлы

        while self.solution_flg and self.no_solution_flg:
            # Выполняем поиск по родителям и получаем количество обработанных правил
            rule_cnt = self.parent_search()

            if not self.solution_flg:
                return

            # Если не осталось правил для обработки, завершаем поиск
            if rule_cnt == 0:
                self.no_solution_flg = False
                print("Решение не найдено")

    def parent_search(self):
        cnt_rules = 0  # Счетчик обработанных правил

        # Проходим по всем правилам в базе знаний
        for rule in self.rule_arr:
            print(f'[Rule {rule.number}] Текущая правило')
            if not self.is_rule_processable(rule):
                continue  # Пропускаем правило, если оно уже обработано

            if self.is_close_nodes_cover(rule.node_arr):
                # Если все входящие узлы правила закрыты, обрабатываем правило
                cnt_rules += self.process_valid_rule(rule)
            else:
                self.handle_uncovered_rule(rule)

            self.print_state(rule)

        print(f'{cnt_rules} правил было доказано')
        return cnt_rules

    def is_rule_processable(self, rule: Rule):
        # Проверка, было ли правило уже обработано
        if rule.label != Label.OPEN:
            print(f'[Rule {rule.number}] было уже обработано')
            print('-' * 128 + '\n')
            return False
        return True

    def process_valid_rule(self, rule: Rule):
        # Обработка валидного правила
        print(f'[Rule {rule.number}] Все входящие узлы включены в закрытые узлы')

        rule.label = Label.CLOSE  # Меняем статус правила на закрытое
        self.close_rule_lst.append(rule)  # Добавляем правило в закрытые
        self.close_node_lst.append(rule.out_node)  # Добавляем выходной узел в закрытые
        self.set_nodes_closed(rule.node_arr)  # Закрываем входящие узлы

        if rule.out_node == self.goal_node:
            # Если выходной узел равен целевому, решение найдено
            self.solution_flg = False
            print(f'[Rule {rule.number}] выходной узел равен целевому')

        return 1

    def handle_uncovered_rule(self, rule: Rule):
        print(f'[Rule {rule.number}] не все входные узлы закрыты')

    def is_close_nodes_cover(self, in_node_arr: [Node]):
        # Проверка, покрывают ли закрытые узлы входящие узлы правила
        return all(node in self.close_node_lst for node in in_node_arr)

    def set_nodes_closed(self, node_arr):
        # Закрытие узлов путем смены их статуса
        for node in node_arr:
            node.flag = Label.CLOSE

    def print_state(self, rule: Rule):
        print(f'[Rule {rule.number}] список закрытых правил: ', end='')
        self.print_rules(self.close_rule_lst)
        print(f'[Rule {rule.number}] список закрытых узлов: ', end='')
        self.print_nodes(self.close_node_lst)
        print('-' * 128 + '\n')

        self.draw_graph(self.rule_arr, self.close_node_lst, self.prohibited_node_lst)

    def print_rules(self, rule_arr: [Rule]):
        print(' '.join(str(rule.number) for rule in rule_arr))

    def print_nodes(self, node_arr: [Node]):
        print(' '.join(str(node) for node in node_arr))