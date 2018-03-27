import AST

import classes

indent_char = '| '
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
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(classes.BinExpr)
    def printTree(self, indent=0):
        res = indent_char * indent
        res += self.op + '\n'
        res += self.left.printTree(indent + 1) if isinstance(self.left, (classes.Expression, classes.Const))\
            else indent_char * (indent + 1) + self.left
        res += self.right.printTree(indent + 1) if isinstance(self.right, (classes.Expression, classes.Const))\
            else indent_char * (indent + 1) + self.right
        return res

    @addToClass(classes.Assignment)
    def printTree(self, indent=0):
        res = indent * indent_char + "=\n"
        res += indent_char * (indent + 1) + self.var + "\n"
        res += self.expr.printTree(indent + 1) if isinstance(self.expr, (classes.Expression, classes.Const))\
            else indent_char * (indent + 1) + self.expr
        return res

    @addToClass(classes.Break)
    def printTree(self, indent=0):
        return indent * indent_char + " BREAK\n"

    @addToClass(classes.Continue)
    def printTree(self, indent=0):
        return indent * indent_char + " CONTINUE\n"

    @addToClass(classes.Variable)
    def printTree(self, indent=0):
        res = indent * indent_char
        res += self.id + '\n'
        return res

    @addToClass(classes.If)
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        return res

    @addToClass(classes.IfElse)
    def printTree(self, indent=0):
        res = indent * indent_char + "IF\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        res += indent * indent_char + "ELSE\n"
        res += self.elseinstr.printTree(indent + 1)
        return res

    @addToClass(classes.While)
    def printTree(self, indent=0):
        res = indent * indent_char + "WHILE\n"
        res += self.cond.printTree(indent + 1)
        res += self.instr.printTree(indent + 1)
        return res

    @addToClass(classes.ReturnInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "RETURN\n"
        res += self.expr.printTree(indent + 1) if isinstance(self.expr, (classes.Expression, classes.Const))\
            else (indent + 1) * indent_char + self.expr
        return res

    @addToClass(classes.PrintInstr)
    def printTree(self, indent=0):
        res = indent * indent_char + "PRINT\n"
        res += self.to_print.printTree(indent + 1) if isinstance(self.to_print, (classes.Expression, classes.Const))\
            else (indent + 1) * indent_char + self.to_print
        return res

    @addToClass(classes.Instructions)
    def printTree(self, indent=0):
        res = ""
        for i in self.instructions:
            res += i.printTree(indent)
        return res