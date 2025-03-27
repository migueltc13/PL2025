#!/usr/bin/env python3

import ply.lex as lex

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
# LL(1) - Recursive Descent Parser
###

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.next_token()

    def next_token(self):
        self.current_token = self.lexer.token()
        return self.current_token

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        result = self.expression()
        if self.current_token is not None:
            raise SyntaxError(f"Unexpected token {self.current_token.value}")
        return result

    def expression(self):
        """expression : term expression_prime"""
        left = self.term()
        return self.expression_prime(left)

    def expression_prime(self, left):
        """expression_prime : ('+' term expression_prime | '-' term expression_prime) | ε"""
        if self.current_token is not None and self.current_token.type in ('+', '-'):
            op = self.current_token.type
            self.eat(op)
            right = self.term()
            if op == '+':
                new_left = left + right
            else:
                new_left = left - right
            return self.expression_prime(new_left)
        return left

    def term(self):
        """term : factor term_prime"""
        left = self.factor()
        return self.term_prime(left)

    def term_prime(self, left):
        """term_prime : ('*' factor term_prime | '/' factor term_prime) | ε"""
        if self.current_token is not None and self.current_token.type in ('*', '/'):
            op = self.current_token.type
            self.eat(op)
            right = self.factor()
            if op == '*':
                new_left = left * right
            else:
                new_left = left / right
            return self.term_prime(new_left)
        return left

    def factor(self):
        """factor : NUMBER | '(' expression ')'"""
        if self.current_token.type == 'NUMBER':
            val = int(self.current_token.value)
            self.eat('NUMBER')
            return val
        elif self.current_token.type == '(':
            self.eat('(')
            expr_val = self.expression()
            self.eat(')')
            return expr_val
        else:
            raise SyntaxError(f"Unexpected token {self.current_token.value}")


def main():
    lexer = lex.lex()

    while True:
        try:
            data = input(">> ")
        except (KeyboardInterrupt, EOFError):
            break

        if not data:
            continue

        lexer.input(data)
        parser = Parser(lexer)
        try:
            result = parser.parse()
            print(result)
        except SyntaxError as e:
            print(f"Syntax error: {e}")


if __name__ == "__main__":
    main()
