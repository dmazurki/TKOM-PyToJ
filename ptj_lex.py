import ply.lex as lex

keywords = {
    'and': 'AND',
    'break': 'BREAK',
    'class': 'CLASS',
    'continue': 'CONTINUE',
    'def': 'DEF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'for': 'FOR',
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
    'OPEN_CURLY_BRACKET',
    'CLOSE_CURLY_BRACKET',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'COMA',
    'DOT',
    'COLON',
    'SEMICOLON',
    'HASH',
    'APOSTROPHE',
    'QUOTATION_MARKS',
    'BACKSLASH',
    'ASSIGNMENT',
    'PLUS_ASSIGNMENT',
    'MINUS_ASSIGNMENT',
    'ASTERISK_ASSIGNMENT',
    'SLASH_ASSIGNMENT',
    'PERCENT_ASSIGNMENT'
]


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t


indent_stack = [0]


def t_NEWLINE(t):
    r'\n+[ ]*'
    indentation_start = t.value.find(' ')
    indentation_length = indentation_start is not -1 and len(t.value[indentation_start:]) or 0
    last_indent = indent_stack[-1]
    if indentation_length > last_indent:
        indent_stack.append(indentation_length)
        t.type = "INDENT"
    elif indentation_length < last_indent:
        dedent_quantity = 0
        while indent_stack[-1] > indentation_length:
            dedent_quantity += 1
            indent_stack.pop()
        t.type = "DEDENT"
        t.quantity = dedent_quantity
    else:
        t.type = "NEWLINE"

    return t


escapeseq = r'\\.'
shortstringchar_ap = r'([^\\\n\'])'
shortstringitem_ap = r'(' + shortstringchar_ap + '|' + escapeseq + ')'
shortstring_ap = r'\'(' + shortstringitem_ap + ')*\''
shortstringchar_qu = r'([^\\\n"])'
shortstringitem_qu = r'(' + shortstringchar_qu + '|' + escapeseq + ')'
shortstring_qu = r'"(' + shortstringitem_qu + ')*"'
stringliteral = r'(' + shortstring_ap + '|' + shortstring_qu + ')'


@lex.TOKEN(stringliteral)
def t_STRING_LITERAL(t):
    return t


t_INTEGER_LITERAL = r'([0-9]+)'

exponent = r'((e|E)[+-]?[0-9]+)'
pointfloat = r'((([0-9]*\.[0-9]+)|([0-9]+\.))' + exponent + '?)'
exponentfloat = r'(([0-9]+)' + exponent + ')'
floatnumber = r'' + pointfloat + '|' + exponentfloat


@lex.TOKEN(floatnumber)
def t_FLOATING_POINT_LITERAL(t):
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
t_OPEN_CURLY_BRACKET = r'\{'
t_CLOSE_CURLY_BRACKET = r'\}'
t_OPEN_BRACKET = r'\['
t_CLOSE_BRACKET = r'\]'
t_COMA = r'\,'
t_DOT = r'\.'
t_COLON = r':'
t_SEMICOLON = r';'
t_HASH = r'\#'
t_APOSTROPHE = r'\''
t_QUOTATION_MARKS = r'\"'
t_BACKSLASH = r'\\'
t_ASSIGNMENT = r'='
t_PLUS_ASSIGNMENT = r'\+='
t_MINUS_ASSIGNMENT = r'-='
t_ASTERISK_ASSIGNMENT = r'\*='
t_SLASH_ASSIGNMENT = r'/='
t_PERCENT_ASSIGNMENT = r'%'


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def resetLexer():
    del indent_stack[1:]


class PtjLexer:
    def __init__(self):
        self.lexer = lex.lex()
        self.indentation = None

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
        self.lexer.input(code)

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t


ptj_lexer = PtjLexer()

if __name__ == '__main__':
    code = open('test_code')
    ptj_lexer.input(code.read())
    for tok in ptj_lexer:
        print str(tok)
