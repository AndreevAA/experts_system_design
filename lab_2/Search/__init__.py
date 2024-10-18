from Rule import Rule
from Node import Node
from Label import Label
from Stack import Stack


# Поиск в ширину о данных к целе
# (include parent method -- looks for closed rules)
class Search:
    def __init__(self, rule_arr: [Rule]):
        self.rule_arr = rule_arr  # база знаний
        self.open_node_st = Stack()
        self.open_rule_lst = []
        self.close_node_lst = []
        self.close_rule_lst = []
        self.prohibited_node_lst = []
        self.prohibited_rule_lst = []

        self.goal_node = None
        self.solution_flg = True
        self.no_solution_flg = True

    def run(self, goal_node: Node, in_node_arr: [Node]):
        self.goal_node = goal_node
        self.open_node_st.push(goal_node)
        self.close_node_lst = in_node_arr

        while self.solution_flg and self.no_solution_flg:
            rule_cnt = self.parent_search()

            # решение найдено
            if not self.solution_flg:
                return

            if rule_cnt == 0:
                self.no_solution_flg = False
                print("Решение не найдено")

    def parent_search(self):
        cnt_rules = 0

        for rule in self.rule_arr:
            print(f'[Rule {rule.number}] Текущая правило')
            if not self.is_rule_processable(rule):
                continue

            if self.is_close_nodes_cover(rule.node_arr):
                cnt_rules += self.process_valid_rule(rule)
            else:
                self.handle_uncovered_rule(rule)

            self.print_state(rule)

        print(f'{cnt_rules} правил было доказано')
        return cnt_rules

    def is_rule_processable(self, rule: Rule):
        if rule.label != Label.OPEN:
            print(f'[Rule {rule.number}] было уже обработано')
            print('-' * 128 + '\n')
            return False
        return True

    def process_valid_rule(self, rule: Rule):
        print(f'[Rule {rule.number}] Все входящие узлы включены в закрытые узлы')

        rule.label = Label.CLOSE
        self.close_rule_lst.append(rule)
        self.close_node_lst.append(rule.out_node)
        self.set_nodes_closed(rule.node_arr)

        if rule.out_node == self.goal_node:
            self.solution_flg = False
            print(f'[Rule {rule.number}] выходной узел равен целевому')

        return 1

    def handle_uncovered_rule(self, rule: Rule):
        print(f'[Rule {rule.number}] не все входные узлы закрыты')

    def is_close_nodes_cover(self, in_node_arr: [Node]):
        return all(node in self.close_node_lst for node in in_node_arr)

    def set_nodes_closed(self, node_arr):
        for node in node_arr:
            node.flag = Label.CLOSE

    def print_state(self, rule: Rule):
        print(f'[Rule {rule.number}] список закрытых правил: ', end='')
        self.print_rules(self.close_rule_lst)
        print(f'[Rule {rule.number}] список закрытых узлов: ', end='')
        self.print_nodes(self.close_node_lst)
        print('-' * 128 + '\n')

    def print_rules(self, rule_arr: [Rule]):
        print(' '.join(str(rule.number) for rule in rule_arr))

    def print_nodes(self, node_arr: [Node]):
        print(' '.join(str(node) for node in node_arr))