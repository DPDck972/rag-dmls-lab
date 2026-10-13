# Prompts

**Estado:** contratos definidos, arquivos de prompt ainda pendentes.

Os contratos serão escritos e validados junto com as funções do notebook:

| Arquivo previsto | Finalidade |
| --- | --- |
| `generator.txt` | Gerar respostas fundamentadas, com o mesmo prompt final nas duas variantes. |
| `router.txt` | Escolher resposta direta, recuperação única ou recuperação iterativa. |
| `decomposer.txt` | Produzir consultas complementares preservando a pergunta original. |
| `evidence_check.txt` | Verificar cobertura e indicar informações ainda sem evidência. |

O roteador e o verificador não receberão o gabarito. Os prompts finais deverão
ser versionados e identificados nas execuções oficiais.

O notebook possui atualmente um prompt inline de geração, usado apenas na
demonstração. Ele instrui o modelo a responder em inglês usando somente o
contexto recuperado. Esse prompt deverá ser movido para `generator.txt`
antes da execução oficial.

O roteador da demonstração é baseado em marcadores de consulta, não em um
prompt de classificação. A implementação final deverá versionar a estratégia
de roteamento junto com os prompts de controle.
