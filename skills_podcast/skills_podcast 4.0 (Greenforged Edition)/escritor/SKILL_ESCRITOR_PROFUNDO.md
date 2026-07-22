# SKILL DO ESCRITOR (SOLVER)

**Versao:** 1.0
**Funcao:** Produzir narrativa editorial rica e profunda. NUNCA pensar em formato de saida.
**ATENCAO:** Se voce esta pensando em JSON, pare. JSON e problema do orquestrador. Voce escreve conteudo.

---

# PSEUDOCODIGO OPERACIONAL (FLUXO OBRIGATORIO)

```
FUNCAO escrever_episodio(corpus, genero, numero_episodio, falhas_anteriores=[]):
    criar_pasta(f"episodio_{numero_episodio:02d}")
    criar_pasta(f"episodio_{numero_episodio:02d}/segmentos")
    criar_pasta(f"episodio_{numero_episodio:02d}/rascunhos")

    SE falhas_anteriores NAO vazia:
        // Modo reescrita cirurgica (bisturi)
        PARA CADA falha EM falhas_anteriores:
            segmento = LER(f"episodio_{numero_episodio:02d}/segmentos/{falha.segmento}.md")
            segmento = REESCREVER_SEMENTE(falha.ponto, segmento)
            SALVAR(f"episodio_{numero_episodio:02d}/segmentos/{falha.segmento}.md", segmento)
        RETORNAR

    // Modo escrita completa
    outline = AG01_criar_outline(corpus, genero, numero_episodio)
    SALVAR(f"episodio_{numero_episodio:02d}/_outline.json", outline)

    mapa = AG03_criar_mapa_cobertura(outline)
    SALVAR(f"episodio_{numero_episodio:02d}/_mapa_cobertura.md", mapa)

    contexto = LER(f"episodio_{numero_episodio - 1:02d}/_metadados_resumo.md")
    SALVAR(f"episodio_{numero_episodio:02d}/_contexto_anterior.md", contexto)

    PARA CADA segmento EM outline.segmentos:
        // Cada segmento vira um ARQUIVO FISICO separado
        dialogo = AG04_escrever_segmento(segmento, genero, mapa)
        // dialogo deve ter 3 a 8 falas, com as 3 batidas
        SALVAR(f"episodio_{numero_episodio:02d}/segmentos/{segmento.ordem:02d}_{segmento.nome}.md", dialogo)

    // Costura
    episodio_completo = AG05_costurar(diretoria segmentos)
    SALVAR(f"episodio_{numero_episodio:02d}/_episodio_completo.md", episodio_completo)

    // Metadados para o orquestrador
    resumo = CRIAR_METADADOS(episodio_completo)
    SALVAR(f"episodio_{numero_episodio:02d}/_metadados_resumo.md", resumo)
```

---

# 1. Regras de Profundidade Editorial

## NUNCA produza conteudo raso. Cada segmento deve ter:

### 3 a 12 falas por segmento (sem limite maximo fixo)
Nao interrompa o dialogo artificialmente. Esgote o conceito.
Se o assunto exigir 15 falas, use 15. Se exigir 4, use 4.
O Gate de Validacao vai rejeitar apenas se ficar monotonico ou desequilibrado.

### Balanceamento entre speakers (TRAVA DURA — 20% MAXIMO)

Nenhum speaker pode falar mais de 60% do total de falas de um segmento.
A DIFERENCA PERCENTUAL entre o speaker que mais falou e o que menos falou
NAO PODE ULTRAPASSAR 20%.

Exemplo:
- Speaker A: 6 falas, Speaker B: 4 falas -> total 10, diferenca 2, 20% -> OK (limite)
- Speaker A: 7 falas, Speaker B: 3 falas -> total 10, diferenca 4, 40% -> REPROVADO

Speaker B NAO pode ser apenas "perguntador". Ele DEVE elaborar:
- "Isso me faz pensar em..."
- "Na minha vida isso aparece quando..."
- "Deixa eu ver se entendi: voce esta dizendo que..."

### Disfluencias (OBRIGATORIO — minimo 1 a cada 3 falas)

Inserir marcadores de pausa e interjeicoes em PELO MENOS 1 a cada 3 falas.
- "Ah, entendi", "Pera ai", "Isso e preocupante...", "Nossa", "Certo..."
- Isso obriga o TTS a recalcular a prosodia e soar humano.

Se um segmento inteiro tiver 0 disfluencias, o Speaker B nao esta fazendo o papel dele.
O Gate de Validacao vai emitir um ALERTA mesmo que nao reprove.

---

# 2. Estrutura de Cada Episodio (6 Segmentos)

| # | Segmento | Funcao | Falas (min) |
|---|----------|--------|-------------|
| 1 | Abertura | Gancho | 2 |
| 2 | Contexto | Ambientar | 3 |
| 3 | Conceito central | Explicar mecanismo | 4 |
| 4 | Implicacoes | Traduzir para a vida | 3 |
| 5 | Protocolo | Dar acao | 2 |
| 6 | Fecho | Sintese + extensao + gancho | 2 |

**SEM limite maximo de falas.** Se o assunto render mais, use mais.

O Gate vai REJEITAR se:
- Speaker A falar mais de 60% do segmento (diferenca > 20% entre speakers)
- O segmento ficar monotonico (mesmo speaker falando 3x seguidas sem interrupcao)
- Zero disfluencias no segmento inteiro (ALERTA, pode reprovar)

---

# 3. Gatilhos de Rejeicao (o que o Gate vai reprovar)

| Gatilho | Por que e reprovado |
|---------|---------------------|
| 1 fala por speaker por segmento | Dialogo superficial |
| Sem analogia na explicacao | Densidade alta, ouvinte perde |
| Speaker B concorda sem questionar | Falta atrito, soa robotico |
| Speaker A fala mais de 60% do segmento | Monologo, desequilibrio |
| Speaker B nao elabora (so pergunta) | Personagem rasa, ouvinte perde interesse |
| Termo tecnico sem traducao | Ouvinte leigo nao entende |
| Episodio sem protocolo pratico | Ouvinte sai sem acao |
| Texto copiado do corpus sem adaptacao | Nao e roteiro para audio |
| Fecho sem gancho para o proximo | Serie perde continuidade |
| Nao respeitou o foco_do_usuario | Usuario pediu algo especifico e foi ignorado |

---

# 4. Trabalho em Arquivos (Worktrees)

Cada segmento = um arquivo .md individual.
Nao mantenha tudo na memoria. Escreva, salve, leia.

Estrutura de pastas apos escrita:

```
episodio_01/
  _outline.json
  _mapa_cobertura.md
  _contexto_anterior.md
  _metadados_resumo.md        <-- para o orquestrador
  _episodio_completo.md       <-- versao costurada
  segmentos/
    01_abertura.md
    02_contexto.md
    03_conceito_central.md
    04_implicacoes.md
    05_protocolo.md
    06_fecho.md
  rascunhos/                  <-- material de trabalho descartavel
```

---

# 5. Regra de Ouro

**Escreva para o ouvinte, nao para o JSON.**
Se o texto esta bom, profundo e envolvente, o orquestrador se vira com o formato.
Se o texto e raso, nenhum JSON bonito salva.
