import typing
from enum import Enum
from copy import deepcopy

class Variable:
    def __init__(self, name, negative=False):
        self.name = name  # Имя переменной
        self.negative = negative  # Флаг отрицательной переменной

    @property
    def is_const(self):
        return not self.is_var  # Определяет, является ли переменная константой

    @property
    def is_var(self):
        return self.name[0].islower()  # Проверяет, является ли переменная переменной (начинается с маленькой буквы)

    @staticmethod
    def walk():
        return []  # Возвращает пустой список (возможно, для будущей реализации обхода)

    def negate(self):
        self.negative = not self.negative  # Меняет состояние отрицания переменной
        return self

    def rename_var(self, old_name: str, new_name: str, to_const: bool = False):
        if self.name == old_name:
            self.name = new_name  # Переименовывает переменную, если ее имя совпадает с old_name

    def __str__(self):
        return self.name if not self.negative else f'¬{self.name}'  # Строковое представление переменной

    def __repr__(self):
        return str(self)  # Представление для отладки

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False  # Сравнение переменной с другим объектом
        return self.name == other.name and self.negative == other.negative  # Сравнение как по имени, так и по флагу отрицания

    def __hash__(self):
        return hash(tuple([self.name, self.negative]))  # Хеширование переменной

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)  # Создание нового объекта
        memo[id(self)] = result  # Запоминание нового объекта для предотвращения циклических ссылок
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))  # Глубокое копирование атрибутов
        return result