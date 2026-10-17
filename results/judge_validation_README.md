# Fase 4 — Validação humana do juiz (judge_validation.csv)

**Arquivo:** `results/judge_validation.csv` (40 amostras, deduplicadas por texto da resposta).

## Tarefa

Para cada linha, julgar a `answer` **contra a rubrica** (como o juiz faria), sem olhar o
veredicto do juiz antes de decidir:

1. `human_verdict` — `CORRECT` se a resposta transmite o núcleo de **todos** os pontos
   `rubric_musts` (ou um ponto de `rubric_alternatives` válido); `INCORRECT` caso
   contrário (incluindo abstenções — abstener de responder não cobre a rubrica).
2. `content_in_book` — `sim` / `nao` / `incerto`: o conteúdo necessário para responder
   **existe no livro**? (consulte o PDF: `corpus/documentos/…2022.pdf`). Preencher
   especialmente nas abstenções (`is_abst=True`): o modelo alegou "não está no
   contexto" — verifique se a alegação é verdadeira **contra o livro inteiro**, não
   só contra os 4 chunks recuperados.
3. `human_note` — comentário livre opcional (ex.: juiz leniente, rubrica ambígua).

## O que cada bucket quer medir

| bucket | manual |
|---|---|
| `A_lenient_correct` | abstenções que o juiz julgou CORRECT — medir leniência |
| `B_pure_llm_error` | falhas do closed-book (o único erro do pure_llm) |
| `C_embedding_error` | erros com resposta dada no melhor RAG |
| `D_honest_abstention` | abstenções INCORRECT — confirmar recall do retrieval |
| `E_correct_answered` / `_fill` | amostra correta para medir falso-positivo |

`n_occ` / `variants_seen` dizem quantas das 420 respostas aquela amostra representa
(o mesmo texto repetiu entre variantes/repetições — a ponderação usa `n_occ`).

## Após preencher

Devolver o CSV; o cálculo de concordância (por bucket e por variante), kappa e o
relatório ficam com o time. Preencher no Excel/LibreOffice mantendo as colunas.
