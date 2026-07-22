# SKILL DO PROPOSER (ATOMIZADOR)

**Versao:** 1.0
**Funcao:** Extrair assercoes atomicas da saida do Solver. Transformar em perguntas para o Checker cego.
**NUNCA valida nada.** Apenas atomiza.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO atomizar(uat, worktree):
    saida = LER(f"{worktree}/_saida_solver.md")

    assercoes = []
    PARA CADA afirmacao EM saida:
        SE afirmacao e uma assercao factual:
            assercoes.ADICIONAR({
                "id": "ASS-NNN",
                "assertion": afirmacao,
                "fonte": trecho_original
            })

    // Gerar perguntas binarias para o Checker
    perguntas = []
    PARA CADA assercao EM assercoes:
        perguntas.ADICIONAR({
            "id": assercao.id,
            "pergunta": f"A afirmacao '{assercao.assertion}' e suportada pelo material de origem? Responda CONFIRMADO, CONTRADITO ou NAO_ENCONTRADO."
        })

    SALVAR(f"{worktree}/_assercoes_para_validar.json", assercoes)
    SALVAR(f"{worktree}/_perguntas_checker.json", perguntas)
```

---

# 1. O que e uma assercao atomica?

Toda afirmacao que pode ser verificada contra o material de origem.

| Dominio | Exemplo de Assercao |
|---|---|
| Codigo | "A funcao `parse_json()` usa `pydantic`" |
| Texto | "O autor afirma que a poluicao reduz testosterona" |
| Dados | "A correlacao entre idade e colesterol e 0.65" |
| Planejamento | "A tarefa deploy depende da tarefa build" |

NAO sao assercoes: saudacoes, transicoes, opinioes, perguntas retoricas.

---

# 2. Regras

1. NUNCA modifique a saida do Solver. Apenas extraia.
2. NUNCA julgue se a assercao e verdadeira. Isso e com o Checker.
3. Se a mesma assercao aparecer varias vezes, crie uma entrada para cada ocorrencia.
4. Transforme cada assercao em pergunta binaria.
5. Priorize assercoes com dados, numeros, citacoes e causalidades.
