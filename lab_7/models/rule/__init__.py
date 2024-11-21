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
