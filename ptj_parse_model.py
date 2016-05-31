class Program:
    def __init__(self, elem=None, program=None):

        if program is not None:
            self.elements = program.elements
        else:
            self.elements = []

        if elem is not None:
            self.elements.append(elem)


class Literal:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Identifier:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class AttributeRef:
    def __init__(self, left_val, right_val):
        self.left_val = left_val
        self.right_val = right_val


class UnaryExpression:
    def __init__(self, value, operator):
        self.value = value
        self.operator = operator


class BinaryExpression:
    def __init__(self, op1, operator, op2):
        self.op1 = op1
        self.op2 = op2
        self.operator = operator


class ConditionalExpression:
    def __init__(self, success, requirement, failure):
        self.success = success
        self.requirement = requirement
        self.failure = failure


class Call:
    def __init__(self, caller, arguments):
        self.caller = caller
        self.arguments = arguments


class Assignment:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression


class AugmentedAssignment:
    def __init__(self, target, operator, expression):
        self.target = target
        self.operator = operator
        self.expression = expression


class PassStmt:
    def __init__(self): pass


class PrintStmt:
    def __init__(self, arguments):
        self.arguments = arguments


class ReturnStmt:
    def __init__(self, expression=None):
        self.expression = expression


class BreakStmt:
    def __init__(self): pass


class ContinueStmt:
    def __init__(self): pass


class ImportStmt:
    def __init__(self, module_to_import):
        self.module = module_to_import


class StmtList:
    def __init__(self, first_statement=None):
        if first_statement is None:
            self.statement_list = []
        else:
            self.statement_list = [first_statement]

    def add_stmt(self, new_stmt):
        self.statement_list.append(new_stmt)


class IndentedStmtList:
    def __init__(self, first_statement=None):
        if first_statement is None:
            self.statement_list = []
        else:
            self.statement_list = [first_statement]

    def add_stmt(self, new_stmt):
        self.statement_list.append(new_stmt)


class WhileStmt:
    def __init__(self, condition, suite, else_suite=None):
        self.condition = condition
        self.suite = suite
        self.else_suite = else_suite


class IfStmt:
    def __init__(self, condition_suite_blocks, else_suite=None):
        self.blocks = condition_suite_blocks
        self.else_suite = else_suite


class FuncDef:
    def __init__(self, name, parameters, suite):
        self.name = name
        self.parameters = parameters
        self.suite = suite


class ClassDef:
    def __init__(self, name, parent, methods):
        self.name = name
        self.parent = parent
        self.methods = methods
