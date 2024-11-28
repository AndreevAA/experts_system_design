# структура подстановок (таблица подстановок: какие значения присвоены переменным и какие переменные связаны между собой.)
class Table:
    def __init__(self):
        self.variables = dict()  # храним переменные
        self.links = dict()  # связанные значения

    # Вывод на экран и вывод ошибок
    def reset(self, other):
        self.variables = other.variables
        self.links = other.links

    def val(self, var):
        return self.variables[var.name]

    def var_links(self, var):
        return self.links[self.variables[var.name]]

    def __str__(self):
        res = ""
        for const in self.links.keys():
            res += str(self.links[const]) + ": " + str(const) + "\n"
        return res