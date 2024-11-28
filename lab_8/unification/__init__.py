import copy


class Unification:

    def __init__(self, table, p1, p2):
        self.table = table
        self.p1 = p1
        self.p2 = p2

    def run(self):
        # получаеем атомы которые нужно унифицировать
        # Проверяем, равны имена предикатов p1,p2 или нет
        if self.p1.name != self.p2.name:
            # Если имена не равны, то унификация невозможна
            print('Имена не совпадают')
            return False

        # Проверяем, равны ли длины массивов переменных предикатов p1 и p2
        if len(self.p1.terminals) != len(self.p2.terminals):
            # Если длины не равны, то унификация невозможна
            print('Длины не совпадают')
            return False

        original = copy.deepcopy(self.table)
        # Перебирает пары термов t1 и t2 из списков термов атомов p1 и p2, используя функцию zip, которая сопоставляет элементы с одинаковыми индексами.
        for t1, t2 in zip(self.p1.terminals, self.p2.terminals):
            # Проверяем является ли терм t1 переменной (проверка флага)
            if t1.variable:
                # Если первый терм переменная, проверяем является ли второй терм переменной (проверка флага)
                if t2.variable:
                    y = True  # флаг возможности унификации

                    # Проверяем есть ли обе переменные в таблице подстановок
                    if t1.name not in self.table.variables and t2.name not in self.table.variables:
                        # Если их нет, добавляем и связываем
                        self.table.variables[t1.name] = t2.name
                        self.table.variables[t2.name] = t1.name

                    # Проверяем есть ли первая переменная в таблице подстановок
                    elif t1.name not in self.table.variables:
                        # Переменные равны и связаны между собой
                        self.table.variables[t1.name] = self.table.variables[t2.name]

                    # Проверяем есть ли вторая переменная в таблице подстановок
                    elif t2.name not in self.table.variables:
                        # Переменные равны и связаны между собой
                        self.table.variables[t1.name] = self.table.variables[t2.name]

                    # Проверяем равенство значений переменных в таблице подстановок
                    elif self.table.variables[t1.name] != self.table.variables[t2.name]:
                        # Если значения не равны, то меняем флаг унификации (она невозможна)
                        y = False

                    if y == False:
                        print("Переменная ", t1.name, " не соответствует другой переменной ", t2.name, ": ",
                              self.table.val(t1),
                              " != ", self.table.val(t2), sep='')
                        self.table.reset(original)
                        return False

                # Если первый терм переменная, а второй терм константа
                else:
                    y = True
                    # Проверяем, есть ли переменная t1 в таблице подстановок и есть ли у нее значение (константа)
                    if t1.name in self.table.variables and type(self.table.variables[t1.name]) is not str:
                        # проверяем, равно ли значение переменной t1 в таблице подстановок значению константы t2
                        if self.table.variables[t1.name].value != t2.value:
                            # если не равно, то меняем флаг унификации, она невозможна
                            y = False

                    # Если переменной нет в таблцие подстановок
                    if t1.name not in self.table.variables:
                        # присваиванем значению переменной t1 в таблице подстановок значения константы t2.
                        self.table.variables[t1.name] = t2

                    # Если у переменной нет значения (константы)
                    if type(self.table.variables[t1.name]) is str:
                        # присваиванем значению переменной t1 в таблице подстановок значения константы t2. и всем связанным переменным тоже
                        k = self.table.variables[t1.name]
                        self.table.variables[t1.name] = t2
                        self.table.variables[k] = t2
                        self.table.links[t2.value] = {k}

                    # проверяем, есть ли константа t2 в таблице связей
                    if t2.value not in self.table.links:
                        # Связываем переменную с этой константой.
                        self.table.links[t2.value] = {t1.name}
                    else:
                        # если константы нет в таблице связей, то дабвляем эту связь
                        self.table.links[t2.value].add(t1.name)

                    if y == False:
                        print("Несоответствующее значение переменной константе: ", t1.name, " = ", self.table.val(t1),
                              "константа", t2.value)
                        self.table.reset(original)
                        return False


            # Терм t1 не является переменной
            else:
                # Проверяем является ли второй терм t2 переменной (проверка флага)
                if t2.variable:
                    # t2 переменная
                    y = True

                    # Проверяем, есть ли переменная t1 в таблице подстановок и есть ли у нее значение (константа)
                    if t2.name in self.table.variables and type(self.table.variables[t2.name]) is not str:
                        # проверяем, равно ли значение переменной t1 в таблице подстановок значению константы t2
                        if self.table.variables[t2.name].value != t1.value:
                            # если не равно, то меняем флаг унификации, она невозможна
                            y = False

                    # Если переменной нет в таблцие подстановок
                    if t2.name not in self.table.variables:
                        # присваиванем значению переменной t1 в таблице подстановок значения константы t2.
                        self.table.variables[t2.name] = t1

                    # Если у переменной нет значения (константы)
                    if type(self.table.variables[t2.name]) is str:
                        # присваиванем значению переменной t1 в таблице подстановок значения константы t2. и всем связанным переменным тоже
                        k = self.table.variables[t2.name]
                        self.table.variables[t2.name] = t1
                        self.table.variables[k] = t1
                        self.table.links[t1.value] = {k}

                    # проверяет, есть ли константа t1 в таблице связей
                    if t1.value not in self.table.links:
                        # Связываем переменную с этой константой.
                        self.table.links[t1.value] = {t2.name}
                    else:
                        # если константы нет в таблице связей, то дабвляем эту связь
                        self.table.links[t1.value].add(t2.name)

                    if y == False:
                        print("Несоответствующее значение переменной константы:", t2.name, "=", self.table.val(t2),
                              "константа", t1.value)
                        self.table.reset(original)
                        return False
                else:
                    # t2 не перменная, сравниваем начения двух констант
                    if t1.value != t2.value:
                        print("Константы не соответствуют:", t1.value, "!=", t2.value)
                        self.table.reset(original)
                        return False
        return True
