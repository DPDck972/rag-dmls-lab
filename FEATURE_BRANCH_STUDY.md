# Feature Branch Study — `feat/rag-experiment-evaluation`

**Repo:** https://github.com/micarlio/rag-dmls-lab.git
**Branch:** `origin/feat/rag-experiment-evaluation`
**Head:** `3acb00c` — `docs: correct repository tree in readme` (2026-10-15)
**Base:** `509bec4` (`main`) by micarlo — 2026-10-12
**Status:** 9 commits ahead of `main`, linear history, no merge.
**Study updated for:** head `3acb00c` (previously studied at `1eadf5a`).

## 1. Purpose

Original commit (still the base of the branch): turn the empty scaffold on
`main` into a runnable demo scaffold.

Since then the branch matured into the **official experiment**: 3 pipeline
variants (baseline / adaptive / self_rag) × 20 questions × 3 repetitions =
180 answers, persisted to `results/` with a grader, traces, manifest,
diagnostics and figures. Docs now describe an executed experiment.

## 2. Tree (current)

```
README.md, notebook.ipynb, questions.json, requirements.txt
configs/experiment.json
corpus/README.md, corpus/manifest.csv, corpus/documentos/*.pdf (gitignored)
prompts/README.md, prompts/generator.txt
results/
├── accuracy.csv, accuracy_summary.csv, summary.csv
├── baseline_r1..r3.csv, self_rag_r1..r3.csv, results_adaptive.csv
├── by_repetition/{adaptive,baseline,self_rag}_r1..r3.csv
├── disagreements.csv, divergencias_variantes.csv, diagnostico_baseline.csv
├── run_manifest.json
├── analise_rag_dmls.xlsx
├── imagem/{acuracia_sinal_ruido,boxplot_latencia,chamadas_e_latencia,qualidade_respostas}.png
└── traces/official_runs.jsonl
docs/README.md
```

Note: `projeto_RAG.ipynb` (whole Colab run dump) was added in `405c6ab`
and removed in `7d4eda5`, its content merged into `notebook.ipynb`.
`corpus/manifest.csv` still unchanged vs `main`.

## 3. Commit history

| Commit | Author | Date | Summary |
|---|---|---|---|
| `1eadf5a` | Arles Wasb | 10-13 | feat: prepare RAG experiment for evaluation (original study target) |
| `63fec83` | rdrgmnzs | 10-14 | feat: implement general generator prompt loading and formatting |
| `405c6ab` | Arles Wasb (co: Copilot) | 10-14 | feat: add official RAG experiment results |
| `5383695` | Arles Wasb | 10-14 | chore: record remaining experiment traces |
| `b529c0d` | Arles Wasb | 10-14 | chore: record final experiment outputs |
| `88ed992` | Arles Wasb | 10-14 | chore: append latest experiment trace |
| `7d4eda5` | Arles Wasb (co: Copilot) | 10-14 | feat: update RAG experiment notebook and results |
| `a973bcd` | Arles Wasb (co: Copilot) | 10-14 | docs: align readmes with completed experiment |
| `3acb00c` | Arles Wasb (co: Copilot) | 10-15 | docs: correct repository tree in readme |

- `63fec83` is the only commit by rdrgmnzs; everything else Arles Wasb,
  several marked `Co-authored-by: Copilot`.
- The three `chore` commits (`5383695`–`88ed992`) append CSV rows and JSONL
  trace lines incrementally while server repetitions were completing.
- `7d4eda5` is the big rewrite: notebook expansion + regenerated final
  result files; it also reintroduces `per_repetition/` and drops
  `results/README.md`.

## 4. Config — `configs/experiment.json`

Only delta vs `1eadf5a`: added `"self_rag_repetitions": 3`.

Note: `status` is still `"scaffold_ready"` even though the run happened.
A `"run_done"`-style update was never made.

## 5. Questions — `questions.json`

