#!/usr/bin/env python3
"""Fase 4 - preenchimento da validacao do juiz pelo rotulador-LLM.

O GLM (agente) julga as 40 amostras contra a rubrica, seguindo o README.
Proveniencia: rotulador = LLM agente, nao humano. Auditavel via human_note.
Preenche human_verdict, content_in_book, human_note e imprime as metricas.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'results' / 'judge_validation.csv'

# (sample_id, human_verdict, content_in_book, human_note)
LABELS = [
    ('JV01', 'INCORRECT', 'sim',
     'Abstencao honesta sobre o contexto recuperado, mas o tema esta no '
     'livro (cap 01: a maior parte do projeto e engineering). Miss de '
     'retrieval. Juiz leniente: marcou CORRECT numa abstencao que nao '
     'cobre a rubrica.'),
    ('JV02', 'INCORRECT', 'sim',
     'Abstencao. O trade-off de selecao (custo, latencia, estabilidade, '
     'explicabilidade) aparece no livro, com cobertura fina. Abstencao '
     'nao cobre a rubrica: INCORRECT.'),
    ('JV03', 'INCORRECT', 'sim',
     'Reconhece o trade-off em um chunk e absteve; nucleo da rubrica nao '
     'transmitido. Tema percente ao livro, mas com cobertura fina.'),
    ('JV04', 'INCORRECT', 'sim',
     'Abstencao. Bias e noise estao no livro (cap 03: selection bias, '
     'noise e quality com muitas ocorrencias). Miss de retrieval.'),
    ('JV05', 'INCORRECT', 'sim',
     'pure_llm alega que o livro nao foi especificado: erro de contrato, '
     'o prompt implica o corpus DMLS. O debate data versus algoritmos '
     'esta no livro (page 20, citacao de Rogati). Falha 3 vezes.'),
    ('JV06', 'INCORRECT', 'sim',
     'Mesma resposta de JV05, texto repetido entre repeticoes.'),
    ('JV07', 'INCORRECT', 'sim',
     'Resposta so menciona accuracy metrics. A rubrica pede sinais de '
     'data (drift, valores faltantes, outliers) e de model (drift de '
     'predicoes, confianca). Monitoring e cap 06 do livro; o embedding '
     'recuperou mal. Concorda com o juiz.'),
    ('JV08', 'INCORRECT', 'sim',
     'Abstencao; mesmo comentario de JV01. Tema no livro, retrieval '
     'perdeu.'),
    ('JV09', 'INCORRECT', 'sim',
     'Abstencao; monitoring e logging sao cap 06-07. Miss de retrieval, '
     'abstencao honesta: sem inventar conteudo (gating funcionou).'),
    ('JV10', 'INCORRECT', 'sim',
     'Abstencao; tema no livro com cobertura fina (model selection, '
     'explainability). Miss de retrieval.'),
    ('JV11', 'INCORRECT', 'sim',
     'Abstencao; monitoring signals sao texto inteiro do cap 06. Miss '
     'de retrieval genuino (granularidade ou indice).'),
    ('JV12', 'INCORRECT', 'sim',
     'Idem JV09, mesma questao no adaptive_expansion.'),
    ('JV13', 'INCORRECT', 'nao',
     'VERIFICACAO MECANICA: A/B testing, canary e online evaluation tem '
     'ZERO ocorrencias no PDF 2022. Questao fora do corpus. A abstencao '
     'era a conduta correta e o juiz pune honestidade. Defeito de '
     'design do questionario. pure_llm so acerta com conhecimento '
     'externo ao livro.'),
    ('JV14', 'INCORRECT', 'sim',
     'Abstencao; tema do cap 03. Miss de retrieval.'),
    ('JV15', 'INCORRECT', 'sim',
     'FALSO POSITIVO DO JUIZ: resposta define loop generico (mercado '
     'financeiro, software) e nunca apresenta o mecanismo centrado do '
     'livro: predicoes do modelo alimentam dados de treino (feedback '
     'loops, chapter 2/9). A rubrica exige as duas coisas: INCORRECT.'),
    ('JV16', 'CORRECT', 'sim',
     'Nucleo presente: offline controlado versus producao real com '
     'dados novos. Nao nomeia distribution shift nem feedback loops '
     'explicitamente. Cobertura parcial, nucleo ok.'),
    ('JV17', 'CORRECT', 'sim',
     'Amplitude de engineering coberta (dados, deployment, monitoring, '
     'escalabilidade, confiabilidade). Resposta generica mas cobre os '
     'dois musts da rubrica.'),
    ('JV18', 'CORRECT', 'sim',
     'Drift detection e metricas em trafego real presentes. Faltam '
     'valores faltantes, outliers e sinais de confianca: nucleo '
     'presente.'),
    ('JV19', 'CORRECT', 'sim',
     'Custo, estabilidade e explicabilidade balanceados. Resposta de '
     'memoria (with no corpus), mas cobre os musts.'),
    ('JV20', 'CORRECT', 'nao',
     'A/B tests e metricas comportamentais: conteudo correto, porem o '
     'tema tem ZERO ocorrencias no livro. Venceu por knowledge '
     'parametrico fora do corpus. Corrobora o achado de Q15: a unica '
     'forma de acertar era de memoria.'),
    ('JV21', 'CORRECT', 'sim',
     'Debate caracterizado com posicao data-centric aceitavel '
     '(alternativa valida da rubrica). Cita Rogati e AlexNet do '
     'contexto.'),
    ('JV22', 'CORRECT', 'sim',
     'Batch periodico e barato versus online imediato e caro: nucleo '
     'presente. Nuance de stale e de entidades conhecidas a priori '
     'ausente.'),
    ('JV23', 'INCORRECT', 'sim',
     'FALSO POSITIVO DO JUIZ: responde sobre slices e Simpson paradox '
     '(tema de Q08) e nao os musts de workflow: qualidade do modelo '
     'nao e qualidade do sistema; coleta, labeling e serving influenciam '
     'o resultado. A primeira frase ecoa a pergunta; a justificativa '
     'mira o tema errado.'),
    ('JV24', 'CORRECT', 'sim',
     'Trade-off central presente. Nuance de stale ausente.'),
    ('JV25', 'CORRECT', 'sim',
     'Slices com fairness, dados direcionados e imbalance: musts '
     'cobertos.'),
    ('JV26', 'CORRECT', 'sim',
     'Idem JV24, texto quase identico.'),
    ('JV27', 'CORRECT', 'sim',
     'Design hibrido (precompute para queries populares, online para o '
     'resto) presente: alternativa valida da rubrica.'),
    ('JV28', 'CORRECT', 'sim',
     'Agregado mascara subgrupos, com mecanismo claro.'),
    ('JV29', 'CORRECT', 'sim',
     'Idem JV21, texto igual (self_rag converge para o baseline).'),
    ('JV30', 'CORRECT', 'sim',
     'Idem JV21 (adaptive_route deterministico, mesmo texto).'),
    ('JV31', 'CORRECT', 'sim',
     'Explica o efeito via train-serving skew e selection bias: '
     'alternativa defensavel da rubrica. Correlacoes erradas ficam '
     'implicitas.'),
    ('JV32', 'CORRECT', 'sim',
     'Idem JV31, com importance weighting do cap 03.'),
    ('JV33', 'CORRECT', 'sim',
     'Batch periodico versus online realtime com custos de '
     'infraestrutura: nucleo ok.'),
    ('JV34', 'CORRECT', 'sim',
     'Idem JV28.'),
    ('JV35', 'CORRECT', 'sim',
     'Pre usa dados do treino, post usa dados reais com concept drift: '
     'nucleos 1 e 3 presentes, must 2 parcial.'),
    ('JV36', 'CORRECT', 'sim',
     'Idem JV28.'),
    ('JV37', 'CORRECT', 'sim',
     'Idem JV22, texto quase igual. Stale ausente, nucleo ok.'),
    ('JV38', 'CORRECT', 'sim',
     'Rogati e data foundations citados; quality e quantity definem o '
     'teto do desempenho: musts transmitidos.'),
    ('JV39', 'CORRECT', 'sim',
     'Slices com exemplo concreto (mobile traffic).'),
    ('JV40', 'CORRECT', 'sim',
     'Ponto de referencia e avaliador de complexidade presentes. O '
     'must de expor problemas de dados cedo fica ausente: nucleo '
     'geral ok.'),
]


def main():
    df = pd.read_csv(OUT)
    ldf = pd.DataFrame(LABELS, columns=['sample_id', 'human_verdict',
                                        'content_in_book', 'human_note'])
    assert len(ldf) == 40, f'esperava 40 rotulos, recebi {len(ldf)}'
    assert set(ldf.sample_id) == set(df.sample_id), 'sample_id mismatch'
    df = df.drop(columns=['human_verdict', 'content_in_book', 'human_note'],
                  errors='ignore')
    df = df.merge(ldf, on='sample_id', validate='1:1')
    df.to_csv(OUT, index=False)

    from sklearn.metrics import cohen_kappa_score
    judge = (df.verdict == 'CORRECT').astype(int)
    human = (df.human_verdict == 'CORRECT').astype(int)
    agree = (judge == human).mean()
    kappa = cohen_kappa_score(judge, human)
    print(f'\nAcordo juiz x rotulador: {agree:.1%} | kappa={kappa:.3f}')
    print('\nDiscordancias:')
    for r in df[judge != human].itertuples():
        print(f'  {r.sample_id} {r.question_id} {r.variant}: '
              f'juiz={r.verdict} humano={r.human_verdict} bucket={r.bucket}')
    lbl = ('livro_out_of_corpus', 'livro_in_corpus')
    codes = df.content_in_book.map(lambda x: lbl[0] if x == 'nao' else lbl[1])
    print('\ncontent_in_book (40 amostras):')
    print(codes.value_counts().to_string())
    ab = df[df.is_abst]
    print('\nAbstencoes alegadas pelo RAG e o conteudo no livro:')
    print(ab.groupby('content_in_book').size().to_string())
    w = df.n_occ.values
    print(f'\nPonderado por n_occ (420 respostas):')
    print(f'  juiz CORRECT   = {np.average(judge, weights=w):.3f}')
    print(f'  humano CORRECT = {np.average(human, weights=w):.3f}')


if __name__ == '__main__':
    sys.exit(main())
