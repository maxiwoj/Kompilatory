#!/usr/bin/python
import sys
from symtable import Symbol

from Lab4 import classes
from Lab4.Symbol_Table import SymbolTable, UndefinedVariableException, \
    VariableSymbol
from Lab4.types_definitions import *


class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        elif node is None:
            return
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, classes.Node):
                            self.visit(item)
                elif isinstance(child, classes.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    # def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)


class TypeChecker(NodeVisitor):

    def __init__(self) -> None:
        self.table = SymbolTable(None, "root")

    def visit_Node(self, node):
        return self.visit(node.instructions)

    def visit_BinExpr(self, node):
        # alternative usage,
        # requires definition of accept method in class Node
        type1 = self.visit(node.left)  # type1 = node.left.accept(self)
        type2 = self.visit(node.right)  # type2 = node.right.accept(self)
        op = node.op
        try:
            return_type = conclude_bin_expr_type(type1, type2, op, node.position)
            return return_type
        except (MissingDefinitionException, IncompatibleTypesException, WrongDimensionException) as e:
            print(e.message)


    def visit_UnExpr(self, node):
        if node.operator == '-':
            return self.visit(node.expression)
        else:
            var_type = self.visit(node.expression)
            if isinstance(var_type, Scalar):
                IncompatibleTypesException(
                    'Operation ' + node.operator + 'is allowed only on matrixes')
            var_type.dimensions = list(reversed(var_type.dimensions))
            return var_type

    def visit_Int(self, node):
        return Constant(INT, node.value)

    def visit_String(self, node):
        return Constant(STRING, node.value)

    def visit_Float(self, node):
        return Constant(FLOAT, node.value)

    def visit_Variable(self, node):
        try:
            definition = self.table.get(node.id, node.position)
            return definition.type
        except UndefinedVariableException as e:
            print(e.message)
            return Type(UNDEFINED)

    def visit_Assignment(self, node):
        expression_type = self.visit(node.expression)
        if node.assignType == '=':
            self.table.put(node.variable.id, VariableSymbol(node.variable.id,
                                                            expression_type))
        else:
            try:
                variable = self.table.get(node.variable.id, node.variable.position)
                self.table.put(variable.name,
                               VariableSymbol(variable.name,
                                              conclude_bin_expr_type(variable.type,
                                                                     expression_type,
                                                                     assignOperationMap[node.assignType], node.position)))
            except UndefinedVariableException:
                raise UndefinedVariableException(
                    "Variable " + node.variable + " referenced brefore assignment", node.position)

        return expression_type

    def visit_Rows(self, node):
        row_lengths = []
        row_types = []
        # if len(node.row_list) == 0: # this won't be passed through parser
        #     raise WrongDimensionException(
        #         "Matrix's dimension has to be greater than 0")
        for row in node.row_list:
            row_type, row_length = self.visit(row)
            row_types.append(row_type.type) # Row type is of type Scalar
            row_lengths.append(row_length)
        if len(set(row_lengths)) != 1:
            raise WrongDimensionException(
                "Row lengths cannot vary in one matrix", node.position)
        if len(set(row_types)) != 1:
            raise InconsistentTypesException("Matrix has to be of one type", node.position)

        matrix_dim = [len(row_lengths), row_lengths[0]]
        return Matrix(row_types[0], matrix_dim)

    def visit_Row(self, node):
        types = []
        # if len(node.expr_list) == 0: # This won't be passed through parser
        #     raise WrongDimensionException(
        #         "Matrix's dimension has to be greater than 0")
        for expr in node.expr_list:
            types.append(self.visit(expr))
        if len(set(map(lambda x: x.type, types))) != 1:
            raise InconsistentTypesException(
                "Matrix has to be of one type expressions", node.position)
        else:
            return types[0], len(types)

    def visit_MatrixInitializer(self, node):
        try:
            type = self.visit(node.rows)
            return type
        except (WrongDimensionException, InconsistentTypesException) as e:
            print(e.message)
        return Matrix(UNDEFINED, [sys.maxsize, sys.maxsize])

    def visit_MatrixLocations(self, node):
        locations = []
        expression_type = self.visit(node.location)
        if expression_type.type == INT:
            if isinstance(expression_type, Constant):
                locations.append(expression_type.value)
            else:
                locations.append(None)
        else:
            raise IncompatibleTypesException(
                "Matrix reference/dimension has to be of type INT", node.position)

        rest_locations = self.visit(node.dim_locations)
        if type(rest_locations) == list:
            locations += rest_locations

        elif rest_locations.type == INT:
            if isinstance(rest_locations, Constant):
                locations.append(rest_locations.value)
            else:
                locations.append(None)
        else:
            raise IncompatibleTypesException(
                "Matrix reference/dimension has to be of type INT", node.position)

        return locations

    def visit_MatrixReference(self, node):
        global matrix_type
        try:
            matrix_type = self.table.get(node.matrix_id, node.position).type
            locations = self.visit(node.locations)
            if not isinstance(matrix_type, Matrix):
                raise IncompatibleTypesException(
                    'Variable ' + node.matrix_id + ' is not a matrix', node.position)
            if len(matrix_type.dimensions) != len(locations):
                raise WrongDimensionException(
                    "Reference does not match matrix dimension", node.position)
            for i, location in enumerate(locations):
                if location is not None:
                    if location >= matrix_type.dimensions[i]:
                        raise WrongDimensionException(
                            "Matrix dimension is smaller than referenced", node.position)
            return Scalar(matrix_type.type)
        except IncompatibleTypesException as e:
            print(e.message)
            return Scalar(matrix_type.type)
        except UndefinedVariableException as e:
            print(e.message)
            return Scalar(UNDEFINED)

    def visit_ZerosInitFun(self, node):
        try:
            in_type = self.visit(node.expression)
            if in_type.type != INT:
                raise IncompatibleTypesException('Matrix size has to be an INT', node.position)
            if isinstance(in_type, Constant):
                return Matrix(INT, [in_type.value, in_type.value])
        except IncompatibleTypesException as e:
            print(e.message)
        return Matrix(INT, [sys.maxsize, sys.maxsize])

    def visit_EyeInitFun(self, node):
        try:
            in_type = self.visit(node.expression)
            if in_type.type != INT:
                raise IncompatibleTypesException('Matrix size has to be an INT', node.position)
            if isinstance(in_type, Constant):
                return Matrix(INT, [in_type.value, in_type.value])
        except IncompatibleTypesException as e:
            print(e.message)
        return Matrix(INT, [sys.maxsize, sys.maxsize])

    def visit_OnesInitFun(self, node):
        try:
            in_type = self.visit(node.expression)
            if in_type.type != INT:
                raise IncompatibleTypesException('Matrix size has to be an INT', node.position)
            if isinstance(in_type, Constant):
                return Matrix(INT, [in_type.value, in_type.value])
        except IncompatibleTypesException as e:
            print(e.message)
        return Matrix(INT,[sys.maxsize, sys.maxsize])

    def visit_Range(self, node):
        if self.visit(node.from_limit) != INT or self.visit(
                node.to_limit) != INT:
            raise IncompatibleTypesException("Range arguments must be of type int", node.position)
        return Range(node.from_limit, node.to_limit)

    def visit_ForInstruction(self, node):
        try:
            range = self.visit(node.range)
            if range.type != RANGE:
                raise IncompatibleTypesException("Range must be of type range and is: " + range.type)
        except IncompatibleTypesException as e:
            print(e.message)
        self.table = self.table.pushScope('for')
        self.table.put(node.var, VariableSymbol(node.var, Scalar(INT)))
        self.visit(node.instruction_block)
        self.table = self.table.popScope()
        return None

    def visit_IfElse(self, node):
        if self.visit(node.condition).type != INT:
            raise WrongConditionTypeException('Condition must be a boolean condition!', node.position)
        self.table = self.table.pushScope('IfElse_If')
        self.visit(node.instructions)
        self.table = self.table.popScope()
        self.table = self.table.pushScope('IfElse_Else')
        self.visit(node.else_instructions)
        self.table = self.table.popScope()

    def visit_If(self, node):
        if self.visit(node.condition).type != INT:
            raise WrongConditionTypeException('Condition must be a boolean condition!', node.position)
        self.visit(node.instructions)

    def visit_While(self, node):
        if self.visit(node.condition).type != INT:
            raise WrongConditionTypeException('Condition must be a boolean condition!', node.position)

        self.visit(node.instructions)

    def visit_Continue(self, node):
        if self.table.popScope() is None:
            raise MissplacedInstructionException(
                'Continue Instruction can\'t be placed outside instruction Block', node.position)

    def visit_Break(self, node):
        if self.table.popScope() is None:
            raise MissplacedInstructionException(
                'Break Instruction can\'t be placed outside instruction Block', node.position)

    def visit_ReturnInstr(self, node):
        if self.table.popScope() is None:
            raise MissplacedInstructionException(
                'Return instruction can\'t be placed outside instruction Block', node.position)

    def visit_InstructionBlock(self, node):
        self.visit(node.instructions)

    def visit_PrintExpressions(self, node):
        return [self.visit(node.expression)] + self.visit(node.expressions)

    def visit_PrintExpression(self, node):
        return [self.visit(node.to_print)]

    def visit_PrintInstr(self, node):
        self.visit(node.value)

    def visit_Instructions(self, node):
        try:
            self.visit(node.instructions)
            self.visit(node.instruction)
        except TypeException as e:
            print(e.message)
