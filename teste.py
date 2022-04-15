import ply.lex as lex
import ply.yacc as yacc
import re
import sys

tokens = ['REGEX', 'RETURN' , 'STRING']

literals = ['(',')',',']

def t_RETURN(t):
    r'return'
    print(t)

def t_REGEX(t):
    r"(r'.*)'"
    print(t)

def t_STRING(t):
    r"[^\(,)]+"
    print(t)


t_ignore = " \r\t\n"



def t_error(t):
    print("Illegal Character!")
    t.lexer.skip(1)


lexer = lex.lex()


def p_regra(p):
    "regra : REGEX RETURN '(' conteudo ')'"

def p_conteudo_vazio(p):
    "conteudo : "

def p_conteudo_elementos(p):
    "conteudo : elementos"

def p_elementos_elem(p):
    "elementos : STRING"

def p_elementos_varios(p):
    "elementos : conteudo ',' STRING"

def p_error(p):
    print("Syntax error!")


parser = yacc.yacc()

for line in sys.stdin:
    parser.parse(line)

#" return '(' conteudo ')' "
#"conteudo : elem "
#"conteudo : conteudo , elem"
#"elem : "