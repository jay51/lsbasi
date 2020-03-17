from ast import AST 
from tokens import Tokens


class AST:
    pass



class UnaryOp(AST):
    def __init__(self, op, expr):
        self.op = op 
        self.token = op
        self.expr = expr



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


class Compound(AST):
    """ Represents a 'BEGIN ... END block """
    def __init__(self):
        self.children = []



class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.token = op
        self.right = right



class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value



class NoOp(AST):
    pass



class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()


    def error(self):
        raise Exception("Invalid Syntax")



    def eat(self, token_type):
        # print(f"curr: {self.current_token}, token_type: {token_type}")
        if(self.current_token.type == token_type):
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    

    # PARSING PROGRAM TO COMPOUND STATMENTS (part 9)
    def program(self):
        """ program: compound_statement DOT """
        node = self.compound_statement()
        self.eat(Tokens.DOT)
        return node



    def compound_statement(self):
        """ compound_statement: BEGIN statement_list END """
        self.eat(Tokens.BEGIN.type)
        nodes = self.statement_list()
        self.eat(Tokens.END.type)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root


    def statement_list(self):
        """
            statement_list: statement
                            | statement SEMI statement_list
        """

        node = self.statement()
        results = [node]

        while self.current_token.type == Tokens.SEMI:
            self.eat(Tokens.SEMI)
            results.append(self.statement())

        if self.current_token.type == Tokens.ID:
            self.error()

        return results


    def statement(self):
        """
            statement: compound_statement
                        | assignment_statement
                        | empty
        """

        if self.current_token.type == Tokens.BEGIN.type:
            node = self.compound_statement()
        elif self.current_token.type == Tokens.ID:
            node = self.assignment_statement()
        else:
            node = self.empty()

        return node


    def assignment_statement(self):
        """ assignment_statement: variable ASSIGN expr """
        
        # print(self.current_token)
        left = self.variable() # Var(Token(ID, <name>))
        token = self.current_token
        self.eat(Tokens.ASSIGN)
        right = self.expr()

        node = Assign(left, token, right)
        return node
    

    def variable(self):
        """ variable: ID """

        node = Var(self.current_token)
        self.eat(Tokens.ID)
        return node


    def empty(self):
        return NoOp()


    # PARSING NUMBERS AND EXPRESSIONS (part 7-8)
    def factor(self):
        """ factor : PLUS  factor
                    | MINUS factor
                    | INTEGER
                    | LPAREN expr RPAREN
                    | variable
        """

        token = self.current_token
        if(token.type == Tokens.PLUS):
            self.eat(Tokens.PLUS)
            node = UnaryOp(token, self.factor())
            return node

        if(token.type == Tokens.MINUS):
            self.eat(Tokens.MINUS)
            node = UnaryOp(token, self.factor())
            return node

        if(token.type == Tokens.INTEGER):
            self.eat(Tokens.INTEGER)
            return Num(token)

        elif(token.type == Tokens.LPAREN):
            self.eat(Tokens.LPAREN)
            node = self.expr()
            self.eat(Tokens.RPAREN)
            return node

        else:
            node = self.variable()
            return node



    def term(self):
        """ do MUL, DIV before PLUS, MINUS ..."""
        node = self.factor()

        while(self.current_token.type in (Tokens.MUL, Tokens.DIV)):
            token = self.current_token
            if(token.type == Tokens.MUL):
                self.eat(Tokens.MUL)
            elif(token.type == Tokens.DIV):
                self.eat(Tokens.DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node



    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while(self.current_token.type in (Tokens.PLUS, Tokens.MINUS)):
            token = self.current_token
            if(token.type == Tokens.PLUS):
                self.eat(Tokens.PLUS)
            else:
                self.eat(Tokens.MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node


    def parse(self):
        node = self.program()
        if self.current_token.type != Tokens.EOF:
            self.error() # program should end at "END ."

        return node





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
