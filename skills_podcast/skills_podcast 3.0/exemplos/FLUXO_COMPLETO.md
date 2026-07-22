# Exemplo de Fluxo Completo

Este exemplo mostra como o sistema orquestra a producao de um podcast do inicio ao fim.

---

## Cenario

Usuario quer produzir um podcast baseado no livro "O Homem Sabotado" (30 capitulos).

---

## Passo 1 — Orquestrador le o estado

```
LER("estado_da_obra.md")
// estado vazio -> iniciar do zero
```

---

## Passo 2 — Orquestrador analisa o corpus e cria o plano

```
corpus = LER("O_Homem_Sabotado_EDICAO_FINAL.md")
plano = AG01_criar_plano(corpus)
// 30 episodios, um por capitulo
SALVAR("estado_da_obra.md", plano)
```

---

## Passo 3 — Loop de producao (Episodio 01)

### 3a. Orquestrador invoca Escritor

```
INVOCAR(escritor, {
  corpus: "O_Homem_Sabotado.md",
  genero: "GENERO_PODCAST_NARRATIVO_EDUCACIONAL.md",
  episodio: 1
})
```

### 3b. Escritor cria a estrutura de pastas

```
criar_pasta("episodio_01/segmentos")
criar_pasta("episodio_01/rascunhos")
```

### 3c. Escritor escreve cada segmento em arquivo individual

```
PARA CADA segmento EM outline.segmentos:
    dialogo = GERAR_DIALOGO(segmento)
    // dialogo com 4-6 trocas, 3 batidas, atrito, disfluencias
    SALVAR("episodio_01/segmentos/01_abertura.md", dialogo)
    SALVAR("episodio_01/segmentos/02_contexto.md", dialogo)
    SALVAR("episodio_01/segmentos/03_conceito.md", dialogo)
    SALVAR("episodio_01/segmentos/04_implicacoes.md", dialogo)
    SALVAR("episodio_01/segmentos/05_protocolo.md", dialogo)
    SALVAR("episodio_01/segmentos/06_fecho.md", dialogo)
```

### 3d. Escritor costura e gera metadados

```
costurado = AG05_costurar(pasta segmentos)
SALVAR("episodio_01/_episodio_completo.md", costurado)

resumo = CRIAR_METADADOS(costurado)
SALVAR("episodio_01/_metadados_resumo.md", resumo)

AVISAR(orquestrador, "Ep 01 pronto")
```

---

## Passo 4 — Orquestrador invoca Atomizador

```
INVOCAR(atomizador, {
  episodio: "episodio_01",
  texto: "_episodio_completo.md"
})
```

Atomizador extrai 47 afirmacoes factuais do texto.
Gera 47 perguntas para o validador.
Salva em `episodio_01/_perguntas_validador.json`.

---

## Passo 5 — Orquestrador invoca Validador Cego

```
INVOCAR(validador, {
  episodio: "episodio_01",
  perguntas: "_perguntas_validador.json",
  corpus: "O_Homem_Sabotado.md"
  // ATENCAO: validador NAO recebe "_episodio_completo.md"
})
```

Validador responde:
- 44 CONFIRMADO
- 2 NAO_ENCONTRADO
- 1 CONTRADITO

**Resultado: REPROVADO** (tolerancia zero para CONTRADITO).

---

## Passo 6 — Orquestrador devolve ao Escritor para reescrita cirurgica

```
INVOCAR(escritor, {
  episodio: 1,
  falhas: [
    {segmento: "03_conceito", ponto: "Speaker A disse X mas corpus diz Y"},
    {segmento: "05_protocolo", ponto: "Speaker A mencionou estudo nao encontrado no corpus"}
  ]
})
```

Escritor reescreve APENAS os 2 segmentos com problemas.
Nao reescreve o episodio inteiro.

---

## Passo 7 — Segundo ciclo de validacao

```
// Repetir Passo 4 e 5
Resultado: APROVADO (47/47 CONFIRMADO)
```

---

## Passo 8 — Orquestrador marca como concluido

```
estado.episodio_01.status = "concluido"
SALVAR("estado_da_obra.md", estado)
```

---

## Passo 9 — Proximo episodio

O escritor le o `_metadados_resumo.md` do episodio 01
para criar o `_contexto_anterior.md` do episodio 02.

O loop continua ate o episodio 30.

---

## Passo 10 — Apos todos os episodios

```
CONSOLIDAR_JSON() -> 99_Roteiro_Final/roteiro_podcast.json
INVOCAR(produtor_audio, {json: "roteiro_podcast.json", tts: "Kokoro"})
// Produtor consulta usuario, instala Kokoro se necessario, gera MP3
```

---

## Resumo

| Fase | Quem faz | O que produz |
|------|----------|-------------|
| 1-2 | Orquestrador | Plano + estado da obra |
| 3 | Escritor | Segmentos em arquivos fisicos |
| 4 | Atomizador | Afirmacoes + perguntas |
| 5 | Validador | Resultado booleano |
| 6 | Escritor | Reescrita cirurgica (se necessario) |
| 7-9 | Orquestrador | Controle de estado |
| 10 | Orquestrador + Produtor | JSON + MP3 |
