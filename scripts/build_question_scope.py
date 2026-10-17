#!/usr/bin/env python3
"""v3: gera configs/question_scope.json - escopo do corpus por questao.

Para cada uma das 20 questoes busca termos-chave no PDF integral (pypdf,
mesmo chunking do experimento) e grava in_book + citação curta + página.
O grader usa in_book para distinguir abstencao justificada (tema fora do
corpus) de miss de retrieval.

Uso: python scripts/build_question_scope.py
Saida: configs/question_scope.json
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'configs' / 'question_scope.json'

TERM_SETS = {
    'Q01': ['quality and quantity', 'data foundations', 'foundational', 'data quality'],
    'Q02': ['more data', 'intelligent algorithms', 'better algorithms'],
    'Q03': ['simple baseline', 'baseline model', 'baselines'],
    'Q04': ['selection bias', 'bias', 'noise', 'data quality'],
    'Q05': ['feedback loop', 'feedback loops'],
    'Q06': ['monitoring', 'data distribution shifts'],
    'Q07': ['evaluation', 'deployment'],
    'Q08': ['slice', 'slices', 'subset'],
    'Q09': ['distribution shift', 'training data'],
    'Q10': ['latency', 'throughput', 'batch', 'online'],
    'Q11': ['retrain', 'retraining'],
    'Q12': ['monitoring', 'logging', 'logs'],
    'Q13': ['rare events', 'underrepresented', 'minority', 'fairness'],
    'Q14': ['engineering', 'deployment', 'infrastructure'],
    'Q15': ['a/b', 'canary', 'shadow deployment', 'online evaluation', 'interleaving'],
    'Q16': ['data pipeline', 'reproducibility', 'pipeline'],
    'Q17': ['technical debt', 'C4 model'],
    'Q18': ['batch prediction', 'online prediction'],
    'Q19': ['model selection', 'explainability', 'inference cost'],
    'Q20': ['workflow', 'end user', 'end-to-end'],
}


def chunkify(text, size=800, overlap=120):
    out, cur = [], 0
    while cur < len(text):
        out.append(text[cur:cur + size])
        cur += size - overlap
    return out


def find_pdf():
    for cand in [REPO / 'corpus' / 'documentos' / 'designing-machine-learning-systems-2022.pdf',
                 Path('/home/rodrigo/Downloads/Programas/designing-machine-learning-systems-2022.pdf')]:
        if cand.exists():
            return cand
    raise FileNotFoundError('PDF local do livro não encontrado.')


def main():
    from pypdf import PdfReader
    reader = PdfReader(str(find_pdf()))
    text = ''.join((p.extract_text() or '') for p in reader.pages)

    scope = {}
    total_absent = 0
    for qid in sorted(TERM_SETS):
        hits = []
        for term in TERM_SETS[qid]:
            n = len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
            if n:
                i = text.lower().find(term.lower())
                hits.append((term, n, max(1, text[:i].count('\f') + text[:i].count('\x0c')) + 1,
                             text[max(0, i - 50):i + 80].replace('\n', ' ').strip()))
        if hits:
            best = max(hits, key=lambda h: h[1])
            scope[qid] = {'in_book': True, 'best_term': best[0],
                          'best_count': best[1], 'quote': best[3],
                          'terms_found': [h[0] for h in hits]}
        else:
            scope[qid] = {'in_book': False, 'best_term': None,
                          'best_count': 0, 'quote': '',
                          'terms_found': [], 'searched_terms': TERM_SETS[qid]}
            total_absent += 1

    OUT.write_text(json.dumps(scope, ensure_ascii=False, indent=2) + '\n',
                   encoding='utf-8')
    print(f'{OUT} | {len(scope)} questões | fora do corpus: {total_absent}')
    for qid, v in scope.items():
        if not v['in_book']:
            print(f'  {qid}: FORA DO CORPUS (termos buscados: {v["searched_terms"]})')


if __name__ == '__main__':
    main()
