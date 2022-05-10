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

literals = {'[',']',',','='}

tokens = ["LEXER","YACC","LITERALS","IGNORE","TOKENS","EXPREG","STRING","COMMENT","NEWLINE",
          "RETURN","ERROR","TOKEN","ATRIB","PRECEDENCE","TUPLO","ID","VALOR","REGRAGRAM","CODIGO",
          "GRAMMAR", "ENDGRAMMAR","RESTO"]

states = [
    ("lexer", "exclusive"),
    ("tokens", "exclusive"),
    ("regex", "exclusive"),
    ("yacc", "exclusive"),
    ("grammar", "exclusive")
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

def t_regex_RETURN(t):
    r'return[^\n]+'
    lexer.pop_state()
    return t

def t_regex_ERROR(t):
    r'error[^\n]+'
    lexer.pop_state()
    return t

#lexer

def t_lexer_YACC(t):
    r'YACC'
    lexer.pop_state()
    lexer.push_state("yacc")
    return t

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
    r"\#\#[^\n]+$"
    return t

def t_lexer_EXPREG(t):
    r'(\\\s|\S)+'
    lexer.push_state("regex")
    return t


#grammar state

def t_grammar_REGRAGRAM(t):
    r'[a-zA-Z]+\s:\s[^{]+'
    return t

def t_grammar_CODIGO(t):
    r"\{.*\}"
    return t

def t_grammar_ENDGRAMMAR(t):
    r"%%"
    lexer.pop_state()
    lexer.pop_state()

#yacc



def t_yacc_PRECEDENCE(t):
    r"%precedence"
    return t

def t_yacc_TUPLO(t):
    r"\(('right'|'left'|'nonassoc'),(\'(\w+|[^A-Za-z,'])\'(,)?)+\)"
    return t

def t_yacc_GRAMMAR(t):
    r"%grammar"
    lexer.push_state("grammar")
    return t

def t_yacc_ID(t):
    r"[a-zA-Z]+"
    return t

def t_yacc_VALOR(t):
    r"[^\n=]+"
    return t


#INITIAL

def t_LEXER(t):
    r'LEX'
    lexer.push_state("lexer")
    return t

def t_RESTO(t):
    r'(.|\n)+'
    return t


#ignore
t_tokens_ignore = " \t\r"
t_regex_ignore = " \t\r"
t_lexer_ignore = " \n\t\r"
t_yacc_ignore = " \n\t\r"
t_grammar_ignore = " \n\t\r"
t_ignore = " \n\t\r"

#error

def t_ANY_error(t):
    print("Illegal character!", t.value)

f = open("test.txt")

content = f.read()

lexer = lex.lex()

lexer.input(content)
for tok in lexer:
    print(tok)



#gramática ficheiro

def p_ficheiro(p):
    "ficheiro : lex yacc"

#gramática lex

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

def p_acao_return(p):
    "acao : RETURN"

def p_acao_error(p):
    "acao : ERROR"

#gramática yacc

def p_yacc(p):
    "yacc : YACC coteudoyacc"

def p_conteudoyacc(p):
    "conteudoyacc : precedence variables producoes"

def p_precedence(p):
    "precedence : PRECEDENCE '=' '[' tuplos ']'"

def p_tuplos_vazio(p):
    "tuplos : "

def p_tuplos_varios(p):
    "tuplos : tuplos ',' TUPLO"

def p_variables_vazio(p):
    "variables : "

def p_variables_varias(p):
    "variables : variables variable"

def p_variable(p):
    "variable : ID '=' VALOR"

def p_producoes_vazio(p):
    "producoes : "

def p_producoes_varias(p):
    "producoes : producoes producao"
    
def p_producao(p):
    "producao : REGRAGRAM CODIGO"



def p_error(p):
    print("Syntax Error in:", p.value)


parser = yacc.yacc()

f = open("test.txt")

content = f.read()

#parser.parse(content)
