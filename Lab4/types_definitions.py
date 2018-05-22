from collections import defaultdict


class TypeException(Exception):
    def __init__(self, message, position):
        self.message = str(position) + ': ' + message

RANGE = 'range'
INT = 'float'
STRING = 'string'
FLOAT = 'float'
UNDEFINED = None


class Type:
    def __init__(self, var_type) -> None:
        self.type = var_type


class Matrix(Type):
    def __init__(self, var_type, dimensions) -> None:
        super().__init__(var_type)
        self.dimensions = dimensions


class Scalar(Type):
    def __init__(self, var_type) -> None:
        super().__init__(var_type)

class Constant(Scalar):
    def __init__(self, var_type, value) -> None:
        super().__init__(var_type)
        self.value = value

class Range(Type):
    def __init__(self, from_val, to_val) -> None:
        super().__init__(RANGE)
        self.to_val = to_val
        self.from_val = from_val



class MissingDefinitionException(TypeException):
    pass


class IncompatibleTypesException(TypeException):
    pass


class InconsistentTypesException(TypeException):
    pass


class WrongDimensionException(TypeException):
    pass

class WrongConditionTypeException(TypeException):
    pass

class MissplacedInstructionException(TypeException):
    pass


types_table = defaultdict(
    lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '<', '>', 'LEQ', 'GEQ', 'EQUAL', 'NOTEQ']:
    types_table[op][INT][INT] = INT

# for op in ['+', '-', '*', '/']:
for op in ['+', '-', '*', '/', 'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV']:
    types_table[op][INT][FLOAT] = FLOAT
    types_table[op][FLOAT][INT] = FLOAT
    types_table[op][FLOAT][FLOAT] = FLOAT
for op in ['<', '>', 'LEQ', 'GEQ', 'EQUAL', 'NOTEQ']:
    types_table[op][INT][FLOAT] = INT
    types_table[op][FLOAT][INT] = INT
    types_table[op][FLOAT][FLOAT] = INT
    types_table[op][STRING][STRING] = INT

types_table['+'][STRING][STRING] = STRING
types_table['*'][STRING][INT] = STRING

assignOperationMap = {'ADDASSIGN': '+',
                      'SUBASSIGN': '-',
                      'MULASSIGN': '*',
                      'DIVASSIGN': '/'}


def conclude_bin_expr_type(type1, type2, op, position):
    if type1.type == UNDEFINED:
        type1 = type2
    elif type2.type == UNDEFINED:
        type2 = type1



    if isinstance(type1, Matrix) and isinstance(type2, Matrix):
        if op in ['DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV', '+', '-']:
            if type1.dimensions == type2.dimensions:
                return types_table[op][type1.type][type2.type], type1.dimensions
            else:
                raise WrongDimensionException(
                    'matrixes types are incorrenct for ' + op + ' operation', position)
        elif op == '*':
            if type1.dimensions[1] == type2.dimensions[0]:
                return types_table[op][type1.type][type2.type], [type1.type,
                                                                 type2.dimensions]
            else:
                raise WrongDimensionException(
                    'matrixes types are incorrenct for ' + op + ' operation', position)
        elif op == '/':
            if type1.dimensions[1] == type2.dimensions[0] and type2.dimensions[
                0] == type2.dimensions[1]:
                return types_table[op][type1.type][type2.type], [
                    type1.dimensions[0],
                    type1.dimensions[1]]
            else:
                raise WrongDimensionException(
                    'matrixes types are incorrenct for ' + op + ' operation', position)
        elif op in ['==', '!=']:
            return types_table[op][type1.type][type2.type]
        else:
            raise IncompatibleTypesException(
                'Operator ' + op + ' is not allowed for matrixes', position)

    if isinstance(type1, Scalar) and isinstance(type2, Scalar):
        return types_table[op][type1][type2]


    else:
        if isinstance(type1, Matrix) and op in ['+', '*']:
            return types_table[op][type1.type][type2]
        elif isinstance(type2, Matrix) and op in ['+', '*']:
            return types_table[op][type1][type2.type]

    return types_table[op][type1][type2]
