import typing
from enum import Enum
from copy import deepcopy


class Operation:
    def __init__(self, op_type: OpType, args: typing.List):
        assert op_type not in [OpType.ALL, OpType.EXISTS]
        self.type = op_type
        self.args = args

    def walk(self):
        for arg in self.args:
            for x in arg.walk():
                yield x
            yield arg

    def negate(self):
        assert self.type in [OpType.OR, OpType.AND, OpType.NOT]
        if self.type == OpType.NOT:
            return self.args[0]

        self.type = OpType.OR if self.type == OpType.AND else OpType.AND
        for i, arg in enumerate(self.args):
            self.args[i] = Operation(OpType.NOT, [self.args[i]])
        return self

    def rename_var(self, old_name, new_name):
        for arg in self.args:
            arg.rename_var(old_name, new_name)

    def __str__(self):
        def need_brackets(arg):
            return not isinstance(arg, Variable) \
                and not isinstance(arg, Predicate) \
                and not (isinstance(arg, Operation) and arg.type == OpType.NOT and self.type != OpType.NOT)

        def add_opt_brackets(arg):
            if need_brackets(arg):
                return f'({arg})'
            return str(arg)

        if self.type != OpType.NOT:
            return f' {SYMBOLS[self.type.value]} '.join(map(add_opt_brackets, self.args))
        else:
            a1 = add_opt_brackets(self.args[0])
            return f'¬{a1}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Operation):
            return False
        if self.type != other.type or len(self.args) != len(other.args):
            return False
        for arg1, arg2 in zip(self.args, other.args):
            if arg1 != arg2:
                return False
        return True

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result