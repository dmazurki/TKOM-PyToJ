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

    __repr__ = __str__


class Identifier:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    __repr__ = __str__


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


# class PositionalArguments:
#     def __init__(self, first_argument=None):
#         if first_argument is None:
#             self.argument_list = []
#         else:
#             self.argument_list = [first_argument]
#
#     def addArgument(self, new_arg):
#         self.argument_list.append(new_arg)
#
#     def __str__(self):
#         return ', '.join([str(x) for x in self.argument_list])


class Call:
    def __init__(self, caller, arguments):
        self.caller = caller
        self.arguments = arguments

    def __str__(self):
        return str(self.caller) + '(' + str(self.arguments) + ')'


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
        return 'print ' + str(self.arguments)


class ReturnStmt:
    def __init__(self, expression = None):
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

class ImportStmt:
    def __init__(self, module_to_import):
        self.module = module_to_import

    def __str__(self):
        return 'import ' + str(self.module)



class StmtList:
    def __init__(self, first_statement=None):
        if first_statement is None:
            self.statement_list = []
        else:
            self.statement_list = [first_statement]

    def addStmt(self, new_stmt):
        self.statement_list.append(new_stmt)

    def __str__(self):
        return ', '.join([str(x) for x in self.statement_list])


class IndentedStmtList:
    def __init__(self, first_statement=None):
        if first_statement is None:
            self.statement_list = []
        else:
            self.statement_list = [first_statement]

    def addStmt(self, new_stmt):
        self.statement_list.append(new_stmt)

    def __str__(self):
        return '\n<INDENT>\n' + '\n'.join([str(x) for x in self.statement_list]) + '\n<DEDENT>\n'


class WhileStmt:
    def __init__(self, condition, suite, else_suite=None):
        self.condition = condition
        self.suite = suite
        self.else_suite = else_suite

    def __str__(self):
        return 'while ' + str(self.condition) + ' : ' + str(self.suite) + (
            ' else: ' + str(self.else_suite) if self.else_suite is not None else ' ')


class IfStmt:
    def __init__(self, condition_suite_blocks, else_suite=None):
        self.blocks = condition_suite_blocks
        self.else_suite = else_suite

    def __str__(self):
        ret_value = ''

        for x in range(0, len(self.blocks)):
            if x == 0:
                ret_value += ('if ' + str(self.blocks[0][0]) + ':' + str(self.blocks[0][1]))
            else:
                ret_value += ('elif ' + str(self.blocks[x][0]) + ':' + str(self.blocks[x][1]))
            if self.else_suite is not None:
                ret_value += ('else ' + str(self.else_suite))
        return ret_value


class FuncDef:
    def __init__(self, name, parameters, suite):
        self.name = name
        self.parameters = parameters
        self.suite = suite

    def __str__(self):
        ret_value = 'def '
        ret_value += str(self.name) + '('
        ret_value += ', '.join([str(x) for x in self.parameters])
        ret_value += '):' + str(self.suite)
        return ret_value


class ClassDef:
    def __init__(self, name, parent, methods):
        self.name = name
        self.parent = parent
        self.methods = methods

    def __str__(self):
        ret_value = 'class '
        ret_value += str(self.name)
        if self.parent is not None:
            ret_value += '(' + str(self.parent) + ')'
        ret_value += ':'
        if self.methods.__class__ == PassStmt:
            ret_value += str(self.methods)
        else:
            ret_value += '\n' + '\n'.join([str(x) for x in self.methods])
        return ret_value
