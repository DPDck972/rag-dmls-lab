# Resultados

**Estado:** nenhum experimento executado.

Os CSVs serão gerados pelo notebook, com respostas e medições reais.

## Arquivos previstos

| Arquivo | Conteúdo |
| --- | --- |
| `baseline_r1.csv` | Primeira execução oficial das 20 perguntas no baseline. |
| `baseline_r2.csv` | Segunda execução oficial do baseline. |
| `baseline_r3.csv` | Terceira execução oficial do baseline. |
| `results_adaptive.csv` | Resultados do Adaptive, identificados por repetição. |
| `summary.csv` | Comparação por variante, execução e categoria de pergunta. |
| `disagreements.csv` | Divergências entre variantes, evidências e análise. |
| `baseline_variability.csv` | Variações observadas entre as três execuções. |
| `run_manifest.json` | Configurações, hashes, versões e ambiente das execuções. |

`traces/` guardará os registros completos em JSONL: decisões de controle,
consultas, candidatos, contexto, respostas, falhas, tempos e contagens.
`figures/` guardará figuras derivadas dos resultados.

Cada resposta deve identificar pergunta, variante e execução, além de registrar
correção, fontes, latência e chamadas ao modelo.
Todos os resultados oficiais serão versionados. A tabela final deverá poder ser
regenerada a partir dos CSVs sem chamar os modelos novamente.
