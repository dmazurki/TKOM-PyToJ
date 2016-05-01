import ply.yacc as yacc
from ptj_lex import tokens
import ptj_parse_model

start = 'program'

def p_program(p):
    """program : NEWLINE
               | primary
               | program primary
               | program NEWLINE"""
    if len(p) == 2 and p[1] != '\n':
        p[0] = ptj_parse_model.Program(p[1])
    elif len(p) == 2:
        p[0] = ptj_parse_model.Program()
    elif len(p) == 3 and p[2] != '\n':
        p[0] = ptj_parse_model.Program(program=p[1], elem=p[2])
    else:
        p[0] = ptj_parse_model.Program(program=p[1])

def p_literal(p):
    """literal : STRING_LITERAL
               | INTEGER_LITERAL
               | FLOATING_POINT_LITERAL"""
    p[0] = ptj_parse_model.Literal(p[1])

def p_identifier(p):
    """identifier : IDENTIFIER"""
    p[0] = ptj_parse_model.Identifier(p[1])

def p_atom(p):
    """atom : identifier
            | literal"""
    p[0] = ptj_parse_model.Atom(p[1])

#TODO add call!
def p_primary(p):
    """primary : atom
               | attributeref"""
    p[0] = ptj_parse_model.Primary(p[1])

def p_attributeref(p):
    """attributeref : primary DOT identifier"""
    p[0] = ptj_parse_model.AttributeRef(p[1], p[3])


def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")
parser = yacc.yacc()


if __name__ == '__main__':
    code = open('test_code')
    result = parser.parse(code.read())
    print str(result)

