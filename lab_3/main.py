from Node import Node
from Rule import Rule
from Search import Search


# Функция для отображения найденного пути
def show(arr: list):
    if arr is None:
        print("Not found")  # Если путь не найден
        return
    # Выводит путь в обратном порядке от конца к началу
    for i in range(len(arr) - 1, -1, -1):
        if i != 0:
            print(f'{arr[i]} <- ', end='')  # Указывает на предыдущий узел
        else:
            print(f'{arr[i]}')  # Печатает начальный узел

# Тестовая функция для создания узлов и правил
def test_1():
    # Создание узлов
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)
    node8 = Node(8)
    node9 = Node(9)

    node11 = Node(11)
    node12 = Node(12)
    node13 = Node(13)
    node14 = Node(14)
    node15 = Node(15)
    # node17 = Node(17)
    node18 = Node(18)
    node19 = Node(19)
    node20 = Node(20)
    node21 = Node(21)
    node22 = Node(22)
    node23 = Node(23)
    node24 = Node(24)
    node25 = Node(25)

    node31 = Node(31)
    node33 = Node(33)

    rule_arr = [
        Rule(101, node3, [node1, node2]),
        Rule(102, node7, [node3, node2, node4]),
        Rule(103, node4, [node5, node6]),
        Rule(104, node3, [node8, node31]),
        Rule(105, node14, [node7, node9]),
        Rule(106, node9, [node4, node18, node11]),
        Rule(107, node11, [node12, node13]),
        Rule(108, node33, [node21, node15]),
        Rule(109, node19, [node13, node20, node24]),
        Rule(110, node14, [node9, node21]),
        Rule(111, node9, [node11, node25]),
        Rule(112, node21, [node25, node19]),
        Rule(113, node25, [node20, node13]),
        Rule(114, node12, [node22, node23]),
        Rule(115, node21, [node19, node24]),
    ]

    # Search(rule_arr).run(node14, [node5, node6, node2, node1, node18,
                                  #                               node22, node23, node7, node13])

    Search(rule_arr).run(node14, [node11, node20, node24, node12, node13])


if __name__ == "__main__":
    test_1()