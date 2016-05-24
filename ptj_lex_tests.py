import unittest
import ptj_lex


class IndentTest(unittest.TestCase):
    def testIndent(self):
        # given
        code_to_test = '''\
        line
          line
           line
        line
             line
        line\
        '''
        expected_tokens = ['INDENT', 'INDENT', 'DEDENT', 'DEDENT', 'INDENT', 'DEDENT']
        # when
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.type for tok in ptj_lex.ptj_lexer if tok.type == 'INDENT' or tok.type == 'DEDENT']
        # then
        self.assertListEqual(tokens, expected_tokens, 'Wrong indenting sequence!')


class LiteralTest(unittest.TestCase):
    def testStringLiteral(self):
        # given
        code = '"text" "a"x"b"'
        expected_tokens = ['"text"', '"a"', '"b"']
        # when
        ptj_lex.ptj_lexer.input(code)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'STRING_LITERAL']
        # then
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))

    def testIntegerLiteral(self):
        # given
        code_to_test = '0 01 19940'
        expected_tokens = ['0', '01', '19940']
        # when
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'INTEGER_LITERAL']
        # then
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))

    def testFloatingPointLiteral(self):
        # given
        code_to_test = '.12 12.12 12. 10e10 10e-10 1.e01 00.00e00'
        expected_tokens = code_to_test.split()
        # when
        ptj_lex.ptj_lexer.input(code_to_test)
        tokens = [tok.value for tok in ptj_lex.ptj_lexer if tok.type == 'FLOATING_POINT_LITERAL']
        # then
        self.assertListEqual(tokens, expected_tokens,
                             'Wrong token list! ' + str(tokens) + ' expected: ' + str(expected_tokens))


if __name__ == '__main__':
    unittest.main()
