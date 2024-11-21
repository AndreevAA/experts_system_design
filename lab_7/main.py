from prover import *
from tests import *
from prepare import *


def main():
    facts, rules, goal = Tests().test_5()

    # Подготавливаем факты, правила и цель для использования в доказательствах
    facts, rules, goal = prepare(facts, rules, goal)

    # Создаем экземпляр Prover с подготовленными фактами и правилами, затем пытаемся доказать цель
    matched = Prover(facts, rules).prove(goal)

    # Если не удалось найти соответствие (доказательство), печатаем 'ЛОЖЬ'
    if not matched:
        print('ЛОЖЬ')
    else:
        print('ИСТИНА:')
        for match in matched:
            print("\t", match, sep='')


if __name__ == '__main__':
    main()
