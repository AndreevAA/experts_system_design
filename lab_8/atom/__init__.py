class Atom:
    def __init__(self, name, terminals):
        self.name = name
        self.terminals = terminals

    def __str__(self):
        strterms = ""
        for term in self.terminals:
            strterms += str(term) + ", "
        return self.name + '(' + strterms.strip(", ") + ')'

    def __repr__(self):
        return self.__str__()
