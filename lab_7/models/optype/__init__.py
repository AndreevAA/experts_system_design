import typing
from enum import Enum
from copy import deepcopy

class OpType(Enum):
    ALL = 0
    EXISTS = 1
    OR = 2
    AND = 3
    NOT = 4
    IMPLY = 5
    EQUAL = 6
