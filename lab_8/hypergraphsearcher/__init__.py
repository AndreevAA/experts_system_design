from table import Table
from unification import Unification

class HyperGraphSearcher:
    def __init__(self, rules):
        self.rules = rules
        self.table = None

        # Списки доказанных атомов и правил
        self.proven_atoms = list()
        self.proven_rules = list()

        # Списки открытых атомов и правил
        self.opened_atoms = list()
        self.opened_rules = list()
        self.used_atoms = list()

        self.found = False  # флаг решения

    def search_from_target(self, input_atoms, target_atom):
        self.table = Table()

        # Добавляем целевой атом в список открытых атомов
        self.opened_atoms.insert(0, target_atom)
        # Заносим входные данные (атомы) в список доказанных атомов
        self.proven_atoms = list(input_atoms)

        # Подцель берем из головы И потомки записываются в голову, механзм СТЕКА
        current = self.opened_atoms[0]

        # Пока не найдено решение или не закончились атомы (потомки)
        while not self.found and len(self.opened_atoms) != 0:
            print('\nТекущая подцель', current)

            print(f"Список доказанных атомов: ", self.proven_atoms)
            print(f"Список доказанных правил: ", self.proven_rules)

            end_vertex = True  # Флаг все атомы доказаны
            prove_num = False  # Флаг доказанного номера правила
            check_unif = True  # Флаг нужно провести унификацию

            # Пока не конец базы правил
            for num, rule in self.rules.items():

                # Метод потомков, ищем правило в базе правил, выходной атом которого унфицируется с подцелью
                if check_unif:
                    if Unification(self.table, rule.output_vertex, current).run():
                        print('Номер текущего правила: ', num)
                        print("Унификация выполнена:", rule.output_vertex, current)
                        print('Tаблица подстановок:', self.table.variables)
                        print('Таблица cвязей:', self.table.links)
                        check_unif = False
                        self.used_atoms.insert(0, current)

                if not check_unif:
                    # Смотрим входные атомы для текущего правила
                    for node in rule.input_atoms:
                        # Проверяем входят ли входные атомы в список закрытых атомов
                        if node not in self.used_atoms:
                            print('\nАтом', node)
                            end_vertex = False
                            prove_num = False

                            # Если номер текущего правила не в списке открытых, добавляем номер правила в список открытых
                            if num not in self.opened_rules:
                                self.opened_rules.insert(0, num)

                            # Пока не конец базы фактов
                            for proven in self.proven_atoms:
                                if Unification(self.table, node, proven).run():
                                    print("Атом", node, "уже доказан")
                                    print('Tаблица подстановок:', self.table.variables)
                                    print('Таблица cвязей:', self.table.links)

                                    prove_num = True
                                    self.used_atoms.insert(0, node)
                                    break

                            if prove_num == False:
                                # Если атом текущего правила не в списке открытых, добавляем атом в список открытых
                                if node not in self.opened_atoms and node not in self.used_atoms:
                                    self.opened_atoms.insert(0, node)

                                # Меняем подцель, берем из головы
                                current = self.opened_atoms[0]
                                print('Атом становится новой подцелью')
                                check_unif = True
                                # Переходим к раскрытию новой подцели
                                break

                    # Если все атомы в списке фактов (закрытых) -> разметка
                    if prove_num:
                        # Распространение
                        for i in range(len(current.terminals)):
                            current.terminals[i] = self.table.variables[str(current.terminals[i])]

                        if len(self.opened_atoms) != 0:
                            # Добавляем в список фактов (закрытых), убираем подцель из стека
                            self.proven_atoms.append(self.opened_atoms.pop(0))
                            if len(self.opened_rules) != 0:
                                self.proven_rules.append(self.opened_rules.pop(0))

                        print(f"Список доказанных атомов: ", self.proven_atoms)
                        print(f"Список доказанных правил: ", self.proven_rules)

                        # Выбираем следующий атом (подцель) из головы
                        if len(self.opened_atoms) != 0 and len(self.opened_rules) != 0:
                            current = self.opened_atoms[0]

                        # Список открытых атомов пуст
                        else:
                            # Проверяем есть ли целевой атом в списке доказанных
                            if target_atom in self.proven_atoms:
                                print('Целевой атом в списке доказанных!')
                                self.found = True  # меняем флаг решения
                                break
                            else:
                                print("Список открытых атомов пуст!")
                                break
                        break

            # Если все атомы в правиле доказаны
            if end_vertex:
                print('Доказали все атомы в правиле, правило доказано!')

                if len(self.opened_atoms) != 0:
                    # Добавляем эту вершину в список доказанных
                    self.proven_atoms.append(self.opened_atoms.pop(0))

                    if len(self.opened_rules) != 0:
                        # Добавляем номер правила в список доказанных
                        self.proven_rules.append(self.opened_rules.pop(0))

                print('\nКонечные списки')
                print(f"Список доказанных атомов: ", self.proven_atoms)
                print(f"Список доказанных правил: ", self.proven_rules)

                if len(self.opened_atoms) != 0:
                    # Меняем подцель
                    current = self.opened_atoms[0]
                else:
                    self.found = True

        if self.found:
            print('\nРешение найдено!')
            return self.found, self.proven_atoms, self.proven_rules
        else:
            if len(self.opened_atoms) == 0:
                print('\nАтом НЕ найден! Список открытых атомов пуст!')
                return self.found