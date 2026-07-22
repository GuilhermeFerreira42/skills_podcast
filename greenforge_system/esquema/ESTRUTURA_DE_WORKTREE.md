# Estrutura de Worktree para cada UAT

```
worktree_uat_NNN/
│
├── _descricao_da_uat.md          <-- o que precisa ser feito
├── _saida_solver.md              <-- saida do Solver (so ele ve)
├── _assercoes_para_validar.json  <-- assercoes extraidas pelo Proposer
├── _perguntas_checker.json       <-- perguntas para o Checker (sem saida original)
├── _resultado_validacao.json     <-- resultado do Checker cego
│
└── artefatos/                    <-- resultados parciais (opcional)
    ├── funcao_login.py
    └── ...
```

## Regras de Isolamento

1. Cada UAT tem sua propria pasta. O Solver so ve a pasta da UAT atual e o material de origem.
2. O Checker so ve as perguntas e o material de origem. NUNCA ve `_saida_solver.md`.
3. O Orquestrador ve tudo, mas so escreve no ledger.
4. O Consolidador so ve as UATs CONCLUIDAS e APROVADAS.
