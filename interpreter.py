
from types import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF
from lexer import Lexer
from parser import Parser


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

    def visit_BinOp(self, node):
        if(node.op.type == PLUS):
            return self.visit(node.left) + self.visit(node.right)
        elif(node.op.type == MINUS):
            return self.visit(node.left) - self.visit(node.right)
        elif(node.op.type == MUL):
            return self.visit(node.left) * self.visit(node.right)
        elif(node.op.type == DIV):
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
    # TREE IS A BINOP NODE OF LEFT AND RIGHT NODES
        tree = self.parser.parse()
        return self.visit(tree)




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







