#!/usr/bin/env python
import sys
import pprint
import ply.yacc as yacc

import classes
from scanner import Scanner


class Parser:

    def __init__(self) -> None:
        self.scanner = Scanner()
        self.errors = False

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '=', '+=', '-=', '*=', '/='),
        ("nonassoc", '<', '>', 'EQUAL', 'NEQUAL', 'LEQ', 'GEQ'),
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", '.+', '.-'),
        ("left", '.*', './')
    )


    def p_file(p):
        ''' file : instructions '''
        p[0] = p[1]

    def p_instructions_1(p):
        """instructions : instructions instruction"""
        p[0] = classes.Instructions(p[1], p[2])

    def p_instructions_2(p):
        """instructions : instruction ';'"""
        p[0] = classes.Instructions(None, p[1])

    def p_instruction(p):
        """ instruction : assignment_instruction
                        | print_instruction
                        | return_instruction
                        | break_instruction
                        | continue_instruction
                        | for_instruction
                        | while_instruction
                        | choice_instruction"""
        p[0] = p[1]

    def p_break_instruction(p):
        """break_instruction : BREAK"""
        p[0] = classes.Break()

    def p_continue_instruction(p):
        """continue_instruction : CONTINUE"""
        p[0] = classes.Continue()

    def p_return_instruction(p):
        """return_instruction : RETURN expression"""
        p[0] = classes.ReturnInstr(p[2])

    def p_print_instruction(p):
        """print_instr : PRINT print_expressions ';' """
        p[0] = classes.PrintInstr(p[2])

    def p_print_expressions(p):
        '''printexpressions : print_expression
                            | print_expressions, print_expression'''
        if len(p) > 2:
            p[0] = classes.PrintExpressions(p[1], p[2])
        else:
            p[0] = classes.PrintExpressions(None, p[1])


    def p_print_expression(p):
        """print_expression : STRING | expression"""
        p[0] = classes.PrintExpression(p[2])

    def p_expression(p):
        """expression : bin_expression | un_expression | constant | matrix_init_fun"""
        p[0] = p[1]

    def p_matrix_init_fun_zeros(p):
        """matrix_init_fun : ZEROS '(' expression ')'"""
        p[0] = classes.ZerosInitFun(p[3])

    def p_matrix_init_fun_ones(p):
        """matrix_init_fun : ONES '(' expression ')'"""
        p[0] = classes.OnesInitFun(p[3])

    def p_matrix_init_fun_eye(p):
        """matrix_init_fun : EYE '(' expression ')'"""
        p[0] = classes.EyeInitFun(p[3])

    def p_bin_expression(p):
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
        p[0] = classes.BinExpr(p[2], p[1], p[3])

    def p_constant(p):
        """constant : FLOAT
                    | INT
                    | matrix_initialization"""
        p[0] = p[1]

    def p_matrix_initialization(p):
        """matrix_initialization : '[' rows; row ']'
                                 | '[' row ']'"""
        if len(p) > 4:
            p[0] = classes.MatrixInitializer(p[2], p[3])
        else:
            p[0] = classes.MatrixInitializer(None, p[2])

    def p_un_expression_1(p):
        """un_expression : expression '\''"""
        p[0] = classes.UnExpr(p[2], p[1])

    def p_un_expression_2(p):
        """un_expression : '-' expression"""
        p[0] = classes.UnExpr(p[1], p[2])

    def p_assign_instr_end(p):
        """assign_instr : variable assign_block expression"""
        p[0] = classes.EndAssignment(p[1], p[2], p[3])

    def p_assign_instr_midle(p):
        """assign_instr : variable assign_block assign_instr"""
        p[0] = classes.MiddleAssignment(p[1], p[2], p[3])


    def p_variable(p):
        """variable : ID | ID '[' matrix_reference ']'"""
        if len(p) == 2:
            p[0] = classes.Variable(p[1])
        else:
            p[0] = classes.MatrixReference(p[1], p[3])

    def p_matrix_reference(p):
        """matrix_reference : locations, expression
                            | expression"""
        if len(p) > 2:
            p[0] = classes.MatrixLocations(p[1], p[2])
        else:
            p[0] = classes.MatrixLocations(None, p[2])

    def p_assign_block(p):
        """assign_block : '=' | '+=' | '-=' | '*=' | '/='"""
        p[0] = p[1]

    def p_while_instr(p):
        """while_instr : WHILE '(' expression ')' instruction_block"""
        p[0] = classes.While(p[3], p[5])

    def p_instruction_block(p):
        """instruction_block : instruction ';'
                             | '{' instructions '}'"""
        if len(p) > 3:
            p[0] = classes.Instruction(p[1])
        else:
            p[0] = classes.InstructionBlock(p[2])

    def p_if_instruction(p):
        """if_instruction : IF '(' expression ')' instruction_block %proc IFX
                          | IF '(' expression ')' instruction_block ELSE instruction_block
                          | IF '(' expression ')' instruction_block elif_block %proc IFX
                          | IF '(' expression ')' instruction_block elif_block ELSE instruction_block"""

        if p[6] == 'else':
            p[0] = classes.IfElse(p[3], p[5], p[7])
        elif len(p) > 7:
            if p[7] == 'else':
                p[0] = classes.If_Else_If(p[3], p[5], p[6])
            else:
                p[0] = classes.If_Else_if_Else(p[3], p[5], p[6], p[8])
        else:
            p[0] = classes.If(p[3], p[5])

    def p_elif_block(p):
        """elif_block : ELSE IF '(' expression ')' instruction_block
                      | ELSE IF '(' expression ')' instruction_block elif_block"""
        if len(p) > 7:
            p[0] = classes.ElIfBlock(p[4], p[6], p[7])
        else:
            p[0] = classes.ElIfBlock(p[4], p[6], None)


    def p_for_instruction(p):
        """for_instruction : FOR range instruction_block"""
        p[0] = classes.ForInstruction(p[2], p[3])

    def p_range(p):
        """range : ID '=' expression ':' expression"""
        p[0] = classes.Range(p[1], p[3], p[5])


