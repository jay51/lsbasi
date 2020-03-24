
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Tokens:
    
    INTEGER     = "INTEGER"
    PLUS        = "PLUS"
    MINUS       = "MINUS"
    MUL         = "MUL"
    FLOATDIV    = "DIV"
    LPAREN      = "("
    RPAREN      = ")"
    EOF         = "EOF"
    ID          = "ID"
    ASSIGN      = "ASSIGN"
    SEMI        = "SEMI"
    DOT         = "DOT"
    # RESERVED_KEYWORDS
    BEGIN       = Token("BEGIN", "BEGIN")
    END         = Token("END", "END")
    DIV         = Token("INTDIV", "//")
    
    
    
    
    
    
