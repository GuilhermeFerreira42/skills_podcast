# Estado da Obra

**Projeto:** {{NOME_DO_PROJETO}}
**Ultima atualizacao:** {{DATA_HORA}}
**Status geral:** {{EM_ANDAMENTO | CONCLUIDO | INTERROMPIDO}}
**Chamadas gastas ate agora:** {{NUMERO}}
**Limite de chamadas:** {{LIMITE}}

---

## Progresso por Episodio

| # | Titulo | Segmentos | Status | Ultima acao |
|---|--------|-----------|--------|-------------|
| 00 | Introducao | 6/6 | CONCLUIDO | Validado e aprovado |
| 01 | Titulo do Ep | 4/6 | ESCREVENDO | Segmento 05 pendente |
| 02 | Titulo do Ep | 0/6 | PENDENTE | Aguardando |
| ... | ... | ... | ... | ... |
| 30 | Titulo do Ep | 0/6 | PENDENTE | Aguardando |

---

## Segmentos em Andamento

**Episodio 01 — Segmento 04 (Implicacoes)**
- Status: ESCRITO, aguardando atomizacao
- Escritor concluiu. Proximo: Atomizador.

**Episodio 01 — Segmento 05 (Protocolo)**
- Status: PENDENTE
- Escritor ainda nao iniciou.

---

## Pendências e Bloqueios

- Ep 01, Seg 05: escritor precisa de contexto adicional do corpus
- Ep 02: aguardando Ep 01 ser concluido para criar contexto anterior

---

## Regras para o Orquestrador

1. SEMPRE ler este arquivo antes de comecar uma nova acao.
2. SEMPRE atualizar este arquivo apos cada acao atomica.
3. Se o limite de chamadas for atingido, marcar status como INTERROMPIDO.
4. Na proxima execucao, ler o estado e continuar de onde parou.
5. Nao refazer o que ja esta marcado como CONCLUIDO.
