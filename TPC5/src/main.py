#!/usr/bin/env python3

import sys
import json
import re
import ply.lex as lex
import ply.yacc as yacc
from datetime import datetime
from tabulate import tabulate


###
# State
###

class State:
    """Vending machine state"""
    on = True
    stock = {}
    balance = 0  # Cents


state = State()


###
# Lexical analysis
###

tokens = [
    "CMD_AJUDA",
    "CMD_LISTAR",
    "CMD_MOEDA",
    "CMD_SELECIONAR",
    "CMD_ABASTECER",
    "CMD_REMOVER",
    "CMD_SAIR",
    "CODIGO",
    "MOEDA",
    "PRICE",
    "QUANTIDADE",
    "NOME"
]

literals = [
    ",",
    "."
]


def t_COMANDO(t):
    r"(?i:ajuda|listar|moeda|selecionar|abastecer|remover|sair)"
    t.type = f"CMD_{t.value.upper()}"
    return t


def t_CODIGO(t):
    r"[A-Z][0-9]{2}"
    return t


def t_MOEDA(t):
    r"1c|2c|5c|10c|20c|50c|1e|2e"
    return t


def t_PRICE(t):
    r'\d+\.\d{1,2}'  # Matches prices like 0.7 or 1.50
    # Convert to cents as integer
    euros, cents = t.value.split('.')
    cents = cents.ljust(2, '0')[:2]  # Ensure exactly 2 decimal places
    t.value = int(euros) * 100 + int(cents)
    return t


def t_QUANTIDADE(t):
    r"\d+"
    t.value = int(t.value)
    return t


def t_NOME(t):
    r'"[^"]*"|\'[^\']*\''
    t.value = t.value[1:-1]  # Remove quotes
    return t


t_ignore = " \t"


def t_error(t):
    raise ValueError(f"Illegal character '{t.value[0]}'")


###
# Helper functions
###

def coin_value(coin):
    return {
        "1c":    1,
        "2c":    2,
        "5c":    5,
        "10c":  10,
        "20c":  20,
        "50c":  50,
        "1e":  100,
        "2e":  200
    }[coin]


def coin_change(change):
    coins = ["2e", "1e", "50c", "20c", "10c", "5c", "2c", "1c"]
    change_coins = {}
    for coin in coins:
        while change >= coin_value(coin):
            change -= coin_value(coin)
            if coin in change_coins:
                change_coins[coin] += 1
            else:
                change_coins[coin] = 1

    return change_coins


###
# Syntactic analysis
###

def p_comando(p):
    """
    comando : ajuda
            | listar
            | moeda
            | selecionar
            | abastecer
            | remover
            | sair
    """


def p_ajuda(p):
    """
    ajuda : CMD_AJUDA
    """
    print(
        "maq: Comandos disponíveis:\n"
        "  AJUDA                           Mostra esta mensagem\n"
        "  LISTAR                          Lista os produtos disponíveis\n"
        "  MOEDA <lista de moedas>         Adiciona moedas à máquina\n"
        "  SELECIONAR <cod>                Seleciona um produto\n"
        "  ABASTECER\n"
        "    <cod> <quant>                 Adiciona quantidade ao produto\n"
        "    <cod> <nome> <quant> <preço>  Adiciona novo produto\n"
        "  REMOVER <cod>                   Remove um produto\n"
        "  SAIR                            Sair com o seu troco, se existente"
    )


def p_listar(p):
    """
    listar : CMD_LISTAR
    """
    # TODO Use tabulate as local module to avoid installing it
    headers = ["cod", "nome", "quantidade", "preço"]
    table = [
        [item["cod"], item["nome"], item["quant"], item["preco"]]
        for item in state.stock.values()
    ]

    print("maq:")
    print(tabulate(table, headers=headers, tablefmt="orgtbl"))


def p_moeda(p):
    """
    moeda : CMD_MOEDA list_moedas '.'
    """
    total = sum(coin_value(coin) for coin in p[2])
    state.balance += total
    print(f"maq: Saldo = {state.balance // 100}e{state.balance % 100}c")