Unchanged from `1eadf5a`: 20 questions, no answer-key field.
See Gap §12.1 — the grader expects `answer_key`, and the run that produced
`accuracy.csv` clearly used one (its log prints "Loaded answer key for 20
questions"), so the committed file is not the file that the run graded.

## 6. Notebook — `notebook.ipynb` (50 cells)

Executed-output notebook (`colab` metadata, accelerator GPU, kernelspec
`python3`); outputs show `/content/results/...` paths and a GPU
NVIDIA RTX PRO 6000 Blackwell (97887 MiB). The old small 7-cell layout was replaced.

Functional blocks (cell ids in labels):

- **Setup (0–9):** pip install, Ollama install, `ollama serve`,
  `ollama pull qwen2.5:7b` + `llama3.1:8b`, warmups. Idempotent, guarded.
- **Config load (10–11):** `find_root()` works both on Colab and local
  (`questions.json` + experiment.json markers); loads config and questions.
- **Corpus (12–15):** `read_pdf_pages()` + `chunk_pages_with_source()`
  (800/120) → **713 chunks**; chunks carry page provenance.
- **Retrieval (16–18):** TF-IDF (`stop_words=english`, ngram 1-2);
  `expand_query()`; `retrieve_top_k(..., expand=)` — `expand=False` keeps
  raw query; `format_prompt()` loads `prompts/generator.txt` template
  (`{question}` / `{context}`); keyword `route_question()` with the 10
  regexes below.
- **Generation & variants (19–20):** `call_ollama()` POST
  `127.0.0.1:11434/api/generate` with `temperature=0.0` and
  `seed=42`; `build_context()` numbered `[Passage i]` truncated at 1600
  chars; `rrf_fuse()` reciprocal-rank fusion (c=60);
  `adaptive_retrieve()`; `answer_question_baseline/adaptive/self_rag`.
- **Smoke test (21–22):** first 5 questions × 3 variants, asserts non-empty
  answers, Ollama reachable, latency in [0,600], Self-RAG verdicts parse,
  llm_calls contract (2 w/o revision, 3 w/ revision).
- **Official run (23–29):** pre-checks (rrf in source, expand param,
  dataset size); `call_ollama` wrapper for call counting; `warmup()` per
  variant; `sha256_file()`; per-variant loops that write
  `results/{baseline,self_rag}_r*.csv`, `results_adaptive.csv`,
  `per_repetition/*.csv`, `traces/official_runs.jsonl`,
  `run_manifest.json`.
- **Grader (30–31):** answer key; judge LLM **`llama3.1:8b`**, one-word
  contract CORRECT|INCORRECT via regex; grades 180 answers →
  `accuracy.csv`/`accuracy_summary.csv`; per-difficulty breakdown; Self-RAG
  cost-benefit cross (did `revised` answers change verdicts);
  divergent-verdict questions.
- **Analysis (32–49):** `analise_rag_dmls.xlsx` (openpyxl bars),
  seaborn boxplot of latency, per-question diagnosis table with baseline
  chunks + gabarito, sinal-vs-ruído figure, variant-divergences table,
  llm_calls/latency by difficulty, qualitative evaluation, conclusions
  (signal vs noise, abstention figure, limitations list).

## 7. Routing & variant pipelines

Route patterns (from `run_manifest.json`, same 10 markers as demo):
`\bcompar\w*`, `\btrade-?offs?\b`, `\barchitectures?\b`,
`\bdesign(?:s|ing|ed)?\b`, `\bmonitor(?:ing)?\b`, `\blatenc(?:y|ies)\b`,
`\bcosts?\b`, `\bobservabilit\w*`, `\bsystems?\b`, `\bserving\b`.

Route list: 6 questions → baseline route (Q01, Q07, Q08, Q09, Q11, Q14),
14 → adaptive.

| Aspect | Baseline | Adaptive | Self-RAG |
|---|---|---|---|
| Retrieval | raw query, top_k | `expand_query` + (if routed) 3 fixed extra queries, RRF-fused, top_k | raw query (no expansion), top_k |
| LLM calls | 1 | 1 | 2–3 (draft → verifier → optional regen) |
| Verifier | — | — | `SUPPORTED`/`NOT_SUPPORTED`, same qwen2.5:7b |
| Latency avg | 0.54 s | 0.37 s | 0.63 s |
| Regeneration | never | never | only if `NOT_SUPPORTED` |

`rrf_fuse` is expected in `adaptive`'s `hits`; `baseline` and `self_rag`
share identical retrieval — that's the controlled comparison.

## 8. Execution environment

Local Ollama on a GPU server (NVIDIA RTX PRO 6000 Blackwell, 97 GB),
`temperature: 0.0` and `seed: 42` for determinism. Latencies of 0.19–0.675 s
per answer vs the demo's 9.6–20.2 s. `per_repetition/` side-copies isolate
variance by repetition. Duplicates dedup key `text[:200]`.
Trace: 180 lines

## 9. Results

`accuracy_summary.csv` (judge = llama3.1:8b):

| variant | accuracy | parse_errors | n |
|---|---|---|---|
| adaptive | 0.40 | 0 | 60 |
| baseline | 0.30 | 0 | 60 |
| self_rag | 0.30 | 0 | 60 |

Notebook's own caveat (cell 49): the judge was never validated against human
grading. **Adaptive's win comes from abstention:** it abstains ~60% of the
time (regex-detected) and is 24/24 correct when it answers; baseline and
self_rag answer 42× and are 18/42 correct. Self-RAG's extra 2–3 LLM calls
bought no accuracy (0.30, same as baseline).

Artifacts: `acuracia_sinal_ruido.png`, `boxplot_latencia.png`,
`chamadas_e_latencia.png`, `qualidade_respostas.png` under `results/imagem/`,
`analise_rag_dmls.xlsx`, `por_repetition/*.csv`.

## 10. Dependencies — `requirements.txt`

Unchanged vs `1eadf5a`: `requests, pypdf, pandas, numpy, matplotlib,
scikit-learn` with `>=` minimums. No chromadb; no vector DB. Ollama
remains an external requirement (server + two model pulls: qwen2.5:7b and
llama3.1:8b for judging).

## 11. Docs state

- `README.md`: updated to "experimento executado", structure tree with
  the full `results/` layout (this tree had to be corrected once more in
  `3acb00c`).
- `prompts/README.md`: now says `generator.txt` is versioned and used;
  router & Self-RAG criticism remain **in code**, no separate prompt files
  for router/decomposer/verifier.
- `corpus/README.md`: acknowledges TF-IDF-only lexical retrieval;
  embeddings still pending; PDF excluded from Git, hash registered in
  `corpus/manifest.csv` and `run_manifest.json` (`688ba...`).
- `docs/README.md`: article/slides still pending; methodology checklist
  (20 questions, categories, model config, metrics, TF-IDF limits,
  smoke-vs-official separation) recorded; nothing written yet.
- `results/README.md` was **deleted** (its contract list §8 of the old
  study is satisfied in practice by the actual files).

## 12. Gaps before "article-ready" (updated)

1. **`questions.json` lacks answer keys** — the grader requires
   `answer_key`/`answer` per question; the committed file would fail the
   very first grader assert. The accuracy numbers reproduce only with a
   local (uncommitted) variant of this file.
2. Router (10 regexes) and Self-RAG verifier prompt are hard-coded in
   notebook — still not prompt files (generator.txt remains the only
   versioned prompt).
3. Self-RAG verifier uses the **same generator model** (qwen2.5:7b), not
   a dedicated critic model; `llama3.1:8b` is only the accuracy judge.
4. `configs/experiment.json` `status` still `scaffold_ready` despite the
   executed run.
5. `results/README.md` was deleted; no replacement contract lives in
   `results/`, the README tree lists the artifacts but not their schemas.
6. Corpora: 713 chunks but 4-chapter slice definition still by way of
   hard-coded notebook slicing, still not reproducible from config alone.
7. The Colab reproduce path improved (setup cells, GPU noted in README)
   but is worded as "still needs validation".
8. Judge model unvalidated — flagged as limitation in cell 49.
9. Abstentions are detected by regex inside the analysis cell only (no
   column persisted in `accuracy.csv`); the 24/24-precision claim is not
   stored in a dedicated artifact.
10. `main` is still the empty scaffold — everything (source + results)
    lives only on this branch.

## 13. Reproduce

1. `git clone` branch; place PDF at
   `corpus/documentos/designing-machine-learning-systems-2022.pdf`
   (SHA-256 must match manifest's `688ba89d...`).
2. `questions.json` must have `answer_key`(-like) fields per question
   (committing them is pending — §12.1).
3. Install requirements, start Ollama, `pull qwen2.5:7b` and
   `pull llama3.1:8b`.
4. Set GPU accelerator (or accept slow CPU latencies) and open notebook;
   run cells in order. Official run writes to `results/`.

## 14. Verdict

Demo → executed experiment in 8 commits over two days. Results are honest
about their own limitations (unvalidated judge, abstention as source of
Adaptive's advantage, no causal claims about divergences). Single-point-of-
work risks: results were produced inside one Colab session with local
`/content` paths; the answer key that graded them is not in the repo. Fix
§12.1, commit the study file itself (`FEATURE_BRANCH_STUDY.md` is untracked),
and this branch is genuinely close to merge-ready.
