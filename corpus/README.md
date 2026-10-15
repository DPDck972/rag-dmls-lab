# Corpus

**Estado:** corpus local utilizado na execução oficial; o PDF permanece fora do
Git por ser material comercial.

Guardar os documentos originais em `documentos/`. O arquivo `.gitkeep` mantém a pasta no Git enquanto estiver vazia e não faz
parte do corpus. O PDF comercial não é versionado.

O notebook espera encontrar uma cópia no caminho indicado abaixo. A
identificação e o hash da cópia utilizada ficam registrados em `manifest.csv` e
também no manifesto da execução oficial em `results/run_manifest.json`.

## Livro candidato

- **Título:** Designing Machine Learning Systems, de Chip Huyen.
- **Edição:** primeira edição, publicada em 2022
- **Identificador:** `DOC01`.
- **Cópia local:** `documentos/designing-machine-learning-systems-2022.pdf`.
- **Referência oficial:** [O'Reilly](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/).

## Uso no experimento

O notebook extrai o texto do PDF com `pypdf`, divide o conteúdo em chunks e
cria um índice TF-IDF para a recuperação. A execução registrada produziu 713
chunks e utilizou recuperação lexical nas variantes Baseline RAG, Adaptive RAG
e Self-RAG.

O modelo de embeddings aparece na configuração como referência de infraestrutura
prevista, mas a recuperação semântica por embeddings não foi incorporada à
execução realizada. Portanto, os resultados versionados não devem ser
interpretados como uma comparação entre recuperação lexical e semântica.
