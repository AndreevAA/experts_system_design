class Variable:  # структура переменная
    def __init__(self, name):
        self.name = name  # имя
        self.variable = True  # флаг переменная

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()
