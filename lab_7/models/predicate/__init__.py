import typing
from enum import Enum
from copy import deepcopy
from models.variable import *

class Predicate:
    def __init__(self, name, args: typing.List[Variable], negative=False):
        # Инициализация предиката с его именем, аргументами и отрицательностью
        self.name = name
        self.args = args
        self.negative = negative

    @staticmethod
    def walk():
        # Метод, возвращающий пустой список (возможно, для последующей доработки)
        return []

    def negate(self):
        # Инвертирует состояние отрицательности предиката
        self.negative = not self.negative
        return self

    def rename_var(self, old_name: str, new_name: str, to_const: bool = False):
        # Переименовывает переменные в аргументах предиката
        for arg in self.args:
            arg.rename_var(old_name, new_name, to_const)

    def __str__(self):
        # Возвращает строковое представление предиката
        x = f'{self.name}({", ".join([str(x) for x in self.args])})'
        return x if not self.negative else f'¬{x}'

    def __repr__(self):
        # Использует строковое представление для отображения
        return str(self)

    def __eq__(self, other):
        # Сравнивает предикаты на равенство
        if not isinstance(other, Predicate):
            return False
        if self.name != other.name or len(self.args) != len(other.args):
            return False
        if self.negative != other.negative:
            return False
        for arg1, arg2 in zip(self.args, other.args):
            if arg1 != arg2:
                return False
        return True

    def __hash__(self):
        # Восстанавливает хэш для предиката, основанный на его имени и аргументах
        return hash(tuple([self.name, self.negative, *self.args]))

    def __deepcopy__(self, memo):
        # Реализует глубокое копирование предиката
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result