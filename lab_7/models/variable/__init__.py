import typing
from enum import Enum
from copy import deepcopy


class Variable:
    def __init__(self, name, negative=False):
        self.name = name
        self.negative = negative

    @property
    def is_const(self):
        return not self.is_var

    @property
    def is_var(self):
        return self.name[0].islower()

    @staticmethod
    def walk():
        return []

    def negate(self):
        self.negative = not self.negative
        return self

    def rename_var(self, old_name: str, new_name: str, to_const: bool = False):
        if self.name == old_name:
            self.name = new_name

    def __str__(self):
        return self.name if not self.negative else f'¬{self.name}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return self.name == other.name and self.negative == other.negative

    def __hash__(self):
        return hash(tuple([self.name, self.negative]))

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

