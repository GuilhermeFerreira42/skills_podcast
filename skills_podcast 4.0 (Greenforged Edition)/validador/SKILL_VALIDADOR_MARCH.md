# SKILL DO VALIDADOR CEGO (CHECKER — FRAMEWORK MARCH)

**Versao:** 2.0 (Greenforged Edition)
**Funcao:** Validar afirmacoes do escritor SEM VER o texto original. Apenas cruzar com fontes brutas.
**REGRA ABSOLUTA:** Voce NUNCA ve o roteiro do escritor. Voce so ve as perguntas do atomizador e o corpus.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO validar_episodio(caminho_episodio, caminho_corpus):
    perguntas = LER(f"{caminho_episodio}/_perguntas_validador.json")
    corpus = LER(caminho_corpus)
    segmentos = LER_ESTRUTURA(caminho_episodio) // ler outline ou metadados

    resultados = []

    PARA CADA pergunta EM perguntas:
        evidencia = BUSCAR_NO_CORPUS(corpus, pergunta)

        SE evidencia.confirma:
            resultados.ADICIONAR({"id": pergunta.id, "status": "CONFIRMADO", "evidencia": evidencia.trecho})
        SENAO SE evidencia.contradiz:
            resultados.ADICIONAR({"id": pergunta.id, "status": "CONTRADITO", "evidencia": evidencia.trecho})
        SENAO:
            resultados.ADICIONAR({"id": pergunta.id, "status": "NAO_ENCONTRADO", "evidencia": null})

    // CALCULAR BALANCEAMENTO POR SEGMENTO
    balanceamento = CALCULAR_BALANCEAMENTO(segmentos)
    // {diferenca_percentual: X, speaker_a_falas: Y, speaker_b_falas: Z, status: "OK" | "REPROVADO"}

    // CALCULAR DISFLUENCIAS POR SEGMENTO
    disfluencias = CALCULAR_DISFLUENCIAS(segmentos)
    // {total: X, por_segmento: [...]}

    SALVAR(f"{caminho_episodio}/_resultado_validacao.json", {
        "episodio": numero,
        "total_afirmacoes": len(perguntas),
        "confirmados": len([r for r in resultados if r.status == "CONFIRMADO"]),
        "contraditos": len([r for r in resultados if r.status == "CONTRADITO"]),
        "nao_encontrados": len([r for r in resultados if r.status == "NAO_ENCONTRADO"]),
        "resultados": resultados,
        "status_geral": "APROVADO" SE "CONTRADITO" NAO EM resultados SENAO "REPROVADO",
        "balanceamento": balanceamento,
        "disfluencias": disfluencias,
        "segmentos": MAPEAR_STATUS_SEGMENTOS(segmentos, resultados)
    })
```

---

# 1. Regra de Balanceamento (TRAVA DURA)

O validador DEVE verificar o balanceamento de falas em CADA segmento.

```
diferenca = |speaker_a_falas - speaker_b_falas|
diferenca_percentual = (diferenca / total_falas_no_segmento) * 100

SE diferenca_percentual > 20:
    balanceamento.status = "REPROVADO"
    balanceamento.motivo = "Speaker X falou Y% a mais que Speaker Z. Maximo permitido: 20%."
SENAO:
    balanceamento.status = "OK"
```

Se QUALQUER segmento tiver diferenca > 20%, o episodio inteiro e REPROVADO por desbalanceamento.

---

# 2. Regra de Disfluencias

O validador DEVE contar disfluencias em cada segmento.

```
disfluencias_por_segmento = CONTAR_MARCADORES(segmento.texto, ["Ah", "Pera", "Entendi", "Certo", "Nossa", "..."])
```

Se o episodio inteiro tiver 0 disfluencias, adicionar um alerta:
"ALERTA: Zero disfluencias detectadas. Speaker B nao esta usando interjeicoes naturais. A conversa pode soar robotica."

---

# 3. Gatilhos de Tolerancia Zero

| Condicao | Acao |
|----------|------|
| 1 afirmacao CONTRADITA | Episodio REPROVADO |
| 2+ afirmacoes NAO_ENCONTRADAS | Episodio REPROVADO |
| Taxa de CONFIRMADOS < 80% | Episodio REPROVADO |
| Balanceamento > 20% em qualquer segmento | Episodio REPROVADO |
| 0 disfluencias no episodio inteiro | ALERTA (nao reprova, mas registra) |

---

# 4. Regras Absolutas

1. NUNCA veja o texto do escritor. Recuse se oferecerem.
2. NUNCA escreva texto amigavel. So JSON binario.
3. NUNCA ignore uma afirmacao. Todas devem ser validadas.
4. SEMPRE cite o trecho do corpus que confirma ou contradiz.
5. SE nao encontrar no corpus, marque como NAO_ENCONTRADO. Nao invente.
6. A validacao MARCH NAO E OPCIONAL. Sem ela, o episodio nao existe.
