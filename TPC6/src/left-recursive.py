#!/usr/bin/env python3

import ply.lex as lex
import ply.yacc as yacc

###
# Lexer
###

tokens = [
    "NUMBER",
]

literals = [
    "+",
    "-",
    "*",
    "/",
    "(",
    ")",
]

t_NUMBER = r"\d+"

t_ignore = " \t"


def t_error(t):
    print(f"Invalid token: {t.value!r}")
    t.lexer.skip(1)


###
# Parser - Left recursive
###

def p_expression(p):
    """
    expression : expression '+' term
               | expression '-' term
               | term
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]


def p_term(p):
    """
    term : term '*' factor
         | term '/' factor
         | factor
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "*":
        p[0] = p[1] * p[3]
    elif p[2] == "/":
        p[0] = p[1] / p[3]


def p_factor(p):
    """
    factor : NUMBER
           | '(' expression ')'
    """
    if len(p) == 2:
        p[0] = int(p[1])
    else:
        p[0] = p[2]


def p_error(p):
    print(f"Syntax error at {p.value!r}")


def main():
    lexer = lex.lex()
    parser = yacc.yacc()

    while True:
        try:
            data = input(">> ")
        except (KeyboardInterrupt, EOFError):
            break

        if not data:
            continue

        result = parser.parse(data, lexer=lexer)
        print(result)


if __name__ == "__main__":
    main()
