from ast import AST 
from tokens import Tokens


class AST:
    pass


class NoOp(AST):
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



class Program(AST):
    def __init__(self, name, block):
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement):
        self.declarations = declarations
        self.compound_statement = compound_statement



class VarDecl(AST):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node



class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value



class ProcedureDecl(AST):
    def __init__(self, proc_name, block_node):
        self.proc_name = proc_name
        self.block_node = block_node




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


    def program(self):
        """ program: PROGRAM variable SEMI block DOT"""
        self.eat(Tokens.PROGRAM.type)
        var_node = self.variable()
        prog_name = var_node.value
        self.eat(Tokens.SEMI)

        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(Tokens.DOT)

        return program_node


    def block(self):
        """ block: declarations compound_statement """
        declaration_nodes = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_nodes, compound_statement_node)
        return node


    def declarations(self):
        """ declarations: VAR (variable_declaration SEMI) +
                        | empty
        """
        declarations = []
        if(self.current_token.type == Tokens.VAR.type):
            self.eat(Tokens.VAR.type)

            while(self.current_token.type == Tokens.ID):
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(Tokens.SEMI)


        # parse ProcedureDecl to make AST node
        while(self.current_token.type == Tokens.PROCEDURE.type):
            self.eat(Tokens.PROCEDURE.type)
            proc_name = self.current_token.value
            self.eat(Tokens.ID)
            self.eat(Tokens.SEMI)
            block_node = self.block()
            proc_decl = ProcedureDecl(proc_name, block_node)
            declarations.append(proc_decl)
            self.eat(Tokens.SEMI)

        return declarations



    def variable_declaration(self):
        """ variable_declaration: ID (COMMA ID)* COLON type_spec """
        var_nodes = [ Var(self.current_token) ] # FIRST ID
        self.eat(Tokens.ID)

        # pickup vars seprated by ,
        while(self.current_token.type == Tokens.COMMA):
            self.eat(Tokens.COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(Tokens.ID)

        self.eat(Tokens.COLON)

        type_node = self.type_spec()
        var_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]

        return var_declarations


    # Do we need to eat the ;
    def type_spec(self):
        """ type_spec: INTEGER
                    | REAL
        """
        token = self.current_token
        if(token.type == Tokens.INTEGER.type):
            self.eat(Tokens.INTEGER.type)
        elif(token.type == Tokens.REAL.type):
            self.eat(Tokens.REAL.type)

        node = Type(token)
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
        if self.current_token.type == Tokens.TERNARY:
            self.eat(Tokens.TERNARY)
            # we need to check the value returned from the right expr
            if right.value:
                right = self.expr()
                self.eat(Tokens.COLON)
                self.expr()

            else:
                self.expr()
                self.eat(Tokens.COLON)
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
                    | INTEGER_CONST
                    | REAL_CONST
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

        if(token.type == Tokens.INT_CONST):
            self.eat(Tokens.INT_CONST)
            return Num(token)

        if(token.type == Tokens.REAL_CONST):
            self.eat(Tokens.REAL_CONST)
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
        """ term: factor ((MUL | INTDIV | FLOATDIV) factor """
        node = self.factor()

        while(self.current_token.type in (Tokens.MUL, Tokens.FLOATDIV, Tokens.DIV.type)):
            token = self.current_token
            if(token.type == Tokens.MUL):
                self.eat(Tokens.MUL)

            elif(token.type == Tokens.FLOATDIV):
                self.eat(Tokens.FLOATDIV)

            elif(token.type == Tokens.DIV.type): # INT DIV
                self.eat(Tokens.DIV.type)


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
