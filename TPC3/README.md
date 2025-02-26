# PL - TPC3 - Conversor de MarkDown para HTML

## Introdução

Neste trabalho semanal, foi proposto a implementação de um conversor simples de
Markdown para HTML.

## Implementação

Para esta solução decidiu-se uma abordagem modular baseada em expressões regulares,
que permite a conversão de cada elemento do Markdown para HTML.

É definido no início do programa uma lista que contém tuplos com a seguinte estrutura:
1. Expressão regular para encontrar o elemento do Markdown.
2. Função que converte o elemento para HTML.
3. Flags adicionais para a expressão regular.

Ao usar uma lista é possível definir a ordem de conversão dos elementos, o que
permite a conversão correta de elementos que possam conter outros elementos, como
por exemplo, a conversão de texto em negrito e itálico, ou de links e imagens.

Para além dos elementos de Markdown propostos, foram adicionados
[Horizontal Rules](https://www.markdownguide.org/basic-syntax/#horizontal-rules)
e *in-line code blocks*.

Uma consideração importante que não foi abordada neste trabalho foi a conversão
de *nested lists*, ou seja, listas dentro de listas. Para tal seria necessário
múltiplas iterações sobre o texto, e uma expressão regular *non-greedy* para
encontrar a lista mais interna em primeiro lugar.

Múltiplas iterações sobre o texto poderiam ser implementadas de seguinte forma:

```python
previous_contents = None
while contents != previous_contents:
    for pattern, repl, flags in substitutions:
        contents = re.sub(pattern, repl, contents, flags=flags)
```

Ou, mais sofisticadamente, reaplicando a função aos conteúdos de determinados
elementos que podem conter outros elementos, com recurso a *named groups* das
expressões regulares.

## Ficheiros

- [src/main.py](src/main.py) - Programa principal que converte o Markdown para HTML.
- [input/test.md](input/test.md) - Ficheiro para um teste completo dos elementos de Markdown implementados.
- [output/test.html](output/test.html) - Resultado da conversão do ficheiro de teste para HTML.

## Conclusão

Este trabalho permitiu concluir a utilidade de *named groups* em expressões regulares,
assim como construir expressões regulares *non-greedy* para encontrar o menor
elemento possível, como nos elementos de negrito, itálico e *in-line code blocks*.

## Autor

Realizado a 26 de Fevereiro de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
