import typing
from enum import Enum
from copy import deepcopy

SYMBOLS = '∀∃|&¬→='




def sym2type(sym):
    idx = SYMBOLS.index(sym)
    return OpType(idx)








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


class Predicate:
    def __init__(self, name, args: typing.List[Variable], negative=False):
        self.name = name
        self.args = args
        self.negative = negative

    @staticmethod
    def walk():
        return []

    def negate(self):
        self.negative = not self.negative
        return self

    def rename_var(self, old_name: str, new_name: str, to_const: bool = False):
        for arg in self.args:
            arg.rename_var(old_name, new_name, to_const)

    def __str__(self):
        x = f'{self.name}({", ".join([str(x) for x in self.args])})'
        return x if not self.negative else f'¬{x}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
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
        return hash(tuple([self.name, self.negative, *self.args]))

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class Rule:
    """
    Логическое выражение
    вида x1 & ... & xn -> y1
    """

    def __init__(self, imply_op):
        assert imply_op.type == OpType.IMPLY

        self.op = imply_op

        # доказываемый терм
        self.out_term = imply_op.args[1]

        # входные термы
        in_terms = imply_op.args[0]
        if isinstance(in_terms, Operation):
            assert in_terms.type == OpType.AND
            self.in_terms = in_terms.args
        elif isinstance(in_terms, Predicate):
            self.in_terms = [in_terms]

        self.approved = False

    @property
    def atoms(self):
        return self.op.args

    def rename_var(self, old_name: str, new_name: str, to_const: bool):
        for a in self.atoms:
            for arg in a.args:
                arg.rename_var(old_name, new_name, to_const)

    def __str__(self):
        return str(self.op)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.op == other.op

    def __hash__(self):
        return hash(self.op)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result
