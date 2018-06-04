class Node(object):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        self.printTree()

    def set_position(self, position):
        self.position = position

# OK
class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        self.printTree()

# OK
class Variable(Node):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        self.printTree()

# OK
class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

    def __str__(self):
        self.printTree()

# OK
class PrintInstr(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        self.printTree()

# OK
class Assignment(Node):
    def __init__(self, variable, assignType, expression):
        self.assignType = assignType
        self.variable = variable
        self.expression = expression

    def __str__(self):
        self.printTree()

# OK
class If(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        self.printTree()

# OK
class IfElse(Node):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions

    def __str__(self):
        self.printTree()

# OK
class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        self.printTree()

# OK
class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

# OK
class Break(Node):

    def __init__(self):
        pass

    def __str__(self):
        self.printTree()

# OK
class Continue(Node):

    def __init__(self):
        pass

    def __str__(self):
        self.printTree()

# OK
class PrintExpression(Node):
    def __init__(self, to_print):
        self.to_print = to_print

    def __str__(self):
        self.printTree()

# OK
class PrintExpressions(Node):
    def __init__(self, print_expressions, print_expression) -> None:
        self.print_expression = print_expression
        self.print_expressions = print_expressions

    def __str__(self):
        self.printTree()

# OK
class UnExpr(Node):
    def __init__(self, operator, expression):
        self.expression = expression
        self.operator = operator

    def __str__(self):
        self.printTree()

# OK
class InstructionBlock(Node):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        self.printTree()

# OK
class ForInstruction(Node):

    def __init__(self, var, range, instruction_block):
        self.var = var
        self.range = range
        self.instruction_block = instruction_block

    def __str__(self):
        self.printTree()

# OK
class Range(Node):
    def __init__(self, from_limit, to_limit):
        self.from_limit = from_limit
        self.to_limit = to_limit

    def __str__(self):
        self.printTree()

# OK
class MatrixInitializer(Node):
    def __init__(self, rows):
        self.rows = rows

    def __str__(self):
        self.printTree()

# OK
class MatrixReference(Node):

    def __init__(self, id, locations):
        self.id = id
        self.locations = locations

    def __str__(self):
        self.printTree()

# OK
class MatrixLocations(Node):

    def __init__(self, dim_locations, location):
        self.dim_locations = dim_locations
        self.location = location

    def __str__(self):
        self.printTree()

# OK
class ZerosInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

# OK
class OnesInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

# OK
class EyeInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        self.printTree()

# OK
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

# ?
class Row(Node):
    def __init__(self):
        self.expr_list = []

    def append_expr(self, a):
        self.expr_list.append(a)

    def cons_expr(self, expr_list, a):
        self.expr_list = list(expr_list)
        self.expr_list.append(a)

    def __str__(self):
        self.printTree()

# OK
class Float(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        self.printTree()

# OK
class Int(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        self.printTree()

# OK
class String(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        self.printTree()
