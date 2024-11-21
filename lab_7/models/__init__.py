import typing
from enum import Enum
from copy import deepcopy
from models.optype import OpType


SYMBOLS = '∀∃|&¬→='


def sym2type(sym):
    idx = SYMBOLS.index(sym)
    return OpType(idx)