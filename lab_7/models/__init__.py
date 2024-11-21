import typing
from enum import Enum
from copy import deepcopy
from models.optype import OpType

# Определяет набор символов для логических операций и кванторов
SYMBOLS = '∀∃|&¬→='

def sym2type(sym):
    # Функция для преобразования символа логической операции в соответствующий тип OpType
    idx = SYMBOLS.index(sym)  # Находит индекс символа в строке SYMBOLS
    return OpType(idx)