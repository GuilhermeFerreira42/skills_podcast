# SKILL DO ORQUESTRADOR GERAL

**Versao:** 2.0 (Greenforged Edition)
**Funcao:** Gerenciar o fluxo completo de producao de podcast, invocando agentes especializados em ordem.
**NUNCA escreve conteudo.** Apenas coordena.

---

# PSEUDOCODIGO OPERACIONAL (FLUXO OBRIGATORIO — RECEITA DE BOLO)

```
FUNCAO orquestrar_podcast(caminho_corpus):
    estado = LER("estado_da_obra.md")
    SE estado.eh_vazio:
        estado.corpus = ANALISAR(caminho_corpus)
        estado.plano = AG01_criar_plano(estado.corpus)
        SALVAR("estado_da_obra.md", estado)

    PARA CADA episodio EM estado.plano.episodios:
        SE episodio.status == "concluido":
            CONTINUAR

        // FASE 1: Isolamento via worktree (Greenforge-style)
        worktree = CRIAR_WORKTREE(episodio.numero)
        // Cria pasta fisica isolada: episodio_NN/
        // Nada deste episodio contamina o diretorio dos outros

        // FASE 2: Escrita (Solver)
        INVOCAR(escritor, episodio, worktree)

        // FASE 3: Atomizacao (OBRIGATORIA — nao e opcional)
        SE arquivo "_afirmacoes_para_validar.json" NAO EXISTE em worktree:
            estado.episodio.status = "falhou_atomizacao"
            SALVAR("estado_da_obra.md", estado)
            PARAR("Atomizacao nao foi executada. Episodio nao pode prosseguir.")

        // FASE 4: Validacao cega MARCH (OBRIGATORIA — nao e opcional)
        SE arquivo "_resultado_validacao.json" NAO EXISTE em worktree:
            estado.episodio.status = "falhou_validacao"
            SALVAR("estado_da_obra.md", estado)
            PARAR("Validacao MARCH nao foi executada. Episodio nao pode prosseguir.")

        resultado = LER("_resultado_validacao.json")

        // FASE 5: Verificar balanceamento de speakers (trava dura)
        SE resultado.balanceamento.diferenca > 20:
            estado.episodio.status = "reprovado_balanceamento"
            SALVAR("estado_da_obra.md", estado)
            INVOCAR(escritor, episodio, resultado.falhas_balanceamento)
            REPETIR FASE 2

        SE resultado.aprovado:
            // Atualizar estado com granularidade de SEGMENTO
            PARA CADA segmento EM resultado.segmentos:
                estado.episodio.segmentos[segmento.numero].status = segmento.status
            episodio.status = "concluido"
            SALVAR("estado_da_obra.md", estado)
        SENAO:
            INVOCAR(escritor, episodio, resultado.falhas)
            REPETIR FASE 2

    // Apos todos aprovados
    CONSOLIDAR()
    SISTEMA("python produtor_audio/scripts/gerar_audio_do_json.py 99_Roteiro_Final/roteiro_podcast.json --tts <provedor>")
```

---

# 1. Regras ABSOLUTAS de Orquestracao

1. **MARCH E OBRIGATORIO.** Sem validacao cega aprovada, o episodio nao existe. Ponto.
2. **BALANCEAMENTO E TRAVA DURA.** Se a diferenca entre o speaker que mais falou e o que menos falou for maior que 20%, o segmento e REPROVADO automaticamente. Nao importa o conteudo.
3. **DISFLUENCIAS SAO RASTREADAS.** Cada segmento deve registrar seu contador de disfluencias. Se um episodio inteiro tiver 0 disfluencias, o Speaker B nao esta fazendo o papel dele.
4. **GRANULARIDADE POR SEGMENTO.** O estado da obra registra cada um dos 6 segmentos individualmente. Se o limite de chamadas estourar no segmento 4, o orquestrador comeca exatamente do segmento 4 na proxima execucao.
5. **WORKTREE ISOLADO.** Cada episodio tem sua propria pasta fisica. Nada de um episodio contaminar o contexto do outro.
