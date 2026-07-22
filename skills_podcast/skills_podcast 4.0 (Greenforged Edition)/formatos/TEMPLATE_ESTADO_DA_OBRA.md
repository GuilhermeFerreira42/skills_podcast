# Estado da Obra

**Projeto:** {{NOME_DO_PROJETO}}
**Ultima atualizacao:** {{DATA_HORA}}
**Status geral:** {{EM_ANDAMENTO | CONCLUIDO | INTERROMPIDO}}
**Chamadas gastas ate agora:** {{NUMERO}}
**Limite de chamadas:** {{LIMITE}}

---

## Progresso por Episodio (Granularidade por Segmento)

| Ep | Titulo | Seg01 | Seg02 | Seg03 | Seg04 | Seg05 | Seg06 | Status Geral | Validacao MARCH | Balanc. |
|----|--------|-------|-------|-------|-------|-------|-------|-------------|-----------------|---------|
| 00 | Intro  | CONCL | CONCL | CONCL | CONCL | CONCL | CONCL | CONCLUIDO   | APROVADO        | OK 52/48|
| 01 | Titulo | CONCL | CONCL | CONCL | ESCR  | PEND  | PEND  | ESCREVENDO  | PENDENTE        | -       |
| 02 | Titulo | PEND  | PEND  | PEND  | PEND  | PEND  | PEND  | PENDENTE    | -               | -       |

**Legenda:** PEND=Pendente, ESCR=Escrevendo, REV=Em revisao, CONCL=Concluido, REPR=Reprovado

---

## Detalhamento por Episodio

### Episodio 01 — {{TITULO}}

| Seg | Nome | Status | Disfluencias | Falas A | Falas B | Diferenca | Ultima acao |
|-----|------|--------|-------------|---------|---------|-----------|-------------|
| 1   | Abertura | CONCL | 3 | 2 | 2 | 0% | Validado |
| 2   | Contexto | CONCL | 2 | 3 | 3 | 0% | Validado |
| 3   | Conceito | CONCL | 4 | 4 | 3 | 14% | Validado |
| 4   | Implic. | ESCR | - | - | - | - | Escritor trabalhando |
| 5   | Protocolo | PEND | - | - | - | - | Aguardando |
| 6   | Fecho | PEND | - | - | - | - | Aguardando |

### Episodio 02 — {{TITULO}}

... (mesma estrutura)

---

## Pendências e Bloqueios

- Ep 01, Seg 04: aguardando conclusao do Escritor
- Ep 02: aguardando Ep 01 ser concluido para criar contexto anterior

---

## Regras para o Orquestrador (Greenforged Edition)

1. SEMPRE ler este arquivo antes de comecar uma nova acao.
2. SEMPRE atualizar este arquivo apos CADA segmento concluido.
3. **VALIDACAO MARCH E OBRIGATORIA.** Sem `_resultado_validacao.json` aprovado, o episodio NAO esta concluido.
4. **BALANCEAMENTO E TRAVA DURA.** Se a diferenca de falas entre speakers for > 20%, reprovar automaticamente.
5. **DISFLUENCIAS SAO RASTREADAS POR SEGMENTO.** Se um episodio tiver 0 disfluencias, o Speaker B nao esta fazendo o papel dele.
6. Se o limite de chamadas for atingido, marcar status como INTERROMPIDO e o ultimo segmento exato.
7. Na proxima execucao, ler o estado e comecar EXATAMENTE do segmento interrompido.
