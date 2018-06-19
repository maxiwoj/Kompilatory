#!/usr/bin/env python
from Lab2.scanner import Scanner
from Lab4 import classes


class Mparser:

    def __init__(self) -> None:
        self.scanner = Scanner()
        self.errors = False

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '=', 'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN'),
        # ASSINGN
        ("nonassoc", '<', '>', 'EQUAL', 'NOTEQ', 'LEQ', 'GEQ'),  # EQUAL
        ("left", '+', '-'),
        ("left", '*', '/'),
        ("left", 'DOTADD', 'DOTSUB'),
        ("left", 'DOTMUL', 'DOTDIV'),
        ("left", 'TRANSPOSE')
    )

    def position(self, token):
        return (token.lineno, self.scanner.find_column(token))

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: (type: {2}, value: '{3}')".format(p.lineno,
                                                                                      self.scanner.find_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

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
        p[0].set_position(p[1].position)
        # p[0].set_position(p[1].)

    def p_break_instruction(self, p):
        """break_instruction : BREAK"""
        p[0] = classes.Break()
        p[0].set_position(self.position(p.slice[1]))

    def p_continue_instruction(self, p):
        """continue_instruction : CONTINUE"""
        p[0] = classes.Continue()
        p[0].set_position(self.position(p.slice[1]))

    def p_return_instruction(self, p):
        """return_instruction : RETURN expression"""
        p[0] = classes.ReturnInstr(p[2])
        p[0].set_position(self.position(p.slice[1]))

    def p_print_instruction(self, p):
        """print_instr : PRINT print_expressions"""
        p[0] = classes.PrintInstr(p[2])
        p[0].set_position(self.position(p.slice[1]))

    def p_print_expressions(self, p):
        """print_expressions : print_expression
                            | print_expression ',' print_expressions"""
        if len(p) > 2:
            p[0] = classes.PrintExpressions(p[3], p[1])
        else:
            p[0] = classes.PrintExpression(p[1])

    def p_print_expression(self, p):
        """print_expression : expression"""
        p[0] = classes.PrintExpression(p[1])  # prev p[2]
        p[0].set_position(p[1].position)

    def p_expression(self, p):
        """expression : bin_expression
                      | un_expression
                      | constant
                      | variable
                      | matrix_init_fun"""
        p[0] = p[1]  # not a class

    def p_matrix_init_fun_zeros(self, p):
        """matrix_init_fun : ZEROS '(' expression ')'"""
        p[0] = classes.ZerosInitFun(p[3])
        p[0].set_position(self.position(p.slice[1]))

    def p_matrix_init_fun_ones(self, p):
        """matrix_init_fun : ONES '(' expression ')'"""
        p[0] = classes.OnesInitFun(p[3])
        p[0].set_position(self.position(p.slice[1]))

    def p_matrix_init_fun_eye(self, p):
        """matrix_init_fun : EYE '(' expression ')'"""
        p[0] = classes.EyeInitFun(p[3])
        p[0].set_position(self.position(p.slice[1]))

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
        p[0] = classes.BinExpr(p.slice[2].type, p[1], p[3])
        p[0].set_position(self.position(p.slice[2]))

    def p_constant_matrix(self, p):
        """constant : matrix_initialization"""
        p[0] = p[1]

    def p_constant_int(self, p):
        """constant : INT"""
        p[0] = classes.Int(p[1])
        p[0].set_position(self.position(p.slice[1]))

    def p_constant_string(self, p):
        """constant : STRING"""
        p[0] = classes.String(p[1])
        p[0].set_position(self.position(p.slice[1]))

    def p_constant_float(self, p):
        """constant : FLOAT"""
        p[0] = classes.Float(p[1])
        p[0].set_position(self.position(p.slice[1]))

    def p_matrix_initialization(self, p):
        """matrix_initialization : '[' rows ']'"""
        p[0] = classes.MatrixInitializer(p[2])
        p[0].set_position(self.position(p.slice[1]))

    def p_rows(self, p):
        """rows : row ';' rows
                | row"""
        p[0] = classes.Rows()
        if len(p) > 2:
            p[0].cons_row(p[3].row_list, p[1])
            p[0].set_position(self.position(p.slice[2]))
        else:
            p[0].append_row(p[1])

    def p_row(self, p):
        """row : expression ',' row
               | expression"""
        p[0] = classes.Row()
        if len(p) > 2:
            p[0].cons_expr(p[3].expr_list, p[1])
        else:
            p[0].append_expr(p[1])


    def p_un_expression_1(self, p):
        """un_expression : expression TRANSPOSE"""
        p[0] = classes.UnExpr("TRANSPOSE", p[1])
        p[0].set_position(self.position(p.slice[2]))

    def p_un_expression_2(self, p):
        """un_expression : '-' expression"""
        p[0] = classes.UnExpr("NEGATION", p[2])
        p[0].set_position(self.position(p.slice[1]))

    def p_assign_instr(self, p):
        """assign_instr : variable '=' expression
                        | variable ADDASSIGN expression
                        | variable SUBASSIGN expression
                        | variable MULASSIGN expression
                        | variable DIVASSIGN expression"""
        p[0] = classes.Assignment(p[1], p[2], p[3])
        p[0].set_position(self.position(p.slice[2]))

    def p_variable(self, p):
        """variable : ID
                    | ID '[' matrix_locations ']'"""
        if len(p) == 2:
            p[0] = classes.Variable(p[1])
        else:
            p[0] = classes.MatrixReference(p[1], p[3])
        p[0].set_position(self.position(p.slice[1]))

    def p_matrix_locations(self, p):
        """matrix_locations : expression ',' matrix_locations
                            | expression"""
        if len(p) > 2:
            p[0] = classes.MatrixLocations(p[3], p[1])
        else:
            p[0] = p[1]

    def p_while_instr(self, p):
        """while_instr : WHILE '(' expression ')' instruction_block"""
        p[0] = classes.While(p[3], p[5])
        p[0].set_position(self.position(p.slice[1]))

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
        p[0].set_position(self.position(p.slice[1]))

    def p_for_instruction(self, p):
        """for_instruction : FOR ID '=' range instruction_block"""
        p[0] = classes.ForInstruction(p[2], p[4], p[5])
        p[0].set_position(self.position(p.slice[1]))

    def p_range(self, p):
        """range : expression ':' expression"""
        p[0] = classes.Range(p[1], p[3])
        p[0].set_position(self.position(p.slice[1]))
