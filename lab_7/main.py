from prover import *
from tests import *
from prepare import *


def main():
    facts, rules, goal = Tests().test_5()
    facts, rules, goal = prepare(facts, rules, goal)

    matched = Prover(facts, rules).prove(goal)

    if not matched:
        print('ЛОЖЬ')
    else:
        print('ИСТИНА:')
        for match in matched:
            print("\t", match, sep='')


if __name__ == '__main__':
    main()
