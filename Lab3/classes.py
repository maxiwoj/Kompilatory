class Node(object):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        self.printTree()


class Variable(Node):
    def __init__(self, value):
        self.value = value
        self.type = type(value)

    def __str__(self):
        self.printTree()


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

    def __str__(self):
        self.printTree()

class PrintInstr(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        self.printTree()

class Assignment(Node):
    def __init__(self, variable, assignType):
        self.assignType = assignType
        self.variable = variable

    def __str__(self):
        self.printTree()


class EndAssignment(Assignment):
    def __init__(self, variable, assignType, expression):
        super(EndAssignment, self).__init__(variable, assignType)
        self.expression = expression

    def __str__(self):
        self.printTree()

class MiddleAssignment(Assignment):
    def __init__(self, variable, assignType, assignment):
        super(MiddleAssignment, self).__init__(variable, assignType)
        self.assignment = assignment

    def __str__(self):
        self.printTree()


class If(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        self.printTree()


class IfElse(Node):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions

    def __str__(self):
        self.printTree()


class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        self.printTree()

class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

class Break(Node):

    def __init__(self):
        pass

    def __str__(self):
        self.printTree()


class Continue(Node):

    def __init__(self):
        pass

    def __str__(self):
        self.printTree()


class PrintExpression(Node):
    def __init__(self, to_print):
        self.to_print = to_print

    def __str__(self):
        self.printTree()


class PrintExpressions(Node):
    def __init__(self, print_expressions, print_expression) -> None:
        self.print_expression = print_expression
        self.print_expressions = print_expressions

    def __str__(self):
        self.printTree()


class UnExpr(Node):
    def __init__(self, operator, expression):
        self.expression = expression
        self.operator = operator

    def __str__(self):
        self.printTree()


class InstructionBlock(Node):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        self.printTree()

class ForInstruction(Node):

    def __init__(self, var, range, instruction_block):
        self.var = var
        self.range = range
        self.instruction_block = instruction_block

    def __str__(self):
        self.printTree()


class Range(Node):
    def __init__(self, from_limit, to_limit):
        self.from_limit = from_limit
        self.to_limit = to_limit

    def __str__(self):
        self.printTree()


class MatrixInitializer(Node):
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        self.printTree()


class MatrixReference(Node):

    def __init__(self, matrix_id, locations):
        self.matrix_id = matrix_id
        self.locations = locations

    def __str__(self):
        self.printTree()


class MatrixLocations(Node):

    def __init__(self, dim_locations, location):
        self.dim_locations = dim_locations
        self.location = location

    def __str__(self):
        self.printTree()


class ZerosInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

class OnesInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

class EyeInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

class Rows(Node):
    def __init__(self):
        self.row_list = []

    def append_row(self, a):
        self.row_list.append(a)

    def cons_row(self, row_list, a):
        self.row_list = list(row_list)
        self.row_list.append(a)

    def __str__(self):
        self.printTree()

class Row(Node):
    def __init__(self):
        self.int_list = []

    def append_int(self, a):
        self.int_list.append(a)

    def cons_int(self, int_list, a):
        self.int_list = list(int_list)
        self.int_list.append(a)

    def __str__(self):
        self.printTree()
