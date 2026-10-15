# Prompts

**Estado:** `generator.txt` versionado e utilizado na execução; as decisões de
roteamento e reflexão permanecem implementadas no notebook.

Os arquivos de prompt e as estratégias correspondentes são:

| Artefato | Finalidade |
| --- | --- |
| `generator.txt` | Gerar respostas fundamentadas para as três variantes. |
| Estratégia no notebook | Roteamento Baseline/Adaptive por padrões da consulta. |
| Estratégia no notebook | Crítica estruturada do Self-RAG e decisão de nova recuperação. |

Não foram criados arquivos separados para roteador, decomposição ou verificação
de evidências. Essas etapas são construídas pelo código do notebook e seus
metadados ficam registrados nos CSVs e no trace JSONL da execução.

O notebook carrega esse prompt de `prompts/generator.txt` via
`load_generator_template()` e aplica `format_prompt(question, context)`.
O template usa os placeholders `{question}` e `{context}` e instrui o modelo
a responder em inglês usando somente o contexto recuperado.

O roteador utilizado é baseado em marcadores de consulta, não em um prompt de
classificação. A expansão da consulta é aplicada na variante Adaptive RAG. O
Self-RAG usa uma crítica estruturada para avaliar relevância e suporte factual,
podendo acionar uma nova rodada de recuperação e geração.
