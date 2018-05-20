#!/usr/bin/python
from symtable import Symbol

from Lab4.types_definitions import TypeException


class VariableSymbol(Symbol):

    def __init__(self, name, type):
        self.type = type
        self.name = name
    #


class UndefinedVariableException(TypeException):
    def __init__(self, message):
        self.message = message

class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.name = name
        self.parent = parent
        self.symbols = {}
        self.child_scopes = []

    #

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol

    #

    def get(self, name):  # get variable symbol or fundef from <name> entry
        variable = self.symbols.get(name)
        if variable:
            return variable
        else:
            if self.parent is not None:
                return self.parent.get(name)
            else:
                raise UndefinedVariableException(
                    "Variable " + name + " is not defined")

    #

    def getParentScope(self):
        return self.parent

    #

    def pushScope(self, name):
        return SymbolTable(self, name)

    #

    def popScope(self):
        return self.parent
    #
