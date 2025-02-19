# PL - TPC2 - Análise de um dataset de obras musicais

## Descrição

Neste trabalho, após a leitura e processamento de um ficheiro CSV
([data/obras.csv](data/obras.csv)), são criados os seguintes resultados:
1. Lista ordenada alfabeticamente dos compositores musicais;
2. Distribuição das obras por período: quantas obras catalogadas em cada período;
3. Dicionário em que, a cada período, está a associada uma lista alfabética dos
títulos das obras desse período.

## Implementação

Primeiramente são obtidos os registos do ficheiro CSV com recurso ao seguinte
padrão *regex*:

```regex
^(.*)(?:\n {8}(.*?))*$
```

O uso deste padrão deve-se ao facto das células do ficheiro CSV, neste caso a
coluna `desc`, poderem conter símbolo(s) de nova linha, o que impede a leitura
linha a linha do ficheiro. Após o uso deste padrão combinado com a função
`re.findall` com o argumento `re.MULTILINE`, obtém-se uma lista em que cada
elemento é um registo do ficheiro CSV.

De seguida, após se descartar a primeira linha (cabeçalho), é necessário a
separação dos diferentes campos de cada registo.

---

Após uma análise breve dos dados do ficheiro, conclui-se que a coluna `desc`
pode conter o caractere `;` e sendo este também o delimitador utilizado no ficheiro,
foi necessário a implementação de um *parser* de cada registo do CSV, que permita
a distinção dos significados distintos deste caractere.

Para tal, seguiu-se uma abordagem similar à do [TPC1](../TPC1/README.md), em que
é utilizado um interruptor para controlar a soma dos valores, neste caso são identificados
os seguintes `tokens` com os respetivos significados:
- `;"` - (`off`) início de um novo campo, o qual pode conter o caractere `;` com significado textual;
- `";` - (`on`) fim de um campo que após lido altera o significado do caractere `;` para ser novamente um delimitador;
- `;`  - significados distintos consoante o estado do interruptor:
    - `off` - caractere textual;
    - `on` - delimitador de campos.

Com esta representação do *parser* de campos, é possível a leitura correta dos
mesmos de cada registo do ficheiro CSV, com recurso à função `re.split` e o
padrão *regex*: `(;")|(";)|(;)`.

Exemplo:

Suponha-se o seguinte registo do ficheiro CSV:

```
Lost Penny;"The ""Fiesta"" in G major; Op. 999.";1745;Barroco;Ludwig;01:00:26;O2
```

A *tokenização* deste registo seria, com o *regex* supracitado:

```
[
    'Lost Penny',
    ';"',
    'The ""Fiesta"" in G major'
    ';',
    ' Op. 999.',
    '";',
    '1745',
    ';',
    'Barroco',
    ';',
    'Ludwig',
    ';',
    '01:00:26',
    ';',
    'O2'
]
```

E com o respetivo *parsing* dos campos implementado em [src/main.py](src/main.py),
obtém-se a seguinte lista de campos:

```
[
    'Lost Penny',
    'The ""Fiesta"" in G major; Op. 999.',
    '1745',
    'Barroco',
    'Ludwig',
    '01:00:26',
    'O2'
]
```

---

Por fim, deu-se a análise dos dados ao longo dos registos do ficheiro CSV, sendo estes
adicionados ao dicionário `results` que contém os resultados finais. Após a leitura do
CSV, os resultados dos `compositores` são ordenados alfabeticamente, assim como
para cada lista de títulos de obras no dicionário `obras` associada a um período.

Os resultados finais são impressos no *stdout*, assim como são guardados no
ficheiro [out/results.json](out/results.json).

## Ficheiros

- [src/main.py](src/main.py) - implementação da leitura, processamento e análise dos dados do ficheiro CSV;
- [data/obras.csv](data/obras.csv) - ficheiro CSV com os dados das obras musicais;
- [out/results.json](out/results.json) - ficheiro JSON com os resultados finais.

## Conclusão

Este trabalho demonstrou a implementação de um *parser* que possui a capacidade de
ler símbolos com diferentes significados, dependendo do contexto em que se encontram.
Esta funcionalidade é mandatória para o processamento de linguagens.

## Autor

Realizado a 19 de Fevereiro de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
