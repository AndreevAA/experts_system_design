class Constant:  # структура константа
    def __init__(self, value):
        self.value = value  # значение
        self.variable = False  # флаг НЕ переменная

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.__str__()