# Prompts

**Estado:** `generator.txt` versionado; demais prompts ainda pendentes.

Os contratos serão escritos e validados junto com as funções do notebook:

| Arquivo previsto | Finalidade |
| --- | --- |
| `generator.txt` | Gerar respostas fundamentadas, com o mesmo prompt final nas duas variantes. |
| `router.txt` | Escolher resposta direta, recuperação única ou recuperação iterativa. |
| `decomposer.txt` | Produzir consultas complementares preservando a pergunta original. |
| `evidence_check.txt` | Verificar cobertura e indicar informações ainda sem evidência. |

O roteador e o verificador não receberão o gabarito. Os prompts finais deverão
ser versionados e identificados nas execuções oficiais.

O notebook carrega esse prompt de `prompts/generator.txt` via
`load_generator_template()` e aplica `format_prompt(question, context)`.
O template usa os placeholders `{question}` e `{context}` e instrui o modelo
a responder em inglês usando somente o contexto recuperado.

O roteador da demonstração é baseado em marcadores de consulta, não em um
prompt de classificação. A implementação final deverá versionar a estratégia
de roteamento junto com os prompts de controle.
