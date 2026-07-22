# Greenforge System — Orquestrador Universal de Tarefas

**Versao:** 1.0
**Licenca:** MIT
**Arquitetura:** Hexagonal — Motor de Orquestracao + Adaptadores de Dominio
**Funcao:** Orquestrar QUALQUER tarefa complexa (codigo, texto, dados, planejamento, pesquisa) com o mesmo rigor do Podcast System.

## Arquitetura

```
                    ORQUESTRADOR MESTRE
                  (gerencia o fluxo, nao executa)
                          |
         +----------------+----------------+
         |                |                |
    DECOMPOSITOR      SOLVER           PROPOSER
    (Planner)         (Executor)       (Atomizador)
    quebra a          executa cada     extrai assercoes
    tarefa em UATs    UAT             atomicas da saida
         |                |                |
         +----------------+----------------+
                          |
                    CHECKER CEGO
                    (MARCH universal)
                    valida assercoes contra
                    material de origem
                          |
                    CONSOLIDADOR
                    junta UATs aprovadas
                          |
                    ADAPTADORES PLUGAVEIS
                    (codigo, texto, dados, ...)
```

## Estrutura de Pastas

```
greenforge_system/
├── README.md
├── BEM-VINDO.md
├── orquestrador/
│   ├── SKILL_ORQUESTRADOR_GREENFORGE.md
│   └── BOOT_ORQUESTRADOR_GREENFORGE.md
├── decompositor/
│   ├── SKILL_DECOMPOSITOR.md
│   └── BOOT_DECOMPOSITOR.md
├── solver/
│   ├── SKILL_SOLVER.md
│   └── BOOT_SOLVER.md
├── proposer/
│   ├── SKILL_PROPOSER.md
│   └── BOOT_PROPOSER.md
├── checker/
│   ├── SKILL_CHECKER_MARCH.md
│   └── BOOT_CHECKER.md
├── consolidador/
│   ├── SKILL_CONSOLIDADOR.md
│   └── BOOT_CONSOLIDADOR.md
├── adaptadores/
│   └── exemplos/
│       ├── ADAPTADOR_CODIGO.md
│       ├── ADAPTADOR_TEXTO.md
│       └── ADAPTADOR_DADOS.md
├── formatos/
│   ├── CONTRATO_VERIFICADOR.md
│   └── TEMPLATE_LEDGER_ESTADO.md
├── esquema/
│   └── ESTRUTURA_DE_WORKTREE.md
├── exemplos/
│   └── FLUXO_COMPLETO.md
└── scripts/
    └── executar_greenforge.py
```

## Como Usar

Veja o arquivo BEM-VINDO.md para instrucoes de inicializacao.
