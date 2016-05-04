import unittest
import ptj_lex


class IndentTest(unittest.TestCase):
    def testIndent(self):
        code_to_test = '''\
        x
          x
           x
        x
             x
        x\
        '''
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.type for tok in ptj_lex.ptj_lexer if tok.type == 'INDENT' or tok.type == 'DEDENT']
        expected_tokens = ['INDENT', 'INDENT', 'DEDENT', 'DEDENT', 'INDENT', 'DEDENT']
        self.assertListEqual(tokens, expected_tokens, 'Wrong indenting sequence!')

    def tearDown(self):
        ptj_lex.resetLexer()


class LiteralTest(unittest.TestCase):
    def tearDown(self):
        ptj_lex.resetLexer()

    def testStringLiteral(self):
        code_to_test = '''
        "x\a"'''
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'STRING_LITERAL']
        expected_tokens = ['"x\a"']
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))

    def testIntegerLiteral(self):
        code_to_test = '0 01 19940'
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'INTEGER_LITERAL']
        expected_tokens = ['0', '01', '19940']
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))

    def testFloatingPointLiteral(self):
        code_to_test = '.12 12.12 12. 10e10 10e-10 1.e01 00.00e00'
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'FLOATING_POINT_LITERAL']
        expected_tokens = code_to_test.split()
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))
