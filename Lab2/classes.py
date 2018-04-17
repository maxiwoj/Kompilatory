class Node(object):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(instructions: [" + str(
            self.instructions) + "])}"


class BinExpr(Node):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(op: [" + str(
            self.op) + "]), (left: [" + str(self.left) + "]), (right: [" + str(
            self.right) + "])}"


class Variable(Node):
    def __init__(self, value):
        self.value = value
        self.type = type(value)

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(value: [" + str(
            self.value) + "]), (type: [" + str(self.type) + "])}"


class Instructions(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(instructions: [" + str(
            self.instructions) + "]), (instruction: [" + str(
            self.instruction) + "])}"

class PrintInstr(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(value: [" + str(
            self.value) + "])}"


class Assignment(Node):
    def __init__(self, variable, assignType):
        self.assignType = assignType
        self.variable = variable

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(assignType: [" + str(
            self.assignType) + "]), (id: [" + str(self.variable) + "])}"


class EndAssignment(Assignment):
    def __init__(self, variable, assignType, expression):
        super(EndAssignment, self).__init__(variable, assignType)
        self.expression = expression

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(Super(EndAssignment): [" +\
               super(EndAssignment, self).__str__() + "]), (expression: [" +\
               str(self.expression) + "])}"


class MiddleAssignment(Assignment):
    def __init__(self, variable, assignType, assignment):
        super(MiddleAssignment, self).__init__(variable, assignType)
        self.assignment = assignment

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{((Super(MiddleAssignment): [" + str(
            super(MiddleAssignment, self).__init__(self.variable,
                                                   self.assignType)) + "]), (expression: [" + str(
            self.assignment) + "])}"


class If(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(condition: [" + str(
            self.condition) + "]), (instructions: [" + str(
            self.instructions) + "])}"


class IfElse(Node):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(condition: [" + str(
            self.condition) + "]), (instructions: [" + str(
            self.instructions) + "]), (else_instructions: [" + str(
            self.else_instructions) + "])}"


class While(Node):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(condition: [" + str(
            self.condition) + "]), (instructions: [" + str(
            self.instructions) + "])}"


class ReturnInstr(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(expression: [" + str(
            self.expression) + "])}"


class Break(Node):

    def __init__(self):
        pass

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{}"


class Continue(Node):

    def __init__(self):
        pass

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{}"


class PrintExpression(Node):
    def __init__(self, to_print):
        self.to_print = to_print

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(to_print: [" + str(
            self.to_print) + "])}"


class PrintExpressions(Node):
    def __init__(self, print_expressions, print_expression) -> None:
        self.print_expression = print_expression
        self.print_expressions = print_expressions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(print_expression: [" + str(
            self.print_expression) + "]), (print_expressions: [" + str(
            self.print_expressions) + "])}"


class UnExpr(Node):
    def __init__(self, expression, operator):
        self.expression = expression
        self.operator = operator

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(expression: [" + str(
            self.expression) + "]), (operator: [" + str(self.operator) + "])}"


class InstructionBlock(Node):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(instructions: [" + str(
            self.instructions) + "])}"

class ForInstruction(Node):

    def __init__(self, var, range, instruction_block):
        self.var = var
        self.range = range
        self.instruction_block = instruction_block

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(range: [" + str(
            self.range) + "]), (instruction_block: [" + str(
            self.instruction_block) + "])}"


class Range(Node):
    def __init__(self, from_limit, to_limit):
        self.from_limit = from_limit
        self.to_limit = to_limit

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(from_limit: [" + str(
            self.from_limit) + "]), (to_limit: [" + str(self.to_limit) + "])}"


class MatrixInitializer(Node):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(rows: [" + str(
            self.rows) + "]), (row: [" + str(self.row) + "])}"


class MatrixReference(Node):

    def __init__(self, matrix_id, locations):
        self.matrix_id = matrix_id
        self.locations = locations

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(matrix_id: [" + str(
            self.matrix_id) + "]), (locations: [" + str(self.locations) + "])}"


class MatrixLocations(Node):

    def __init__(self, dim_locations, location):
        self.dim_locations = dim_locations
        self.location = location

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(dim_locations: [" + str(
            self.dim_locations) + "]), (location: [" + str(
            self.location) + "])}"


class ZerosInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(expression: [" + str(
            self.expression) + "])}"


class OnesInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(expression: [" + str(
            self.expression) + "])}"


class EyeInitFun(Node):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "[" + self.__class__.__name__ + "]{(expression: [" + str(
            self.expression) + "])}"
