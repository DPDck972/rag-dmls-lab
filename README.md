# rag-dmls-lab

Projeto da Unidade 01 — RAG avançado sobre *Designing Machine Learning Systems*.

**Disciplina:** DCA0305 — Design de Sistemas Baseados em Aprendizado de Máquina  
**Grupo:** 1  
**Família:** F4 — Controle do processo  
**Técnica proposta:** comparação entre Baseline RAG, Adaptive RAG e Self-RAG
**Estado:** experimento executado; resultados, diagnósticos e visualizações
versionados em `results/`.

## Objetivo

Comparar um RAG básico, uma variante que adapta o esforço de recuperação à
pergunta e uma variante Self-RAG que critica o suporte da própria resposta.
Investigar qualidade das respostas, latência, chamadas ao LLM e variação entre
execuções.

## Estrutura do projeto

```text
rag-dmls-lab/
├── configs
│   └── experiment.json
├── corpus
│   ├── documentos
│   │   └── designing-machine-learning-systems-2022.pdf
│   ├── manifest.csv
│   └── README.md
├── docs
│   └── README.md
├── notebook.ipynb
├── prompts
│   ├── generator.txt
│   └── README.md
├── questions.json
├── README.md
├── requirements.txt
└── results
    ├── accuracy.csv
    ├── accuracy_summary.csv
    ├── analise_rag_dmls.xlsx
    ├── baseline_r1.csv
    ├── baseline_r2.csv
    ├── baseline_r3.csv
    ├── diagnostico_baseline.csv
    ├── disagreements.csv
    ├── divergencias_variantes.csv
    ├── imagem
    │   ├── acuracia_sinal_ruido.png
    │   ├── boxplot_latencia.png
    │   ├── chamadas_e_latencia.png
    │   └── qualidade_respostas.png
    ├── por_repeticao
    │   ├── adaptive_r1.csv
    │   ├── adaptive_r2.csv
    │   ├── adaptive_r3.csv
    │   ├── baseline_r1.csv
    │   ├── baseline_r2.csv
    │   ├── baseline_r3.csv
    │   ├── self_rag_r1.csv
    │   ├── self_rag_r2.csv
    │   └── self_rag_r3.csv
    ├── results_adaptive.csv
    ├── run_manifest.json
    ├── self_rag_r1.csv
    ├── self_rag_r2.csv
    ├── self_rag_r3.csv
    ├── summary.csv
    └── traces
        └── official_runs.jsonl
```

## Corpus local

O livro candidato é *Designing Machine Learning Systems*, de Chip Huyen,
primeira edição, de 2022. A cópia local está em
`corpus/documentos/designing-machine-learning-systems-2022.pdf`.
O arquivo está excluído do Git; sua identificação e hash estão registrados em
`corpus/manifest.csv`. A página oficial da edição está disponível na
[O'Reilly](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/).

As 20 perguntas de avaliação estão definidas em `questions.json`, em inglês,
com categorias e níveis de dificuldade. O notebook implementa extração do PDF,
chunking, recuperação TF-IDF, expansão de consultas, roteamento
baseline/adaptive, crítica Self-RAG e geração via Ollama.

O Self-RAG gera uma resposta inicial, solicita uma crítica estruturada sobre
relevância e suporte factual e faz uma nova recuperação quando a crítica indica
evidência insuficiente. O prompt de geração é carregado de
`prompts/generator.txt`, mantendo o contrato de geração separado do código do
notebook.

## Execução inicial

Abra `notebook.ipynb` em um ambiente Jupyter com o kernel
`Python (rag-dmls-lab)`, a partir desta pasta. O notebook já contém uma
demonstração do pipeline RAG e requer que o PDF esteja no caminho indicado.
O Ollama deve estar em execução com o modelo configurado em
`configs/experiment.json`.

No Colab, disponibilize o repositório completo em `/content/rag-dmls-lab`
antes de executar as células. A reprodução no Colab ainda precisa ser validada, para exte experimento foi utilizada uma GPU: NVIDIA RTX PRO 6000 Blackwell Server Edition, 97887 MiB.
Em ambiente local, o kernel registrado é `Python (rag-dmls-lab)`.

O fluxo começa pelo smoke test com as primeiras perguntas. Para reproduzir a
execução oficial, execute a célula `run_official_experiment()` e, em seguida,
as células de análise do notebook. A configuração processa 20 perguntas em
três repetições para cada variante, totalizando 180 respostas. Os resultados
brutos, agregados e derivados são salvos em `results/`.

As variantes são:

- **Baseline RAG:** uma recuperação lexical e uma geração;
- **Adaptive RAG:** expansão/roteamento da consulta antes da geração;
- **Self-RAG:** geração inicial, crítica estruturada e nova recuperação/geração
  quando a resposta não está suficientemente apoiada nas evidências.

O Self-RAG registra `llm_calls`, `retrieval_rounds`, `reflection_triggered` e
`reflection_supported` para permitir a comparação de custo e comportamento.

## Resultados

Os principais artefatos versionados são:

- `summary.csv`: base consolidada das respostas e métricas das variantes;
- `accuracy.csv` e `accuracy_summary.csv`: avaliações de acurácia e seus
  agregados;
- `diagnostico_baseline.csv`: diagnóstico específico das execuções Baseline;
- `divergencias_variantes.csv` e `disagreements.csv`: comparação das respostas
  e divergências entre variantes;
- `run_manifest.json`: configuração, hashes e metadados da execução;
- `traces/official_runs.jsonl`: trace detalhado das execuções;
- `analise_rag_dmls.xlsx`: planilha consolidada para inspeção dos resultados;
- `imagem/`: gráficos de acurácia, latência, chamadas ao modelo e qualidade;
- `por_repeticao/`: resultados separados por variante e repetição.

Os arquivos de resultado permitem analisar qualidade, latência, custo de
inferência, número de chamadas ao LLM, recuperação e estabilidade entre
repetições sem executar novamente os modelos.

## Repositório independente

Esta pasta é a raiz de um repositório Git próprio, separado do material da
disciplina. O remoto `origin` aponta para
[`micarlio/rag-dmls-lab`](https://github.com/micarlio/rag-dmls-lab).

O código, as configurações, as perguntas, o manifesto e os resultados oficiais
poderão ser versionados. O PDF comercial permanecerá local enquanto não houver
permissão de redistribuição. Quem reproduzir o projeto deverá disponibilizar uma
cópia da mesma edição no caminho indicado em `corpus/README.md`.
