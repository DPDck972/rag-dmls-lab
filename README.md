# rag-dmls-lab

Projeto da Unidade 01 — RAG avançado sobre *Designing Machine Learning Systems*.

**Disciplina:** DCA0305 — Design de Sistemas Baseados em Aprendizado de Máquina  
**Grupo:** 1  
**Família:** F4 — Controle do processo  
**Técnica proposta:** Adaptive RAG com roteador LLM de 3 níveis, contra Baseline RAG, Self-RAG e controles (LLM puro, embedding), com ablações  
**Estado:** **v2 executada** (7 variantes × 20 questões × 3 seeds = 420 respostas, A100 80GB no Colab). Run v1 congelada em `results/run_2026-10-15_v1/`; resultados v2 em `results/` (cópia local) e no Google Drive da branch.

## Objetivo

Comparar sete variantes da família F4 (controle do processo) sobre o mesmo
corpus e o mesmo juiz:

- **pure_llm** — o gerador sem recuperação alguma (contrafato);
- **baseline** — 1 round de recuperação lexical (TF-IDF) + geração;
- **adaptive_route** — roteador LLM decide LABEL_A (sem retrieval) / LABEL_B
  (1 round) / LABEL_C (iterativo com subqueries derivadas da pergunta + RRF);
- **adaptive_expansion** — sempre subqueries + RRF (ablação do roteador);
- **adaptive_full** — roteador + expansão por label (variante principal);
- **self_rag** — geração, verificador, retry **com nova recuperação**
  (subquery derivada do draft + RRF), 0–2 rounds;
- **embedding** — retrieval semântico (`nomic-embed-text`) + geração.

Métrica primária: cobertura (1 − abstenção) × precisão condicional;
acurácia bruta como métrica secundária. Juiz (`llama3.1:8b`) com dedup de
respostas e duplo voto por resposta única (auto-concordância pactuada ≥ 90%).

## Estrutura do projeto

```text
rag-dmls-lab/
├── configs/experiment.json          # config 2.0 (7 variantes, seeds, drive|local)
├── corpus/                          # PDF do livro (local, não versionado) + manifest.csv
├── notebook.ipynb                   # experimento v2 completo (Colab-first)
├── notebook_addendum.ipynb          # legado da fase de addendum (não usado na v2)
├── prompts/                         # router, generator, verifier, no_context, retry, abstention
├── questions.json                   # 20 questões + answer_rubric (definida ANTES da run)
├── scripts/
│   ├── build_judge_validation.py    # Fase 4: amostra estratificada de 40
│   ├── fill_judge_validation.py     # Fase 4: rotulador-LLM + métricas de acordo
│   └── bookcheck.py                 # Fase 4: verificação mecânica do livro (pypdf)
├── results/
│   ├── run_2026-10-15_v1/           # snapshot imutável da run v1 (congelado)
│   ├── judge_validation.csv         # Fase 4: 40 amostras + rotulações
│   ├── judge_validation_README.md   # protocolo de rotulagem
│   └── README.md                    # índice das duas runs
└── FEATURE_BRANCH_STUDY.md          # estudo local — NÃO versionado (.gitignore)
```

## Corpus local

O livro é *Designing Machine Learning Systems*, de Chip Huyen, primeira
edição, de 2022, PDF integral. A cópia local está em
`corpus/documentos/designing-machine-learning-systems-2022.pdf`
(excluída do Git; hash registrado em `corpus/manifest.csv`
— sha256 `688ba89d…`, idêntico ao das duas runs). No Colab, o PDF vive em
`Meu Drive/rag-dmls-v2/` e a célula de setup o valida e copia para o clone.

As 20 questões (`questions.json`, em inglês) definem `difficulty`, `category`
e `answer_rubric` — pontos obrigatórios (`must`) e alternativas aceitas —
**fixadas antes da run**; a `answer_key` da v1 é preservada como legado.

## v1 → v2: correções principais

1. **Repetições com variância real** — seeds `[42, 43, 44]` por repetição na
   temperatura 0 (a v1 era determinística: 58/60 respostas idênticas).
2. **Self-RAG corrigido** — na v1 o retry re-gerava **sobre as mesmas
   evidências** (sem nova recuperação; 18/18 revisões INCORRECT). Na v2 o
   retry faz **nova recuperação** com subquery derivada do draft + RRF.
3. **Adaptive RAG fiel ao paper** (Jeong et al. 2024) — roteador LLM de 3
   níveis via `prompts/router.txt`, decisões por pergunta com cache, subqueries
   derivadas da pergunta (a v1 usava 3 queries genéricas fixas e regex estática).
4. **Rubrica antes da run** — a v1 backfillava `answer_key` após a execução;
   a v2 usa `answer_rubric` (43 pontos `must` + 22 alternativas aceitas).
5. **Juiz com dedup + duplo voto** — cada resposta única é julgada 2× com
   seeds diferentes; discordância vira `JUDGE_DISAGREE`; auto-concordância
   ≥ 90% é assegurada por assert.
6. **Abstenção unificada** — regex única em `prompts/abstention.txt`
   (a métrica "Taxa de Alucinação" da v1 era, na verdade, abstenção).
7. **Proveniência completa** — hashes de config/questions no manifest, campo
   `gpu` registrado, trace em append, RESUME por (variante, repetição).
8. **Genéricas fixas removidas** — zero queries fixas no trace do adaptive.

## Execução no Colab (run v2)

