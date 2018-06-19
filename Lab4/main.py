import sys

import ply.yacc as yacc

from Lab4.Mparser import Mparser
from Lab4.TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/init.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()

    ast = parser.parse(text, lexer=Mparser.scanner)

    # Below code shows how to use visitor
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)
