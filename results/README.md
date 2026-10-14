# Resultados

**Estado:** executor oficial implementado para Baseline, Adaptive e Self-RAG;
aguarda a nova execução oficial de 180 respostas.

Os CSVs são gerados pela função `run_official_experiment()` no notebook, com
respostas e medições reais. A função não é chamada automaticamente: execute-a
somente depois de o smoke test passar.

A demonstração produz apenas um `DataFrame` em memória para uma amostra das
perguntas e não gera arquivos oficiais. A execução oficial percorre as 20
perguntas, respeita as repetições da configuração e gera os arquivos abaixo,
além do trace JSONL.

## Arquivos previstos

| Arquivo | Conteúdo |
| --- | --- |
| `baseline_r1.csv` | Primeira execução oficial das 20 perguntas no baseline. |
| `baseline_r2.csv` | Segunda execução oficial do baseline. |
| `baseline_r3.csv` | Terceira execução oficial do baseline. |
| `results_adaptive.csv` | Resultados do Adaptive, identificados por repetição. |
| `self_rag_r1.csv` | Primeira execução oficial do Self-RAG. |
| `self_rag_r2.csv` | Segunda execução oficial do Self-RAG. |
| `self_rag_r3.csv` | Terceira execução oficial do Self-RAG. |
| `summary.csv` | Comparação por variante, execução e categoria de pergunta. |
| `disagreements.csv` | Divergências entre variantes, evidências e análise. |
| `baseline_variability.csv` | Variações observadas entre as três execuções. |
| `run_manifest.json` | Configurações, hashes, versões e ambiente das execuções. |

`traces/` guardará os registros completos em JSONL: decisões de controle,
consultas, candidatos, contexto, respostas, falhas, tempos e contagens.
`figures/` guardará figuras derivadas dos resultados.

Cada resposta deve identificar pergunta, variante e execução, além de registrar
correção, fontes, latência e chamadas ao modelo. Para o Self-RAG, o trace
também registra a crítica, as rodadas de recuperação e se a reflexão acionou
uma nova recuperação.
Todos os resultados oficiais serão versionados. A tabela final deverá poder ser
regenerada a partir dos CSVs sem chamar os modelos novamente.

## Critério para resultados oficiais

Uma execução oficial deverá registrar a versão da configuração, o hash do
corpus, o modelo utilizado, a variante (`baseline` ou `adaptive`), a repetição,
os trechos recuperados, a resposta, a latência e as chamadas ao modelo. Os
resultados só devem ser publicados após a execução completa das 20 perguntas.
