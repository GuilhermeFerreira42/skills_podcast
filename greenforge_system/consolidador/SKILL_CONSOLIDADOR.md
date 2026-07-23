# SKILL DO CONSOLIDADOR

**Versao:** 1.1
**Funcao:** Juntar todas as UATs aprovadas em uma saida final coesa, com verificacao de fronteira e auditoria.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO consolidar(plano):
    saida_final = []

    PARA CADA uat EM plano.unidades:
        worktree = f"worktree_{uat.id}/"
        resultado = LER(f"{worktree}/_resultado_validacao.json")

        SE resultado.status_geral != "APROVADO":
            AVISAR(f"UAT {uat.id} nao aprovada. Ignorando.")
            CONTINUAR

        saida = LER(f"{worktree}/_saida_solver.md")

        // ===== VERIFICACAO DE FRONTEIRA DO WORKTREE =====
        // Varrer todos os caminhos dos artefatos e verificar
        // se comecam com o prefixo do worktree da UAT
        PARA CADA artefato EM LISTAR_ARQUIVOS(worktree):
            caminho_completo = RESOLVER_CAMINHO(artefato)
            prefixo_esperado = RESOLVER_CAMINHO(worktree)
            SE NAO COMECA_COM(caminho_completo, prefixo_esperado):
                AVISAR(f"VIOLACAO DE FRONTEIRA: {artefato} esta fora do worktree {uat.id}")
                UAT_REJEITADA(uat.id, "Artefato fora do worktree")
                CONTINUAR

        // ===== AUDITORIA DO PROMPT DO CHECKER =====
        // Verificar se o log do prompt do Checker existe
        SE ARQUIVO_EXISTE(f"{worktree}/_log_prompt_checker.md"):
            log_prompt = LER(f"{worktree}/_log_prompt_checker.md")
            saida_solver = LER(f"{worktree}/_saida_solver.md")
            SE log_prompt CONTEM saida_solver:
                AVISAR(f"VIOLACAO DE CEGUEIRA: UAT {uat.id} teve prompt do Checker contaminado")
                UAT_REJEITADA(uat.id, "Cegueira do Checker violada")
                CONTINUAR
        SENAO:
            AVISAR(f"ALERTA: UAT {uat.id} nao possui _log_prompt_checker.md. Auditoria de cegueira nao realizada.")

        saida_final.ADICIONAR({
            "uat_id": uat.id,
            "descricao": uat.descricao,
            "dominio": uat.adaptador,
            "conteudo": saida,
            "status_validacao": "APROVADO",
            "taxa_confirmacao": resultado.taxa_confirmados
        })

    // ===== VALIDADOR CEGO FINAL (MARCH NA MACRO) =====
    // O Consolidador agora atua como um CHECKER CEGO do fluxo inteiro.
    // Ele recebe APENAS o plano original e a saida final consolidada.
    // Ele NAO teve acesso ao passo a passo (nao viu as UATs individuais).
    // Ele responde: a saida final cumpre o que o plano prometia?

    plano = LER("_plano_de_trabalho.md")
    promessa_do_plano = plano.projeto + ": " + plano.dominio + " - " + str(plano.total_uats) + " UATs"

    cumpre = VERIFICAR_SE_SAIDA_CUMPRE_PLANO(promessa_do_plano, saida_final)
    // Cumpre SIM ou NAO

    SALVAR("_relatorio_validacao_final.json", {
        "plano": promessa_do_plano,
        "total_uats_no_plano": plano.total_uats,
        "uats_entregues": len(saida_final),
        "uats_reprovadas": plano.total_uats - len(saida_final),
        "cumpre_plano": cumpre,
        "status_final": "APROVADO" SE cumpre == "SIM" E len(saida_final) == plano.total_uats SENAO "REPROVADO"
    })

    SALVAR("_saida_final.md", saida_final)
    APRESENTAR_AO_USUARIO(saida_final)
    SE cumpre != "SIM":
        AVISAR("ALERTA: A saida final pode nao cumprir integralmente o plano original. Revise o _relatorio_validacao_final.json.")
```

---

# 1. Verificacao de Fronteira do Worktree

Antes de aceitar qualquer UAT, o Consolidador varre TODOS os arquivos do worktree e verifica se eles comecam com o prefixo do diretorio daquela UAT.

Se algum arquivo apontar para fora (ex: `../../sistema/arquivo_importante.py`), a UAT e rejeitada com VIOLACAO DE FRONTEIRA.

Isso impede que o Solver escreva fora da caixa.

---

# 2. Auditoria de Cegueira do Checker

O Consolidador verifica se o `_log_prompt_checker.md` contem o conteudo do `_saida_solver.md`.

Se contiver, a UAT e rejeitada porque o Checker nao foi realmente cego.

Se o log nao existir, um alerta e registrado.

---

# 3. Validador Cego Final (MARCH na Macro)

O Consolidador agora tem DUAS responsabilidades:
1. Juntar as UATs aprovadas (como antes)
2. **Validar cegamente** se a saida final cumpre o plano original

A segunda etapa e o MARCH aplicado no fluxo inteiro:
- O Consolidador recebe o plano original (o que foi prometido)
- O Consolidador recebe a saida final (o que foi entregue)
- O Consolidador NAO teve acesso ao passo a passo da execucao
- Ele responde: a entrega cumpre a promessa? SIM ou NAO

Isso pega o caso onde cada UAT passou no Checker local, mas o conjunto final nao responde a tarefa do usuario.

---

# 4. Regras

1. Inclua APENAS UATs com status APROVADO e que passaram na verificacao de fronteira.
2. Se uma UAT violou a fronteira, REJEITE e registre.
3. Se uma UAT violou a cegueira do Checker, REJEITE e registre.
4. Preserve a ordem definida no plano de trabalho.
5. Nao modifique o conteudo das UATs. Apenas junte.
