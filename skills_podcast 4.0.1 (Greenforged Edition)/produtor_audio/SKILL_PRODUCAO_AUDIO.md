# SKILL DO PRODUTOR DE AUDIO

**Versao:** 2.0
**Funcao:** Receber JSON padronizado e gerar arquivos MP3.
**NUNCA edita o roteiro.** Apenas converte em audio.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO produzir_audio(caminho_json, config_tts):
    // caminho_json e passado PELO ORQUESTRADOR como argumento
    // Exemplo: python gerar_audio_do_json.py 99_Roteiro_Final/roteiro_podcast.json --tts kokoro
    roteiro = LER(caminho_json)

    // Consulta obrigatoria ao usuario
    SE config_tts.provedor NAO DEFINIDO:
        provedor = PERGUNTAR_USUARIO("Qual TTS usar? [edge-tts/Kokoro/OpenAI/Chatterbox/Fish]")
        se provedor == "edge-tts": INSTALAR("pip install edge-tts")
        se provedor == "Kokoro": INSTALAR("pip install kokoro-onnx soundfile")
        se provedor == "OpenAI": SOLICITAR("API key da OpenAI")
        ...

    PARA CADA episodio EM roteiro.episodios:
        audio_episodio = []
        PARA CADA segmento EM episodio.segmentos:
            PARA CADA fala EM segmento.falas:
                voz = MAPEAR_VOZ(fala.speaker_id, config_tts)
                audio = GERAR_TTS(fala.texto, voz)
                audio_episodio.ADICIONAR(audio)

        CONCATENAR(audio_episodio, saida=f"episodio_{episodio.numero}.mp3")

    CONCATENAR_TODOS(saida="PODCAST_COMPLETO.mp3")
```

---

# 1. Consulta ao Usuario (OBRIGATORIO)

Antes de comecar, apresente as opcoes:

| Provedor | Custo | Qualidade | Requisitos |
|---|---|---|---|
| edge-tts | Gratuito | Boa | Internet |
| Kokoro-82M | Gratuito | Otima | CPU, 4GB RAM |
| OpenAI TTS | ~$0.015/min | Excelente | API key |
| Chatterbox | Gratuito | Excelente | GPU 5GB VRAM |
| Fish Audio | Gratuito limitado | Otima | API key |

Pergunte: qual prefere? Se nao responder, use edge-tts.

---

# 2. Mapeamento de Vozes (Padrao)

| Speaker | Voz Padrao (edge-tts) | Voz Padrao (Kokoro) |
|---|---|---|
| Speaker A | pt-BR-AntonioNeural | pm_alex |
| Speaker B | pt-BR-FranciscaNeural | pf_dora |
| Speaker C | pt-BR-AntonioNeural | pm_santa |
| Speaker D | pt-BR-ThalitaMultilingualNeural | pf_dora |

---

# 3. Tratamento de Disfluencias

O JSON pode conter falas marcadas como `"disfluencia": true`.
Isso indica pausas ou interjeicoes. O TTS deve mante-las no texto, pois sao intencionais para naturalidade.

Nao remova. Nao "corrija". Mantenha como esta.

---

# 4. Saida

- `PODCAST_COMPLETO.mp3` — episodios concatenados em ordem
- `episodios_individuais/` — cada episodio separado

---

# 5. Regras

1. Nao edite o texto. Nem para corrigir gramatica.
2. Nao pule falas. Toda fala do JSON vira audio.
3. Preserve a ordem exata.
4. Se um provedor falhar, instale antes de prosseguir.
5. Disfluencias sao intencionais. Mantenha.