1. Abrir o notebook direto do GitHub na branch:
   `https://colab.research.google.com/github/micarlio/rag-dmls-lab/blob/feat/v2-experiment/notebook.ipynb`
2. Runtime GPU (a run v2 usou **A100 80GB**; T4 funciona, só mais lenta).
3. Executar de cima para baixo: a célula 0a monta o Drive, valida o sha256
   do PDF contra o hash congelado da v1, clona a branch em
   `/content/rag-dmls-lab`, copia o PDF para o corpus e aponta
   `results_dir` para o Drive (`rag-dmls-v2/results/`).
4. Smoke test com 3 questões × 7 variantes antes da run oficial
   (7 × 20 × 3 = **420 respostas**, ~1,5–3h na A100).
5. Desconexão não perde trabalho: reexecute de cima para baixo — o setup
   reusa clone/PDF/Drive e a run retoma por (variante, repetição) via RESUME.
6. Grader → planilha `analise_rag_dmls_v2.xlsx` → análises
   (cobertura × precisão condicional, roteador `router_label × difficulty`,
   divergências entre variantes, sinal vs ruído).

Reprodução local: mesmo notebook (a célula de setup detecta que não está no
Colab e segue a configuração local, `results_dir: results_v2`).

## Resultados v2 (resumo com validação do juiz)

- **pure_llm** lidera: acurácia 0,95 (IC bootstrap 0,85–1,00), McNemar vs
  baseline **p = 0,0044** — o modelo conhece o livro; fechado não é batido
  por este RAG em questões conceituais.
- **Geração nunca erra quando o retrieval acerta**: precisão condicional
  ≈ 1,0 em todas as variantes com recuperação. **100% das perdas do RAG são
  falhas de recall** — abstenção honesta ("o contexto não contém X") em
  ~30% das tentativas (Q06, Q11, Q12, Q15, Q17 clusters).
- **embedding** é o melhor RAG (0,833; cobertura 0,80).
- **adaptive ≡ baseline** (p = 1,0): zero LABEL_A (o roteador nunca "abriu
  mão" do retrieval) e as subqueries do LABEL_C não resgataram os chunks
  perdidos. **self_rag ≡ baseline** (p = 1,0): o retry não salvou abstenção.
- **Q02** é o único ponto de valor do retrieval: puramente de cabeça, o
  `pure_llm` erra 3/3; com contexto, todas as variantes acertam.
- Seeds funcionaram: 40–60% das questões têm ≥ 2 textos distintos entre
  repetições (v1: ~3%); `adaptive_route` permanece 100% determinístico.
- **Validação do juiz (Fase 4, `results/judge_validation.csv`)**: acordo
  juiz × rotulador **85% (κ = 0,667)**, com viés unidirecional de leniência
  do juiz (4/4 abstenções CORRECT eram INCORRECT; 2 falsos-positivos
  temáticos). Números absolutos da v2 são teto; a ordenação se mantém.
- **Q15 está fora do corpus** (0 ocorrências de A/B testing, canary ou
  online evaluation no PDF — verificação mecânica em `scripts/bookcheck.py`):
  abster-se era a conduta correta e o juiz pune; o pure_llm acerta por
  conhecimento externo ao livro. Defeito de design documentado.
- ~91% das abstenções RAG da amostra de validação referem-se a conteúdo
  que **está no livro** → miss de recall real, não deficiência do gerador.

### Limitações

- Rotulador da Fase 4 é **LLM agente** (GLM, declarado no README de
  `results/`), não humano — protocolo auditável linha a linha, mas a
  calibração numérica pode diferir de uma rotulagem humana.
- `pure_llm` nunca absteve de fato (cobertura real 1,00): 5 respostas
  contêm frase de hedge que o detector de abstenção classificou como
  abstenção (falso positivo → "cobertura" 0,90 subestima o pure_llm;
  a precisão condicional 0,944 é calculada sobre essa base).
- Acurácias por questão (n = 20) têm IC largos; inferência pareada
  (McNemar) é a mais informativa.
- Latência não é comparável entre v1 (RTX PRO 6000 Blackwell) e v2
  (A100) — comparação apenas intra-run.

## Resultados (artefatos)

Run v1 (congelada): `results/run_2026-10-15_v1/` — ver `SNAPSHOT.md`
para a proveniência completa (3 variantes × 20 × 3 = 180 respostas).

Run v2 (a referência é o Drive `rag-dmls-v2/results/`; cópia local nos
mesmos arquivos): `accuracy.csv`/`accuracy_summary.csv` (juiz duplo-voto),
`coverage_precision.csv` (métrica primária), gravando por (variante,
repetição) `<variante>_r{1,2,3}.csv`, `router_analysis.csv`
(`router_label × difficulty`), `router_log.json` (auditoria das decisões),
`divergencias_variantes.csv`, `run_manifest.json` (hashes + gpu),
`traces/v2_runs.jsonl` (420 eventos com evidências), `analise_rag_dmls_v2.xlsx`,
`judge_validation.csv` (Fase 4).

## Repositório independente

Esta pasta é a raiz de um repositório Git próprio, separado do material da
disciplina. O remoto `origin` aponta para
[`micarlio/rag-dmls-lab`](https://github.com/micarlio/rag-dmls-lab)
(branch `feat/v2-experiment` na v2). O PDF comercial permanece fora do Git;
quem reproduzir deve disponibilizar a cópia da mesma edição no caminho
indicado em `corpus/manifest.csv`. `FEATURE_BRANCH_STUDY.md` é material
local de estudo, presente apenas nesta pasta (listado no `.gitignore`).
