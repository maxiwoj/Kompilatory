import numpy as np
import sys
import operator
# from Lab5.Memory import *

from Lab4 import classes
from Lab5.visit import *

def multiply(a,b):
    return
bin_ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "DOTADD": operator.add,
    "DOTSUB": operator.sub,
    "DOTMUL": np.multiply,
    "DOTDIV": np.divide,
    "<": operator.lt,
    ">": operator.gt,
    "LEQ": operator.le,
    "GEQ": operator.ge,
    "EQUAL": operator.eq,
    "NOTEQ": operator.ne,
}
un_ops = {
    "NEGATION": operator.neg,
    "TRANSPOSE": np.transpose
}

sys.setrecursionlimit(10000)

class Interpreter(object):


    @on('node')
    def visit(self, node):
        pass

    @when(classes.Instructions)
    def visit(self, node):
        node.instructions.accept(self)
        node.instruction.accept(self)

    @when(classes.InstructionBlock)
    def visit(self, node):
        return node.instructions.accept(self)


    @when(classes.PrintInstr)
    def visit(self, node):
        print(node.value.accept(self))


    @when(classes.PrintExpression)
    def visit(self, node):
        return (node.to_print.accept(self),)

    @when(classes.PrintExpressions)
    def visit(self, node):
        return node.print_expression.accept(self) + node.print_expressions.accept(self)

    @when(classes.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return bin_ops[node.op](r1, r2)


    @when(classes.UnExpr)
    def visit(self, node):
        r1 = node.expression.accept(self)
        return un_ops[node.operator](r1)

    @when(classes.Variable)
    def visit(self, node):
    #     TODO: PUSH VARIABLE
    pass

    @when(classes.Assignment)
    def visit(self, node):
    # TODO
    pass

    @when(classes.Range)
    def visit(self, node):
        return range(node.from_limit.accept(self), node.to_limit.accept(self))

    @when(classes.ForInstruction)
    def visit(self, node):
        rangge = node.range.accept(self)
    #     TODO: Push scope
        for i in rangge:
        # TODO: add variable as range //don't know if it's OK
        #     node.var.id <- i

            node.instruction_block.accept(self)



    # simplistic while loop interpretation
    @when(classes.While)
    def visit(self, node):
        r = None
        while node.condition.accept(self):
            r = node.instructions.accept(self)
        return r


    @when(classes.If)
    def visit(self, node):
        # TODO: Push scope
        r = None
        if node.condition.accept(self):
            r = node.instruction.accept(self)
        return r


    @when(classes.IfElse)
    def visit(self, node):
        # TODO: Push scope
        r = None
        if node.condition.accept(self):
            r = node.instructions.accept(self)
        else:
            r = node.else_instructions.accept(self)
        return r

    @when(classes.ReturnInstr)
    def visit(self, node):
        return node.expression.accept(self)

    @when(classes.Break)
    def visit(self, node):
#         TODO: Pop scope
        pass

    @when(classes.Continue)
    def visit(self, node):
#         TODO: Pop scope
        pass

    @when(classes.Int)
    def visit(self, node):
        return node.value

    @when(classes.String)
    def visit(self, node):
        return node.value

    @when(classes.Float)
    def visit(self, node):
        return node.value

    @when(classes.ZerosInitFun)
    def visit(self, node):
        r = node.expression.accept(self)
        return np.zeros((r,r))

    @when(classes.OnesInitFun)
    def visit(self, node):
        r = node.expression.accept(self)
        return np.ones((r, r))

    @when(classes.EyeInitFun)
    def visit(self, node):
        r = node.expression.accept(self)
        return np.eye(r)

    @when(classes.MatrixInitializer)
    def visit(self, node):
        return np.array(node.rows.accept(self))

    @when(classes.Rows)
    def visit(self, node):
        return node.row_list

    @when(classes.MatrixLocations)
    def visit(self, node):
        loc = node.location.accept(self)
        locs = node.dim_locations.accept(self)
        # TODO: Change this
        if type(locs) != tuple:
            locs = (locs, )
        return (loc, ) + locs

    @when(classes.MatrixReference)
    def visit(self, node):
        location = node.locations.accept(self)
        matrix = None # Memory.get(node.matrix_id)
        return matrix[location]


