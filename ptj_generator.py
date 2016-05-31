import sys
import ptj_parse_model
import ptj_parse
import ptj_lex
import StringIO


class Generator:
    def __init__(self, output, get_type_from_name):
        self.output = output
        self.indent = 0
        self.java_code = ''
        self.class_fields = []
        self.names_in_scope = []
        self.current_class_fields = []
        self.class_reference_name = None
        self.get_type_from_name = get_type_from_name

    def generate_java_code(self, program=None):
        self.indent = 0
        self.java_code = StringIO.StringIO()
        for elem in program.elements:
            if elem.__class__ == ptj_parse_model.ClassDef:
                self.java_code.write(self.process_class_def(elem))
            elif elem.__class__ == ptj_parse_model.ImportStmt:
                self.java_code.write(self.process_import_stmt(elem))

        self.output.write(self.java_code.getvalue())

    def process_class_def(self, class_def):
        del self.class_fields[:]
        result = StringIO.StringIO()
        self.newline_and_indent(result)
        result.write('class ' + str(class_def.name))
        if class_def.parent is not None:
            result.write(' extends ' + str(class_def.parent) + '{')
        self.indent += 1

        methods = []
        for method_def in class_def.methods:
            methods.append(self.process_method_def(method_def))

        for field in self.class_fields:
            self.newline_and_indent(result)
            result.write('private Object ' + field + ';')

        for method_def in methods:
            result.write(method_def)

        self.indent -= 1
        self.newline_and_indent(result)
        result.write('}\n')
        return result.getvalue()

    def process_import_stmt(self, import_stmt):
        return 'import ' + str(import_stmt.module) + ';'

    # TODO init method / creating return stmt
    def process_method_def(self, method_def):
        self.names_in_scope.append([str(x) for x in method_def.parameters])
        self.class_reference_name = str(method_def.parameters[0])

        result = StringIO.StringIO()
        self.newline_and_indent(result)
        result.write('public Object ' + str(method_def.name) + '(' + ', '.join(
            ['Object ' + str(x) for x in method_def.parameters[1:]]) + ')')
        result.write(self.process_suite(method_def.suite))

        self.names_in_scope.pop()
        return result.getvalue()

    def process_statement(self, statement):
        result = StringIO.StringIO()
        if statement.__class__ == ptj_parse_model.Assignment:
            result.write(self.process_assignment(statement))
        elif statement.__class__ == ptj_parse_model.AugmentedAssignment:
            result.write(self.process_augmented_assignment(statement))
        elif statement.__class__ == ptj_parse_model.PassStmt:
            result.write('{}')
        elif statement.__class__ == ptj_parse_model.PrintStmt:
            result.write(self.process_print_stmt(statement))
        elif statement.__class__ == ptj_parse_model.ReturnStmt:
            result.write(self.process_return_stmt(statement))
        elif statement.__class__ == ptj_parse_model.BreakStmt:
            result.write('break')
        elif statement.__class__ == ptj_parse_model.ContinueStmt:
            result.write('continue')
        elif statement.__class__ == ptj_parse_model.StmtList:
            for statement in statement.statement_list:
                result.write(self.process_statement(statement) + ';')
            self.newline_and_indent(result)
        elif statement.__class__ == ptj_parse_model.WhileStmt:
            result.write(self.process_while_stmt(statement))
        elif statement.__class__ == ptj_parse_model.IfStmt:
            result.write(self.process_if_stmt(statement))
        elif statement.__class__ == ptj_parse_model.Call:
            result.write(self.process_call(statement))
        else:
            result.write('unknown_statement')
        return result.getvalue()

    def process_print_stmt(self, print_stmt):
        result = StringIO.StringIO()
        result.write('System.out.println(')
        if len(print_stmt.arguments) is not 0:
            result.write(self.process_expression(print_stmt.arguments[0], 'String'))
            for arg in print_stmt.arguments[1:]:
                result.write('+' + self.process_expression(arg, 'String'))
        result.write(')')
        return result.getvalue()

    def process_assignment(self, assignment):
        result = StringIO.StringIO()
        target = assignment.target
        if target.__class__ == ptj_parse_model.Identifier:
            if str(target) not in self.names_in_scope[-1]:
                result.write('Object ' + str(target) + '; ')
                self.names_in_scope[-1].append(str(target))
        elif target.__class__ == ptj_parse_model.AttributeRef:
            if str(target.left_val) == self.class_reference_name:
                field_name = target.right_val.__class__ == ptj_parse_model.Identifier and str(target.right_val) or str(
                    target.right_val.left_val)
                if str(field_name) not in self.class_fields: self.class_fields.append(str(field_name))

        result.write(self.process_expression(assignment.target))
        result.write(' = ')
        result.write(self.process_expression(assignment.expression))
        return result.getvalue()

    def process_augmented_assignment(self, aug_assignment):
        result = StringIO.StringIO()

        result.write(self.process_expression(aug_assignment.target))
        result.write(str(aug_assignment.operator))
        result.write(self.process_expression(aug_assignment.expression, 'double'))
        return result.getvalue()

    def process_return_stmt(self, return_stmt):
        result = StringIO.StringIO()
        result.write('return ')
        result.write(self.process_expression(return_stmt.expression))
        return result.getvalue()

    def process_expression(self, expression, casting=None):
        result = StringIO.StringIO()
        if expression.__class__ == ptj_parse_model.UnaryExpression:
            result.write(self.process_unary_expression(expression))
        elif expression.__class__ == ptj_parse_model.BinaryExpression:
            result.write(self.process_binary_expression(expression))
        elif expression.__class__ == ptj_parse_model.Literal:
            result.write(str(expression.value))
        elif expression.__class__ == ptj_parse_model.Identifier:
            result.write(self.process_identifier(expression, casting))
        elif expression.__class__ == ptj_parse_model.AttributeRef:
            pre_result = self.process_attribute_ref(expression)
            if casting is not None:
                pre_result = self.cast_attribute_ref(pre_result, casting)
            result.write(pre_result)
        elif expression.__class__ == ptj_parse_model.Call:
            result.write(self.process_call(expression, casting))
        else:
            result.write('unknown_expression:' + str(expression.__class__))

        return result.getvalue()

    def process_identifier(self, identifier, casting):

        text = identifier.value

        if text == 'True':
            text = 'true'
        elif text == 'False':
            text = 'false'
        elif text == 'None':
            text =  'null'

        if text == self.class_reference_name:
            text = 'this'
        if casting is not None:
            if self.get_type_from_name is True and text.find('_') is not -1:
                casting_type = text[text.rfind('_') + 1:]
                return '(' + casting_type + ')' + text
            else:
                return '(' + str(casting) + ')' + text

        return text

    def process_call(self, call, casting = None):
        done, value = self.pre_process_call(call)

        if done:
            return value

        result = StringIO.StringIO()
        caller = self.process_expression(call.caller)
        dot_pos = caller.rfind('.')
        underscore_pos = caller.rfind('_')

        if casting is not None:
            if self.get_type_from_name is True and underscore_pos > dot_pos:
                cast_type = caller[underscore_pos + 1:]
                result.write('(' + cast_type + ')')
            elif casting is not '':
                result.write('(' + str(casting) + ')')

        if dot_pos is not -1:
            caller_obj = caller[:dot_pos]
            caller_func = caller[dot_pos + 1:]

            if self.get_type_from_name and caller_obj.rfind('_') is not -1:
                casting_pos = caller_obj.rfind('_')
                cast = caller_obj[casting_pos + 1:]
                result.write('((' + cast + ')' + caller_obj + ').' + caller_func)
                result.write(self.process_param_list(call.arguments))
            else:
                result.write(caller_obj + '.' + 'getClass().getMethod("' + caller_func + '"')
                for x in range(0, len(call.arguments)):
                    result.write(', Object')
                result.write(').invoke')
                invoke_arguments = [ptj_parse_model.Identifier(caller_obj)] + call.arguments
                result.write(self.process_param_list(invoke_arguments))
        else:
            result.write(caller + self.process_param_list(call.arguments))

        return result.getvalue()

    def pre_process_call(self, call):
        caller = self.process_expression(call.caller)
        if caller == 'str' and len(call.arguments) == 1:
            object_calling = call.arguments[0]
            java_fc_name = ptj_parse_model.Identifier('toString')
            caller = ptj_parse_model.AttributeRef(object_calling, java_fc_name)
            call.caller = caller
            call.arguments = []
            return False, None
        elif caller == 'raw_input':
            return True, 'new Scanner(System.in).next()'

        return False, None

    def process_param_list(self, param_list):
        result = StringIO.StringIO()
        result.write('(')
        if len(param_list) is not 0:
            result.write(self.process_expression(param_list[0]))
            for arg in param_list[1:]:
                result.write(', ' + self.process_expression(arg))
        result.write(')')
        return result.getvalue()

    def process_attribute_ref(self, attribute_ref):
        result = StringIO.StringIO()
        result.write(self.process_expression(attribute_ref.left_val))
        result.write('.')
        result.write(self.process_expression(attribute_ref.right_val))
        return result.getvalue()

    def cast_attribute_ref(self, java_code, casting):
        dot_pos = java_code.rfind('.')
        underscore_pos = java_code.rfind('_')
        if self.get_type_from_name is True and underscore_pos > dot_pos:
            cast_type = java_code[underscore_pos + 1:]
            return '(' + cast_type + ')' + java_code
        elif casting is not '':
            return '(' + str(casting) + ')' + java_code
        else:
            return java_code

    def process_unary_expression(self, unary_expr):
        result = StringIO.StringIO()
        operator_str = str(unary_expr.operator)
        result.write(operator_str)
        result.write(self.process_expression(unary_expr.value, 'double'))
        return result.getvalue()

    def process_binary_expression(self, binary_expression):
        result = StringIO.StringIO()
        operator_str = str(binary_expression.operator)
        casting = None
        if operator_str in ['+', '-', '*', '/', '%', '<', '>']:
            casting = 'double'
        else:
            casting = 'Object'

        if operator_str == 'is not':
            operator_str = '!='
        elif operator_str == '<>':
            operator_str = '!='
        elif operator_str == 'is':
            operator_str = '=='
        elif operator_str == 'and':
            operator_str = '&&'
        elif operator_str == 'or':
            operator_str = '||'

        result.write(self.process_expression(binary_expression.op1, casting))
        result.write(' ' + operator_str + ' ')
        result.write(self.process_expression(binary_expression.op2, casting))
        return result.getvalue()

    def process_while_stmt(self, while_stmt):
        result = StringIO.StringIO()
        result.write('while(true)')
        while_stmt.else_suite.add_stmt(ptj_parse_model.StmtList(ptj_parse_model.BreakStmt()))
        internal = ptj_parse_model.IfStmt([[while_stmt.condition, while_stmt.suite]], while_stmt.else_suite)
        suite = ptj_parse_model.IndentedStmtList(internal)
        result.write(self.process_suite(suite))
        return result.getvalue()

    def process_if_stmt(self, if_stmt):
        result = StringIO.StringIO()

        result.write('if(')
        result.write(self.process_expression(if_stmt.blocks[0][0]))
        result.write(')')
        result.write(self.process_suite(if_stmt.blocks[0][1]))

        for index in range(1, len(if_stmt.blocks)):
            result.write('else if(')
            result.write(self.process_expression(if_stmt.blocks[index][0]))
            result.write(')')
            result.write(self.process_suite(if_stmt.blocks[index][1]))

        if if_stmt.else_suite is not None:
            result.write('else')
            result.write(self.process_suite(if_stmt.else_suite))

        return result.getvalue()

    def process_suite(self, suite):
        result = StringIO.StringIO()
        result.write('{')
        if suite.__class__ == ptj_parse_model.IndentedStmtList:
            self.indent += 1
            self.newline_and_indent(result)
            for statement in suite.statement_list:
                result.write(self.process_statement(statement))
            self.indent -= 1
            result.write('}')
            self.newline_and_indent(result)
        elif suite.__class__ == ptj_parse_model.StmtList:
            for statement in suite.statement_list:
                result.write(self.process_statement(statement) + ';')
            result.write('}')
        return result.getvalue()

    def newline_and_indent(self, destination):
        destination.write('\n' + " " * self.indent)


if __name__ == "__main__":
    # f = open('test_code')
    # ptj_lex.ptj_lexer.input(f.read())
    # for token in ptj_lex.ptj_lexer:
    #     print str(token)
    p = ptj_parse.generateProgram('test_code')
    g = Generator(sys.stdout, True)
    g.generate_java_code(p)
