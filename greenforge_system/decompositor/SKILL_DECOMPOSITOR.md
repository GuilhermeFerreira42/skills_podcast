# SKILL DO DECOMPOSITOR (PLANNER)

**Versao:** 1.1
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
            "descricao": "Descricao clara e atomica",
            "dominio": analise.dominio,
            "adaptador": analise.tipo,  // "codigo", "texto", "dados", "planejamento"
            "material_origem": analise.material_origem,
            "saida_esperada": "formato esperado",
            "dependencias": [], // IDs das UATs que devem vir antes
            "status": "PENDENTE",
            "tamanho_estimado": "P | M | G"  // Pequena, Media, Grande
        }
        uats.ADICIONAR(uat)

    // ===== AUTO-VERIFICACAO DO PLANO =====
    // 1. Verificar dependencias circulares
    PARA CADA uat EM uats:
        SE uat.id EM uat.dependencias:
            ERRO_FATAL(f"UAT {uat.id} depende dela mesma")

    // 2. Verificar ciclo no grafo de dependencias
    grafo = CRIAR_GRAFO(uats)
    SE DETECTAR_CICLO(grafo):
        // Se houver ciclo, requebrar as UATs afetadas
        uats = REQUEBRAR_UATS_COM_CICLO(uats, grafo)

    // 3. Verificar tamanho das UATs
    PARA CADA uat EM uats:
        SE uat.tamanho_estimado == "G":
            // UAT grande: quebrar em 2 ou mais UATs menores
            novas_uats = DIVIDIR_UAT(uat)
            uats.REMOVER(uat)
            uats.EXTENDER(novas_uats)

    // 4. Verificar IDs duplicados
    ids = [uat.id PARA uat EM uats]
    SE len(ids) != len(CRIAR_CONJUNTO(ids)):
        ERRO_FATAL("IDs de UAT duplicados encontrados")

    // 5. Garantir que cada UAT tenha adaptador definido
    PARA CADA uat EM uats:
        SE uat.adaptador NAO DEFINIDO:
            uat.adaptador = "texto" // fallback seguro

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
2. Cada UAT deve ter um ADAPTADOR definido (codigo, texto, dados, planejamento).
3. Cada UAT deve ser INDEPENDENTE (sem dependencia ciclica).
4. Cada UAT deve ser VERIFICAVEL individualmente.
5. NUNCA crie UATs grandes demais. Se uma UAT parece grande, quebre-a em mais UATs.
6. O plano DEVE passar pela auto-verificacao antes de ser salvo.

---

# 2. Exemplos de Decomposicao

| Tarefa | UATs | Adaptador |
|--------|------|-----------|
| "Criar funcao de login" | 1. Criar modelo, 2. Criar rota, 3. Middleware JWT, 4. Testes | codigo |
| "Analisar artigo cientifico" | 1. Tese principal, 2. Metodologia, 3. Fontes, 4. Conclusoes | texto |
| "Validar dataset" | 1. Schema, 2. Nulos, 3. Tipos, 4. Outliers | dados |

---

# 3. Gatilhos de Rejeicao do Plano

| Condicao | Acao |
|----------|------|
| UAT depende dela mesma | REJEITAR — erro fatal |
| Ciclo detectado no grafo | REQUEBRAR automaticamente |
| UAT marcada como G (grande) | DIVIDIR em UATs menores |
| ID duplicado | REJEITAR — erro fatal |
| Adaptador nao definido | DEFINIR como "texto" (fallback) |
