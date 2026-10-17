#!/usr/bin/env python3
"""Fase 4 - apoio mecanico para o content_in_book.

Para cada questao das 40 amostras, busca no PDF integral (pypdf, chunks de
800 chars como no experimento) os termos-chave derivados da pergunta e das
abstencoes alegadas, e reporta: presente/ausente + citacao curta + pagina.
Saida: /tmp/opencode/bookcheck.csv
"""
import json
import re
from pathlib import Path

import pandas as pd

REPO = Path('/home/rodrigo/Documentos/UFRN/2026.2 - PROJETO DE SISTEMAS BASEADOS EM APRENDIZADO DE MAQUINA/rag-dmls-lab')
PDF = REPO / 'corpus' / 'documentos' / 'designing-machine-learning-systems-2022.pdf'
if not PDF.exists():
    PDF = Path('/home/rodrigo/Downloads/Programas/designing-machine-learning-systems-2022.pdf')

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

TERM_SETS = {
    'Q01': ['quality and quantity', 'data foundations', 'foundational'],
    'Q02': ['better algorithms', 'more data', 'intelligent algorithms'],
    'Q03': ['simple baseline', 'baseline model', 'baseline'],
    'Q04': ['label noise', 'collection bias', 'data quality'],
    'Q05': ['feedback loop', 'hidden feedback loops'],
    'Q06': ['monitoring', 'monitor the system', 'data distribution shifts'],
    'Q07': ['evaluation', 'deployment', 'post-deployment'],
    'Q08': ['slice', 'slices', 'subset'],
    'Q09': ['training data', 'prediction', 'distribution shift'],
    'Q10': ['latency', 'throughput', 'batch', 'online'],
    'Q11': ['retrain', 'retraining', 'retraining decisions'],
    'Q12': ['monitoring', 'logging', 'log'],
    'Q13': ['rare events', 'underrepresented', 'underrepresented groups', 'minority'],
    'Q14': ['deployment strategies', 'continuous deployment', 'data science pipeline'],
    'Q15': ['A/B test', 'A/B testing', 'canary', 'shadow'],
    'Q16': ['data pipeline', 'reproducibility', 'pipeline'],
    'Q17': ['technical debt', 'ML debt', 'C4 model'],
    'Q18': ['batch prediction', 'online prediction'],
    'Q19': ['model selection', 'explainability', 'inference cost'],
    'Q20': ['workflow', 'end user', 'whole workflow'],
}


def chunkify(text):
    chunks = []
    cur = 0
    while cur < len(text):
        chunks.append(text[cur:cur + CHUNK_SIZE])
        cur += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def main():
    from pypdf import PdfReader
    reader = PdfReader(str(PDF))
    pages = [(i, p.extract_text() or '') for i, p in enumerate(reader.pages)]
    chunks = []
    for page_no, text in pages:
        for ch in chunkify(text):
            chunks.append((page_no + 1, ch))
    print(f'{len(chunks)} chunks de {len(pages)} paginas')

    rows = []
    for qid, terms in TERM_SETS.items():
        found = []
        for term in terms:
            pat = re.compile(re.escape(term.lower()))
            hits = [(pg, ch) for pg, ch in chunks if pat.search(ch.lower())]
            if hits:
                pg, ch = hits[0]
                pos = ch.lower().find(term.lower())
                quote = ch[max(0, pos - 60):pos + 80].replace('\n', ' ')
                found.append((term, len(hits), pg, quote))
        if found:
            term, n, pg, quote = max(found, key=lambda x: x[1])
            rows.append({'question_id': qid, 'in_book': 'sim',
                         'terms_ok': ','.join(f'{t}({n})' for t, n, _, _ in found),
                         'page': pg, 'quote': quote.strip()})
        else:
            rows.append({'question_id': qid, 'in_book': 'NAO',
                         'terms_ok': '', 'page': '', 'quote': ''})

    out = pd.DataFrame(rows)
    out.to_csv('/tmp/opencode/bookcheck.csv', index=False)
    print(out[['question_id', 'in_book', 'terms_ok', 'page']].to_string(index=False))


if __name__ == '__main__':
    main()
