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

tokens = ["LEXER","YACC","LITERALS","IGNORE","TOKENS","EXPREG","STRING","COMM","NEWLINE",
          "RETURN","ERROR","TOKEN","ATRIB","PRECEDENCE","TUPLO","ID","VALOR","REGRAGRAM","CODIGO",
          "GRAMMAR", "ENDGRAMMAR","RESTO","VARS","TEXT"]

states = [
    ("lexer", "exclusive"),
    ("tokens", "exclusive"),
    ("regex", "exclusive"),
    ("yacc", "exclusive"),
    ("grammar", "exclusive"),
    ("vars","exclusive"),
    ("comment","exclusive")
]


def t_ANY_COMM(t):
    r'\#\#'
    lexer.push_state("comment")
    pass


#comment state

def t_comment_TEXT(t):
    "[^\n]+"
    lexer.pop_state()
    pass


#tokens state

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


#vars state

def t_vars_GRAMMAR(t):
    r"%grammar"
    lexer.pop_state()
    lexer.push_state("grammar")
    return t

def t_vars_ID(t):
    r"[a-zA-Z]+"
    return t

def t_vars_VALOR(t):
    r"[^\n=]+"
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

def t_yacc_VARS(t):
    "%vars"
    lexer.push_state("vars")
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
t_comment_ignore = " \n\t\r"
t_vars_ignore = " \n\t\r"
t_ignore = " \n\t\r"

#error

def t_ANY_error(t):
    print("Illegal character!", t.value)

f = open("test.txt")

content = f.read()

lexer = lex.lex()

#lexer.input(content)
#for tok in lexer:
#    print(tok)



#gramática ficheiro

def p_ficheiro(p):
    "ficheiro : lex yacc RESTO"
    p[0] = "import re\nimport ply.lex as lex\nimport ply.yacc as yacc\n\n\n" + p[1] + "\n\n\n" + p[2] + "\n\n\n" + p[3]

#gramática lex

def p_lex(p):
    "lex : LEXER conteudolex"
    p[0] = p[2] + "\n\nlexer = lex.lex()\n\n\n"

def p_conteudolex(p):
    "conteudolex : comandos regras"
    p[0] = p[1] + "\n" + p[2]

def p_comandos_vazio(p):
    "comandos : "
    p[0] = ""

def p_comandos_lista(p):
    "comandos : comando comandos"
    p[0] = p[1] + "\n" + p[2]

def p_comando_literals(p):
    "comando : LITERALS ATRIB STRING"
    p[0] = p[1].replace("%", "") + p[2] + p[3]

def p_comando_ignore(p):
    "comando : IGNORE ATRIB STRING"
    p[0] = p[1].replace("%", "") + p[2] + p[3]

def p_comando_tokens(p):
    "comando : TOKENS ATRIB listatok"
    p[0] = p[1].replace("%", "") + p[2] + p[3]

def p_listatok(p):
    "listatok : '[' conteudo ']'"
    p[0] = p[1] + p[2] + p[3]
    
def p_conteudo_vazio(p):
    "conteudo : "
    p[0] = ""
    
def p_conteudo_lista(p):
    "conteudo : tokens"
    p[0] = p[1]

def p_tokens_token(p):
    "tokens : TOKEN"
    p[0] = p[1]
    
def p_tokens_lista(p):
    "tokens : TOKEN ',' tokens"
    p[0] = p[1] + p[2] + p[3]

def p_regras_vazio(p):
    "regras : "
    p[0] = ""
    
def p_regras_lista(p):
    "regras : regra regras"
    p[0] = p[1] + p[2]

def p_regra(p):
    "regra : EXPREG acao"
    tmp = p[2].split('%')
    value = tmp[1].split(',')
    p[0] = tmp[0] + "r'" + p[1] + "'" + "\n\t" + "t.value=" + value[1][:-1] + "\n\treturn t" + "\n\n"

def p_acao_return(p):
    "acao : RETURN"
    pattern = re.compile(r'return\(\'([a-zA-Z]+)\'')
    mo = pattern.search(p[1])
    token = mo.group(1)
    p[0] = "def t_" + token + "(t):\n\t" + "%" + p[1]

def p_acao_error(p):
    "acao : ERROR"
    p[0] = "def t_error(t):\n\t" + "%" + p[1].replace("error","print")
    

#gramática yacc

def p_yacc(p):
    "yacc : YACC conteudoyacc"
    p[0] =  p[2]

def p_conteudoyacc(p):
    "conteudoyacc : precedence VARS variables GRAMMAR producoes"
    p[0] = p[1] + p[3] + p[5]

def p_precedence(p):
    "precedence : PRECEDENCE '=' '[' lista ']'"
    p[0] = p[1].replace("%", "") + p[2] + p[3] + "\n" + p[4] + "\n" + p[5] + "\n\n"

def p_lista_vazio(p):
    "lista : "
    p[0] = ""

def p_lista_varios(p):
    "lista : tuplos"
    p[0] = p[1]
    
def p_tuplos(p):
    "tuplos : TUPLO tuplos2"
    p[0] = p[1] + p[2]

def p_tuplos2_vazio(p):
    "tuplos2 : "
    p[0] = ""

def p_tuplos2_varios(p):
    "tuplos2 : ',' TUPLO tuplos2"
    p[0] = p[1] + "\n" + p[2] + p[3]


def p_variables_vazio(p):
    "variables : "
    p[0] = ""

def p_variables_varias(p):
    "variables : variables variable"
    p[0] = p[1] + p[2] + "\n\n"

def p_variable(p):
    "variable : ID '=' VALOR"
    p[0] = p[1] + p[2] + p[3]

def p_producoes_vazio(p):
    "producoes : "
    p[0] = ""

def p_producoes_varias(p):
    "producoes : producoes producao"
    p[0] = p[1] + p[2]
    
def p_producao(p):
    "producao : REGRAGRAM CODIGO"
    splits = p[1].split(':')
    funcname = splits[0]
  
    regra = p[2].replace("{", "")
    regra = regra.replace("}","")
    regra = regra.replace(" ", "")
    p[0] = "def p_" + funcname.replace(" ", "") + "_" + str(p.parser.count) + "(t):\n\t"+ "\"" + p[1] +"\"" +"\n\t"+ regra + "\n\n"
    p.parser.count += 1

def p_error(p):
    print("Syntax Error in:", p.value, p.lexpos)


parser = yacc.yacc()
parser.count = 0

f = open("test.txt")

content = f.read()
f = open("output.py", "w")
f.write(parser.parse(content))
