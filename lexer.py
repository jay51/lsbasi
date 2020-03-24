from tokens import Token
from tokens import Tokens



class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_char = self.text[self.pos] # inital start


    def __iter__(self):
        return self

    def __next__(self):
        if(self.curr_char is not None):
            return self.get_next_token()
        else:
            raise StopIteration


    def advance(self):
        """ get the next char in input string """
        self.pos += 1
        if(self.pos > len(self.text) -1):
            # end of input
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]


    def peek(self):
        peek_pos = self.pos + 1
        if(peek_pos > len(self.text)-1):
            return None
        return self.text[peek_pos]


    def skip_whitespace(self):
        """ get the next char in input that is not white sapce """
        while(self.curr_char is not None and self.curr_char.isspace()):
            self.advance()


    def integer(self):
        """ return (multidigit) int from input """
        number = ""
        while(self.curr_char is not None and self.curr_char.isdigit()):
            number += self.curr_char
            self.advance()

        return int(number)


    def _id(self):
        """ handel identifiers and reserved keywords """
        result = ""
        while(self.curr_char is not None and self.curr_char.isalnum()):
            result += self.curr_char
            self.advance()

        # return a Token
        if(hasattr(Tokens, result)):
            return getattr(Tokens, result)

        return Token(Tokens.ID, result)



    def error(self):
        raise Exception("Invalid charactor")


    def get_next_token(self):
        """ tokenizer sentence """

        while(self.curr_char is not None):

            if self.curr_char.isspace():
                self.skip_whitespace()
                continue

            if self.curr_char.isdigit():
                return Token(Tokens.INTEGER, self.integer())

            if self.curr_char == "+":
                self.advance()
                return Token(Tokens.PLUS, "+")

            if self.curr_char == "-":
                self.advance()
                return Token(Tokens.MINUS, "-")

            if self.curr_char == "*":
                self.advance()
                return Token(Tokens.MUL, "*")

            if self.curr_char == "/":
                self.advance()
                return Token(Tokens.FLOATDIV, "/")

            if self.curr_char == "(":
                self.advance()
                return Token(Tokens.LPAREN, "(")

            if self.curr_char == ")":
                self.advance()
                return Token(Tokens.RPAREN, ")")

            if self.curr_char.isalpha():
                return self._id()

            if self.curr_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(Tokens.ASSIGN, ":=")

            if self.curr_char == ";":
                self.advance()
                return Token(Tokens.SEMI, ";")

            if self.curr_char == ".":
                self.advance()
                return Token(Tokens.DOT, ".")


            self.error()

        return Token(Tokens.EOF, None)




# to use the lexer 
# l = Lexer("2 * 3 + 3")
# for token in l:
# or call l.get_next_token()

