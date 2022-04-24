import re
import ply.lex as lex
import ply.yacc as yacc

def split(word):
    return [char for char in word]

def listToString(list):
    ret = ""
    i = 0
    for elem in list:
        if i == 0:
            ret = ret + elem + "\"" + ", "
        if i != len(list)-1:
            ret = ret + "\"" + elem + "\"" + ", "
        elif i == len(list)-1:
            ret = ret + "\"" + elem
        i += 1
    return ret

literals = {'[',']',','}

tokens = ["LEXER","LITERALS","IGNORE","TOKENS","EXPREG","STRING","COMMENT","NEWLINE","RETURN","ERROR","TOKEN","CODIGO", "ATRIB"]

states = [
    ("lexer", "exclusive"),
    ("tokens", "exclusive"),
    ("regex", "exclusive")
]


#tokens

def t_tokens_ATRIB(t):
    r'='
    return t

def t_tokens_TOKEN(t):
    r'\'[^\']+\''
    return t

def t_tokens_NEWLINE(t):
    r'\n'
    lexer.pop_state()


#regex

def t_regex_CODIGO(t):
    r'[^\n]+'
    lexer.pop_state()
    return t


#lexer

def t_lexer_ATRIB(t):
    r'='
    return t

def t_lexer_STRING(t):
    r'"[^"]*"'
    return t

def t_lexer_LITERALS(t):
    r'%literals'
    return t

def t_lexer_IGNORE(t):
    r'%ignore'
    return t

def t_lexer_TOKENS(t):
    r'%tokens'
    lexer.push_state("tokens")
    return t

def t_lexer_COMMENT(t):
    "\#\#[^\n]+$"
    return t

def t_lexer_EXPREG(t):
    r'(\\\s|\S)+'
    lexer.push_state("regex")
    return t

#INITIAL

def t_LEXER(t):
    r'LEX'
    lexer.push_state("lexer")
    return t

#ignore
t_tokens_ignore = " \t\r"
t_regex_ignore = " \n\t\r"
t_lexer_ignore = " \n\t\r"
t_ignore = " \n\t\r"

#error

def t_ANY_error(t):
    print("Illegal character!", t.value[0])


lexer = lex.lex()


def p_ficheiro(p):
    "ficheiro : lex"

def p_lex(p):
    "lex : LEXER conteudolex"

def p_conteudolex(p):
    "conteudolex : comandos regras"

def p_comandos_vazio(p):
    "comandos : "

def p_comandos_lista(p):
    "comandos : comando comandos"

def p_comando_literals(p):
    "comando : LITERALS ATRIB STRING"

def p_comando_ignore(p):
    "comando : IGNORE ATRIB STRING"

def p_comando_tokens(p):
    "comando : TOKENS ATRIB listatok"

def p_listatok(p):
    "listatok : '[' conteudo ']'"
    
def p_conteudo_vazio(p):
    "conteudo : "
    
def p_conteudo_lista(p):
    "conteudo : tokens"

def p_tokens_token(p):
    "tokens : TOKEN"
    
def p_tokens_lista(p):
    "tokens : TOKEN ',' tokens"


def p_regras_vazio(p):
    "regras : "
    
def p_regras_lista(p):
    "regras : regra regras"

def p_regra(p):
    "regra : EXPREG acao"


def p_acao(p):
    "acao : CODIGO"


def p_error(p):
    print("Syntax Error in:", p.value)


parser = yacc.yacc()

f = open("test.txt")

content = f.read()

parser.parse(content)
