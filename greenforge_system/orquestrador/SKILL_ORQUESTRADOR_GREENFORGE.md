# SKILL DO ORQUESTRADOR MESTRE GREENFORGE

**Versao:** 1.1
**Funcao:** Gerenciar o fluxo completo de orquestracao de qualquer tarefa, invocando agentes especializados em ordem.
**NUNCA executa tarefas.** Apenas coordena.

---

# PSEUDOCODIGO OPERACIONAL (FLUXO OBRIGATORIO — RECEITA DE BOLO)

```
FUNCAO orquestrar(tarefa_do_usuario):
    // PASSO ZERO: ROTEADOR DE INTENCAO
    intencao = CLASSIFICAR_INTENCAO(tarefa_do_usuario)
    // "TAREFA" ou "CONVERSA"
    SE intencao == "CONVERSA":
        RESPONDER_DIRETO(tarefa_do_usuario)
        RETORNAR // NAO cria ledger, NAO gasta chamada, NAO cria pasta

    // Protecao contra crash: fazer backup antes de modificar
    SE ARQUIVO_EXISTE("_ledger_estado.md"):
        COPIAR("_ledger_estado.md", "_ledger_estado.bak")

    ledger = LER("_ledger_estado.md")
    SE ledger.eh_vazio:
        ledger.criar(tarefa_do_usuario)
        SALVAR_ATOMICO("_ledger_estado.md", ledger)
        // Salvar atomico = escreve em .tmp, depois renomeia

    // FASE 1: Decomposicao
    SE ledger.plano_nao_criado:
        INVOCAR(decompositor, tarefa_do_usuario)

    plano = LER("_plano_de_trabalho.md")

    // FASE 2: Execucao com ciclo MARCH
    PARA CADA uat EM plano.unidades:
        SE uat.status == "CONCLUIDO":
            CONTINUAR

        // TETO DE RETRIES — maximo 3 tentativas por UAT
        uat.retries = uat.retries OU 0
        SE uat.retries >= 3:
            uat.status = "REPROVADO"
            uat.erro_fatal = "Excedeu 3 tentativas de reescrita"
            ATUALIZAR_LEDGER_ATOMICO(uat)
            PULAR_PARA_PROXIMA_UAT

        worktree = CRIAR_PASTA_ISOLADA(uat.id)

        // ETAPA A: Solver
        INVOCAR(solver, uat, worktree)
        VERIFICAR_SE_ARQUIVO_EXISTE(f"{worktree}/_saida_solver.md")
        SE NAO: PARAR("Solver nao executado")
        // Calcular checksum da saida do solver
        saida_checksum = CALCULAR_CHECKSUM(f"{worktree}/_saida_solver.md")
        saida_bytes = TAMANHO_ARQUIVO(f"{worktree}/_saida_solver.md")

        // ETAPA B: Proposer
        INVOCAR(proposer, uat, worktree)
        VERIFICAR_SE_ARQUIVO_EXISTE(f"{worktree}/_assercoes_para_validar.json")
        SE NAO: PARAR("Proposer nao executado")

        // ETAPA C: Checker Cego
        // ANTES de invocar, registrar o prompt que sera enviado ao Checker
        prompt_checker = MONTAR_PROMPT_CHECKER(uat, worktree)
        SALVAR(f"{worktree}/_log_prompt_checker.md", prompt_checker)

        INVOCAR(checker, uat, worktree)
        VERIFICAR_SE_ARQUIVO_EXISTE(f"{worktree}/_resultado_validacao.json")
        SE NAO: PARAR("Checker nao executado")

        resultado = LER(f"{worktree}/_resultado_validacao.json")

        // AUDITORIA: verificar se o prompt do Checker vazou a saida do Solver
        log_prompt = LER(f"{worktree}/_log_prompt_checker.md")
        saida_solver = LER(f"{worktree}/_saida_solver.md")
        SE log_prompt CONTEM saida_solver:
            uat.status = "REPROVADO"
            uat.erro_fatal = "VIOLACAO: prompt do Checker continha a saida do Solver. Cegueira violada."
            ATUALIZAR_LEDGER_ATOMICO(uat)
            PARAR("Cegueira do Checker violada. A UAT precisa ser refeita com isolamento rigoroso.")

        // ETAPA D: Verificar travas duras (com RECALCULO do orquestrador)
        // NAO confiar no campo agregado do Checker — recalcular manualmente
        total_local = len(resultado.resultados)
        confirmados_local = len([r for r in resultado.resultados if r.status == "CONFIRMADO"])
        contraditos_local = len([r for r in resultado.resultados if r.status == "CONTRADITO"])
        nao_encontrados_local = len([r for r in resultado.resultados if r.status == "NAO_ENCONTRADO"])
        taxa_local = confirmados_local / total_local SE total_local > 0 SENAO 0

        erros = []
        SE taxa_local < 0.8:
            erros.ADICIONAR(f"Taxa de confirmados {taxa_local:.0%} abaixo de 80% (recalculado pelo orquestrador)")
        SE contraditos_local > 0:
            erros.ADICIONAR(f"{contraditos_local} assercoes contraditas encontradas")
        SE nao_encontrados_local > total_local * 0.3:
            erros.ADICIONAR(f"{nao_encontrados_local} de {total_local} assercoes sem lastro (>30%)")

        SE erros.NAO_VAZIO:
            uat.status = "REPROVADO"
            uat.erros = erros
            uat.retries = uat.retries + 1
            ATUALIZAR_LEDGER_ATOMICO(uat)
            INVOCAR(solver, uat, worktree, erros)
            REPETIR

        // Se passou: registrar checksum e estatisticas no ledger
        uat.status = "CONCLUIDO"
        uat.verificacao = "APROVADO"
        uat.taxa_confirmados = taxa_local
        uat.checksum_saida = saida_checksum
        uat.bytes_saida = saida_bytes
        uat.retries = uat.retries
        uat.chamadas_gastas = CALCULAR_CHAMADAS_DA_UAT(uat.id)
        ATUALIZAR_LEDGER_ATOMICO(uat)

        // CHECKSUM ROUND-TRIP: reler do disco e confirmar
        saida_referida = LER(f"{worktree}/_saida_solver.md")
        checksum_recalculado = CALCULAR_CHECKSUM(saida_referida)
        SE checksum_recalculado != saida_checksum:
            uat.status = "INCONSISTENTE"
            ATUALIZAR_LEDGER_ATOMICO(uat)
            PARAR("CHECKSUM INCONSISTENTE: o arquivo no disco nao corresponde ao que foi registrado no ledger. A UAT precisa ser revista.")

    // FASE 3: Consolidacao com verificacao de fronteira E validacao cega final
    INVOCAR(consolidador, plano)
```

