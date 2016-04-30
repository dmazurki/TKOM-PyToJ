import ply.lex as lex

keywords = (
    'and',
    'break',
    'class',
    'continue',
    'def',
    'elif',
    'else',
    'for',
    'from',
    'import',
    'if',
    'is',
    'not',
    'or',
    'pass',
    'print',
    'return',
    'while'
)
tokens = keywords + (
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
)


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t


indentStack = [0]


def t_NEWLINE(t):
    r'\n[ ]*'
    indentLength = len(t.value) - 1
    lastIndent = indentStack[-1]

    if indentLength > lastIndent:
        indentStack.append(indentLength)
        t.type = "INDENT"
    elif indentLength < lastIndent:
        while indentStack[-1] > indentLength: indentStack.pop()
        t.type = "DEDENT"
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
pointfloat = r'((([0-9]*\.[0-9]+)|([0-9]*\.))' + exponent + '?)'
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
    del indentStack[1:]


lexer = lex.lex()
