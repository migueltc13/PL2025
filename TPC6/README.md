# PL - TPC6 - Recursivo Descendente para expressões aritméticas

## Introdução

Este trabalho prático consiste na implementação de um parser recursivo descendente
(LL(1)) para avaliação de expressões aritméticas.
O objetivo foi converter uma gramática *left-recursive* original (implementada com `ply.yacc`)
para uma versão LL(1) utilizando o método recursivo descendente.

A calculadora suporta as operações básicas (+, -, *, /), números inteiros e parênteses
para definição de prioridades, mantendo a precedência normal dos operadores
(multiplicação e divisão sobre adição e subtração).

## Implementação

O projeto contém duas versões distintas do parser:

1. **`src/left-recursive.py`** - Versão original com gramática *left-recursive*,
implementada com recurso a `ply.yacc`:
   - Utiliza a abordagem tradicional de operadores com recursividade à esquerda
   - Vantagem: Mais intuitiva na definição das regras de produção
   - Desvantagem: Não é compatível com parsers LL(1)

2. **`src/main.py`** - Versão LL(1) recursiva descendente:
   - Elimina a recursividade à esquerda transformando as produções em recursividade à direita
   - Implementa explicitamente a precedência de operadores
   - Segue o padrão clássico de parser LL(1) com métodos para cada não-terminal
   - Inclui tratamento de erros mais detalhado

### Conversão de *Left-Recursive* para LL(1)

A transformação da gramática original para LL(1) seguiu estes princípios:

1. **Regra da expressão**:
   - Original (*left-recursive*):
     ```
     expression : expression '+' term
                | expression '-' term
                | term
     ```
   - Convertida (LL(1)):
     ```
     expression : term expression_prime
     expression_prime : '+' term expression_prime
                     | '-' term expression_prime
                     | ε
     ```

2. **Regra do termo**:
   - Original:
     ```
     term : term '*' factor
          | term '/' factor
          | factor
     ```
   - Convertida:
     ```
     term : factor term_prime
     term_prime : '*' factor term_prime
               | '/' factor term_prime
               | ε
     ```

## Testes

O parser foi testado com diversos casos de uso:

```
>> 2 + 3 * 4
14
>> (2 + 3) * 4
20
>> 10 / 2 - 3
2.0
>> 3 + 4 * (2 - 1)
7
>> 10 / (2 + 3)
2.0
```

## Autor

Realizado a 24 de Março de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
