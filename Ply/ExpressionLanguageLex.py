import ply.lex as lex

reserved = {
    'as':'AS',
    'function':'FUNCTION',
    'and':'AND',
    'or':'OR',
    'if' : 'IF',
    'else' : 'ELSE',
    'elseif':'ELSEIF',
    'endif':'ENDIF',
    'switch':'SWITCH',
    'case':'CASE',
    'break':'BREAK',
    'continue':'CONTINUE',
    'true':'TRUE',
    'false':'FALSE',
    'while' : 'WHILE',
    'endwhile':'ENDWHILE',
    'for' : 'FOR',
    'endfor': 'ENDFOR',
    'foreach': 'FOREACH',
    'endforeach': 'ENDFOREACH',
    'declare': 'DECLARE',
    'enddeclare': 'ENDDECLARE',
    'do':'DO',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
    'float': 'FLOAT_TYPE',
    'real': 'REAL_TYPE',
    'string': 'STRING_TYPE',
    'array': 'ARRAY_TYPE',
    'object': 'OBJECT_TYPE',
    'bool': 'BOOL_TYPE',
    'boolean': 'BOOLEAN_TYPE',
    'unset': 'UNSET',
    'exit': 'EXIT',
    'die': 'DIE',
    'list': 'LIST',
    'clone': 'CLONE',
    'return':'RETURN',
    'global':'GLOBAL',
    'var': 'VAR', #Remover se não existir
}

tokens = [
    'ASPAS',
    'APOSTROFE',
    'ARROBA',
    'AMPERSAND',
    'ATTR_ASSOC',
    'DOLAR',
    'COMMENT_SINGLE',
    'COMMENT_MULTI',
    'CRASE',
    'BEGIN_PROGRAM',
    'END_PROGRAM',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'DDOT',
    'PERCENT',
    'ASSIGN',
    'CONCATENATE',
    'INCREMENT',
    'INTE_DOT',
    'DECREMENT',
    'ADD_ASSIGN',
    'SUB_ASSIGN',
    'MOD_ASSIGN',
    'PLUS_ASSIGN',
    'DIVIDE_ASSIGN',
    'LPAREN',
    'RPAREN',
    'LKEY',
    'RKEY',
    'LBRACKET',
    'RBRACKET',
    'LESS_THAN',
    'LESS_EQUAL',
    'GREAT_THAN',
    'GREAT_EQUAL',
    'EQUAL',
    'NOT_EQUAL',
    'COLON',
    'SEMICOLON',
    'LEFT_LOGICAL',
    'RIGHT_LOGICAL',
    'IDENTATION',
    'STRING',
    'NUMBER_REAL',
    'NUMBER_INTEGER',
    'VARIABLE'
] + list(reserved.values())


t_ignore = ' \t'
t_AS = r'as'
t_FUNCTION = r'function'
t_AND = r'and'
t_OR = r'or'
t_IF = r'if'
t_ELSE = r'else'
t_ELSEIF= r'elseif'
t_ENDIF = r'endif'
t_SWITCH = r'switch'
t_CASE = r'case'
t_BREAK = r'break'
t_CONTINUE = r'continue'
t_TRUE = r'true'
t_FALSE = r'false'
t_WHILE = r'while'
t_ENDWHILE = r'endwhile'
t_FOR = r'for'
t_ENDFOR = r'endfor' 
t_DO = r'do'
t_INT_TYPE = r'int'
t_DOUBLE_TYPE = r'double'
t_REAL_TYPE = r'real'
t_ARRAY_TYPE = r'array'
t_OBJECT_TYPE = r'object'
t_BOOL_TYPE = r'bool'
t_BOOLEAN_TYPE = r'boolean'
t_UNSET = r'unset'
t_EXIT = r'exit'
t_DIE = r'die'
t_LIST = r'list'
t_CLONE = r'clone'
t_RETURN = r'return'
t_GLOBAL = r'global'
t_VAR = r'var' #Remover se não existir

t_COMMENT_SINGLE = r'\//.* | \#.*'
t_COMMENT_MULTI = r'\/\*(.|\n)*\*\/'
t_BEGIN_PROGRAM =  r'\<\?php'
t_END_PROGRAM   =  r'\?\>'
t_DOLAR =  r'\$'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_PERCENT = r'\%'
t_ASSIGN =  r'\='
t_CONCATENATE =  r'\.\='
t_INCREMENT =  r'\+\+'
t_DECREMENT =  r'\-\-'
t_ADD_ASSIGN = r'\+\='
t_SUB_ASSIGN = r'\-\='
t_MOD_ASSIGN = r'\%\='
t_PLUS_ASSIGN = r'\*\='
t_DIVIDE_ASSIGN =  r'\/\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LKEY = r'\{'
t_RKEY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LESS_THAN = r'\<'
t_LESS_EQUAL = r'\<\='
t_GREAT_THAN =  r'\>'
t_GREAT_EQUAL = r'\>\='
t_EQUAL = r'\=\='
t_NOT_EQUAL = r'\!\='
t_COLON = r'\,'
t_SEMICOLON = r'\;'
t_LEFT_LOGICAL = r'\<\<'
t_RIGHT_LOGICAL = r'\>\>'
t_AMPERSAND = r'\&'
t_ATTR_ASSOC = r'\=\>'
t_CRASE  = r'\`'
t_APOSTROFE  = r'\''
t_ASPAS =  r'\"'
t_DDOT = r'\:'
t_INTE_DOT = r'\?'
t_ARROBA = r'\@'

ArrayTabulacao = [0]
IndicePosicao  =  0
ConstTabulacao =  8

def t_IDENTATION(t):
    r'\n[ \t]*'
    global IndicePosicao
    global ConstTabulacao
    Tamanho = 0
    
    for i in t.value:
        if(i == ' '):
            Tamanho += 1
        else:
            if(i != '\n'):
                Auxiliar = Tamanho // ConstTabulacao
                Tamanho = (Auxiliar + 1) * ConstTabulacao

    if(ArrayTabulacao[IndicePosicao] < Tamanho):
        ArrayTabulacao.append(Tamanho)
        IndicePosicao += 1
    if(ArrayTabulacao[IndicePosicao] > Tamanho):
        if(Tamanho in ArrayTabulacao):
            del ArrayTabulacao[ArrayTabulacao.index(Tamanho)+1:len(ArrayTabulacao)]
            IndicePosicao = ArrayTabulacao.index(Tamanho)
        else:
            print("Identação ilegal foi encontrada")

def t_STRING(t):
    r'\".*\"'
    return t

def t_NUMBER_REAL(t):
    r'-?\d*\.\d+'
    t.value = float(t.value)
    return t
    
def t_NUMBER_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value) 
    return t

def t_VARIABLE(t):
    r'\$[_a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VARIABLE')
    return t

def t_newline(t):
    r'\n+'
    pass

def t_error(t):
    print("Um caracter ilegal foi encontrado: '%s'" % t.value[0])
    t.lexer.skip(1)
 
arquivo ='''<?php
$valor1 = 40;
$valor2 = 20;

if ($valor1 > $valor2)
  "A variavel $valor1 e maior que a variavel $valor2";
else if ($valor2 > $valor1)
  "A variavel $valor2 e maior que a variavel $valor1";
else
   "A variavel $valor1 e igual a variavel $valor2";
?>'''

lexer = lex.lex()
lexer.input(arquivo)

while True:
    token = lexer.token()
    if not token:
        break
    print(token)