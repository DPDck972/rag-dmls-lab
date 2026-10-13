# Corpus

**Estado:** livro armazenado localmente; perguntas definidas; recorte definitivo e ingestão oficial ainda pendentes.

Guardar os documentos originais em `documentos/`. O arquivo `.gitkeep` mantém a pasta no Git enquanto estiver vazia e não faz
parte do corpus. O PDF comercial não é versionado.

O notebook espera encontrar uma cópia no caminho indicado abaixo, e a
identificação e o hash da cópia local ficam registrados em `manifest.csv`.

## Livro candidato

- **Título:** Designing Machine Learning Systems, de Chip Huyen.
- **Edição:** primeira edição, publicada em 2022
- **Identificador:** `DOC01`.
- **Cópia local:** `documentos/designing-machine-learning-systems-2022.pdf`.
- **Referência oficial:** [O'Reilly](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/).

## Uso atual

O notebook extrai o texto do PDF com `pypdf`, divide o conteúdo em chunks e
cria um índice TF-IDF para a demonstração de recuperação. Essa implementação
é um baseline lexical; a recuperação semântica por embeddings ainda não foi
incorporada ao experimento oficial.
