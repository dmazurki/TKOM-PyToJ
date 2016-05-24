# author: Damian Mazurkiewicz
# date: 07.05.2016

import ply.lex as lex

# Wrapper for lex.Lexer() object. It contains token
# definitions and logic for Python indentation handling.
class PtjLexer:
    keywords = {
        'and': 'AND',
        'break': 'BREAK',
        'class': 'CLASS',
        'continue': 'CONTINUE',
        'def': 'DEF',
        'elif': 'ELIF',
        'else': 'ELSE',
        'from': 'FROM',
        'import': 'IMPORT',
        'if': 'IF',
        'is': 'IS',
        'not': 'NOT',
        'or': 'OR',
        'pass': 'PASS',
        'print': 'PRINT',
        'return': 'RETURN',
        'while': 'WHILE'
    }
    tokens = keywords.values() + [
        'IDENTIFIER',
        'NEWLINE',
        'INDENT',
        'DEDENT',
        'STRING_LITERAL',
        'INTEGER_LITERAL',
        'FLOATING_POINT_LITERAL',

        # Operators
        'PLUS',
        'LT',
        'MINUS',
        'GT',
        'LTE',
        'GTE',
        'ASTERISK',
        'SLASH',
        'EQ',
        'NE',
        'PERCENT',

        # Delimiters
        'OPEN_PARENTHESIS',
        'CLOSE_PARENTHESIS',
        'COMA',
        'DOT',
        'COLON',
        'SEMICOLON',
        'ASSIGNMENT',
        'PLUS_ASSIGNMENT',
        'MINUS_ASSIGNMENT',
        'ASTERISK_ASSIGNMENT',
        'SLASH_ASSIGNMENT',
        'PERCENT_ASSIGNMENT'
    ]

    def t_IDENTIFIER(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.keywords.get(t.value, 'IDENTIFIER')
        return t

    def t_NEWLINE(self, t):
        r'\n+[ ]*'
        indentation_start = t.value.find(' ')
        indentation_length = indentation_start is not -1 and len(t.value[indentation_start:]) or 0
        # update line number
        t.lexer.lineno += len(t.value) - indentation_length

        last_indent = self.indent_stack[-1]
        if indentation_length > last_indent:
            self.indent_stack.append(indentation_length)
            t.type = "INDENT"
        elif indentation_length < last_indent:
            dedent_quantity = 0
            while self.indent_stack[-1] > indentation_length:
                dedent_quantity += 1
                self.indent_stack.pop()
            t.type = "DEDENT"
            t.quantity = dedent_quantity
        else:
            t.type = "NEWLINE"

        return t

    # Regular expressions for string literals.
    escapeseq = r'\\.'
    stringchar = r'([^\\"\n])'
    stringitem = r'(' + stringchar + '|' + escapeseq + ')'
    stringliteral = r'"(' + stringitem + ')*"'

    @lex.TOKEN(stringliteral)
    def t_STRING_LITERAL(self, t):
        return t

    t_INTEGER_LITERAL = r'([0-9]+)'

    exponent = r'((e|E)[+-]?[0-9]+)'
    pointfloat = r'((([0-9]*\.[0-9]+)|([0-9]+\.))' + exponent + '?)'
    exponentfloat = r'(([0-9]+)' + exponent + ')'
    floatnumber = r'' + pointfloat + '|' + exponentfloat

    @lex.TOKEN(floatnumber)
    def t_FLOATING_POINT_LITERAL(self, t):
        return t

    t_PLUS = r'\+'
    t_LT = r'<'
    t_MINUS = r'-'
    t_GT = r'>'
    t_LTE = r'<='
    t_GTE = r'>='
    t_ASTERISK = r'\*'
    t_SLASH = r'/'
    t_EQ = r'=='
    t_NE = r'<>|!='
    t_PERCENT = r'%'

    t_OPEN_PARENTHESIS = r'\('
    t_CLOSE_PARENTHESIS = r'\)'
    t_COMA = r'\,'
    t_DOT = r'\.'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_ASSIGNMENT = r'='
    t_PLUS_ASSIGNMENT = r'\+='
    t_MINUS_ASSIGNMENT = r'-='
    t_ASTERISK_ASSIGNMENT = r'\*='
    t_SLASH_ASSIGNMENT = r'/='
    t_PERCENT_ASSIGNMENT = r'%'

    def t_error(self, t):
        print("Illegal character %s" % t.value[0])
        t.lexer.skip(1)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.indentation = None
        self.indent_stack = [0]

    def token(self):
        if self.indentation is not None:
            ret = self.indentation
            if self.indentation.type == 'DEDENT':
                self.indentation.quantity -= 1
                if self.indentation.quantity == 0:
                    self.indentation = None
            else:
                self.indentation = None
            return ret

        tok = self.lexer.token()
        if tok is None:
            return tok

        if tok.type == 'INDENT' or tok.type == 'DEDENT':
            newtok = lex.LexToken()
            newtok.value = tok.value
            newtok.type = tok.type
            newtok.lineno = tok.lineno
            newtok.lexpos = tok.lexpos
            self.indentation = newtok
            if self.indentation.type == 'DEDENT': self.indentation.quantity = tok.quantity

            tok.type = 'NEWLINE'
            tok.value = '\n'

        return tok

    def input(self, code):
        self.indent_stack = [0]
        self.lexer.input(code)

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

ptj_lexer = PtjLexer()

