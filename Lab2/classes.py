class File(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.i = 0

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(instructions: [" + str(self.instructions) + "])}"


class BinExpr(File):

    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(op: [" + str(self.op) + "]), (left: [" + str(self.left) + "]), (right: [" + str(self.right) + "])}"



class Variable(File):
    def __init__(self, value):
        self.value = value
        self.type = type(value)

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(value: [" + str(self.value) + "]), (type: [" + str(self.type) + "])}"


class Instructions(File):
    def __init__(self, instructions, instruction):
        self.instructions = instructions
        self.instruction = instruction

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(instructions: [" + str(self.instructions) + "]), (instruction: [" + str(self.instruction) + "])}"


class Instruction(File):
    def __init__(self, instruction):
        self.instruction = instruction

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(instruction: [" + str(self.instruction) + "])}"


class PrintInstr(File):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(value: [" + str(self.value) + "])}"


class Assignment(File):
    def __init__(self, id, assignType):
        self.assignType = assignType
        self.id = id
		
    def __str__(self):
        return "["+ self.__class__.__name__+"]{(assignType: [" + str(self.assignType) + "]), (id: [" + str(self.id) + "])}"


class EndAssignment(Assignment):
    def __init__(self, id, assignType, expression):
        super(EndAssignment, self).__init__(id, assignType)
        self.expression = expression

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(Super(EndAssignment): [" + str(super(EndAssignment, self).__init__(self.id, self.assignType)) + "]), (expression: [" + str(self.expression) + "])}"


class MiddleAssignment(Assignment):
    def __init__(self, id, assignType, assignment):
        super(MiddleAssignment, self).__init__(id, assignType)
        self.expression = assignment

    def __str__(self):
        return "["+ self.__class__.__name__+"]{((Super(MiddleAssignment): [" + str(super(MiddleAssignment, self).__init__(self.id, self.assignType)) + "]), (expression: [" + str(self.expression) + "])}"


class If(File):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(condition: [" + str(self.condition) + "]), (instructions: [" + str(self.instructions) + "])}"


class IfElse(File):
    def __init__(self, condition, instructions, else_instructions):
        self.condition = condition
        self.instructions = instructions
        self.else_instructions = else_instructions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(condition: [" + str(self.condition) + "]), (instructions: [" + str(self.instructions) + "]), (else_instructions: [" + str(self.else_instructions) + "])}"


class While(File):
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(condition: [" + str(self.condition) + "]), (instructions: [" + str(self.instructions) + "])}"

class ReturnInstr(File):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(expression: [" + str(self.expression) + "])}"


class Break(File):

    def __init__(self):
        pass

    def __str__(self):
        return "["+ self.__class__.__name__+"]{}"


class Continue(File):

    def __init__(self):
        pass

    def __str__(self):
        return "["+ self.__class__.__name__+"]{}"

class PrintExpression(File):
    def __init__(self, to_print):
        self.to_print = to_print

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(to_print: [" + str(self.to_print) + "])}"


class PrintExpressions(File):
    def __init__(self, print_expressions, print_expression) -> None:
        self.print_expression = print_expression
        self.print_expressions = print_expressions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(print_expression: [" + str(self.print_expression) +"]), (print_expressions: [" + str(self.print_expressions) + "])}"


class UnExpr(File):
    def __init__(self, expression, operator):
        self.expression = expression
        self.operator = operator

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(expression: [" + str(self.expression) + "]), (operator: [" + str(self.operator) +"])}"


class InstructionBlock(File):
    def __init__(self, instructions):
        self.instructions = instructions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(instructions: [" + str(self.instructions) + "])}"


class If_Else_If(File):
    def __init__(self, condition, instructions, elseif_instructions):
        self.elseif_instructions = elseif_instructions
        self.instructions = instructions
        self.condition = condition

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(elseif_instructions: [" + str(self.elseif_instructions) + "]), (instructions: [" + str(self.instructions) + "]), (condition: [" + str(self.condition) + "])}"


class If_Else_if_Else(File):
    def __init__(self, condition, instructions, elseif_instructions,
                 else_instructions):
        self.instructions = instructions
        self.condition = condition
        self.elseif_instructions = elseif_instructions
        self.else_instructions = else_instructions

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(instructions: [" + str(self.instructions) + "]), (condition: [" + str(self.condition) +"]), (elseif_instructions: [" + str(self.elseif_instructions) + "]), (else_instructions: [" + str(self.else_instructions) + "])" + "])}"


class ElIfBlock(File):
    def __init__(self, condition, instructions, elif_block):
        self.condition = condition
        self.instructions = instructions
        self.elif_block = elif_block

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(condition: [" + str(self.condition) + "]), (instructions: [" + str(self.instructions) + "]), (elif_block: [" + str(self.elif_block) + "])}"


class ForInstruction(File):

    def __init__(self, range, instruction_block):
        self.range = range
        self.instruction_block = instruction_block

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(range: [" + str(self.range) + "]), (instruction_block: [" + str(self.instruction_block) + "])}"


class Range(File):
    def __init__(self, variable, from_limit, to_limit):
        self.variable = variable
        self.from_limit = from_limit
        self.to_limit = to_limit

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(variable: [" + str(self.variable) + "]), (from_limit: [" + str(self.from_limit) + "]), (to_limit: [" + str(self.to_limit) + "])}"


class MatrixInitializer(File):
    def __init__(self, rows, row):
        self.rows = rows
        self.row = row

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(rows: [" + str(self.rows) + "]), (row: [" + str(self.row) +"])}"


class MatrixReference(File):

    def __init__(self, matrix_id, location):
        self.matrix_id = matrix_id
        self.location = location

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(matrix_id: [" + str(self.matrix_id) + "]), (location: [" + str(self.location) +"])}"


class MatrixLocations(File):

    def __init__(self, dim_locations, location):
        self.dim_locations = dim_locations
        self.location = location

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(dim_locations: [" + str(self.dim_locations) + "]), (location: [" + str(self.location) +"])}"


class ZerosInitFun(File):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(expression: [" + str(self.expression) + "])}"


class OnesInitFun(File):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(expression: [" + str(self.expression) + "])}"


class EyeInitFun(File):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return "["+ self.__class__.__name__+"]{(expression: [" + str(self.expression) + "])}"
