from Rule import Rule
from Node import Node
from Edge import Edge
from Stack import Stack
from Label import Label
import matplotlib.pyplot as plt
import networkx as nx


# Reverse search from goal to deep
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

        self.goal_node = None  # конечный узел
        self.solution_flg = 1  # флаг решения (0 - решение найдено)
        self.no_solution_flg = 1  # флаг отсутствия решения
        self.no_label = 1  # флаг отсутствия метки

    def run(self, goal_node: Node, in_node_arr: [Node]):

        self.goal_node = goal_node  # установка целевого узла
        self.open_node_st.push(goal_node)  # добавление целевого узла в стек
        self.close_node_lst = in_node_arr  # инициализация списка закрытых узлов

        # Основной цикл поиска
        while self.solution_flg and self.no_solution_flg:
            rule_cnt = self.child_search()

            # если решение найдено
            if self.solution_flg == 0:
                print("Solution was found")
                return

            # Если правила не найдены и в стеке меньше двух узлов
            if rule_cnt == 0 and self.open_node_st.length() < 2:
                self.no_solution_flg = 0  # отметка об отсутствии решения
                print("Solution was not found")
            elif rule_cnt == 0:
                print("Backtracking process is going to be launched")
                self.backtracking()  # запуск процесса возврата назад

    def child_search(self):
        """
        Ищет подходящие правила среди открытых узлов и обрабатывает их.
        :return: Количество обработанных правил.
        """
        processed_rules_count = 0  # Счетчик обработанных правил

        for current_rule in self.rule_arr:
            self.__process_rule(current_rule)

            if current_rule.label == Label.OPEN:
                self.__evaluate_rule(current_rule)
                processed_rules_count += self.__check_goal(current_rule)

        return processed_rules_count  # Возврат количества обработанных правил

    def __process_rule(self, rule: Rule):
        active_node = self.open_node_st.peek()  # Получение текущего узла
        print(f'[Rule {rule.number}] Current rule')
        print(f'[Node {active_node.number}] Current node')

        if rule.label != Label.OPEN:
            print(f'[Rule {rule.number}] has been processed before')
            print('-' * 128 + '\n')
            return

    def __evaluate_rule(self, rule: Rule):
        """
        Оценивает текущее правило и выполняет действия по его результатам.

        :param rule: Правило для оценки.
        """
        active_node = self.open_node_st.peek()

        if rule.out_node == active_node:
            print(f'[Rule {rule.number}] matches target node')

            rule.label = Label.VIEWED  # Маркировка как просмотренное
            self.open_rule_lst.append(rule)  # Добавление в открытые

            if not self.add_new_goal(rule.node_arr):
                print("Initiating labeling process")
                self.__label()  # Запуск процесса маркировки

        elif self.is_prohibited_node_exist(rule.node_arr):
            self.prohibited_rule_lst.append(rule)  # Добавление в запрещенные
            rule.label = Label.FORBIDDEN  # Маркировка как запрещенное
            print(f'[Rule {rule.number}] marked as forbidden')
        else:
            print(f'[Rule {rule.number}] did not match any conditions')

    def __check_goal(self, rule: Rule) -> int:
        goal_found = rule.out_node == self.open_node_st.peek()
        if goal_found:
            self.print_info(rule)
            return 1

        self.print_info(rule)
        return 0

    def __update_close_rule_lst(self):
        rule = self.open_rule_lst.pop()  # извлечение закрытого правила
        self.close_rule_lst.append(rule)  # добавление в закрытые правила

        print(f'[Labelling] Rule {rule.number} was added to close rules')

        return rule

    def __update_close_node_lst(self):
        node = self.open_node_st.pop()  # извлечение узла из стека
        self.close_node_lst.append(node)  # добавление в закрытые узлы

        print(f'[Labelling] Node {node.number} was added to close nodes')

        return node

    def __label(self):
        # Процесс маркировки
        while True:
            self.__update_close_rule_lst()
            node = self.__update_close_node_lst()

            if self.goal_node != node:
                # Проверка, является ли текущий узел НЕ целевым
                current_node = self.open_node_st.peek()  # следующий узел
                current_rule = self.open_rule_lst[-1]  # текущее правило
                if current_rule.out_node != current_node:
                    return  # выходим, если выходной узел не равен текущему
            else:
                # Проверка, является ли текущий узел целевым
                self.solution_flg = 0  # решение найдено
                return

    def __add_tmp_rule_to_prohibited_rule_lst(self):
        rule = self.open_rule_lst.pop()  # извлечение текущего правила
        rule.label = Label.FORBIDDEN  # маркировка правила как запрещенного
        self.prohibited_rule_lst.append(rule)  # добавление в запрещенные правила

        print(f'[Backtrack] Rule {rule.number} was added to prohibited rules')

        return rule

    def __add_tmp_node_to_prohibited_node_lst(self):
        current_goal = self.open_node_st.pop()  # извлечение текущего узла

        current_goal.flag = Label.FORBIDDEN  # маркировка узла как запрещенного
        self.prohibited_node_lst.append(current_goal)  # добавление в запрещенные узлы

        print(f'[Backtrack] Node {current_goal.number} was added to prohibited nodes')

    def __delete_open_node_st_nodes(self, node_arr=None):

        if node_arr is None:
            node_arr = []

        for node in node_arr:
            print(f'[Backtrack] Node {node.number} should be removed from opened nodes')
            self.open_node_st.remove_element(node)  # удаление узлов из открытых
        print()

    def backtracking(self):
        # Маркировка текущих узла и правила и добавление в список запрещенных узлов
        self.__add_tmp_node_to_prohibited_node_lst()
        rule = self.__add_tmp_rule_to_prohibited_rule_lst()

        # Удаление узлов их открытых
        self.__delete_open_node_st_nodes(node_arr=rule.node_arr)

    def add_new_goal(self, node_arr: [Node]):
        new_goal_flg = False  # флаг для отслеживания новых целей

        # Добавление новых целей в стек
        for node in node_arr[::-1]:
            if node not in self.close_node_lst:
                self.open_node_st.push(node)  # добавляем узел в стек открытых
                new_goal_flg = True  # отмечаем, что новая цель была добавлена
        return new_goal_flg  # возвращаем флаг новых целей

    def is_prohibited_node_exist(self, node_arr: [Node]):
        # Проверка на наличие запрещенных узлов
        for node in node_arr:
            if node in self.prohibited_node_lst:
                return True  # запрещенный узел найден
        return False  # запрещенных узлов нет

    def print_nodes(self, node_arr: [Node]):
        # Вывод узлов в консоль
        for node in node_arr:
            print(node, end=' ')
        print()

    def print_rules(self, rule_arr: [Rule]):
        # Вывод правил в консоль
        for rule in rule_arr:
            print(rule.number, end=' ')
        print()

    def print_info(self, rule: Rule):
        # Вывод информации о правиле
        print(f'[Rule {rule.number}] list of opened nodes: ', end='    ')
        self.open_node_st.show()  # список открытых узлов
        print(f'[Rule {rule.number}] list of closed nodes: ', end='    ')
        self.print_nodes(self.close_node_lst)  # список закрытых узлов
        print(f'[Rule {rule.number}] list of prohibited nodes: ', end='')
        self.print_nodes(self.prohibited_node_lst)  # список запрещенных узлов
        print(f'[Rule {rule.number}] list of opened rules: ', end='    ')
        self.print_rules(self.open_rule_lst)  # список открытых правил
        print(f'[Rule {rule.number}] list of closed rules: ', end='    ')
        self.print_rules(self.close_rule_lst)  # список закрытых правил
        print(f'[Rule {rule.number}] list of prohibited rules: ', end='')
        self.print_rules(self.prohibited_rule_lst)  # список запрещенных правил

        print('-' * 128 + '\n')  # разделитель между выводами