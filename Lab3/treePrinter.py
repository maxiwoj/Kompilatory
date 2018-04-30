from Lab3 import classes

indent_char = '|   '
print_types = False


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


### konwencja jest taka, ze to kazdy Node powinien zrobic nowa linie
### przy wypisywaniu sie (parent nie musi sie o to troszczyc)
class TreePrinter:
    @addToClass(classes.Node)
    def printTree(self, indent=0):
        res = indent_char * indent
        res += self.instructions.printTree(indent)
        return res

    @addToClass(classes.BinExpr)
    def printTree(self, indent=0):
        res = indent * indent_char + str(self.op) + '\n'
        res += self.left.printTree(indent + 1) if isinstance(self.left, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.left) + "\n"
        res += self.right.printTree(indent + 1) if isinstance(self.right,  (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.right) + "\n"
        return res

    @addToClass(classes.UnExpr)
    def printTree(self, indent=0):
        res = ""
        res += indent * indent_char + str(self.operator) + '\n'
        res += self.expression.printTree(indent + 1) if isinstance(self.expression, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.expression) + "\n"
        return res

    @addToClass(classes.Variable)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + str(self.value) + '\n'
        return res

    @addToClass(classes.MatrixReference)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + 'REF\n'
        res += (indent + 1) * indent_char + str(self.matrix_id) + '\n'
        res += self.locations.printTree(indent + 1)
        return res

    @addToClass(classes.MatrixLocations)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + self.dim_locations.printTree(indent) if issubclass(self.dim_locations.__class__,
                                                                                        classes.Node) else indent * indent_char + str(
            self.dim_locations) + '\n'
        res += indent * indent_char + self.location.printTree(indent) if issubclass(self.dim_locations.__class__,
                                                                                    classes.Node) else indent * indent_char + str(
            self.location) + '\n'
        return res

    @addToClass(classes.EndAssignment)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + str(self.assignType) + "\n"
        res += self.variable.printTree(indent + 1)
        res += self.expression.printTree(indent + 1) if issubclass(self.expression.__class__, classes.Node) else ((indent + 1) * indent_char) + str(self.expression) + '\n'
        return res

    @addToClass(classes.MiddleAssignment)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + str(self.assignType) + "\n"
        res += self.variable.printTree(indent + 1)
        res += self.assignment.printTree(indent + 1)
        return res

    @addToClass(classes.PrintInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "PRINT\n"
        res += self.value.printTree(indent + 1)
        return res

    @addToClass(classes.PrintExpressions)
    def printTree(self, indent=0):
        res = self.print_expressions.printTree(indent)
        res += self.print_expression.printTree(indent)
        return res

    @addToClass(classes.PrintExpression)
    def printTree(self, indent=0):
        res = self.to_print.printTree(indent) if isinstance(self.to_print,
                                                            (classes.UnExpr, classes.BinExpr, classes.Variable,
                                                             classes.MatrixReference, classes.PrintExpression)) \
            else (indent) * indent_char + str(self.to_print) + "\n"
        return res

    @addToClass(classes.ReturnInstr)  # doesn't work because of printing expression, when expresion is number(int)
    def printTree(self, indent=0):
        res = indent * indent_char + "RETURN\n"
        res += self.expression.printTree(indent + 1) if isinstance(self.expression, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.expression) + "\n"
        return res

    @addToClass(classes.Break)  # works fine
    def printTree(self, indent=0):
        return indent * indent_char + " BREAK\n"

    @addToClass(classes.Continue)  # works fine
    def printTree(self, indent=0):
        return indent * indent_char + " CONTINUE\n"

    @addToClass(classes.ForInstruction)     #work almost fine: range is not working because of expression
    def printTree(self, indent=0):
        res = ""
        res += indent * indent_char + "FOR" + "\n"
        res += (indent + 1) * indent_char + str(self.var) + "\n"
        res += self.range.printTree(indent + 1)
        res += self.instruction_block.printTree(indent + 1)
        return res

    @addToClass(classes.While)      #works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "WHILE\n"
        res += self.condition.printTree(indent + 1)
        res += self.instructions.printTree(indent + 1)
        return res

    @addToClass(classes.If)         #works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.condition.printTree(indent + 1)
        res += indent * indent_char + "THEN\n"
        res += self.instructions.printTree(indent + 1)
        return res

    @addToClass(classes.IfElse)     #work fine
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.condition.printTree(indent + 1)
        res += indent * indent_char + "THEN\n"
        res += self.instructions.printTree(indent + 1)
        res += indent * indent_char + "ELSE\n"
        res += self.else_instructions.printTree(indent + 1)
        return res

    @addToClass(classes.Instructions)  # works fine
    def printTree(self, indent=0):
        res = ""
        res += self.instructions.printTree(indent) if issubclass(self.instructions.__class__, classes.Node) else indent * indent_char + str(self.instructions) + '\n'
        res += self.instruction.printTree(indent)
        return res

    @addToClass(classes.Range)
    def printTree(self, indent=0):
        res = indent * indent_char + "RANGE\n"
        res += self.from_limit.printTree(indent+1) if isinstance(self.from_limit, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference)) \
            else (indent + 1) * indent_char + str(self.from_limit) + "\n"
        res += self.to_limit.printTree(indent + 1) if isinstance(self.to_limit,
                                                                 (classes.UnExpr, classes.BinExpr, classes.Variable,
                                                                  classes.MatrixReference)) \
            else (indent + 1) * indent_char + str(self.to_limit) + "\n"
        return res

    @addToClass(classes.MatrixInitializer)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "MATRIX\n"
        res += self.rows.printTree(indent + 1)
        return res

    @addToClass(classes.Rows)  # works fine
    def printTree(self, indent=0):
        res = ""
        for row in self.row_list:
            res += indent * indent_char + "VECTOR\n"
            for el in row.int_list:
                res += (indent + 1) * indent_char + str(el) + '\n'
        return res

    @addToClass(classes.OnesInitFun)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "ones\n"
        res += self.expression.printTree(indent + 1) if isinstance(self.expression, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.expression) + "\n"
        return res

    @addToClass(classes.ZerosInitFun)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "zeros\n"
        res += self.expression.printTree(indent + 1) if isinstance(self.expression, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.expression) + "\n"
        return res

    @addToClass(classes.EyeInitFun)  # works fine
    def printTree(self, indent=0):
        res = indent * indent_char + "eye\n"
        res += self.expression.printTree(indent + 1) if isinstance(self.expression, (classes.UnExpr, classes.BinExpr, classes.Variable, classes.MatrixReference))\
            else (indent + 1) * indent_char + str(self.expression) + "\n"
        return res
