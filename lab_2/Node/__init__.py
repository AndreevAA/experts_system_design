from Label import Label

class Node:
    def __init__(self, number: int, flag: int = Label.OPEN):
        self.number = number
        self.flag = flag

    def __str__(self):
        res = '' + f'{self.number}'
        return res

    def __repr__(self):
        res = '' + f'{self.number}'
        return res