# Prompts

**Estado:** prompts ainda não implementados.

Os contratos serão escritos e validados junto com as funções do notebook:

| Arquivo previsto | Finalidade |
| --- | --- |
| `generator.txt` | Gerar respostas fundamentadas, com o mesmo prompt final nas duas variantes. |
| `router.txt` | Escolher resposta direta, recuperação única ou recuperação iterativa. |
| `decomposer.txt` | Produzir consultas complementares preservando a pergunta original. |
| `evidence_check.txt` | Verificar cobertura e indicar informações ainda sem evidência. |

O roteador e o verificador não receberão o gabarito. Os prompts finais deverão
ser versionados e identificados nas execuções oficiais.
