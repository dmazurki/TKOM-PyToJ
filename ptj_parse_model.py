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


class AttributeRef:
    def __init__(self, left_val, right_val):
        self.left_val = left_val
        self.right_val = right_val

    def __str__(self):
        return "{0}.{1}".format(str(self.left_val), str(self.right_val))


class UnaryExpression:
    def __init__(self, value, operator):
        self.value = value
        self.operator = operator

    def __str__(self):
        return str(self.operator) + ' ' + str(self.value)


class BinaryExpression:
    def __init__(self, op1, operator, op2):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator

    def __str__(self):
        return str(self.op1) + ' ' + str(self.operator) + ' ' + str(self.op2)


class ConditionalExpression:
    def __init__(self, success, requirement, failure):
        self.success = success
        self.requirement = requirement
        self.failure = failure

    def __str__(self):
        return str(self.success) + ' if ' + str(self.requirement) + ' else ' + str(self.failure)


class PositionalArguments:
    def __init__(self, first_argument=None):
        if first_argument is None:
            self.argument_list = []
        else:
            self.argument_list = [first_argument]

    def addArgument(self, new_arg):
        self.argument_list.append(new_arg)

    def __str__(self):
        return str(self.argument_list)


class Call:
    def __init__(self, caller, arguments):
        self.caller = caller
        self.arguments = arguments

    def __str__(self):
        return str(self.caller) + '(' + ', '.join([str(x) for x in self.arguments.argument_list]) + ')'


class Assignment:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

    def __str__(self):
        return str(self.target) + ' = ' + str(self.expression)


class AugmentedAssignment:
    def __init__(self, target, operator, expression):
        self.target = target
        self.operator = operator
        self.expression = expression

    def __str__(self):
        return str(self.target) + ' ' + str(self.operator) + ' ' + str(self.expression)


class PassStmt:
    def __init__(self): pass

    def __str__(self):
        return 'pass'


class PrintStmt:
    def __init__(self, arguments):
        self.arguments = arguments

    def __str__(self):
        return 'print ' + ', '.join([str(x) for x in self.arguments.argument_list])


class ReturnStmt:
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return 'return ' + str(self.expression)


class BreakStmt:
    def __init__(self): pass

    def __str__(self):
        return 'break'


class ContinueStmt:
    def __init__(self): pass

    def __str__(self):
        return 'continue'