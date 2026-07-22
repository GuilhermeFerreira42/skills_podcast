# Estrutura de Projeto Recomendada

Quando o orquestrador inicia um projeto, ele deve criar esta estrutura de pastas.

```
Nome_Do_Podcast/
│
├── estado_da_obra.md              ← CHECKPOINT UNICO (ledger)
├── plano_da_serie.md              ← plano geral aprovado
│
├── 00_Projeto_Editorial/
│   ├── DIRETRIZ_VIGENTE.md
│   ├── fontes_gerais.md
│   ├── glossario_voz.md
│   └── mapa_promessas.md
│
├── 00_Abertura_E_Encerramento/
│   ├── abertura_padrao.md
│   └── encerramento_padrao.md
│
├── episodio_01/                   ← PASTA ISOLADA (worktree)
│   ├── _outline.json
│   ├── _mapa_cobertura.md
│   ├── _contexto_anterior.md
│   ├── _episodio_completo.md      ← costura final
│   ├── _metadados_resumo.md       ← para o orquestrador (slow path)
│   ├── _afirmacoes_para_validar.json
│   ├── _perguntas_validador.json
│   ├── _resultado_validacao.json
│   ├── segmentos/
│   │   ├── 01_abertura.md
│   │   ├── 02_contexto.md
│   │   ├── 03_conceito_central.md
│   │   ├── 04_implicacoes.md
│   │   ├── 05_protocolo.md
│   │   └── 06_fecho.md
│   └── rascunhos/                ← descartavel
│
├── episodio_02/
│   └── ... (mesma estrutura)
│
├── ... (ate N episodios)
│
└── 99_Roteiro_Final/
    ├── roteiro_podcast.json       ← ENTREGAVEL PRINCIPAL
    └── episodios_individuais/     ← JSON por episodio (opcional)
```

## Regras de Isolamento

1. Cada episodio tem sua propria pasta. O escritor so ve a pasta do episodio atual + resumo do anterior.
2. O validador so ve as perguntas e o corpus. NUNCA a pasta do episodio.
3. O atomizador so ve o `_episodio_completo.md` e o corpus.
4. O produtor de audio so ve o `roteiro_podcast.json`.
5. O orquestrador ve TUDO, mas so escreve em `estado_da_obra.md`.
