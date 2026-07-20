# Skills para Automação de Podcast

Este repositório contém as skills e arquivos necessários para automatizar a produção de podcasts, desde a análise do conteúdo bruto até a geração do áudio final.

## Arquitetura

O sistema é dividido em dois agentes independentes:

```
┌─────────────────────────────────────────────────────────────┐
│                    USUÁRIO (EDITOR-CHEFE)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENTE 1: ESCRITOR (Orquestrador Editorial)                │
│  Entrada: corpus + skill + gênero                           │
│  Saída: roteiro_podcast.json (formato padronizado)          │
│  Função: analisar, estruturar, escrever, revisar            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AGENTE 2: PRODUTOR DE ÁUDIO                                │
│  Entrada: roteiro_podcast.json + config TTS                 │
│  Saída: PODCAST_COMPLETO.mp3                                │
│  Função: sintetizar voz, concatenar, entregar               │
└─────────────────────────────────────────────────────────────┘
```

## Estrutura de pastas

```
skills_podcast/
├── README.md                         ← este arquivo
├── formatos/
│   └── FORMATO_ROTEIRO_PODCAST.json  ← formato padronizado de troca
├── escritor/
│   ├── SKILL_BOOK_FORGE_PODCAST.md   ← skill do escritor
│   ├── GENERO_PODCAST_NARRATIVO_EDUCACIONAL.md  ← gênero padrão
│   └── BOOT_INICIAL.md               ← boot para o escritor
└── produtor_audio/
    ├── SKILL_PRODUCAO_AUDIO.md       ← skill do produtor de áudio
    ├── BOOT_PRODUCAO_AUDIO.md        ← boot para o produtor
    └── scripts/
        ├── gerar_podcast_edge_tts.py ← script para edge-tts
        └── gerar_podcast_kokoro.py   ← script para Kokoro-82M
```

## Como usar

### Fluxo completo

1. O usuário entrega o corpus (conteúdo bruto) para o **Agente Escritor**,
   junto com os arquivos `SKILL_BOOK_FORGE_PODCAST.md` e `BOOT_INICIAL.md`.

2. O escritor analisa, estrutura, escreve, revisa e entrega
   `roteiro_podcast.json` no formato padronizado.

3. O usuário entrega o `roteiro_podcast.json` para o **Agente Produtor de Áudio**,
   junto com `SKILL_PRODUCAO_AUDIO.md` e `BOOT_PRODUCAO_AUDIO.md`,
   especificando qual TTS usar.

4. O produtor gera o áudio e entrega `PODCAST_COMPLETO.mp3`.

### Formato de troca

O contrato entre os dois agentes é o arquivo `FORMATO_ROTEIRO_PODCAST.json`
na pasta `formatos/`. Qualquer agente que respeitar esse formato pode
substituir qualquer um dos dois lados.

### TTS disponíveis

| Provedor | Custo | Qualidade | Ideal para |
|---|---|---|---|
| edge-tts (Microsoft) | Gratuito | Boa | Prototipagem rápida |
| Kokoro-82M | Gratuito | Ótima | Produção em CPU |
| OpenAI TTS | ~$0.015/min | Excelente | Qualidade via API |
| Chatterbox | Gratuito | Excelente | GPU disponível |
| Fish Audio | Gratuito limitado | Ótima | API rápida |

## Histórico do projeto

Este sistema foi desenvolvido ao longo de várias sessões de trabalho
combinando as skills BOOK_FORGE (escrita) e BOOK_REVIEW (revisão) com
templates de podcast do Open Notebook LM e múltiplos motores TTS.
O resultado é um pipeline completo e testado que vai do conteúdo bruto
ao áudio final em MP3.
