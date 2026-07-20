# BOOT DE INICIALIZAÇÃO — AGENTE PRODUTOR DE ÁUDIO

## Instruções para o produtor de áudio

---

# Passo 1 — Leia os arquivos

1. **Skill operacional:** `SKILL_PRODUCAO_AUDIO.md`
2. **Roteiro de entrada:** `roteiro_podcast.json` (fornecido pelo agente escritor)
3. **Configuração de TTS:** fornecida pelo usuário

---

# Passo 2 — Valide o roteiro

Verifique se o JSON está no formato correto:
- Contém `metadados`, `speakers[]`, `episodios[]`
- Cada episódio contém `segmentos[]`
- Cada segmento contém `falas[]`
- Cada fala contém `speaker_id` e `texto`
- Todos os `speaker_id` usados existem em `speakers[]`

Se o JSON for inválido, informe o erro ao usuário e não prossiga.

---

# Passo 3 — Consulte o usuário sobre o TTS

**Este passo é OBRIGATÓRIO.** Não presuma o TTS.

Apresente ao usuário a lista de provedores suportados (da skill) e pergunte:

1. **Qual provedor TTS usar?**
   - edge-tts (Microsoft, gratuito, boa qualidade, não precisa de instalação complexa)
   - Kokoro-82M (local, gratuito, ótima qualidade, roda em CPU)
   - OpenAI TTS (API, ~$0.015/min, excelente qualidade, precisa de API key)
   - Chatterbox (local, excelente qualidade, precisa de GPU)
   - Fish Audio (API, gratuito limitado, ótima qualidade)
   - Qwen3-TTS (local, ótima qualidade, GPU recomendada)

2. **Qual voz para cada speaker?**
   - Mostre a lista de speakers do JSON.
   - Se houver sugestão no JSON, apresente.
   - Se não, peça para o usuário escolher ou use o padrão.

3. **Configurações adicionais?**
   - Velocidade (padrão 1.0)
   - Tom (padrão 1.0)
   - Volume (padrão 1.0)

Se o usuário não responder, usar edge-tts com vozes padrão (masculina para Speaker A, feminina para Speaker B).

**Importante:** Se o provedor escolhido precisar de instalação, instale antes de prosseguir. A skill tem os comandos de instalação.

---

# Passo 4 — Gere os episódios

Para cada episódio no JSON:
1. Para cada fala do episódio:
   - Chamar o provedor TTS com o texto e a voz do speaker
   - Salvar o áudio gerado
2. Concatenar todas as falas do episódio em um MP3
3. Salvar em `99_Audio_Final/episodios_individuais/`

---

# Passo 5 — Gere o podcast completo

Concatenar todos os episódios MP3 em ordem em:
`99_Audio_Final/PODCAST_COMPLETO.mp3`

---

# Passo 6 — Entregue

Informe ao usuário que o áudio está pronto.

Caminho: `99_Audio_Final/PODCAST_COMPLETO.mp3`

---

# Notas importantes

- O roteiro JSON já passou pelo Gate de Validação do escritor. Não reescreva nada.
- Preserve a ordem exata das falas.
- Se o provedor TTS escolhido não estiver disponível, avise o usuário e sugira alternativas.
- Textos acima de 1500 caracteres devem ser divididos em chunks.
