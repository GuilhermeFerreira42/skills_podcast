# Podcast System — Sistema de Orquestração Multiagente para Produção de Podcast

Arquitetura de elite para transformar qualquer corpus bruto em podcast de alta profundidade,
com validacao multiagente, persistencia de estado e producao de audio.

## Arquitetura

```
                    ORQUESTRADOR GERAL
                  (gerencia o fluxo, nao escreve)
                          |
         +----------------+----------------+
         |                |                |
    ESCRITOR        ATOMIZADOR       VALIDADOR
    (Solver)        (Proposer)       (Checker cego)
    narrativa       extrai           cruza com
    profunda        afirmacoes       fontes brutas
         |                |                |
         +----------------+----------------+
                          |
                   PRODUTOR DE AUDIO
                   (JSON -> MP3)
```

## Pilares Arquiteturais (5 Pilares)

1. **Modularizacao Atomica** — Worktrees de consciencia. Cada segmento em pasta propria.
2. **Pseudocodigo Operacional** — Fluxo linear obrigatorio no topo de cada skill.
3. **Assimetria de Informacao (MARCH)** — Validador cego, sem ver o roteiro original.
4. **Cadeia Dupla Oscilatoria** — Registro binario + pressao corretiva. Sem texto amigavel.
5. **Disfluencias e Atrito** — Speaker B duvida de proposito. Marcadores de pausa no JSON.

## Persistencia de Estado

Cada agente escreve em `estado_da_obra.md` antes e depois de cada acao.
Assim, qualquer interrupcao (limite de chamadas, queda) permite retomada exata.

## Como Usar

1. O usuario entrega o corpus para o **Orquestrador Geral**.
2. O orquestrador invoca o **Escritor** para cada episodio.
3. O **Atomizador** extrai afirmacoes do texto produzido.
4. O **Validador** cruza as afirmacoes com as fontes (cego ao roteiro).
5. Se aprovado, o **Produtor de Audio** gera o MP3 final.

Cada agente possui seu proprio diretorio com `SKILL.md` e `BOOT.md`.
