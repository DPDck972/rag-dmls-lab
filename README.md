# rag-dmls-lab

Projeto da Unidade 01 — RAG avançado sobre *Designing Machine Learning Systems*.

**Disciplina:** DCA0305 — Design de Sistemas Baseados em Aprendizado de Máquina  
**Grupo:** 1  
**Família:** F4 — Controle do processo  
**Técnica proposta:** Adaptive RAG didático, com roteamento por prompts  
**Estado:** scaffold funcional; perguntas definidas, notebook executável em demonstração e experimento oficial ainda pendente.

## Objetivo

Comparar um RAG básico com uma variante que adapta o esforço de recuperação à
pergunta e às evidências disponíveis. Investigar qualidade das respostas,
latência, chamadas ao LLM e variação entre execuções.

## Estrutura atual

```text
rag-dmls-lab/
├── README.md
├── .gitignore
├── notebook.ipynb
├── questions.json
├── requirements.txt
├── configs/
│   └── experiment.json
├── corpus/
│   ├── README.md
│   ├── manifest.csv
│   └── documentos/
│       └── .gitkeep
├── prompts/
│   └── README.md
├── results/
│   ├── README.md
│   ├── traces/
│   │   └── .gitkeep
│   └── figures/
│       └── .gitkeep
└── docs/
    └── README.md
```

## Corpus local

O livro candidato é *Designing Machine Learning Systems*, de Chip Huyen,
primeira edição, de 2022. A cópia local está em
`corpus/documentos/designing-machine-learning-systems-2022.pdf`.
O arquivo está excluído do Git; sua identificação e hash estão registrados em
`corpus/manifest.csv`. A página oficial da edição está disponível na
[O'Reilly](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/).

As 20 perguntas de avaliação estão definidas em `questions.json`, em inglês,
com categorias e níveis de dificuldade. O notebook implementa atualmente uma
versão demonstrativa com extração do PDF, chunking, recuperação TF-IDF,
expansão de consultas, roteamento baseline/adaptive e geração via Ollama.
O recorte definitivo dos capítulos e a execução oficial ainda precisam ser
registrados.

## Execução inicial

Abra `notebook.ipynb` em um ambiente Jupyter com o kernel
`Python (rag-dmls-lab)`, a partir desta pasta. O notebook já contém uma
demonstração do pipeline RAG e requer que o PDF esteja no caminho indicado.
O Ollama deve estar em execução com o modelo configurado em
`configs/experiment.json`.

No Colab, disponibilize o repositório completo em `/content/rag-dmls-lab`
antes de executar as células. A reprodução no Colab ainda precisa ser validada.
Em ambiente local, o kernel registrado é `Python (rag-dmls-lab)`.

O fluxo atual executa uma amostra com as primeiras perguntas. A execução
oficial das 20 perguntas, as repetições, os traces e os CSVs previstos em
`results/README.md` ainda serão implementados.

## Repositório independente

Esta pasta é a raiz de um repositório Git próprio, separado do material da
disciplina. O remoto `origin` aponta para
[`micarlio/rag-dmls-lab`](https://github.com/micarlio/rag-dmls-lab).

O código, as configurações, as perguntas, o manifesto e os resultados oficiais
poderão ser versionados. O PDF comercial permanecerá local enquanto não houver
permissão de redistribuição. Quem reproduzir o projeto deverá disponibilizar uma
cópia da mesma edição no caminho indicado em `corpus/README.md`.
