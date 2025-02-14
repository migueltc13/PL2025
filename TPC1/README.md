# PL - TPC1 - Somador on/off

## Descrição

Este programa lê linhas de entrada (*stdin*) e soma todas as sequências de dígitos
encontradas, desde que o estado esteja "ligado". O estado inicial é "ligado" e pode
ser alterado pelas palavras "On" e "Off" (insensíveis a maiúsculas/minúsculas).

O caractere "=" imprime o valor atual da soma.

## Simplificação com *regex*

A lógica da função `evaluate` pode ser simplificada com uma única expressão *regex*:

```python
import re

def evaluate(ln, on, result):
    for match in re.finditer(r'on|off|=|\d+', ln, re.IGNORECASE):
        token = match.group()
        if token.lower() == 'on':
            on = True
        elif token.lower() == 'off':
            on = False
        elif token == '=':
            print(result)
        elif on:
            result += int(token)
    return on, result
```

## Teste

*Stdin*:

```
Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens
deu-nos
este trabalho para fazer.=OfF
E deu-nos 7=
dias para o fazer... ON
Cada trabalho destes vale 0.25 valores da nota final!
```

*Stdout*:

```
2032
2032
2057
```

## Conclusão

Este exercício demonstrou como o uso de *regex* simplifica a etapa de *parsing*
do *input*, reduzindo a complexidade da implementação.

Consulte a implementação realizada em [src/main.py](src/main.py).

## Autor

Realizado a 14 de Fevereiro de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
