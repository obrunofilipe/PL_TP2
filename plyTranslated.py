import ply.lex as lex

literals  = {'+', '-', '/', '*', '=', '(', ')'}          ## a single char
t_ignore  = " \t\n"
tokens    = ['VAR', 'NUMBER']


def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t.value


def t_NUMBER(t):  
    r'\d+(\.\d+)?'
    return float(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")


lex.lex()


import ply.yacc as yacc


precedence = [
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS'),
]


# symboltable : dictionary of variables
ts = { }


def p_stat_1(p):
    "stat : VAR '=' exp"
    ts[p[1]] = p[3]

def p_stat_2(p):
    "stat : exp "
    print(p[1])

def p_exp_1(p):
    "exp : exp '+' exp"
    p[0] = p[1] + p[3]


def p_exp_2(p):
    "exp : exp '-' exp"
    p[0] = p[1] - p[3]


def p_exp_3(p):
    "exp : exp '*' exp"
    p[0] = p[1] * p[3]



def p_exp_4(p):
    "exp : exp '/' exp"
    p[0] = p[1] / p[3]


def p_exp_5(p):
    "exp : '-' exp %prec UMINUS"
    p[0] = -p[2]


def p_exp_6(p):
    "exp : '(' exp ')'"             
    p[0] = p[2]


def p_exp_7(p):
    "exp : NUMBER"
    p[0] = p[1] 


def p_exp_8(p):
    "exp : VAR"                     
    p[0] = getval(p[1])


def p_error(t):
    print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")
    

def getval(n):
    if n not in ts: print(f"Undefined name '{n}'")
    return ts.get(n,0)


y = yacc.yacc()
y.parse("3+4*7")