from Rule import Rule
from Node import Node
from Label import Label
from Stack import Stack


# Поиск в ширину о данных к целе
# (include parent method -- looks for closed rules)
class Search:
    def __init__(self, rules: [Rule]):
        self.rules = rules  # База правил
        self.open_nodes = Stack()
        self.closed_rules = []
        self.closed_nodes = []
        self.blocked_rules = []
        self.blocked_nodes = []

        self.target = None  # Целевая нода
        self.found_solution = True
        self.no_solution = True

    def run(self, target: Node, initial_nodes: [Node]):
        self.target = target  # Установка целевой ноды
        self.open_nodes.push(target)  # Добавление целевой ноды в стек открытых
        self.closed_nodes = initial_nodes  # Установка начальных закрытых нод

        while self.found_solution and self.no_solution:
            rule_count = self.search_parent_rules()  # Поиск родительских правил

            if not self.found_solution:
                return

            if rule_count == 0:
                self.no_solution = False
                print("Решение не найдено")

    def search_parent_rules(self):
        count = 0  # Счетчик доказанных правил

        for rule in self.rules:
            if self.is_rule_processed(rule):
                continue  # Переход к следующему правилу, если уже обработано

            if self.are_closed_nodes_covered(rule.node_arr):
                count += self.process_rule(rule)  # Обработка правила и увеличение счетчика

        print(f'Доказано {count} правил')
        return count

    def is_rule_processed(self, rule: Rule) -> bool:
        if rule.label != Label.OPEN:
            print(f'[Правило {rule.number}] уже обработано')
            return True
        return False

    def process_rule(self, rule: Rule) -> int:
        print(f'[Правило {rule.number}] все входные ноды закрыты')
        rule.label = Label.CLOSE
        self.closed_rules.append(rule)  # Добавляем правило в список закрытых
        self.closed_nodes.append(rule.out_node)  # Добавляем выходную ноду в список закрытых
        self.close_nodes(rule.node_arr)  # Закрываем входные ноды

        if rule.out_node == self.target:
            self.found_solution = False
            print(f'[Правило {rule.number}] выходная нода совпадает с целевой')
            return 1

        return 0

    def are_closed_nodes_covered(self, input_nodes: [Node]) -> bool:
        for node in input_nodes:
            if node not in self.closed_nodes:
                return False
        return True

    def close_nodes(self, node_arr):
        for node in node_arr:
            node.flag = Label.CLOSE  # Установка соответствующего флага закрытия

    def display_closed_rules(self):
        print(f'Список закрытых правил: ', end='')
        for rule in self.closed_rules:
            print(rule.number, end=' ')
        print()

    def display_closed_nodes(self):
        print(f'Список закрытых нод: ', end='')
        for node in self.closed_nodes:
            print(node, end=' ')
        print()