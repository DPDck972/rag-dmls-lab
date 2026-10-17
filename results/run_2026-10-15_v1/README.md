# Resultados

Artefatos da execução oficial (2026-10-15, Colab, GPU RTX PRO 6000,
Ollama `qwen2.5:7b`, juiz `llama3.1:8b`). 180 respostas =
3 variantes × 20 questões × 3 repetições.

## Arquivos brutos da run

| Arquivo | Esquema |
| --- | --- |
| `baseline_r1..r3.csv` | uma linha por questão: `question_id, category, difficulty, variant, repetition, route_question, latency_sec, evidence_count, llm_calls, answer` |
| `self_rag_r1..r3.csv` | igual a `baseline_r*.csv`, com colunas extras `draft_verdict, revised` do loop de controle do Self-RAG (nulas nas demais variantes) |
| `results_adaptive.csv` | igual a `baseline_r*.csv`, 60 linhas da variante adaptive |
| `por_repeticao/` | cópias isoladas por variante e repetição (adaptive, baseline, self_rag × r1–r3) |
| `traces/official_runs.jsonl` | 180 linhas JSONL, uma por execução, com `evidence` detalhada (rank e texto) |
| `run_manifest.json` | config da run, hashes (config, questions, corpus), contagens, padrões de roteamento, rota por questão e anotações de edição pós-run |

## Arquivos derivados

| Arquivo | Esquema |
| --- | --- |
| `summary.csv` | base consolidada das 180 execuções usada pelas análises do notebook |
| `accuracy.csv` | veredito do juiz por execução: `question_id, variant, repetition, difficulty, verdict` (com `draft_verdict, revised` nas linhas self_rag quando existirem) |
| `accuracy_summary.csv` | acurácia por variante com `parse_errors` e `n` |
| `abstencoes.csv` | taxa de abstenção, respostas não-abstencionistas e precisão condicional por variante |
| `diagnostico_baseline.csv` | por questão: gabarito, acertos de 3 por variante, trechos recuperados pelo baseline na repetição 1 e a coluna `causa` preenchida |
| `divergencias_variantes.csv` | repetições em que as variantes divergem, com as respostas de cada variante e a coluna `causa` preenchida |
| `disagreements.csv` | comparação de respostas entre variantes por questão (`answers_differ`), sem classificação de causa |
| `analise_rag_dmls.xlsx` | planilha multi-aba para inspeção dos resultados |
| `imagem/` | acurácia por repetição (sinal vs. ruído), boxplot de latência, chamadas e latência por dificuldade, qualidade das respostas |

## Contrato do grader

- Cada questão de `questions.json` carrega `answer_key`; o grader do
  notebook valida a chave antes de gastar chamadas e falha cedo caso
  esteja ausente. O `question_id` enlaça todos os arquivos da pasta.
- O veredito vem do juiz LLM (`llama3.1:8b`) com contrato de uma palavra
  (CORRECT/INCORRECT), parseado por regex; `PARSE_ERROR` é contado em
  `accuracy_summary.csv` e reprova o smoke test se aparecer no Self-RAG.
- A reprodução local sem Ollama reconstrói `official_df` a partir dos
  CSVs commitados, mas os `accuracy*.csv` entregues não são regravados:
  eles reproduzem a run do Colab de 2026-10-15.

## Método detector de abstenções

`abstencoes.csv` foi gerado por heurística lexical aplicada aos CSVs
commitados (regex na coluna `metodo`, reconstruída a partir da expressão
referenciada na célula de visualização final do notebook): ela reproduz
exatamente os números citados na conclusão do notebook (adaptive 60% de
abstenções, 24/24 corretas quando responde; baseline e self_rag 18/42,
43%). As colunas `causa` de `diagnostico_baseline.csv` e
`divergencias_variantes.csv` foram preenchidas neste fechamento e o
notebook regenera ambos os arquivos com esse preenchimento garantido.

## Limitações registradas

- Acurácia: juiz automático não validado contra avaliação manual.
- Abstenção: heurística lexical — respostas com ressalva podem ser
  classificadas como abstenção.
- Causas de divergência: classificação baseada em trechos e respostas
  commitados; a causa da divergência Q12 é hipótese apoiada no desenho
  do pipeline (única diferença: recuperação expandida), não demonstrada
  por similaridade textual.
- `corpus/manifest.csv` registra um sha256 que **não** corresponde ao PDF da
  run oficial (`corpus_sha256: 688ba89d…` no `run_manifest.json`). A
  referência para reprodução da run e das variantes do adendo
  (`notebook_addendum.ipynb`) é o hash do `run_manifest.json`.
