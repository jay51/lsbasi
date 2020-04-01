
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "Token({type}, {value})".format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()


class Tokens:
    
    INT_CONST   = "INTEGER_CONST"
    REAL_CONST  = "REAL_CONST"
    PLUS        = "PLUS"
    MINUS       = "MINUS"
    MUL         = "MUL"
    FLOATDIV    = "DIV"
    COLON       = ":"
    COMMA       = ","
    LPAREN      = "("
    RPAREN      = ")"
    EOF         = "EOF"
    ID          = "ID"
    ASSIGN      = "ASSIGN"
    SEMI        = "SEMI"
    DOT         = "DOT"
    TERNARY     = "?"

    # RESERVED_KEYWORDS
    PROGRAM     = Token("PROGRAM", "PROGRAM")
    VAR         = Token("VAR", "VAR")
    INTEGER     = Token("INTEGER", "INTEGER") # VAR TYPE
    REAL        = Token("REAL", "REAL") # VAR TYPE
    BEGIN       = Token("BEGIN", "BEGIN")
    END         = Token("END", "END")
    DIV         = Token("INTDIV", "//")
    # DIV         = Token("INTEGER_DIV", "DIV"),
    
    
    
    
    
    
