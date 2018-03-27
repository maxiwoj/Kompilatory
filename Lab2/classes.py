class Node(object):
    def __init__(self, declarations, fundefs, instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions
        self.i = 0

    def __str__(self):
        return self.printTree()


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return self.printTree()


class Variable(Node):
    def __init__(self, value):
        self.value = value
        self.type = type(value)

    def __str__(self):
        return self.printTree()


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

    def __str__(self):
        return self.printTree()


class Instruction(Node):
    def __init__(self, instruction):
        self.instruction = instruction

    def __str__(self):
        return self.printTree()


class PrintInstr(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.printTree()


class Assignment(Node):
    def __init__(self, id, assignType):
        self.assignType = assignType
        self.id = id


class EndAssignment(Assignment):
    def __init__(self, id, assignType, expression):
        super(EndAssignment, self).__init__(id, assignType)
        self.expression = expression

    def __str__(self):
        return self.printTree()


class MiddleAssignment(Assignment):
    def __init__(self, id, assignType, assignment):
        super(MiddleAssignment, self).__init__(id, assignType)
        self.expression = assignment

    def __str__(self):
        return self.printTree()


class If(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return self.printTree()


class IfElse(Node):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions

    def __str__(self):
        return self.printTree()


class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return self.printTree()

class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return self.printTree()


class Break(Node):
    def __str__(self):
        return self.printTree()


class Continue(Node):
    def __str__(self):
        return self.printTree()

class PrintExpression(Node):
    def __init__(self, to_print):
        self.to_print = to_print

    def __str__(self):
        # TODO
        return self.printTree()


class PrintExpressions(Node):
    def __init__(self, print_expressions, print_expression) -> None:
        self.print_expression = print_expression
        self.print_expressions = print_expressions

    def __str__(self):
        # TODO
        return self.printTree()


class UnExpr(Node):
    def __init__(self, expression, operator):
        self.expression = expression
        self.operator = operator

    def __str__(self):
        # TODO
        return self.printTree()


class InstructionBlock(Node):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        # TODO
        return self.printTree()


class If_Else_If(Node):
    def __init__(self, condition, instructions, elseif_instructions):
        self.elseif_instructions = elseif_instructions
        self.instructions = instructions
        self.condition = condition

    def __str__(self):
        # TODO:
        return self.printTree()


class If_Else_if_Else(Node):
    def __init__(self, condition, instructions, elseif_instructions,
                 else_instructions):
        self.instructions = instructions
        self.condition = condition
        self.elseif_instructions = elseif_instructions
        self.else_instructions = else_instructions

    def __str__(self):
        # TODO:
        return self.printTree()


class ElIfBlock(Node):
    def __init__(self, condition, instructions, elif_block):
        self.condition = condition
        self.instructions = instructions
        self.elif_block = elif_block

    def __str__(self):
        # TODO
        return self.printTree()


class ForInstruction(Node):

    def __init__(self, range, instruction_block):
        self.range = range
        self.instruction_block = instruction_block

    def __str__(self):
        # TODO
        return self.printTree()


class Range(Node):
    def __init__(self, variable, from_limit, to_limit):
        self.variable = variable
        self.from_limit = from_limit
        self.to_limit = to_limit

    def __str__(self):
        # TODO
        return self.printTree()


class MatrixInitializer(Node):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row

    def __str__(self):
        # TODO
        return self.printTree()


class MatrixReference(Node):

    def __init__(self, matrix_id, location):
        self.matrix_id = matrix_id
        self.location = location

    def __str__(self):
        # TODO
        return self.printTree()


class MatrixLocations(Node):

    def __init__(self, dim_locations, location):
        self.dim_locations = dim_locations
        self.location = location

    def __str__(self):
        # TODO
        return self.printTree()


class ZerosInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        # TODO
        return self.printTree()


class OneswsInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        # TODO
        return self.printTree()


class EyeInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        # TODO
        return self.printTree()
