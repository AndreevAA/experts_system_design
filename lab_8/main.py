import copy
from constant import Constant
from variable import Variable
from atom import Atom
from rule import Rule
from hypergraphsearcher import HyperGraphSearcher


def main():
    c_N = Constant('N')
    c_M1 = Constant('M1')
    c_W = Constant('W')
    c_A1 = Constant('A1')

    v_x = Variable("x")
    v_y = Variable("y")
    v_z = Variable("z")
    v_x1 = Variable("x1")
    v_x2 = Variable("x2")
    v_x3 = Variable("x3")

    node1 = Atom("A", [v_x])
    node2 = Atom("W", [v_y])
    node3 = Atom("S", [v_x, v_y, v_z])
    node4 = Atom("H", [v_z])
    node5 = Atom("C", [v_x])

    node6 = Atom("M", [v_x1])
    node7 = Atom("O", [c_N, v_x1])
    node8 = Atom("S", [c_W, v_x1, c_N])

    node9 = Atom("M", [v_x2])
    node10 = Atom("W", [v_x2])

    node11 = Atom("E", [v_x3, c_A1])
    node12 = Atom("H", [v_x3])

    rules = dict()
    rules[1] = Rule([node1, node2, node3, node4], node5)
    rules[2] = Rule([node6, node7], node8)
    rules[3] = Rule([node9], node10)
    rules[4] = Rule([node11], node12)

    graph = HyperGraphSearcher(rules)

    target = Atom("C", [c_W])
    given = [
        Atom("O", [c_N, c_M1]),
        Atom("M", [c_M1]),
        Atom("A", [c_W]),
        Atom("E", [c_N, c_A1]),
    ]

    res, nodes, rules = graph.search_from_target(given, target)

    print("\nДоказанные атомы:", nodes)
    print("Доказанные правила:", rules)
    print("Таблица подстановок:", graph.table, sep='\n')


if __name__ == "__main__":
    main()