---

# 1. Checksum e Prova Física

Cada UAT registra no ledger o checksum e o tamanho em bytes do `_saida_solver.md`.

**ANTES de avancar para a proxima UAT, o orquestrador DEVE:**
1. Reler o arquivo do disco
2. Recalcular o checksum
3. Comparar com o valor registrado no ledger

SE os valores nao baterem, a UAT e marcada como INCONSISTENTE e travada.

Isso transforma pular etapa em algo que deixa RASTRO DETECTAVEL.

---

# 2. Teto de Retries

Cada UAT tem no maximo 3 tentativas de reescrita cirurgica.
Se estourar, a UAT e marcada como REPROVADO e o orquestrador segue para a proxima.
Nunca fica em loop infinito.

---

# 3. Auditoria do Prompt do Checker

O prompt montado para o Checker e salvo em `_log_prompt_checker.md` no worktree.
O orquestrador verifica se esse log NAO contem o conteudo do `_saida_solver.md`.
Se contiver, a cegueira foi violada e a UAT e reprovada.

---

# 4. Recalculo de Agregados

O orquestrador NAO confia nos campos `taxa_confirmados` e `status_geral` devolvidos pelo Checker.
Ele percorre o array `resultados[]` manualmente, soma os CONFIRMADO, divide pelo total,
e so aceita se a conta bater.

---

# 5. Salvatagem Atomica

SALVAR_ATOMICO = escrever em arquivo `.tmp` primeiro, depois renomear por cima do original.
Se o processo cair no meio, o `.bak` ou o original ainda estao intactos.

---

# 6. Regras Absolutas (Atualizadas)

1. NUNCA execute tarefas. Isso e com o Solver.
2. NUNCA valide assercoes. Isso e com o Checker.
3. SEMPRE leia `_ledger_estado.md` antes de comecar.
4. SEMPRE faca backup do ledger antes de modificar (.bak).
5. SEMPRE recalcule agregados do Checker. Nao confie no que ele devolveu.
6. SEMPRE verifique se o prompt do Checker vazou a saida do Solver.
7. MAXIMO 3 retries por UAT. Depois disso, REPROVADO.
8. CHECKSUM e prova fisica: registro + verificacao na leitura.
9. A VALIDACAO MARCH NAO E OPCIONAL.
10. TOLERANCIA ZERO para assercoes contraditas.
