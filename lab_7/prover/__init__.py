from typing import *
import copy
from parser import *
from models import *


class Prover:
    def __init__(self, facts: List[Predicate], rules: List[Rule]):
        self.facts = facts
        self.rules = rules
        self.closedFacts = []
        self.closedRules = []
        self.counter = 1

    @staticmethod
    def substitute_terms(rules, old_v, new_v, to_const):
        # print(f'{old_v} -> {new_v}')
        for rule in rules:
            if rule is not None:
                rule.rename_var(old_v, new_v, to_const)

    def try_unify(self, a1, a2, rule):
        if a1.name != a2.name or len(a1.args) != len(a2.args):
            return False

        consts_mappings = []
        linked_vars = []

        for arg1, arg2 in zip(a1.args, a2.args):
            if arg1.is_const and arg2.is_const:
                if arg1.name != arg2.name:
                    return False
            elif not arg1.is_const and not arg2.is_const:
                if arg1.name != arg2.name:
                    linked_vars.append([arg1.name, arg2.name])
            else:
                if arg1.is_const:
                    arg1, arg2 = arg2, arg1
                consts_mappings.append([arg1.name, arg2.name])

        # Объединение связанных переменных
        new_vars = dict()
        for var1, var2 in linked_vars:
            if var1 in new_vars and var2 in new_vars:
                num1 = new_vars.get(var1)
                num2 = new_vars.get(var2)
                for var in new_vars:
                    num = new_vars[var]
                    if num == num2:
                        num = num1

            else:
                if var1 in new_vars:
                    new_vars[var2] = new_vars.get(var1)
                elif var2 in new_vars:
                    new_vars[var1] = new_vars.get(var2)
                else:
                    self.counter += 1
                    new_vars[var1] = self.counter
                    new_vars[var2] = self.counter

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
                    return False
            else:
                vars_vals[old_v] = new_v

        # Замена связанных переменных
        for var in new_vars:
            num = new_vars[var]
            new_name = f"@{num}"
            self.substitute_terms([rule], var, new_name, False)
        for old_v in vars_vals:
            new_v = vars_vals[old_v]
            self.substitute_terms([rule], old_v, new_v, True)

        return True

    def is_rule_approved(self, rule: Rule):
        for term in rule.in_terms:
            if term not in self.closedFacts:
                return False
        return True

    def search_rules(self):
        can_found = False
        for idx, rule in enumerate(self.rules):
            if not rule.approved and rule not in self.closedRules:
                was_found = False
                tmp_rule = copy.deepcopy(rule)
                print(f"Попытка доказать правило: {rule}")
                for i, term in enumerate(rule.in_terms):
                    term = tmp_rule.in_terms[i]
                    if term in self.closedFacts:
                        print(f"\tТерм {term} уже доказан")
                    else:
                        closed_facts_len = len(self.closedFacts)
                        for k in range(closed_facts_len):
                            closed_fact = self.closedFacts[k]
                            if self.try_unify(closed_fact, term, tmp_rule):
                                if tmp_rule not in self.rules:
                                    print(f"\tДобавили правило: {tmp_rule}")
                                    self.rules.append(tmp_rule)
                                    was_found = True

                                if term not in self.closedFacts:
                                    print(f"\tНовый закрытый факт: {term}")
                                    self.closedFacts.append(term)
                                    was_found = True

                                tmp_rule = copy.deepcopy(rule)
                                term = tmp_rule.in_terms[i]
                can_found = can_found or was_found
                if self.is_rule_approved(rule):
                    print(f"\tПравило: {rule} доказано")
                    rule.approved = True
                    self.closedRules.append(rule)
                    self.closedFacts.append(rule.out_term)
                    print(f"\tНовый закрытый факт: {rule.out_term}")
                    can_found = True
                # elif was_found:
                #     self.closedRules.append(rule)

        return can_found

    def prove(self, goal: Predicate):
        self.closedFacts = self.facts
        can_found = True

        while can_found and goal not in self.closedFacts:
            can_found = self.search_rules()

            print("\nЗакрытые факты:")
            for closed_fact in self.closedFacts:
                print("\t", closed_fact, sep='')
            print()
            print("-------------------------------")

        return self.get_matched(goal)

    def get_matched(self, goal):
        res = []
        tmp = deepcopy(goal)
        for closed_fact in self.closedFacts:
            if self.try_unify(closed_fact, tmp, None):
                tmp = deepcopy(goal)
                res.append(closed_fact)
        return res