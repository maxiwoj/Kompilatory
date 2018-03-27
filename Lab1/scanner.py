#!/usr/bin/python

import sys
import ply.lex as lex

reserved = {
    'print': 'PRINT',
    'eye': 'EYE',
    'ones': 'ONES',
    'zeros': 'ZEROS',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'while': 'WHILE',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE'
    }

tokens = [
    'LEQ',
    'GEQ',
    'NOTEQ',
    'EQUAL',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    
    'FLOAT',
    'INT',

    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ID'
] + list(reserved.values())

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_PRINT = r'print'
t_EYE = r'eye'
t_ONES = r'ones'
t_ZEROS = r'zeros'
t_CONTINUE = r'continue'
t_RETURN = r'return'
t_WHILE = r'while'
t_FOR = r'for'
t_IF = r'if'
t_ELSE = r'else'

t_LEQ = r'<='
t_GEQ = r'>='
t_NOTEQ = r'!='
t_EQUAL = r'=='
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t

literals = [ '+','-','*','/','(',')','[',']','{','}','=','<','>',':',"'",',',';']

t_ignore = ' \t'

def t_FLOAT(t):
    r'([0-9]*[.])[0-9]+(e-?[0-9]+)?'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'\#.[^\n]*\n'
    t.lexer.lineno += 1
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" %(t.lineno, t.value[0]) )
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


lexer = lex.lex()
fh = None
try:
    fh = open(sys.argv[1] if len(sys.argv) > 1 else "plik.ini", "r");
    text = fh.read()
    lexer.input(text)
    for token in lexer:
        print("position (%d,%d): %s(%s)" %(token.lineno, find_column(text, token), token.type, token.value))
except Exception as e:
    print("open error\n", e)


