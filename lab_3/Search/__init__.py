from Rule import Rule
from Node import Node
from Edge import Edge
from Stack import Stack
from Label import Label
import matplotlib.pyplot as plt
import networkx as nx


# Обратный поиск в глубину от цели

# Класс для поиска маршрута в графе
# 1. Обратный поиск (основной метод)
# 2. Поиск детей для текущей цели
# 3. Возврат назад -- формирование списка запрещенных узлов и правил
# 4. Маркировка
# 5. Создание дерева поиска по списку закрытых правил
class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr  # база знаний
        self.open_node_st = Stack()  # стек открытых узлов
        self.open_rule_lst = []  # список открытых правил
        self.close_node_lst = []  # список закрытых узлов
        self.close_rule_lst = []  # список закрытых правил
        self.prohibited_node_lst = []  # список запрещенных узлов
        self.prohibited_rule_lst = []  # список запрещенных правил

        self.goal_node = None  # целевой узел
        self.solution_flg = 1  # флаг, указывающий на наличие решения
        self.no_solution_flg = 1  # флаг, указывающий на отсутствие решения
        self.no_label = 1  # флаг, указывающий на отсутствие метки

        self.node_positions = {}  # Словарь для хранения фиксированных позиций узлов
        self.visualize = False

    def visualize_graph(self):
        if self.visualize:
            G = nx.Graph()

            # Добавляем узлы в граф с их статусами
            for node in self.close_node_lst + self.prohibited_node_lst + [self.goal_node]:
                G.add_node(node.number, label=str(node.flag))

            # Добавляем ребра для каждой из правил
            for rule in self.rule_arr:
                for node in rule.node_arr:
                    G.add_edge(node.number, rule.out_node.number)

            # Определяем цвета для узлов
            color_map_nodes = []
            for node in G.nodes():
                if node in [n.number for n in self.open_node_st.elements]:
                    color_map_nodes.append('lightgreen')  # ОТКРЫТЫЕ
                elif node in [n.number for n in self.close_node_lst]:
                    color_map_nodes.append('lightblue')  # ЗАКРЫТЫЕ
                elif node in [n.number for n in self.prohibited_node_lst]:
                    color_map_nodes.append('red')  # ЗАПРЕЩЕННЫЕ
                else:
                    color_map_nodes.append('grey')  # не помеченные узлы

            # # Определяем цвета для рёбер
            # color_map_edges = []
            # for rule in self.rule_arr:
            #     if rule.label == Label.FORBIDDEN:
            #         color_map_edges.append('red')  # Закрытые/запрещенные правила
            #     else:
            #         color_map_edges.append('black')  # Все остальные правила

            # Если позиции еще не заданы, вычисляем их
            if not self.node_positions:
                self.node_positions = nx.spring_layout(G, k=0.5, iterations=10000)

            # Отрисовка узлов и рёбер с фиксированными позициями
            nx.draw(G, self.node_positions, node_color=color_map_nodes, with_labels=True,
                    font_weight='bold')

            # Визуализация меток
            labels = {n: str(n) for n in G.nodes()}
            nx.draw_networkx_labels(G, self.node_positions, labels=labels)

            plt.title("Визуализация графа поиска")
            plt.show()

    def run(self, goal_node: Node, in_node_arr: [Node]):
        self.goal_node = goal_node
        self.open_node_st.push(goal_node)  # добавляем целевой узел в стек открытых узлов
        self.close_node_lst = in_node_arr  # инициализируем закрытые узлы

        self.visualize_graph()

        while self.solution_flg and self.no_solution_flg:  # продолжаем до нахождения решения
            rule_cnt = self.child_search()  # ищем дочерние узлы

            if self.solution_flg == 0:
                print("Решение найдено")
                return

            if rule_cnt == 0 and self.open_node_st.length() < 2:
                self.no_solution_flg = 0
                print("Решение не найдено")
            elif rule_cnt == 0:
                print("Запускается процесс обратного поиска")
                self.backtracking()  # запускаем процесс обратного поиска

    def child_search(self):
        cnt_rules = 0  # счетчик правил

        for rule in self.rule_arr:  # перебираем все правила

            current_node = self.open_node_st.peek()  # получаем текущий узел
            if rule.label != Label.OPEN:  # если правило уже закрыто
                self.process_closed_rule(rule)  # обрабатываем закрытое правило
                continue

            # Обрабатываем правило, если оно применяется к текущему узлу
            if rule.out_node == current_node:
                cnt_rules += self.process_applicable_rule(rule)  # обрабатываем применимое правило
                break

            # Проверяем на наличие запрещенных узлов
            if self.is_prohibited_node_exist(rule.node_arr):
                self.process_prohibited_rule(rule)  # обрабатываем запрещенное правило
                continue

            self.print_info(rule)  # выводим информацию о правиле

        return cnt_rules

    def process_closed_rule(self, rule: Rule):
        print(f'[Правило {rule.number}] уже обработано')
        print('-' * 128 + '\n')

    def process_applicable_rule(self, rule: Rule):
        print(f'[Правило {rule.number}] имеет выходной узел, равный целевому')
        rule.label = Label.VIEWED  # помечаем правило как просмотренное
        self.open_rule_lst.append(rule)

        if not self.add_new_goal(rule.node_arr):  # если новое правило не добавлено
            print("Запускается процесс маркировки")  # запускаем процесс маркировки
            self.label()

        self.print_info(rule)  # выводим информацию о правиле
        return 1

    def process_prohibited_rule(self, rule: Rule):
        self.prohibited_rule_lst.append(rule)  # добавляем правило в список запрещенных
        rule.label = Label.FORBIDDEN  # помечаем правило как запрещенное
        self.print_info(rule)  # выводим информацию о правиле

    def label(self):
        while True:
            rule = self.open_rule_lst.pop()  # берем последнее открытое правило
            self.close_rule_lst.append(rule)  # добавляем его в закрытые правила

            node = self.open_node_st.pop()  # берем текущий узел
            self.close_node_lst.append(node)  # добавляем его в закрытые узлы

            print(f'[Маркировка] Правило {rule.number} было добавлено в закрытые правила')
            print(f'[Маркировка] Узел {node.number} был добавлен в закрытые узлы')

            if node == self.goal_node:  # если узел — целевой
                self.solution_flg = 0  # устанавливаем флаг решения в 0
                return

            current_node = self.open_node_st.peek()  # получаем следующий узел
            current_rule = self.open_rule_lst[-1]  # берем последнее открытое правило
            if current_rule.out_node != current_node:
                return

    def backtracking(self):
        current_goal = self.open_node_st.pop()  # берем текущий целевой узел
        rule = self.open_rule_lst.pop()  # берем последнее открытое правило

        current_goal.flag = Label.FORBIDDEN  # помечаем узел как запрещенный
        self.prohibited_node_lst.append(current_goal)  # добавляем его в список запрещенных узлов

        rule.label = Label.FORBIDDEN  # помечаем правило как запрещенное
        self.prohibited_rule_lst.append(rule)  # добавляем его в список запрещенных правил

        print(f'[Обратный поиск] Правило {rule.number} было добавлено в запрещенные правила')
        print(f'[Обратный поиск] Узел {current_goal.number} был добавлен в запрещенные узлы')

        for node in rule.node_arr:  # удаляем все узлы, связанные с правилом
            print(f'[Обратный поиск] Узел {node.number} должен быть удален из открытых узлов')
            self.open_node_st.remove_element(node)
        print()

    def add_new_goal(self, node_arr: [Node]):
        new_goal_flg = False  # флаг для отслеживания добавления нового узла

        for node in node_arr[::-1]:  # перебираем узлы в обратном порядке
            if node not in self.close_node_lst:  # если узел не закрыт
                self.open_node_st.push(node)  # добавляем его в открытые узлы
                new_goal_flg = True  # устанавливаем флаг добавления нового узла в True
        return new_goal_flg

    def is_prohibited_node_exist(self, node_arr: [Node]):
        # Проверяем, есть ли запрещенные узлы среди переданных
        return any(node in self.prohibited_node_lst for node in node_arr)

    def print_nodes(self, node_arr: [Node]):
        for node in node_arr:
            print(node, end=' ')
        print()

    def print_rules(self, rule_arr: [Rule]):
        for rule in rule_arr:
            print(rule.number, end=' ')
        print()

    def print_info(self, rule: Rule):
        # Печатаем информацию о правиле и списки узлов и правил
        print(f'[Правило {rule.number}] список открытых узлов: ', end='    ')
        self.open_node_st.show()
        print(f'[Правило {rule.number}] список закрытых узлов: ', end='    ')
        self.print_nodes(self.close_node_lst)
        print(f'[Правило {rule.number}] список запрещенных узлов: ', end='')
        self.print_nodes(self.prohibited_node_lst)
        print(f'[Правило {rule.number}] список открытых правил: ', end='    ')
        self.print_rules(self.open_rule_lst)
        print(f'[Правило {rule.number}] список закрытых правил: ', end='    ')
        self.print_rules(self.close_rule_lst)
        print(f'[Правило {rule.number}] список запрещенных правил: ', end='')
        self.print_rules(self.prohibited_rule_lst)

        print('-' * 128 + '\n')

        self.visualize_graph()