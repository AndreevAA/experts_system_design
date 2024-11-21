from parser import *
from models import *

def prepare(facts, rules, goal):
    facts = [r.strip().rstrip() for r in facts.split('\n') if len(r.strip().rstrip()) > 0]
    rules = [r.strip().rstrip() for r in rules.split('\n') if len(r.strip().rstrip()) > 0]

    facts_g = []
    for f in facts:
        res = formula.parseString(f)[0]
        facts_g.append(res)

    rules_g = []
    for rule_idx, r in enumerate(rules):
        rule = formula.parseString(r)[0]
        rule = Rule(rule)
        rules_g.append(rule)

    goal_g = formula.parseString(goal)[0]

    print("Факты:")
    for f in facts_g:
        print('\t', f, sep='')

    print("Правила:")
    for r in rules_g:
        print('\t', r, sep='')

    print("Цель:")
    print("\t", goal_g, sep='')
    print('-------------------------------\n')

    return facts_g, rules_g, goal_g
