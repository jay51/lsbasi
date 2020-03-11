
from types import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()



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
        if(self.pos > len(self.text) -1): # don't know it's len(text) -1
            # end of input
            self.curr_char = None
        else:
            self.curr_char = self.text[self.pos]


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


    def error(self):
        raise Exception("Invalid charactor")


    def get_next_token(self):
        """ tokenizer sentence """

        while(self.curr_char is not None):

            if self.curr_char.isspace():
                self.skip_whitespace()
                continue

            if self.curr_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.curr_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.curr_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.curr_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.curr_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.curr_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.curr_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            self.error()

        return Token(EOF, None)




# to use the lexer 
# l = Lexer("2 * 3 + 3")
# for token in l:
# or call l.get_next_token()

