import sys
from Mparser import Mparser
import ply.yacc as yacc

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Mparser = Mparser()
    parser = yacc.yacc(module=Mparser)
    text = file.read()
    program = parser.parse(text, lexer=Mparser.scanner)
    print (program)