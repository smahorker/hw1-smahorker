from enum import Enum

class Token(Enum):
    ID = "ID"
    NUM = "NUM"
    HNUM = "HNUM"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    ASSIGN = "ASSIGN"
    INCR = "INCR"
    PLUS = "PLUS"
    MULT = "MULT"
    SEMI = "SEMI"
    IGNORE = "IGNORE"
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    INT = "INT"
    FLOAT = "FLOAT"

class Lexeme:
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value
    
    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

def idy(l: Lexeme) -> Lexeme:
    return l

def key(l: Lexeme) -> Lexeme:
    keywords = {
        "if": Token.IF,
        "else": Token.ELSE,
        "while": Token.WHILE,
        "int": Token.INT,
        "float": Token.FLOAT
    }
    if l.value in keywords:
        return Lexeme(keywords[l.value], l.value)
    return l

tokens = [
    (Token.ID, r"[a-zA-Z][a-zA-Z0-9]*", key),
    (Token.NUM, r"[0-9]+(\.[0-9]+)?|\.[0-9]+", idy),
    (Token.HNUM, r"0[xX][0-9a-fA-F]+", idy),
    (Token.LPAREN, r"\(", idy),
    (Token.RPAREN, r"\)", idy),
    (Token.LBRACE, r"{", idy),
    (Token.RBRACE, r"}", idy),
    (Token.ASSIGN, r"=", idy),
    (Token.INCR, r"\+\+", idy),
    (Token.PLUS, r"\+", idy),
    (Token.MULT, r"\*", idy),
    (Token.SEMI, r";", idy),
    (Token.IGNORE, r" |\n", idy)
]
