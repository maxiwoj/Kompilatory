#!/usr/bin/env python
from Lab3 import classes
from Lab2.scanner import Scanner


class Mparser:

    def __init__(self) -> None:
        self.scanner = Scanner()
        self.errors = False

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),  #ASSINGN
        ("nonassoc", '<', '>', 'EQUAL', 'NOTEQ', 'LEQ', 'GEQ'),  #EQUAL
#        ("right", 'TRANSPOSE', 'NEGATION')
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV')
    )

    # def p_error(self, p):
    #     if p:
    #         print("Syntax error at line {0}, column {1}: (type: {2}, value: '{3}')".format(p.lineno,
    #                                                                                   p.lexpos - p.lexer.columnno,
    #                                                                                   p.type, p.value))
    #     else:
    #         print("Unexpected end of input")

    def p_file(self, p):
        ''' file : instructions '''
        p[0] = p[1]

    def p_instructions_1(self, p):
        """instructions : instructions instruction"""
        p[0] = classes.Instructions(p[1], p[2])

    def p_instructions_2(self, p):
        """instructions : instruction"""
        p[0] = p[1]

    def p_instruction(self, p):
        """ instruction : assign_instr ';'
                        | print_instr ';'
                        | return_instruction ';'
                        | break_instruction ';'
                        | continue_instruction ';'
                        | for_instruction
                        | while_instr
                        | if_instruction"""
        p[0] = p[1]

    def p_break_instruction(self, p):
        """break_instruction : BREAK"""
        p[0] = classes.Break()

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE"""
        p[0] = classes.Continue()

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression"""
        p[0] = classes.ReturnInstr(p[2])

    def p_print_instruction(self, p):
        """print_instr : PRINT print_expressions"""
        p[0] = classes.PrintInstr(p[2])

    def p_print_expressions(self, p):
        """print_expressions : print_expression
                            | print_expressions ',' print_expression"""
        if len(p) > 2:
            p[0] = classes.PrintExpressions(p[1], p[2])
        else:
            p[0] = classes.PrintExpression(p[1])


    def p_print_expression(self, p):
        """print_expression : expression"""
        p[0] = classes.PrintExpression(p[1]) #prev p[2]

    def p_expression(self, p):
        """expression : bin_expression
                      | un_expression
                      | constant
                      | variable
                      | matrix_init_fun"""
        p[0] = p[1]   #not a class

    def p_matrix_init_fun_zeros(self, p):
        """matrix_init_fun : ZEROS '(' expression ')'"""
        p[0] = classes.ZerosInitFun(p[3])

    def p_matrix_init_fun_ones(self, p):
        """matrix_init_fun : ONES '(' expression ')'"""
        p[0] = classes.OnesInitFun(p[3])

    def p_matrix_init_fun_eye(self, p):
        """matrix_init_fun : EYE '(' expression ')'"""
        p[0] = classes.EyeInitFun(p[3])

    def p_bin_expression(self, p):
        """bin_expression : expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '<' expression
                      | expression '>' expression
                      | expression LEQ expression
                      | expression GEQ expression
                      | expression NOTEQ expression
                      | expression EQUAL expression
                      | expression DOTADD expression
                      | expression DOTSUB expression
                      | expression DOTMUL expression
                      | expression DOTDIV expression"""
        p[0] = classes.BinExpr(p[2], p[1], p[3])

    def p_constant(self, p):
        """constant : FLOAT
                    | INT
                    | STRING
                    | matrix_initialization"""
        p[0] = p[1]

    def p_matrix_initialization(self, p):
        """matrix_initialization : '[' rows ']'"""
        p[0] = classes.MatrixInitializer(p[2])

    def p_rows(self, p):
        """rows : rows ';' row
                | row"""
        p[0] = classes.Rows()
        if len(p) > 2:
            p[0].cons_row(p[1].row_list, p[3])
        else:
            p[0].append_row(p[1])

    def p_row(self, p):
        """row : row ',' INT
               | INT"""
        p[0] = classes.Row()
        if len(p) > 2:
            p[0].cons_int(p[1].int_list, p[3])
        else:
            p[0].append_int(p[1])

    def p_un_expression_1(self, p):
        """un_expression : expression TRANSPOSE"""
        p[0] = classes.UnExpr(p[2], p[1])

    def p_un_expression_2(self, p):
        """un_expression : '-' expression"""
        p[0] = classes.UnExpr(p[1], p[2])


    def p_assign_instr_end(self, p):
        """assign_instr : variable assign_block expression"""
        p[0] = classes.EndAssignment(p[1], p[2], p[3])

    def p_assign_instr_middle(self, p):
        """assign_instr : variable assign_block assign_instr"""
        p[0] = classes.MiddleAssignment(p[1], p[2], p[3])

    def p_variable(self, p):
        """variable : ID
                    | ID '[' matrix_reference ']'"""
        if len(p) == 2:
            p[0] = classes.Variable(p[1])
        else:
            p[0] = classes.MatrixReference(p[1], p[3])

    def p_matrix_reference(self, p):
        """matrix_reference : matrix_reference ',' expression
                            | expression"""
        if len(p) > 2:
            p[0] = classes.MatrixLocations(p[1], p[3])
        else:
            p[0] = p[1]

    def p_assign_bloc(self, p):
        """assign_block : '='
                        | ADDASSIGN
                        | SUBASSIGN
                        | MULASSIGN
                        | DIVASSIGN"""
        p[0] = p[1]

    def p_while_instr(self, p):
        """while_instr : WHILE '(' expression ')' instruction_block"""
        p[0] = classes.While(p[3], p[5])

    def p_instruction_block(self, p):
        """instruction_block : instruction
                             | '{' instructions '}' """
        if len(p) > 3:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_if_instruction(self, p):
        """if_instruction : IF '(' expression ')' instruction_block %prec IFX
                          | IF '(' expression ')' instruction_block ELSE instruction_block"""

        if len(p) < 7:
           p[0] = classes.If(p[3], p[5])
        else:
            p[0] = classes.IfElse(p[3], p[5], p[7])

    def p_for_instruction(self, p):
        """for_instruction : FOR ID '=' range instruction_block"""
        p[0] = classes.ForInstruction(p[2], p[4], p[5])

    def p_range(self, p):
        """range : expression ':' expression"""
        p[0] = classes.Range(p[1], p[3])


