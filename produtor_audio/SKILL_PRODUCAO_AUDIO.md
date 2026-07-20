# SKILL DE PRODUÇÃO DE ÁUDIO PARA PODCAST

## Skill operacional para converter roteiro JSON em áudio MP3

**Versão:** 1.0
**Tipo:** Skill de processo técnico
**Uso:** Recebe roteiro JSON padronizado e gera episódios de áudio
**Função:** Converter roteiro estruturado em arquivos MP3 prontos para publicação

---

# 1. O que é esta skill

Esta skill transforma o arquivo JSON gerado pelo agente escritor em áudio MP3.

Ela não escreve roteiro, não define gênero, não faz revisão editorial. Ela apenas **executa a síntese de voz** usando o provedor TTS escolhido pelo usuário.

## Entrada
- Arquivo `roteiro_podcast.json` no formato padronizado (versão 1.0);
- Configuração de TTS fornecida pelo usuário.

## Saída
- Episódios individuais em MP3;
- Podcast completo unificado em MP3.

---

# 2. Provedores TTS suportados

| Provedor | Tipo | Como acessar | Custo | Qualidade | Requisitos |
|---|---|---|---|---|---|
| edge-tts (Microsoft) | API cloud gratuita | pip install edge-tts | Gratuito | Boa | Internet |
| Kokoro-82M | Local (CPU) | pip install kokoro-onnx soundfile | Gratuito | Ótima | 4GB RAM, sem GPU |
| OpenAI TTS | API cloud paga | pip install openai + API key | ~$0.015/min | Excelente | Internet, API key |
| Chatterbox Turbo | Local (GPU) | pip install chatterbox-tts | Gratuito | Excelente | GPU 5GB VRAM |
| Chatterbox Multilingual | Local (GPU) | pip install chatterbox-tts | Gratuito | Excelente | GPU 6GB VRAM |
| Fish Audio S2.1 Pro | API cloud gratuita | requests + API key fish.audio | Gratuito limitado | Ótima | Internet |
| Qwen3-TTS | Local (GPU/CPU) | pip install qwen-tts | Gratuito | Ótima | GPU recomendada |

## 2.1 Consulta ao usuário

Antes de iniciar a produção, o produtor DEVE consultar o usuário para definir:

1. **Qual provedor TTS usar?** — Apresentar a lista acima com um resumo de prós e contras.
2. **Qual voz para cada speaker?** — Se o JSON tiver vozes sugeridas, apresentá-las. Se não, sugerir com base no gênero dos speakers.
3. **Configurações adicionais?** — Velocidade, tom, volume (se o provedor suportar).

Se o usuário não responder ou disser "padrão", usar edge-tts com vozes padrão.

## 2.2 Instalação de provedores

O produtor DEVE ser capaz de instalar qualquer provedor solicitado. Comandos de instalação:

| Provedor | Instalação |
|---|---|
| edge-tts | `pip install edge-tts` |
| Kokoro-82M | `pip install kokoro-onnx soundfile` |
| OpenAI TTS | `pip install openai` |
| Chatterbox | `pip install chatterbox-tts` |
| Fish Audio | `pip install requests` (já incluso no Python padrão) |
| Qwen3-TTS | `pip install qwen-tts` |

Para provedores locais (Kokoro, Chatterbox, Qwen3), o download dos modelos acontece automaticamente na primeira execução.

---

# 3. Fluxo de trabalho

## Fase 1 — Leitura do roteiro

1. Ler `roteiro_podcast.json`;
2. Validar estrutura contra o formato padronizado;
3. Extrair speakers, episódios, segmentos e falas;
4. Confirmar mapeamento de vozes (qual voz para qual speaker).

## Fase 2 — Mapeamento de vozes

Para cada speaker no JSON, definir qual voz será usada.

Se o usuário fornecer um mapeamento, usar esse.
Se não fornecer, usar padrão:
- Speaker A: voz masculina (ex: AntonioNeural ou pm_alex)
- Speaker B: voz feminina (ex: FranciscaNeural ou pf_dora)
- Speaker C: voz masculina alternativa
- Speaker D: voz feminina alternativa

## Fase 3 — Geração por episódio

Para cada episódio:
1. Criar pasta do episódio;
2. Para cada fala, gerar áudio com o provedor TTS configurado;
3. Concatenar falas em um único MP3;
4. Salvar em `episodios_individuais/`.

## Fase 4 — Geração do podcast completo

Concatenar todos os episódios em ordem em um único MP3.

## Fase 5 — Entrega

Organizar os arquivos finais em `99_Audio_Final/`:
- `99_Audio_Final/PODCAST_COMPLETO.mp3`
- `99_Audio_Final/episodios_individuais/`

---

# 4. Tratamento de textos longos

Se uma fala tiver mais de 1500 caracteres, dividir em chunks menores antes de enviar ao TTS. Para Kokoro, o chunking é automático. Para edge-tts, dividir manualmente.

---

# 5. Tratamento de erros

| Erro | Ação |
|---|---|
| Provedor TTS não encontrado | Informar ao usuário e sugerir alternativas |
| API key inválida | Informar ao usuário |
| Fala muito longa para o provedor | Dividir em chunks menores |
| Falha em uma fala | Tentar novamente 1 vez; se falhar, pular e registrar |
| Arquivo JSON inválido | Informar o erro ao usuário |

---

# 6. Dependências técnicas

- Python 3.10+
- ffmpeg (para concatenação de áudio)
- edge-tts (para TTS Microsoft)
- OU kokoro-onnx + soundfile (para Kokoro local)
- OU openai (para OpenAI TTS)
- OU chatterbox-tts (para Chatterbox local)
- OU requests (para Fish Audio API)

---

# 7. Regras de ouro

1. **Não modificar o roteiro.** O produtor de áudio não edita texto.
2. **Não pular falas.** Toda fala do JSON deve virar áudio.
3. **Preservar ordem.** Falas, segmentos e episódios na ordem exata do JSON.
4. **Último entregável é MP3.** O usuário final não quer WAV.
5. **Se o provedor falhar, avisar o usuário. Não inventar áudio.**
