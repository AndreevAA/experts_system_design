from typing import *
import copy
from parser import *
from models.predicate import *
from models.operation import *
from models.quantifier import *
from models.rule import *
from models.variable import *
from models.optype import *

class Prover:
    def __init__(self, facts: List[Predicate], rules: List[Rule]):
        # Инициализация с фактами и правилами
        self.facts = facts
        self.rules = rules
        self.closedFacts = []
        self.closedRules = []
        self.counter = 1  # Счетчик для уникальных переменных

    @staticmethod
    def substitute_terms(rules, old_v, new_v, to_const):
        # Замена переменной old_v на new_v в правилах
        for rule in rules:
            if rule is not None:
                rule.rename_var(old_v, new_v, to_const)

    def try_unify(self, a1, a2, rule):
        # Попытка унификации двух предикатов a1 и a2 с учетом правила
        if a1.name != a2.name or len(a1.args) != len(a2.args):
            return False  # Не совпадают имена или количество аргументов

        consts_mappings = []  # Для сопоставления констант
        linked_vars = []  # Для связывания переменных

        for arg1, arg2 in zip(a1.args, a2.args):
            if arg1.is_const and arg2.is_const:
                if arg1.name != arg2.name:
                    return False  # Константы не совпадают
            elif not arg1.is_const and not arg2.is_const:
                if arg1.name != arg2.name:
                    linked_vars.append([arg1.name, arg2.name])  # Связываем переменные
            else:
                if arg1.is_const:
                    arg1, arg2 = arg2, arg1  # Сделаем так, чтобы arg1 всегда был переменной
                consts_mappings.append([arg1.name, arg2.name])  # Сопоставляем переменную и константу

        # Объединение связанных переменных
        new_vars = dict()
        for var1, var2 in linked_vars:
            if var1 in new_vars and var2 in new_vars:
                num1 = new_vars.get(var1)
                num2 = new_vars.get(var2)
                for var in new_vars:
                    num = new_vars[var]
                    if num == num2:
                        num = num1  # Объединяем числа для связанных переменных
            else:
                if var1 in new_vars:
                    new_vars[var2] = new_vars.get(var1)  # Присваиваем номер, если одна из переменных уже есть
                elif var2 in new_vars:
                    new_vars[var1] = new_vars.get(var2)
                else:
                    self.counter += 1
                    new_vars[var1] = self.counter  # Новая уникальная переменная
                    new_vars[var2] = self.counter

        # Обновление имён переменных в соответствии с их новыми значениями
        for var in new_vars:
            num = new_vars[var]
            for i in range(len(consts_mappings)):
                old_v, new_v = consts_mappings[i]
                if old_v == var:
                    consts_mappings[i][0] = f'@{num}'

        vars_vals = dict()
        for old_v, new_v in consts_mappings:
            if old_v in vars_vals:
                if vars_vals.get(old_v) != new_v:
                    return False  # Конфликт в сопоставлении
            else:
                vars_vals[old_v] = new_v  # Систематизация значений переменных

        # Замена связанных переменных в правиле
        for var in new_vars:
            num = new_vars[var]
            new_name = f"@{num}"  # Обновлённое имя переменной
            self.substitute_terms([rule], var, new_name, False)
        for old_v in vars_vals:
            new_v = vars_vals[old_v]
            self.substitute_terms([rule], old_v, new_v, True)  # Для константы тоже

        return True

    def is_rule_approved(self, rule: Rule):
        # Проверка, что все термины в правилах закрыты
        for term in rule.in_terms:
            if term not in self.closedFacts:
                return False
        return True

    def search_rules(self):
        # Поиск правил, которые можно доказать
        can_found = False
        for idx, rule in enumerate(self.rules):
            if not rule.approved and rule not in self.closedRules:  # Если правило еще не доказано
                was_found = False
                tmp_rule = copy.deepcopy(rule)  # Работаем с копией правила
                print(f"Попытка доказать правило: {rule}")
                for i, term in enumerate(rule.in_terms):
                    term = tmp_rule.in_terms[i]
                    if term in self.closedFacts:
                        print(f"\tТерм {term} уже доказан")
                    else:
                        closed_facts_len = len(self.closedFacts)
                        for k in range(closed_facts_len):
                            closed_fact = self.closedFacts[k]
                            if self.try_unify(closed_fact, term, tmp_rule):  # Пытаемся унифицировать
                                if tmp_rule not in self.rules:
                                    print(f"\tДобавили правило: {tmp_rule}")
                                    self.rules.append(tmp_rule)  # Добавляем новое правило
                                    was_found = True

                                if term not in self.closedFacts:
                                    print(f"\tНовый закрытый факт: {term}")
                                    self.closedFacts.append(term)  # Добавляем новый закрытый факт
                                    was_found = True

                                tmp_rule = copy.deepcopy(rule)  # Сбрасываем временное правило для следующей итерации
                                term = tmp_rule.in_terms[i]
                can_found = can_found or was_found  # Обновляем флаг поиска
                if self.is_rule_approved(rule):
                    print(f"\tПравило: {rule} доказано")
                    rule.approved = True  # Помечаем правило как доказанное
                    self.closedRules.append(rule)  # Добавляем его в закрытые правила
                    self.closedFacts.append(rule.out_term)  # Новый закрытый факт из правила
                    print(f"\tНовый закрытый факт: {rule.out_term}")
                    can_found = True

        return can_found

    def prove(self, goal: Predicate):
        # Основной метод для доказательства цели
        self.closedFacts = self.facts  # Начинаем с фактов
        can_found = True

        while can_found and goal not in self.closedFacts:
            can_found = self.search_rules()  # Ищем доказательства

            print("\nЗакрытые факты:")
            for closed_fact in self.closedFacts:
                print("\t", closed_fact, sep='')
            print()
            print("-------------------------------")

        return self.get_matched(goal)  # Возвращаем соответствия для целевого предиката

    def get_matched(self, goal):
        # Получаем соответствия для цели среди закрытых фактов
        res = []
        tmp = deepcopy(goal)  # Временная копия цели
        for closed_fact in self.closedFacts:
            if self.try_unify(closed_fact, tmp, None):
                tmp = deepcopy(goal)  # Сбрасываем временную копию
                res.append(closed_fact)  # Добавляем совпадающий закрытый факт
        return res