#!/usr/bin/env python3
"""Fase 4 - gerador da amostra de validacao humana do juiz (judge validation).

Seleciona 40 respostas uteis (dedup por hash do texto) estratificadas para
o rotulador humano julgar contra a rubrica, com foco nos pontos fracos do
juiz-automatico:

  A) leniency: abstencoes que o juiz marcou CORRECT (max 4)
  B) pure_llm INCORRECT (unicas falhas do closed-book)        (todas)
  C) embedding INCORRECT sem abstencao                        (max 3)
  D) abstencao honesta INCORRECT - 2 por variante com retrieval (11)
  E) CORRECT sem abstencao, estratificado por variante        (resto ate 40)

Saidas:
  results/judge_validation.csv  (o rotulador preenche as colunas human_*)
Uso:
  python scripts/build_judge_validation.py [--results-dir DIR]
  DIR deve conter accuracy.csv e traces/v2_runs.jsonl (download do Drive).
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(7)
DEFAULT_RESULTS = Path('/home/rodrigo/Documentos/UFRN/2026.2 - PROJETO DE SISTEMAS BASEADOS EM APRENDIZADO DE MAQUINA/results')


def load(results_dir):
    acc = pd.read_csv(results_dir / 'accuracy.csv')
    tr = [json.loads(l) for l in open(results_dir / 'traces' / 'v2_runs.jsonl', encoding='utf-8')]
    return acc, tr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results-dir', type=Path, default=DEFAULT_RESULTS)
    args = ap.parse_args()

    acc, tr = load(args.results_dir)
    abst_re = re.compile((REPO / 'prompts' / 'abstention.txt').read_text(encoding='utf-8').strip(), re.IGNORECASE)
    questions = json.loads((REPO / 'questions.json').read_text(encoding='utf-8'))['questions']
    q = {x['id']: x for x in questions}

    # texto + evidencia da 1a ocorrencia de cada resposta unica
    acc['answer'] = [next(t['answer'] for t in tr
                          if (t['question_id'], t['variant'], t['repetition'])
                          == (r.question_id, r.variant, r.repetition)) for r in acc.itertuples()]
    uniq = acc.drop_duplicates('answer_sha', keep='first').reset_index(drop=True)
    uniq['is_abst'] = uniq['answer'].map(lambda s: bool(abst_re.search(str(s))))
    uniq['correct'] = uniq['verdict'] == 'CORRECT'
    occ = acc.groupby('answer_sha').agg(
        n_occ=('answer_sha', 'size'),
        variants_seen=('variant', lambda v: ','.join(sorted(set(v)))),
    )
    uniq = uniq.merge(occ, left_on='answer_sha', right_index=True, validate='1:1')

    buckets = {}
    pool = lambda f: uniq.index[f].tolist()  # noqa: E731

    # A) leniency: abst & CORRECT
    a = pool(uniq.is_abst & uniq.correct)
    buckets['A_lenient_correct'] = a[:4]
    # B) pure_llm INCORRECT (o unico erro do closed-book)
    b = pool((~uniq.is_abst) & (~uniq.correct) & (uniq.variant == 'pure_llm'))
    buckets['B_pure_llm_error'] = b
    # C) embedding INCORRECT sem abstencao
    c = pool((~uniq.is_abst) & (~uniq.correct) & (uniq.variant == 'embedding'))
    buckets['C_embedding_error'] = c[:3]
    # D) abstencao honesta INCORRECT: 2 por variante com retrieval, 1 no embedding
    d = []
    for v in ['baseline', 'adaptive_route', 'adaptive_full', 'adaptive_expansion', 'self_rag']:
        pool_d = pool(uniq.is_abst & (~uniq.correct) & (uniq.variant == v))
        RNG.shuffle(pool_d)
        d += pool_d[:2]
    pool_e1 = pool(uniq.is_abst & (~uniq.correct) & (uniq.variant == 'embedding'))
    RNG.shuffle(pool_e1)
    d += pool_e1[:1]
    buckets['D_honest_abstention'] = d
    # E) CORRECT sem abstencao, estratificado ate fechar 40
    plan_e = {'pure_llm': 6, 'baseline': 3, 'embedding': 3, 'self_rag': 3,
              'adaptive_route': 2, 'adaptive_full': 2, 'adaptive_expansion': 2}
    e = []
    taken = set(sum(buckets.values(), []))
    for v, n in plan_e.items():
        pool_v = pool((~uniq.is_abst) & uniq.correct & (uniq.variant == v) & (~uniq.index.isin(taken)))
        RNG.shuffle(pool_v)
        e += pool_v[:n]
    buckets['E_correct_answered'] = e
    # completar/ajustar para exatamente 40
    flat = sum(buckets.values(), [])
    rest = ~uniq.index.isin(flat)
    while len(flat) < 40:
        cand = uniq.index[rest].tolist()
        if not cand:
            break
        flat.append(cand[int(RNG.integers(len(cand)))])
        rest = ~uniq.index.isin(flat)
    buckets['_fill'] = flat[len(sum([v for k, v in buckets.items() if k != '_fill'], [])):]

    sel = uniq.loc[flat].copy()
    sel['bucket'] = [k for k, idxs in buckets.items() for _ in idxs]
    sel['sample_id'] = [f'JV{i:02d}' for i in range(1, len(sel) + 1)]
    sel['rubric_musts'] = sel.question_id.map(lambda qid: '\n'.join('- ' + p for p in q[qid]['answer_rubric']['must']))
    sel['rubric_alternatives'] = sel.question_id.map(
        lambda qid: '\n'.join('- ' + p for p in q[qid]['answer_rubric'].get('accepted_alternatives', [])) or '(none)')
    sel['question_text'] = sel.question_id.map(lambda qid: q[qid]['question'])
    sel['category'] = sel.question_id.map(lambda qid: q[qid].get('category', ''))
    sel['difficulty'] = sel.question_id.map(lambda qid: q[qid].get('difficulty', ''))

    out_cols = ['sample_id', 'bucket', 'question_id', 'question_text', 'category', 'difficulty',
                'variant', 'repetition', 'answer', 'rubric_musts', 'rubric_alternatives',
                'is_abst', 'vote_1', 'vote_2', 'verdict', 'n_occ', 'variants_seen',
                # colunas do rotulador humano
                'human_verdict', 'content_in_book', 'human_note']
    sel = sel.reindex(columns=sel.columns.tolist() + ['human_verdict', 'content_in_book', 'human_note'])
    for c in ('human_verdict', 'content_in_book', 'human_note'):
        sel[c] = ''
    out = sel[out_cols].copy()
    out_dir = REPO / 'results'
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / 'judge_validation.csv'
    out.to_csv(out_path, index=False)

    print(f'gravado: {out_path} ({len(out)} amostras)')
    print('\n=== estratificacao (bucket x veredicto do juiz) ===')
    print(out.groupby(['bucket', 'verdict']).size().to_string())
    print('\n=== por variante ===')
    print(out.variant.value_counts().to_string())
    print(f'\nabst: {int(out.is_abst.sum())} | CORRECT (juiz): {int(out.verdict.eq("CORRECT").sum())}')


if __name__ == '__main__':
    sys.exit(main())
