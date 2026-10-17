# Snapshot da run oficial v1 — 2026-10-15

Esta pasta é **imutável**: é a linha de base do experimento original. A run v2
produz artefatos em `results/` (raiz) ou `results/v2/` e não deve sobrescrever
nada aqui.

## O que há aqui

Artefatos originais de `results/` da run de 2026-10-15 (Colab, GPU RTX PRO
6000 Blackwell, Ollama `qwen2.5:7b`, juiz `llama3.1:8b`): 180 respostas
(3 variantes, 20 questões, 3 repetições), grader, traces, manifest, planilha
e figuras. O detalhamento dos arquivos está em `README.md`.

## Arquivos congelados adicionais (proveniência)

A run original registrou `config_sha256: d36a68f3…` e `questions_sha256:
54f2bf28…` no `run_manifest.json`, mas os arquivos com esses hashes nunca
foram commitados. Durante a Fase 0 do plano v2 foram reconstruídos:

- `config_run.json` — `git show 405c6ab:configs/experiment.json`
  (commit "feat: add official RAG experiment results"). Hash validado:
  **d36a68f36075680e…** ✓
- `questions_run.json` — re-serialização do `questions.json` atual
  (`json.dumps(..., ensure_ascii=False, indent=2)` sem quebra de linha final).
  Conteúdo **idêntico** ao commitado em `a565a77` (a única diferença era um
  `\n` final). Hash validado: **54f2bf2879a0ce7a…** ✓

O PDF do livro usado na run (`corpus_sha256: 688ba89d…`) não está presente
neste repositório local; `corpus/manifest.csv` registra esse hash. A
reprodução exige restaurar uma cópia com o hash correspondente.

## Consequência para a validade do `accuracy.csv`

O gabarito usado pelo grader da run v1 é o conteúdo de `questions_run.json`
— que é o mesmo gabarito hoje em `questions.json` (mesmos textos das chaves
`answer_key`). As métricas de acurácia da v1 continuam auditáveis contra
`questions_run.json`; a crítica de proveniência do relatório v1 se refere ao
**processo** (gabarito backfillado após a run, arquivos nunca commitados),
não ao conteúdo: nenhum texto de `answer_key` mudou.
