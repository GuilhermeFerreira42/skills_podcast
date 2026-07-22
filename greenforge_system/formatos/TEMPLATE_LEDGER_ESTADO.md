# Ledger de Estado

**Projeto:** {{NOME_DO_PROJETO}}
**Dominio:** {{CODIGO | TEXTO | DADOS | PLANEJAMENTO | OUTRO}}
**Ultima atualizacao:** {{DATA_HORA}}
**Status geral:** {{EM_ANDAMENTO | CONCLUIDO | INTERROMPIDO}}
**Chamadas gastas ate agora:** {{NUMERO}}

---

## REGRA ABSOLUTA — VERIFICACAO MARCH

NENHUMA UAT PODE SER MARCADA COMO CONCLUIDA SEM A COLUNA `Verificacao` PREENCHIDA COM `APROVADO`.

Valores permitidos: `APROVADO`, `REPROVADO`, `PENDENTE`, `-`.
Se a coluna estiver vazia ou com valor diferente, o ledger esta INVALIDO.

---

## Progresso por UAT

| UAT | Descricao | Status | Verificacao | Taxa | Dominio | Ultima acao |
|-----|-----------|--------|-------------|------|---------|-------------|
| 001 | Criar funcao X | CONCLUIDO | APROVADO | 95% | codigo | Validado |
| 002 | Escrever testes | ESCREVENDO | PENDENTE | - | codigo | Solver ativo |
| 003 | Documentar API | PENDENTE | - | - | texto | Aguardando |

**Legenda:** PEND=Pendente, ESCR=Escrevendo, REV=Em revisao, CONCL=Concluido, REPR=Reprovado

---

## Worktrees Ativos

| UAT | Worktree | Status |
|-----|----------|--------|
| 001 | worktree_uat_001/ | CONCLUIDO |
| 002 | worktree_uat_002/ | ATIVO |

---

## Pendencias e Bloqueios

- UAT 003: aguardando UAT 001 ser concluida (dependencia)
- Limite de chamadas: 45/50 usadas

---

## Regras

1. SEMPRE ler este arquivo antes de comecar.
2. SEMPRE atualizar apos cada acao.
3. Verificacao MARCH e OBRIGATORIA. Sem `_resultado_validacao.json` aprovado, a UAT nao existe.
4. Tolerancia zero para assercoes contraditas.
5. Se o limite de chamadas for atingido, marcar INTERROMPIDO e salvar ultima UAT exata.
