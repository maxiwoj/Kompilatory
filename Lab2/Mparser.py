#!/usr/bin/env python
import sys
import pprint
import ply.yacc as yacc

import classes
from scanner import Scanner


class Mparser:

    def __init__(self) -> None:
        self.scanner = Scanner()
        self.errors = False

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '=', '+=', '-=', '*=', '/='),  #ASSINGN
        ("nonassoc", '<', '>', 'EQUAL', 'NEQUAL', 'LEQ', 'GEQ'),  #EQUAL NEQUAL ? - not lefT?
#        ("right", 'TRANSPOSE', 'NEGATION'),    MISSING
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", '.+', '.-'),
        ("left", '.*', './')
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: (type: {2}, value: '{3}')".format(p.lineno,
                                                                                      p.lexpos - p.lexer.columnno,
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_file(self, p):
        ''' file : instructions '''
        p[0] = ('FILE', p[1])

    def p_instructions_1(self, p):
        """instructions : instructions instruction"""
        p[0] = ('INSTRUCTIONS', p[1], p[2])

    def p_instructions_2(self, p):
        """instructions : instruction ';'"""
        p[0] = ('INSTRUCTIONS', None, p[1])

    def p_instruction(self, p):
        """ instruction : assignment_instruction
                        | print_instruction
                        | return_instruction
                        | break_instruction
                        | continue_instruction
                        | for_instruction
                        | while_instruction
                        | choice_instruction"""
        p[0] = ('INSTRUCTION', p[1])

    def p_break_instruction(self, p):
        """break_instruction : BREAK"""
        p[0] = ('BREAK')

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE"""
        p[0] = ('CONTINUE')

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression"""
        p[0] = ('RETURN', p[2])

    def p_print_instruction(self, p):
        """print_instr : PRINT print_expressions ';' """
        p[0] = ('PRINT_INSTR' ,p[2])

    def p_print_expressions(self, p):
        '''print_expressions : print_expression
                            | print_expressions, print_expression'''
        if len(p) > 2:
            p[0] = ('PRINT_EXPRS', p[1], p[2])
        else:
            p[0] = ('PRINT_EXPRS', None, p[1])


    def p_print_expression(self, p):
        """print_expression : STRING | expression"""
        p[0] = ('PRINT_EXPR', p[2])

    def p_expression(self, p):
        """expression : bin_expression | un_expression | constant | matrix_init_fun"""
        p[0] = p[1]

    def p_matrix_init_fun_zeros(self, p):
        """matrix_init_fun : ZEROS '(' expression ')'"""
        p[0] = ('ZEROS', p[3])

    def p_matrix_init_fun_ones(self, p):
        """matrix_init_fun : ONES '(' expression ')'"""
        p[0] = ('ONES', p[3])

    def p_matrix_init_fun_eye(self, p):
        """matrix_init_fun : EYE '(' expression ')'"""
        p[0] = ('EYE', p[3])

    def p_bin_expression(self, p):
        """expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression < expression
                      | expression > expression
                      | expression LEQ expression
                      | expression GEQ expression
                      | expression NOTEQ expression
                      | expression EQUAL expression
                      | expression DOTADD expression
                      | expression DOTSUB expression
                      | expression DOTMUL expression
                      | expression DOTDIV expression"""
        #p[0] = ('BIN_EXPR', p[2], p[1], p[3])
        p[0] = ('BIN_EXPR', p[1])

    def p_constant(self, p):
        """constant : FLOAT             #TODO STRING
                    | INT
                    | matrix_initialization"""
        p[0] = p[1]

    def p_matrix_initialization(self, p):
        """matrix_initialization : '[' rows; row ']'
                                 | '[' row ']'"""
        if len(p) > 4:
            p[0] = ('MATRIX_INIT', p[2], p[3])
        else:
            p[0] = ('MATRIX_INIT', None, p[2])

    def p_un_expression_1(self, p):
        """un_expression : expression '\''"""
        p[0] = ('UN_EXPR', p[2], p[1])

    def p_un_expression_2(self, p):
        """un_expression : '-' expression"""
        p[0] = ('UN_EXPR', p[1], p[2])

    def p_assign_instr_end(self, p):
        """assign_instr : variable assign_block expression"""
        p[0] = ('END_ASSIGN', p[1], p[2], p[3])

    def p_assign_instr_midle(self, p):
        """assign_instr : variable assign_block assign_instr"""
        p[0] = ('MIDDLE_ASSIGN', p[1], p[2], p[3])


    def p_variable(self, p):
        """variable : ID | ID '[' matrix_reference ']'"""
        if len(p) == 2:
            p[0] = ('VARIABLE', p[1])
        else:
            p[0] = ('MATRIX_REF', p[1], p[3])

    def p_matrix_reference(self, p):
        """matrix_reference : locations, expression
                            | expression"""
        if len(p) > 2:
            p[0] = ('MATRIX_LOC', p[1], p[2])
        else:
            p[0] = ('MATRIX_LOC', None, p[2])

    def p_assign_block(self, p):
        """assign_block : '=' | '+=' | '-=' | '*=' | '/='"""
        p[0] = p[1]

    def p_while_instr(self, p):
        """while_instr : WHILE '(' expression ')' instruction_block"""
        p[0] = ('WHILE', p[3], p[5])

    def p_instruction_block(self, p):
        """instruction_block : instruction ';'
                             | '{' instructions '}'"""
        if len(p) > 3:
            p[0] = ('INSTRUCTION', p[1])
        else:
            p[0] = ('INSTR_BLOCK', p[2])

    def p_if_instruction(self, p):
        """if_instruction : IF '(' expression ')' instruction_block %proc IFX
                          | IF '(' expression ')' instruction_block ELSE instruction_block
                          | IF '(' expression ')' instruction_block elif_block %proc IFX
                          | IF '(' expression ')' instruction_block elif_block ELSE instruction_block"""

        if p[6] == 'else':
            p[0] = ('IF_ELSE', p[3], p[5], p[7])
        elif len(p) > 7:
            if p[7] == 'else':
                p[0] = ('IF_ELSE_IF', p[3], p[5], p[6])
            else:
                p[0] = ('IF_ELSE_IF_ELSE', p[3], p[5], p[6], p[8])
        else:
            p[0] = ('IF', p[3], p[5])

    def p_elif_block(self, p):
        """elif_block : ELSE IF '(' expression ')' instruction_block
                      | ELSE IF '(' expression ')' instruction_block elif_block"""
        if len(p) > 7:
            p[0] = ('ELIF_BLOCK', p[4], p[6], p[7])
        else:
            p[0] = ('ELIF_BLOCK', p[4], p[6], None)


    def p_for_instruction(self, p):
        """for_instruction : FOR range instruction_block"""
        p[0] = ('FOR', p[2], p[3])

    def p_range(self, p):
        """range : ID '=' expression ':' expression"""
        p[0] = ('RANGE', p[1], p[3], p[5])


