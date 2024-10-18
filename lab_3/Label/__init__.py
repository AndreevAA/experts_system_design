from typing import List
from enum import Enum


class Label(Enum):
    OPEN = 0
    CLOSE = 1
    FORBIDDEN = -1
    VIEWED = 2
