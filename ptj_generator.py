import sys
import ptj_parse_model
import ptj_parse
import StringIO


class Generator:
    def __init__(self, output):
        self.output = output
        self.indent = 0
        self.java_code = ''
        self.class_fields = []
        self.names_in_scope = []
        self.current_class_fields = []
        self.class_reference_name = None
        self.get_type_from_name = True

    def generateJavaCode(self, program=None):
        self.indent = 0
        self.java_code = StringIO.StringIO()
        for elem in program.elements:
            if elem.__class__ == ptj_parse_model.ClassDef:
                self.java_code.write(self.processClassDef(elem))
            elif elem.__class__ == ptj_parse_model.ImportStmt:
                self.java_code.write(self.processImportStmt(elem))

        self.output.write(self.java_code.getvalue())

    def processClassDef(self, class_def):
        del self.class_fields[:]
        result = StringIO.StringIO()
        self.newlineAndIndent(result)
        result.write('class ' + str(class_def.name))
        if class_def.parent is not None:
            result.write(' extends ' + str(class_def.parent) + '{')
        self.indent += 1

        methods = []
        for method_def in class_def.methods:
            methods.append(self.processMethodDef(method_def))

        for field in self.class_fields:
            self.newlineAndIndent(result)
            result.write('private Object ' + field + ';')

        for method_def in methods:
            result.write(method_def)

        self.indent -= 1
        self.newlineAndIndent(result)
        result.write('}')
        return result.getvalue()

    def processImportStmt(self, import_stmt):
        return 'import ' + import_stmt.module + ';'

    def processMethodDef(self, method_def):
        self.names_in_scope.append([str(x) for x in method_def.parameters])
        self.class_reference_name = str(method_def.parameters[0])

        result = StringIO.StringIO()
        self.newlineAndIndent(result)
        result.write('public Object ' + str(method_def.name) + '(' + ', '.join(
            ['Object ' + str(x) for x in method_def.parameters]) + ')')
        result.write(self.processSuite(method_def.suite))

        self.names_in_scope.pop()
        return result.getvalue()

    def processStatement(self, statement):
        result = StringIO.StringIO()
        if statement.__class__ == ptj_parse_model.Assignment:
            result.write(self.processAssignment(statement))
        elif statement.__class__ == ptj_parse_model.AugmentedAssignment:
            pass
        elif statement.__class__ == ptj_parse_model.PassStmt:
            result.write('{}')
        elif statement.__class__ == ptj_parse_model.PrintStmt:
            result.write(self.processPrintStmt(statement))
        elif statement.__class__ == ptj_parse_model.ReturnStmt:
            result.write(self.processReturnStmt(statement))
        elif statement.__class__ == ptj_parse_model.BreakStmt:
            result.write('break')
        elif statement.__class__ == ptj_parse_model.ContinueStmt:
            pass
        elif statement.__class__ == ptj_parse_model.StmtList:
            for statement in statement.statement_list:
                result.write(self.processStatement(statement) + ';')
            self.newlineAndIndent(result)
        elif statement.__class__ == ptj_parse_model.WhileStmt:
            result.write(self.processWhileStmt(statement))
        elif statement.__class__ == ptj_parse_model.IfStmt:
            result.write(self.processIfStmt(statement))
        else:
            result.write('unknown_statement')
        return result.getvalue()

    def processPrintStmt(self, print_stmt):
        result = StringIO.StringIO()
        result.write('System.out.println(')
        if len(print_stmt.arguments) is not 0:
            result.write('(String)' + self.processExpression(print_stmt.arguments[0]))
            for arg in print_stmt.arguments[1:]:
                result.write('+(String)' + self.processExpression(arg))
        result.write(')')
        return result.getvalue()

    def processAssignment(self, assignment):
        result = StringIO.StringIO()
        target = assignment.target
        if target.__class__ == ptj_parse_model.Identifier:
            if str(target) not in self.names_in_scope[-1]:
                result.write('Object ' + str(target) + '; ')
                self.names_in_scope.append(str(target))
        elif target.__class__ == ptj_parse_model.AttributeRef:
            if str(target.left_val) == self.class_reference_name:
                field_name = target.right_val.__class__ == ptj_parse_model.Identifier and str(target.right_val) or str(
                    target.right_val.left_val)
                if str(field_name) not in self.class_fields: self.class_fields.append(str(field_name))

        result.write(self.processExpression(assignment.target))
        result.write(' = ')
        result.write(self.processExpression(assignment.expression))
        return result.getvalue()

    def processReturnStmt(self, return_stmt):
        result = StringIO.StringIO()
        result.write('return ')
        result.write(self.processExpression(return_stmt.expression))
        return result.getvalue()

    def processExpression(self, expression):
        result = StringIO.StringIO()
        if expression.__class__ == ptj_parse_model.BinaryExpression:
            result.write(self.processBinaryExpression(expression))
        elif expression.__class__ == ptj_parse_model.Literal:
            result.write(str(expression.value))
        elif expression.__class__ == ptj_parse_model.Identifier:
            result.write(self.processIdentifier(expression))
        elif expression.__class__ == ptj_parse_model.AttributeRef:
            result.write(self.processAttributeRef(expression))
        elif expression.__class__ == ptj_parse_model.Call:
            result.write(self.processCall(expression))
        else:
            result.write('unknown_expression:' + str(expression.__class__))
        return result.getvalue()

    def processIdentifier(self, identifier):
        text = identifier.value
        if text == 'True':
            return 'true'
        elif text == 'False':
            return 'false'
        elif text == 'None':
            return 'null'
        else:
            return text

    def processCall(self, call):
        result = StringIO.StringIO()
        caller = self.processExpression(call.caller)
        dot_pos = caller.rfind('.')
        if dot_pos is not -1:
            caller_obj = caller[:dot_pos]
            caller_func = caller[dot_pos + 1:]

            if self.get_type_from_name and caller_obj.rfind('_') is not -1:
                casting_pos = caller_obj.rfind('_')
                cast = caller_obj[casting_pos + 1:]
                result.write('((' + cast + ')' + caller_obj + ').' + caller_func)
                result.write(self.processParamList(call.arguments))
            else:
                result.write(caller_obj + '.' + 'getClass().getMethod("' + caller_func + '"')
                for x in range(0, len(call.arguments)):
                    result.write(', Object')
                result.write(').invoke')
                invoke_arguments = [ptj_parse_model.Identifier(caller_obj)] + call.arguments
                result.write(self.processParamList(invoke_arguments))
        else:
            result.write(caller + self.processParamList(call.arguments))

        return result.getvalue()

    def processParamList(self, param_list):
        result = StringIO.StringIO()
        result.write('(')
        if len(param_list) is not 0:
            result.write(self.processExpression(param_list[0]))
            for arg in param_list[1:]:
                result.write(', ' + self.processExpression(arg))
        result.write(')')
        return result.getvalue()

    def processAttributeRef(self, attribute_ref):
        result = StringIO.StringIO()
        result.write(str(attribute_ref.left_val))
        result.write('.')
        result.write(self.processExpression(attribute_ref.right_val))
        return result.getvalue()

    def processBinaryExpression(self, binary_expression):
        result = StringIO.StringIO()
        result.write(self.processExpression(binary_expression.op1))
        result.write(' ' + str(binary_expression.operator) + ' ')
        result.write(self.processExpression(binary_expression.op2))
        return result.getvalue()

    def processWhileStmt(self, while_stmt):
        result = StringIO.StringIO()
        print str(self.names_in_scope)
        result.write('while(true)')
        internal = ptj_parse_model.IfStmt([[while_stmt.condition, while_stmt.suite]], while_stmt.else_suite)
        suite = ptj_parse_model.IndentedStmtList(internal)
        result.write(self.processSuite(suite))
        return result.getvalue()

    def processIfStmt(self, if_stmt):
        result = StringIO.StringIO()

        result.write('if(')
        result.write(self.processExpression(if_stmt.blocks[0][0]))
        result.write(')')
        result.write(self.processSuite(if_stmt.blocks[0][1]))

        for index in range(1, len(if_stmt.blocks)):
            result.write('else if(')
            result.write(self.processExpression(if_stmt.blocks[index][0]))
            result.write(')')
            result.write(self.processSuite(if_stmt.blocks[index][1]))

        if if_stmt.else_suite is not None:
            result.write('else')
            result.write(self.processSuite(if_stmt.else_suite))

        return result.getvalue()

    def processSuite(self, suite):
        result = StringIO.StringIO()
        result.write('{')
        if suite.__class__ == ptj_parse_model.IndentedStmtList:
            self.indent += 1
            self.newlineAndIndent(result)
            for statement in suite.statement_list:
                result.write(self.processStatement(statement))
            self.indent -= 1
            result.write('}')
            self.newlineAndIndent(result)
        elif suite.__class__ == ptj_parse_model.StmtList:
            for statement in suite.statement_list:
                result.write(self.processStatement(statement) + ';')
            result.write('}')
        return result.getvalue()

    def newlineAndIndent(self, destination):
        destination.write('\n' + " " * self.indent)


if __name__ == "__main__":
    program = ptj_parse.generateProgram('test_code')
    g = Generator(sys.stdout)
    g.generateJavaCode(program)
