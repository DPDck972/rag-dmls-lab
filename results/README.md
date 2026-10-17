# results/ — índice das runs

Este diretório contém, desde a v2, as **duas gerações** de resultados do
experimento. Não apagar nada daqui: o snapshot da v1 é proveniência congelada.

## 1. Run v1 (congelada) — `run_2026-10-15_v1/`

Snapshot imutável da run de 2026-10-15 (3 variantes: baseline, adaptive,
self_rag — 180 respostas). Os CSVs vivos da v1 foram movidos para cá na
Fase 0. Ver **`run_2026-10-15_v1/SNAPSHOT.md`** para a proveniência completa:
`config_run.json` e `questions_run.json` foram reconstruídos do histórico e
validados contra os hashes do `run_manifest.json` v1 (`d36a68f3…`),
`corpus/manifest.csv` corrigido para o hash real do PDF (`688ba89d…`).

Limitações documentadas da v1: repetições determinísticas (58/60 respostas
idênticas), Self-RAG sem nova recuperação no retry (18/18 revisões
INCORRECT), `answer_key` backfillada pós-run, adaptive com queries genéricas
fixas e métrica de "alucinação" que era, na verdade, abstenção.

## 2. Run v2 — direção do Drive e arquivos

A **fonte de verdade** da v2 é o Google Drive:
`Meu Drive/rag-dmls-v2/results/` (o notebook, com `results_dir: "drive"`,
grava lá; campo `gpu` no manifest registra NVIDIA A100-SXM4-80GB).
Uma cópia local idêntica foi baixada para a pasta-raiz do projeto de
disciplina (fora deste repo, para não inflar o Git).

Arquivos gerados por (todas derivadas do mesmo kernel, célula a célula
do notebook):

- `accuracy.csv` — 420 linhas: veredito do juiz por (questão, variante,
  repetição) com os 2 votos (`vote_1`, `vote_2`);
- `accuracy_summary.csv` — acurácia, `parse_errors` e n por variante;
- `coverage_precision.csv` — **métrica primária**: cobertura
  (1 − abstenção) × precisão condicional × acurácia bruta;
- `<variante>_r{1,2,3}.csv` — respostas brutas por (variante, repetição)
  com llm_calls, retrieval_rounds, router_label, latência;
- `router_log.json` + `ROUTE_CACHE reconciliado` — decisões do roteador
  (auditoria; cache por questão);
- `router_analysis.csv` — `router_label × difficulty` (20 questões);
- `divergencias_variantes.csv` — matriz de divergência por questão × repetição;
- `run_manifest.json` — config 2.0, hashes (config/project/corpus), gpu;
- `traces/v2_runs.jsonl` — 420 eventos com as top-4 evidências recuperadas;
- `analise_rag_dmls_v2.xlsx` — planilha consolidada (Acurácia, Cobertura,
  Roteador, Divergências, Traces);
- `judge_validation.csv` — **Fase 4**: 40 amostras estratificadas + rotulação
  (ver `judge_validation_README.md`;rotulador = LLM agente, declarado).

Caveats de leitura: números absolutos são teto (juiz leniente — acordo 85%,
κ 0,667, discordâncias todas por leniência), Q15 está fora do corpus e o
detector de abstenção gera falsos positivos em hedging de texto corrido.
A discussão completa está no README da raiz, seção "Resultados v2".
