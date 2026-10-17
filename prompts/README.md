# Prompts

**Estado:** três prompts versionados e usados (por carregamento ou como
referência da run oficial); roteamento continua baseado em marcadores,
implementado no notebook.

Os arquivos de prompt e as estratégias correspondentes são:

| Artefato | Finalidade |
| --- | --- |
| `generator.txt` | Gerar respostas fundamentadas para as três variantes (template com `{question}`/`{context}`). |
| `router.txt` | Padrões regex do roteador baseline/adaptive (um por linha; linhas em branco e comentários são ignorados). |
| `verifier.txt` | Crítica estruturada do Self-RAG (`{question}`/`{context}`/`{draft}`; responde exatamente uma palavra: SUPPORTED/NOT_SUPPORTED). |
| Estratégia no notebook | Expansão da consulta e RRF na variante Adaptive RAG. |

O notebook carrega os três arquivos em runtime (`load_generator_template()`,
`load_router_patterns()`, `load_verifier_prompt()`) e faz assert de que os
conteúdos renderizados permanecem idênticos ao texto executado na run
oficial (registrado em `run_manifest.json`). Mudanças nos arquivos de
prompt invalidam a comparabilidade com a run anterior.

Não há arquivo separado para decomposição de consulta; essa etapa não
faz parte do pipeline implementado.

`load_generator_template()` aplica o template de `prompts/generator.txt`
com os placeholders `{question}` e `{context}`, instruindo o modelo a
responder em inglês usando somente o contexto recuperado.
`load_router_patterns()` carrega os marcadores de `prompts/router.txt`
(marcadores de consulta, não um prompt de classificação; mantido por
compatibilidade com a run oficial) e `load_verifier_prompt()` carrega a
crítica de `prompts/verifier.txt`, que pode acionar nova recuperação e
geração quando o veredito é `NOT_SUPPORTED`.
