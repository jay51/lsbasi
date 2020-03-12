from ast import AST 

from tokens import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF


class AST:
    pass





class BinOp(AST):
    
        def __init__(self, left, op, right):
            self.left = left
            self.token = op
            self.op = op
            self.right = right



class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value



class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()


    def error(self):
        raise Exception("Invalid Syntax")



    def eat(self, token_type):
        if(self.current_token.type == token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()


    def factor(self):
        token = self.current_token
        if(token.type == INTEGER):
            self.eat(INTEGER)
            return Num(token)

        elif(token.type == LPAREN):
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node


    def term(self):
        """ do MUL, DIV before PLUS, MINUS ..."""
        node = self.factor()

        while(self.current_token.type in (MUL, DIV)):
            token = self.current_token
            if(token.type == MUL):
                self.eat(MUL)
            elif(token.type == DIV):
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node



    # THIS FUNCTION COULD RECURSIVELY CALL ITSELF
    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while(self.current_token.type in (PLUS, MINUS)):
            token = self.current_token
            if(token.type == PLUS):
                self.eat(PLUS)
            else:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


    def parse(self):
        return self.expr()





"""
Example of AST 
mul_node = BinOp(
    left=Num(Token(INTEGER, 2)),
    op=Token(MUL, "*"),
    right=Num(Token(INTEGER, 7))
)


add_node = BinOp(
    left=mul_node,
    op=Token(PLUS, "+"),
    right=Num(Token(INTEGER, 3))
)
"""
