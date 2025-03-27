# PL - TPC5 - Máquina de *Vending*

## Introdução

Construção de um interface para a interação com uma máquina de *vending*,
com gestão de *stock* e interação com utilizadores, clientes e operadores.

## Implementação

### Leitura do Ficheiro de *Stock*

O primeiro passo é a leitura do ficheiro `stock.json`, para tal recorreu-se a
função `load` do módulo `json` para carregar o conteúdo do ficheiro para uma
lista, de seguida esta é convertida para um dicionário onde a chave corresponde ao
código do produto e o valor sendo um dicionário com também o código do produto,
o nome, o preço unitário e a quantidade na determinada *slot* da máquina.

Exemplo do ficheiro `stock.json`:

```json
[
    { "cod": "A23", "nome": "Água 0.5L",       "quant":  8, "preco": 0.7 },
    { "cod": "B45", "nome": "Refrigerante 1L", "quant": 15, "preco": 1.5 },
    { "cod": "C67", "nome": "Sumo 330ml",      "quant": 10, "preco": 1.2 },
    { "cod": "D89", "nome": "Cerveja 330ml",   "quant": 20, "preco": 1.0 },
    { "cod": "F01", "nome": "Bolachas Maria",  "quant":  0, "preco": 0.5 }
]
```

### Estado da Máquina

Para o armazenamento temporário do *stock* foi criada uma classe `State` que
representa o estado da máquina de *vending*, que regista o *stock* dos
produtos, o saldo atual da máquina e se a máquina está ligada:

```python
class State:
    """Vending machine state"""
    on = True
    stock = {}
    balance = 0  # Cents
```

---

De seguida deu-se início a análise lexical e sintática para a implementação
da interface de utilizador.

### Análise Lexical

O analisador lexical identifica os seguintes *tokens*:
- Comandos (insensíveis a maiúsculas e minúsculas):
    - `CMD_AJUDA`
    - `CMD_LISTAR`
    - `CMD_MOEDA`
    - `CMD_SELECIONAR`
    - `CMD_ABASTECER`
    - `CMD_REMOVER`
    - `CMD_SAIR`
- `CODIGO`:     Código de um produto       (`[A-Z][0-9]{2}`)
- `MOEDA`:      Representação de uma moeda (`1c|2c|5c|10c|20c|50c|1e|2e`)
- `PRICE`:      Preço de um produto        (`\d+\.\d{1,2}`)
- `QUANTIDADE`: Número inteiro             (`\d+`)
- `NOME`:       Nome do produto            (`"[^"]*"|'[^']*'`)

Nesta etapa são também ignorados os espaços em branco e tabulações, assim como
são definidos os literais `,` e `.`.

Para evitar erros de representação de `float` para valores monetários a unidade
monetária é representada em cêntimos, e esta conversão é feita no analisador
lexical, assim como a conversão de `str` para `int` para a quantidade de produtos,
e a remoção de aspas ou apóstrofos para o nome do produto.

### Análise Sintática

Nesta fase foram definidas as regras de produção da gramática:

```
comando : ajuda
        | listar
        | moeda
        | selecionar
        | abastecer
        | remover
        | sair

ajuda : CMD_AJUDA

listar : CMD_LISTAR

moeda : CMD_MOEDA list_moedas '.'

list_moedas : MOEDA
            | list_moedas ',' MOEDA

selecionar : CMD_SELECIONAR CODIGO

abastecer : CMD_ABASTECER CODIGO QUANTIDADE
          | CMD_ABASTECER CODIGO NOME QUANTIDADE PRICE

remover : CMD_REMOVER CODIGO

sair : CMD_SAIR
```

Para cada regra de produção foi definida uma função que recebe os *tokens*
correspondentes e executa a ação correspondente.

### Interface de Utilizador

Como supramencionado o programa começa pela leitura do *stock* e respetiva conversão.

