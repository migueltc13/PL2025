# PL - TPC4 - Analisador Léxico

## Introdução

Construir um analisador léxico para uma linguagem de query com a qual se podem
escrever frases do género:

```
# DBPedia: obras de Chuck Berry

select ?nome ?desc where {
    ?s a dbo:MusicalArtist.
    ?s foaf:name "Chuck Berry"@en .
    ?w dbo:artist ?s.
    ?w foaf:name ?nome.
    ?w dbo:abstract ?desc
} LIMIT 1000
```

## Implementação

O analisador léxico implementado com recurso ao módulo `ply.lex` reconhece os
seguintes tokens:

- **Palavras-chave**: `SELECT`, `WHERE`, `LIMIT`;
- **Variáveis**: `?nome`, `?s`, etc;
- **Predicados**: `dbo:MusicalArtist`, `foaf:name`, etc;
    - **Predicados Abreviados**: `a`, abreviação de `rdf:type`;
- ***String Literals***: `"Chuck Berry"@en`, com suporte para *tags* de linguagem
opcionais: (`{"STRING": "Chuck Berry", "TAG": "en"}`);
- ***Int Literals***: `1000`;
- **Símbolos**: `.`, `{`, `}`.
- **Comentários**: `# DBPedia: ...`.

Este analisador léxico ignora espaços em branco, tabulações e novas linhas.
Caracteres inválidos são reportados com uma mensagem de erro que indica a linha
e coluna onde estes ocorrem.

## Autor

Realizado a 19 de Março de 2025.

Miguel Torres Carvalho, a95485

<img alt="Miguel Carvalho" width="20%" style="border-radius: 50%" src="https://migueltc13.github.io/images/profile.webp" />
