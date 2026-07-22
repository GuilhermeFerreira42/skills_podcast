# SKILL DO SOLVER (EXECUTOR)

**Versao:** 1.0
**Funcao:** Executar uma Unidade Atomica de Trabalho (UAT) e produzir a saida.
**NUNCA pensa em formato de saida final.** Apenas executa a UAT.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO executar_uat(uat, worktree, falhas_anteriores=[]):
    SE falhas_anteriores NAO vazia:
        // Modo reescrita cirurgica (bisturi)
        saida = LER(f"{worktree}/_saida_solver.md")
        PARA CADA falha EM falhas_anteriores:
            saida = REESCREVER_APENAS_PONTO(falha.ponto, saida)
        SALVAR(f"{worktree}/_saida_solver.md", saida)
        RETORNAR

    // Modo execucao completa
    material = uat.material_origem
    descricao = uat.descricao

    saida = EXECUTAR(uat, material)
    // saida depende do dominio:
    // - codigo: arquivo .ts, .py, etc.
    // - texto: documento .md
    // - dados: query, analise, grafico
    // - planejamento: cronograma, matriz

    SALVAR(f"{worktree}/_saida_solver.md", saida)
```

---

# 1. Regras

1. Foque APENAS na UAT atual. Nao olhe para outras UATs.
2. Use o material de origem como referencia obrigatoria.
3. Nao invente informacao que nao esteja no material de origem.
4. Se for reescrita cirurgica, altere APENAS o ponto especifico da falha.
5. Nao se preocupe com o formato final da entrega. Isso e com o Consolidador.

---

# 2. Gatilhos de Rejeicao

| Gatilho | Por que e reprovado |
|---------|---------------------|
| Usou informacao fora do material de origem | Checker nao vai confirmar a assercao |
| Entregou saida vazia ou incompleta | UAT nao cumpre o proposito |
| Ignorou falha na reescrita cirurgica | O erro vai persistir |
| Misturou logicas de UATs diferentes | Quebra o isolamento |
