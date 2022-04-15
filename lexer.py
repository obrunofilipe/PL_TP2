import ply.lex as lex 
import re


tokens = ['LITERALS', 'IGNORE', 'TOKENS', 'RETURN', 'ERROR']

literals = {'=', '(', ')'}

t_LITERALS = r"literals"
t_IGNORE = r"ignore"
t_TOKENS = r"tokens"
t_RETURN = r"return"
t_ERROR = r"error"

t_ignore = " \t\n\r"


def t_error(t):
    print("Illegal character!")


import ply.yacc as yacc


def p_listchar(p):
    "termo : termo '=' listchar"
    result = "{"
    i = 0
    for c in p:
        if i == length(p[3]) - 1:
            result + "'" + c + "'" + ','
    result = result



parser = yacc.yacc()

