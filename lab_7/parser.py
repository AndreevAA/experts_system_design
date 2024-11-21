import pyparsing as pp
from models.optype import *
from models.variable import *
from models.predicate import *
from models.operation import *
from models.quantifier import *
from models import *

pp.ParserElement.enablePackrat()  # Включаем Packrat Parsing для улучшения производительности парсинга

def create_operation(t):
    opTypes = set(t[0][1::2])  # Получаем уникальные типы операций
    assert len(opTypes) == 1, "Invalid formula"  # Проверяем, что только один тип операции
    if '→' in opTypes:
        assert len(t[0][0::2]) == 2, "Invalid formula"  # Проверяем, что в импликации два операнда
    return Operation(sym2type(t[0][1]), t[0][0::2])  # Возвращаем объект Operation

# Операнды
variable = pp.Regex(r'[a-zA-Zа-яА-ЯёЁ0-9]+').setResultsName('variable').setParseAction(lambda t: Variable(t[0]))  # Определяем переменную

arguments = pp.Group(pp.Suppress('(') + pp.delimitedList(variable) + pp.Suppress(')')).setResultsName('arguments')  # Определяем аргументы предиката

predicate = pp.Regex(r'[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ0-9]*') + arguments  # Определяем предикат
predicate = predicate.setResultsName('predicate').setParseAction(lambda t: Predicate(t[0], t.arguments.asList()))  # Создаем объект Predicate

operand = predicate | variable  # Определяем операнды как предикаты или переменные

formula = pp.Forward()  # Определяем формулу, которую будем парсить
quantifiers = pp.oneOf("∃ ∀") + variable + formula  # Определяем кванторы
quantifiers.setParseAction(lambda t: Quantifier(sym2type(t[0]), t[1], t[2]))  # Создаем объект Quantifier

expr = pp.infixNotation(operand | quantifiers, [  # Определяем выражение с учетом инфиксной нотации
    ("¬", 1, pp.opAssoc.RIGHT, lambda t: Operation(OpType.NOT, [t[0][1]])),  # Обработка операции "НЕ"
    (pp.oneOf("& | → ="), 2, pp.opAssoc.LEFT, create_operation),  # Обработка бинарных операций
])
formula <<= expr  # Присваиваем выражение формуле

def main():
    # Пример парсинга различных формул и вывод результата
    res = formula.parseString('(p2(x) & p3(x) & p4(x)) → p5(x)')
    print(res[0])

    res = formula.parseString('p1(Pepe)')
    print(res[0])

    res = formula.parseString('¬(¬x)')
    print(res[0])

    res = formula.parseString('∀x (x | ¬x)')
    print(res[0])

    res = formula.parseString('p1(x, y)')
    print(res[0])

    res = formula.parseString('¬(x | z) & (¬x → p1(x, y))')
    print(res[0])

    res = formula.parseString('((x | (x → y)) & (y | z)) & (x = z)')
    print(res[0])

    res = formula.parseString('¬(x & y & z)')
    print(res[0])

if __name__ == '__main__':
    main()  # Запускаем главную функцию