De seguida é apresentado uma mensagem de boas-vindas, com o dia atual, o nome
do ficheiro de stock carregado, o número de diversos produtos e o número total
de unidades.

Após a respetiva inicialização do *lexer* e *parser* programa entra num ciclo
aquando o atributo `State.on` é `True`, onde é apresentado o *prompt* `>> ` para
a introdução de comandos, os quais são analisados e executados.

Quando o utilizador introduz um comando inválido é apresentada uma mensagem de
erro com o respetivo *token* inválido.

Por fim quando o utilizador introduz o comando `sair`, ou é detetado uma
interrupção ou indicação de fim de ficheiro, o programa guarda o *stock* registado
no estado da máquina no formato de lista de dicionários, e termina.

#### Comandos Implementados

##### `AJUDA`

Apresenta uma mensagem de ajuda com os comandos disponíveis:

```
maq: Comandos disponíveis:
  AJUDA                           Mostra esta mensagem
  LISTAR                          Lista os produtos disponíveis
  MOEDA <lista de moedas>         Adiciona moedas à máquina
  SELECIONAR <cod>                Seleciona um produto
  ABASTECER
    <cod> <quant>                 Adiciona quantidade ao produto
    <cod> <nome> <quant> <preço>  Adiciona novo produto
  REMOVER <cod>                   Remove um produto
  SAIR                            Sair com o seu troco, se existente
```

##### `LISTAR`

Comando que lista os produtos disponíveis, com o código, nome, quantidade e preço,
em uma tabela formatada:

```
| cod   | nome            |   quantidade |   preço |
|-------+-----------------+--------------+---------|
| A23   | Água 0.5L       |            8 |     0.7 |
| B45   | Refrigerante 1L |           15 |     1.5 |
| C67   | Sumo 330ml      |           10 |     1.2 |
| D89   | Cerveja 330ml   |           20 |     1   |
| F01   | Bolachas Maria  |            0 |     0.5 |
```

##### `MOEDA`

Permite ao cliente adicionar moedas à máquina, com a possibilidade de adicionar
múltiplas moedas de uma só vez, com recurso a uma lista de moedas separadas por
vírgulas e terminadas com um ponto. A máquina indica o saldo atual após a
inserção das moedas.

```
>> MOEDA 1e, 50c, 20c.
maq: Saldo: 1e70c
>> MOEDA 2e.
maq: Saldo = 3e70c
```

De seguida são apresentados alguns casos de erro para este comando.

Moeda inválida:

```
>> MOEDA 1d.
maq: Syntax error at token '1'
```

Falta do terminador de lista de moedas:

```
>> MOEDA 1e, 20c
maq: Unterminated command
```

##### `SELECIONAR`

Permite ao cliente selecionar um produto, indicando o código do produto. Se
o produto estiver disponível e o saldo for suficiente, o produto é vendido e
o saldo e *stock* são atualizados.

```
>> SELECIONAR A23
maq: Pode retirar o produto A23
maq: Saldo = 0e60c
```

Caso o saldo não seja suficiente:

```
>> SELECIONAR A23
maq: Saldo insuficiente para o produto A23
maq: Saldo = 0e60c; Preço = 0e70c
```

Caso o produto não exista (código inválido):

```
>> SELECIONAR A99
maq: O produto A99 não existe
```

Caso o produto exista mas não haja quantidade suficiente:

```
>> SELECIONAR F01
maq: O produto F01 está esgotado
```

##### `ABASTECER`

O comando `ABASTECER` permite ao operador adicionar produtos à máquina, com a
possibilidade de adicionar múltiplas unidades de um produto existente ou adicionar
um novo produto à máquina.

Para adicionar uma quantidade de um produto existente:

```
>> ABASTECER A23 5
maq: Adicionadas 5 unidades do produto A23
```

Para adicionar um novo produto à máquina:

```
>> ABASTECER A99 "Café" 4 0.7
maq: Adicionado novo produto A99 - Café
```

