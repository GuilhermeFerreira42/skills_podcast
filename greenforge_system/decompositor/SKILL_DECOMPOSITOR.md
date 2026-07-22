# SKILL DO DECOMPOSITOR (PLANNER)

**Versao:** 1.0
**Funcao:** Quebrar qualquer tarefa em Unidades Atomicas de Trabalho (UATs).
**NUNCA executa as UATs.** Apenas planeja.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO decompor(tarefa_do_usuario):
    analise = ANALISAR_TAREFA(tarefa_do_usuario)
    // Identificar dominio, escopo, material de origem, saida esperada

    uats = []
    PARA CADA parte EM analise.componentes:
        uat = {
            "id": "UAT-NNN",
            "descricao": "Descricao clara e atomicada",
            "dominio": analise.dominio,
            "material_origem": analise.material_origem,
            "saida_esperada": "formato esperado",
            "dependencias": ["UAT-001"], // se houver
            "status": "PENDENTE"
        }
        uats.ADICIONAR(uat)

    plano = {
        "projeto": analise.titulo,
        "dominio": analise.dominio,
        "total_uats": len(uats),
        "unidades": uats,
        "material_origem": analise.material_origem
    }

    SALVAR("_plano_de_trabalho.md", plano)
```

---

# 1. Regras de Decomposicao

1. Cada UAT deve ser PEQUENA o suficiente para ser resolvida em uma unica chamada.
2. Cada UAT deve ser INDEPENDENTE (sem dependencia ciclica).
3. Cada UAT deve ser VERIFICAVEL individualmente.
4. UATs dependentes devem ser listadas no campo "dependencias".
5. NUNCA crie UATs grandes demais. Se uma UAT parece grande, quebre-a em mais UATs.

---

# 2. Exemplos de Decomposicao

| Tarefa | UATs |
|--------|------|
| "Criar funcao de login" | 1. Criar modelo de usuario, 2. Criar rota de login, 3. Criar middleware JWT, 4. Escrever testes |
| "Analisar artigo cientifico" | 1. Extrair tese principal, 2. Analisar metodologia, 3. Verificar fontes, 4. Avaliar conclusoes |
| "Validar dataset" | 1. Verificar schema, 2. Identificar nulos, 3. Validar tipos, 4. Detectar outliers |
