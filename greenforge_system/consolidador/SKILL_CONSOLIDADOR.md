# SKILL DO CONSOLIDADOR

**Versao:** 1.0
**Funcao:** Juntar todas as UATs aprovadas em uma saida final coesa.

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
        saida_final.ADICIONAR({
            "uat_id": uat.id,
            "descricao": uat.descricao,
            "conteudo": saida,
            "status_validacao": "APROVADO",
            "taxa_confirmacao": resultado.taxa_confirmados
        })

    SALVAR("_saida_final.md", saida_final)
    APRESENTAR_AO_USUARIO(saida_final)
```

---

# 1. Regras

1. Inclua APENAS UATs com status APROVADO.
2. Preserve a ordem definida no plano de trabalho.
3. Se uma UAT foi reprovada, avise o usuario e inclua o motivo.
4. Nao modifique o conteudo das UATs. Apenas junte.
