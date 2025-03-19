#!/usr/bin/env python3

import sys
import ply.lex as lex

tokens = [
    "SELECT",
    "WHERE",
    "LIMIT",
    "VARIABLE",
    "PREDICATE",
    "SHORT_PREDICATE",
    "STRING_LIT",
    "INT_LIT",
    "DOT",
    "OPEN_BRACE",
    "CLOSE_BRACE",
    "COMMENT"
]

t_SELECT      = r'(?i:SELECT)'
t_WHERE       = r'(?i:WHERE)'
t_LIMIT       = r'(?i:LIMIT)'
t_VARIABLE    = r'\?(\w+)'
t_DOT         = r'\.'
t_OPEN_BRACE  = r'\{'
t_CLOSE_BRACE = r'\}'
t_COMMENT     = r'\#.*'

t_ignore = ' \t'


def t_PREDICATE(t):
    r'\w+(?P<FULL>:\w+)?'

    if not t.lexer.lexmatch.group("FULL"):
        t.type = "SHORT_PREDICATE"

    return t


def t_STRING_LIT(t):
    r'(?P<STRING>"[^"]*")(?P<TAG>@\w+)?'
    t.value = {}
    for key in ["STRING", "TAG"]:
        t.value[key] = t.lexer.lexmatch.group(key)

    # General way to set the value as the named captured groups
    # t.value = {
    #     k: v for k, v in t.lexer.lexmatch.groupdict().items()
    #     if k != f"t_{t.type}" and v is not None
    # }
    #
    # Alternative (requires re):
    # t.value = re.match(t_STRLIT.__doc__, t.value).groupdict()

    return t


def t_INT_LIT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


def main():
    if len(sys.argv) != 1:
        print("Usage: python3 main.py < query")
        sys.exit(1)

    lexer = lex.lex()
    lexer.input(sys.stdin.read())
    while token := lexer.token():
        print(token)


if __name__ == "__main__":
    main()