Neste comando são verificados diversos casos de erros, dos quais se destacam:
- Adicionar quantidade de um produto existente:
    - Código do produto não existente;
    - Quantidade inválida;
    - Erros léxicos nos parâmetros `CODIGO` e `QUANTIDADE`.
- Adicionar novo produto:
    - Código do produto já existente;
    - Quantidade inválida;
    - Preço inválido;
    - Erros léxicos nos parâmetros `CODIGO`, `NOME`, `QUANTIDADE` e `PRICE`.

##### `REMOVER`

Permite ao operador remover um produto da máquina, indicando o código do produto.

```
>> REMOVER A23
maq: Produto A23 removido
```

Caso o produto não exista:

```
>> REMOVER A99
maq: O produto A99 não existe
```

##### `SAIR`

Permite ao cliente sair da máquina com o troco, se existente.

```
...
>> SAIR
maq: Pode retirar o troco: 1x50c, 1x10c
maq: Até à próxima
(Stock guardado em 'stock/stock.json')
```

### Teste

Por fim, foi realizado um teste cujo respetivo *input* está guardado em
[input/test.txt](input/test.txt).

O ficheiro de *stock* utilizado foi [stock/stock.json.bak](stock/stock.json.bak).

O ficheiro de *stock* resultante encontra-se em [stock/stock.json](stock/stock.json).

```
maq: 27-03-2025, Stock carregado (stock/stock.json), 5 produtos, 53 unidades
maq: Bom dia. Estou disponível para atender o seu pedido.
>> AJUDA
maq: Comandos disponíveis:
  AJUDA                           Mostra esta mensagem
  LISTAR                          Lista os produtos disponíveis
  MOEDA <lista de moedas>         Adiciona moedas à máquina
  SELECIONAR <cod>                Seleciona um produto
  ABASTECER
    <cod> <quant>                 Adiciona quantidade ao produto
    <cod> <nome> <quant> <preço>  Adiciona novo produto
  REMOVER <cod>                   Remove um produto
  SAIR                            Sair com o seu troco, se existente
>> LISTAR
maq:
| cod   | nome            |   quantidade |   preço |
|-------+-----------------+--------------+---------|
| A23   | Água 0.5L       |            8 |     0.7 |
| B45   | Refrigerante 1L |           15 |     1.5 |
| C67   | Sumo 330ml      |           10 |     1.2 |
| D89   | Cerveja 330ml   |           20 |     1   |
| F01   | Bolachas Maria  |            0 |     0.5 |
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR F01
maq: O produto F01 está esgotado
>> SELECIONAR A99
maq: O produto A99 não existe
>> SELECIONAR A23
maq: Pode retirar o produto A23
maq: Saldo = 0e60c
>> selecionar A23
maq: Saldo insuficiente para o produto A23
maq: Saldo = 0e60c; Preço = 0e70c
>> ABASTECER A23 10
maq: Adicionadas 10 unidades do produto A23
>> ABASTECER A99 "Café" 4 0.7
maq: Adicionado novo produto A99 - Café
>> REMOVER F01
maq: Produto F01 removido
>> REMOVER F01
maq: O produto F01 não existe
>> LISTAR
maq:
| cod   | nome            |   quantidade |   preço |
|-------+-----------------+--------------+---------|
| A23   | Água 0.5L       |           17 |     0.7 |
| B45   | Refrigerante 1L |           15 |     1.5 |
| C67   | Sumo 330ml      |           10 |     1.2 |
| D89   | Cerveja 330ml   |           20 |     1   |
| A99   | Café            |            4 |     0.7 |
>> SAIR
maq: Pode retirar o troco: 1x50c, 1x10c
maq: Até à próxima
```

Para simular este teste copie o ficheiro de *stock* de *backup* para o
ficheiro de *stock* e execute o programa com o *input* de teste:

```bash
cp stock/stock.json.bak stock/stock.json
src/main.py stock/stock.json < input/test.txt
```

## Autor

Realizado a 27 de Março de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
