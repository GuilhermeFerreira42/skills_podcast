# Exemplo de Fluxo Completo

Este exemplo mostra como o Greenforge System orquestra a execucao de uma tarefa de codigo.

---

## Cenario

Usuario quer: "Crie uma funcao de autenticacao JWT em Python com testes."

---

## Passo 1 — Orquestrador le o ledger

```
LER("_ledger_estado.md")
// ledger vazio -> iniciar do zero
```

---

## Passo 2 — Orquestrador invoca Decompositor

```
INVOCAR(decompositor, "Crie uma funcao de autenticacao JWT em Python com testes.")
```

Decompositor gera o plano:

```
UAT-001: Criar modelo de usuario (User model)
UAT-002: Criar funcao de geracao de token JWT
UAT-003: Criar funcao de verificacao de token
UAT-004: Criar middleware de autenticacao
UAT-005: Escrever testes unitarios
```

---

## Passo 3 — Loop de execucao (UAT-001)

### 3a. Orquestrador cria worktree e invoca Solver

```
CRIAR_PASTA("worktree_uat_001")
INVOCAR(solver, {uat: "UAT-001", material: "documentacao da API"})
```

### 3b. Solver executa e salva saida

```
// Solver cria o modelo User em Python
SAIDA = "class User(BaseModel):\n    id: int\n    username: str\n    email: str\n    password_hash: str"
SALVAR("worktree_uat_001/_saida_solver.md", SAIDA)
```

### 3c. Orquestrador invoca Proposer

```
INVOCAR(proposer, {uat: "UAT-001", worktree: "worktree_uat_001"})
```

Proposer extrai assercoes:
- "User model possui campos id, username, email e password_hash"
- "User model herda de BaseModel"
- "password_hash e do tipo str"

### 3d. Orquestrador invoca Checker Cego

```
INVOCAR(checker, {
  perguntas: ["User model possui campos id, username, email e password_hash?"],
  material: "documentacao da API"
  // Checker NAO ve a saida do Solver
})
```

Checker retorna:
- 3 CONFIRMADO, 0 CONTRADITO, 0 NAO_ENCONTRADO
- Taxa: 100%
- Status: APROVADO

### 3e. Orquestrador atualiza ledger

```
uat-001.status = "CONCLUIDO"
uat-001.verificacao = "APROVADO"
SALVAR("_ledger_estado.md", ledger)
```

---

## Passo 4 — Loop continua para UATs 002-005

Mesmo ciclo: Solver, Proposer, Checker, verificar travas, atualizar ledger.

---

## Passo 5 — Apos todas as UATs

```
INVOCAR(consolidador, plano)
```

Consolidador junta tudo e apresenta ao usuario:
- Modelo User
- Funcao JWT gerar/verificar
- Middleware de autenticacao
- Testes unitarios
- Relatorio de validacao

---

## Resumo

| Fase | Quem faz | O que produz |
|------|----------|-------------|
| 1 | Orquestrador | Ledger |
| 2 | Decompositor | Plano de UATs |
| 3a | Orquestrador | Worktree isolado |
| 3b | Solver | Saida da UAT |
| 3c | Proposer | Assercoes atomicas |
| 3d | Checker | Validacao cega |
| 3e | Orquestrador | Ledger atualizado |
| 4 | (repetir) | - |
| 5 | Consolidador | Saida final |
