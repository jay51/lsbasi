#!/usr/bin/env python3

from tokens import Tokens
from lexer import Lexer
from parser import Parser

import sys

class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))



class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = dict()

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
        tree = self.parser.parse()
        return self.visit(tree)



if(__name__ == "__main__"):
    if(len(sys.argv) == 2):
        print(sys.argv[1])
        with open(sys.argv[1], "r") as f:
            file_stream = f.read()
            lex = Lexer(file_stream)
            parser = Parser(lex)
            interpreter = Interpreter(parser)
            result = interpreter.interpret()
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


