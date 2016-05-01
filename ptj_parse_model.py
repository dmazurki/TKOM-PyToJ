class Program:
    def __init__(self, elem=None, program=None):

        if program is not None:
            self.elements = program.elements
        else:
            self.elements = []

        if elem is not None:
            self.elements.append(elem)

    def __str__(self):
        return "\n".join([str(x) for x in self.elements])


class Atom:
    def __init__(self, arg):
        self.value = arg

    def __str__(self):
        return str(self.value)


class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Identifier:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Primary:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class AttributeRef:
    def __init__(self, left_val, right_val):
        self.left_val = left_val
        self.right_val = right_val

    def __str__(self):
        return "{0}.{1}".format(str(self.left_val), str(self.right_val))