def p_listar_moedas(p):
    """
    list_moedas : MOEDA
                | list_moedas ',' MOEDA
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_selecionar(p):
    """
    selecionar : CMD_SELECIONAR CODIGO
    """
    cod = p[2]
    if cod not in state.stock:
        print(f"maq: O produto {cod} não existe")
        return

    item = state.stock[cod]
    if item["quant"] <= 0:
        print(f"maq: O produto {cod} está esgotado")
        return

    price = int(float(item["preco"]) * 100)  # Convert price to cents
    if state.balance < price:
        print(f"maq: Saldo insuficiente para o produto {cod}")
        print(f"maq: Saldo = {state.balance // 100}e{state.balance % 100}c; "
              f"Preço = {price // 100}e{price % 100}c")
        return

    state.balance -= price
    item["quant"] -= 1
    print(f"maq: Pode retirar o produto {cod}")
    print(f"maq: Saldo = {state.balance // 100}e{state.balance % 100}c")


def p_abastecer(p):
    """
    abastecer : CMD_ABASTECER CODIGO QUANTIDADE
              | CMD_ABASTECER CODIGO NOME QUANTIDADE PRICE
    """
    if len(p) == 4:
        # Just adding quantity to existing item
        cod = p[2]
        if cod not in state.stock:
            print(f"maq: O produto {cod} não existe")
            return

        quant = p[3]
        if quant <= 0:
            print(f"maq: Quantidade inválida: {quant}")
            return

        state.stock[cod]["quant"] += quant
        print(f"maq: Adicionadas {quant} unidades do produto {cod}")
    else:
        # Adding new item
        cod = p[2]
        name = p[3]
        quant = p[4]
        price = float(f"{p[5] / 100:.2f}")

        if cod in state.stock:
            print(f"maq: O produto {cod} já existe")
            return

        if quant <= 0:
            print(f"maq: Quantidade inválida: {quant}")
            return

        if price <= 0:
            print(f"maq: Preço inválido: {price}")
            return

        state.stock[cod] = {
            "cod": cod,
            "nome": name,
            "quant": quant,
            "preco": price
        }
        print(f"maq: Adicionado novo produto {cod} - {name}")


def p_remover(p):
    """
    remover : CMD_REMOVER CODIGO
    """
    cod = p[2]
    if cod not in state.stock:
        print(f"maq: O produto {cod} não existe")
        return

    del state.stock[cod]
    print(f"maq: Produto {cod} removido")


def p_sair(p):
    """
    sair : CMD_SAIR
    """
    if state.balance > 0:
        change = coin_change(state.balance)
        print("maq: Pode retirar o troco: ", end="")
        print(", ".join([f"{count}x{coin}" for coin, count in change.items()]))
    print("maq: Até à próxima")
    state.on = False


def p_error(p):
    if p:
        raise ValueError(f"maq: Syntax error at token '{p.value}'")
    else:
        raise ValueError("maq: Unterminated command")


###
# Main
###

def main():
    global state

    if len(sys.argv) != 2:
        print("Usage: main.py <stock_file>")
        sys.exit(1)

    # Load the stock from the json file
    stock_file = sys.argv[1]
    try:
        state.stock = json.loads(open(stock_file).read())
    except Exception as e:
        print("Error: Failed to load the stock from the file", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    # Convert to stock dictionary with "cod" as key
    state.stock = {item["cod"]: item for item in state.stock}

    # Starting message
    print(f"maq: {datetime.now().strftime('%d-%m-%Y')}, "
          f"Stock carregado ({stock_file}), "
          f"{len(state.stock)} produtos, "
          f"{sum(item['quant'] for item in state.stock.values())} unidades")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    # Parser
    lexer = lex.lex()
    parser = yacc.yacc()

    while state.on:
        try:
            line = input(">> ")
        except (KeyboardInterrupt, EOFError):
            break

        if not line:
            continue

        # DEBUG: Show tokens
        # lexer.input(line)
        # print("Tokens:", [tok.type for tok in lexer])
        # lexer.input(line)  # Reset for parser

        try:
            parser.parse(line, lexer=lexer, debug=False)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue

    # Save the stock
    # print(f"Saving stock to {stock_file}")
    with open(stock_file, "w") as f:
        json.dump(list(state.stock.values()), f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
