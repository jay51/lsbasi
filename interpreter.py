#!/usr/bin/env python3

from tokens import Tokens
from lexer import Lexer
from parser import Parser

import sys


class Symbol:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class ButiltinTypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return self.name

    __repr__ = __str__



class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

    def __str__(self):
        return "<{name}:{type}>".format(name=self.name, type=self.type)

    __repr__ = __str__


class SymbolTable:
    def __init__(self):
        self._symbols = dict()
        self.init_builtins()

    def __str__(self):
        s = "Symbols:{symbols}".format(symbols=[value for value in self._symbols.values()])
        return s

    __repr__ = __str__


    def init_builtins(self):
        self.define(ButiltinTypeSymbol("INTEGER"))
        self.define(ButiltinTypeSymbol("REAL"))



    def define(self, symbol):
        print("Define: %s" % symbol)
        self._symbols[symbol.name] = symbol


    def lookup(self, name):
        print("lookup: %s" % name)
        return self._symbols.get(name)




class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))




class SymbolTableBuilder(NodeVisitor):
    def __init__(self):
        self.symtab = SymbolTable()


    def visit_Program(self, node):
        self.visit(node.block)


    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)


    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)


    def visit_Type(self, node):
        pass


    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)


    def visit_NoOp(self, node):
        pass


    def visit_Var(self, node):
        var_name = node.value
        # val = self.GLOBAL_SCOPE.get(var_name)
        var_symbol = self.symtab.lookup(var_name)
        if not var_symbol:
            raise NameError(repr(var_name))



    def visit_Assign(self, node):
        var_name = node.left.value
        # self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        var_symbol = self.symtab.lookup(var_name)
        if not var_symbol:
            raise NameError(repr(var_name))

        self.visit(node.right)



    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)


    def visit_UnaryOp(self, node):
        self.visit(node.expr)


    def visit_Num(self, node):
        pass



    def visit_ProcedureDecl(self, node):
        pass





class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
        self.GLOBAL_SCOPE = dict()


    def visit_Program(self, node):
        self.visit(node.block)


    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

        self.visit(node.compound_statement)


    def visit_VarDecl(self, node):
        pass


    def visit_ProcedureDecl(self, node):
        pass


    def visit_Type(self, node):
        pass


    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)


    def visit_NoOp(self, node):
        pass


    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val:
            return val

        raise NameError(repr(var_name))


    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)


    def visit_BinOp(self, node):
        if(node.op.type == Tokens.PLUS):
            return self.visit(node.left) + self.visit(node.right)
        elif(node.op.type == Tokens.MINUS):
            return self.visit(node.left) - self.visit(node.right)
        elif(node.op.type == Tokens.MUL):
            return self.visit(node.left) * self.visit(node.right)
        elif(node.op.type == Tokens.FLOATDIV):
            return self.visit(node.left) / self.visit(node.right) # float DIV
        elif(node.op.type == Tokens.DIV.type):
            return self.visit(node.left) // self.visit(node.right)

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == Tokens.PLUS:
            return +self.visit(node.expr)
        elif op == Tokens.MINUS:
            return -self.visit(node.expr)


    def visit_Num(self, node):
        return node.value


    def interpret(self):
    # TREE IS A BINOP NODE OF LEFT AND RIGHT NODES
        tree = self.tree
        if tree:
            return self.visit(tree)



if(__name__ == "__main__"):
    if(len(sys.argv) == 2):
        print(sys.argv[1])
        with open(sys.argv[1], "r") as f:
            file_stream = f.read()
            lex = Lexer(file_stream)
            parser = Parser(lex)
            tree = parser.parse()
            symtab_builder = SymbolTableBuilder()
            symtab_builder.visit(tree)
            print("Symbol Table contents:")
            print(symtab_builder.symtab)



            interpreter = Interpreter(tree)
            result = interpreter.interpret()
            print("MEMORY contents:")
            print(interpreter.GLOBAL_SCOPE)


    else:
        while True:
            text = input("cal> ")
            if(text == "exit"):
                break
            else:
                lex = Lexer(text) # make tokens 
                parser = Parser(lex) # make AST from tokens
                interpreter = Interpreter(parser) # interpret AST
                result = interpreter.interpret()
                print(result)


