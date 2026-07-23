# Ledger de Estado

**Projeto:** {{NOME_DO_PROJETO}}
**Dominio:** {{CODIGO | TEXTO | DADOS | PLANEJAMENTO | OUTRO}}
**Ultima atualizacao:** {{DATA_HORA}}
**Status geral:** {{EM_ANDAMENTO | CONCLUIDO | INTERROMPIDO}}
**Chamadas gastas ate agora:** {{NUMERO}}
**Ultimo backup:** {{ARQUIVO}}.bak (gerado automaticamente antes de cada modificacao)

---

## REGRA ABSOLUTA — VERIFICACAO MARCH

NENHUMA UAT PODE SER MARCADA COMO CONCLUIDA SEM A COLUNA `Verificacao` PREENCHIDA COM `APROVADO`.

Valores permitidos: `APROVADO`, `REPROVADO`, `PENDENTE`, `-`.
Se a coluna estiver vazia ou com valor diferente, o ledger esta INVALIDO.

---

## Progresso por UAT

| UAT | Descricao | Dominio | Status | Retries | Verificacao | Taxa | Chamadas | Checksum Saida | Bytes | Ultima acao |
|-----|-----------|---------|--------|---------|-------------|------|----------|----------------|-------|-------------|
| 001 | Criar funcao X | codigo | CONCLUIDO | 0 | APROVADO | 95% | 5 | a3f2b9 | 2048 | Validado |
| 002 | Escrever testes | codigo | ESCREVENDO | 1 | PENDENTE | - | 3 | - | - | Solver ativo |
| 003 | Documentar API | texto | PENDENTE | 0 | - | - | 0 | - | - | Aguardando |

**Legenda:** PEND=Pendente, ESCR=Escrevendo, REV=Em revisao, CONCL=Concluido, REPR=Reprovado, INCONSIST=Inconsistente

---

## Worktrees Ativos

| UAT | Worktree | Status | Fronteira OK? | Cegueira OK? |
|-----|----------|--------|---------------|--------------|
| 001 | worktree_uat_001/ | CONCLUIDO | PASSOU | PASSOU |
| 002 | worktree_uat_002/ | ATIVO | - | - |

---

## Pendencias e Bloqueios

- UAT 003: aguardando UAT 001 ser concluida (dependencia)
- UAT 002: em reescrita (retry 1 de 3)

---

## Regras (Greenforged Edition)

1. SEMPRE ler este arquivo antes de comecar.
2. SEMPRE fazer backup (.bak) antes de modificar.
3. SEMPRE registrar checksum e bytes dos artefatos de saida.
4. Verificacao MARCH e OBRIGATORIA. Sem `_resultado_validacao.json` aprovado, a UAT nao existe.
5. Tolerancia zero para assercoes contraditas.
6. Maximo 3 retries por UAT. Depois disso, REPROVADO.
7. Toda UAT deve passar pela verificacao de fronteira do worktree.
8. Toda UAT deve ter auditoria de cegueira do Checker.
9. Se o limite de chamadas for atingido, marcar INTERROMPIDO e salvar ultima UAT exata.
10. O orquestrador recalcula agregados manualmente. Nao confia nos campos do Checker.
