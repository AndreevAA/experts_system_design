import typing
from enum import Enum
from copy import deepcopy
from models.optype import *
from models import *

class Quantifier:
    def __init__(self, op_type: OpType, var, op):
        assert op_type in [OpType.ALL, OpType.EXISTS]
        self.type = op_type
        self.var = var
        self.op = op

    def walk(self):
        for x in self.op.walk():
            yield x
        yield self.op

    def negate(self):
        self.type = OpType.EXISTS if self.type == OpType.ALL else OpType.ALL
        self.op = Operation(OpType.NOT, [self.op])
        return self

    def rename_var(self, old_name, new_name):
        self.op.rename_var(old_name, new_name)

    def __str__(self):
        if self.op is None:
            return SYMBOLS[self.type.value] + f'{self.var}'
        return SYMBOLS[self.type.value] + f'{self.var} ({self.op})'

    def __repr__(self):
        return str(self)