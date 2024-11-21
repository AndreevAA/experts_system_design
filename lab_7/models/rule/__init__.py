import typing
from enum import Enum
from copy import deepcopy
from models.optype import *
from models.operation import *
from models import *

class Rule:
    """
    Логическое выражение
    вида x1 & ... & xn -> y1
    """

    def __init__(self, imply_op):
        # Проверка, что переданная операция является импликацией
        assert imply_op.type == OpType.IMPLY

        self.op = imply_op  # Операция, представляющая правило

        # Доказываемый терм - правый аргумент импликации
        self.out_term = imply_op.args[1]

        # Входные термы - левый аргумент импликации
        in_terms = imply_op.args[0]
        if isinstance(in_terms, Operation):
            # Если входные термы представлены операцией "И"
            assert in_terms.type == OpType.AND
            self.in_terms = in_terms.args  # Получаем аргументы операции
        elif isinstance(in_terms, Predicate):
            # Если входной терм - предикат, помещаем его в список
            self.in_terms = [in_terms]

        self.approved = False  # Статус утверждения правила

    @property
    def atoms(self):
        # Возвращает аргументы операции
        return self.op.args

    def rename_var(self, old_name: str, new_name: str, to_const: bool):
        # Переименовывает переменные в аргументах правил
        for a in self.atoms:
            for arg in a.args:
                arg.rename_var(old_name, new_name, to_const)

    def __str__(self):
        # Возвращает строковое представление правила
        return str(self.op)

    def __repr__(self):
        # Использует строковое представление для отображения
        return str(self)

    def __eq__(self, other):
        # Сравнивает два правила на равенство
        return self.op == other.op

    def __hash__(self):
        # Возвращает хэш для объекта правила
        return hash(self.op)

    def __deepcopy__(self, memo):
        # Создает глубокую копию правила
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result