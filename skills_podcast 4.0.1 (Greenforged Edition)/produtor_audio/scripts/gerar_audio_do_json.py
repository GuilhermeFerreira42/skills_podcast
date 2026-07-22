#!/usr/bin/env python3
"""
Script universal de geracao de audio a partir do JSON padronizado.
Uso: python gerar_audio_do_json.py <caminho_do_json> [--tts edge-tts|kokoro|openai]

O caminho do JSON e passado pelo orquestrador como argumento.
Mapeamento de vozes e DINAMICO: le do array speakers[] no JSON.
"""

import sys, os, json, asyncio, subprocess, tempfile, re
from pathlib import Path

# Mapeamento padrao por provedor (usado se o JSON nao sugerir vozes)
VOZES_PADRAO = {
    "edge-tts": {"masculino": "pt-BR-AntonioNeural", "feminino": "pt-BR-FranciscaNeural"},
    "kokoro": {"masculino": "pm_alex", "feminino": "pf_dora"},
}

FFMPEG = "ffmpeg"  # assume no PATH


def carregar_roteiro(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def mapear_vozes(roteiro: dict, provedor: str) -> dict:
    """Mapeia speaker_id -> voz, lendo do JSON ou usando padrao."""
    mapa = {}
    padrao = VOZES_PADRAO.get(provedor, VOZES_PADRAO["edge-tts"])

    for speaker in roteiro.get("speakers", []):
        speaker_id = speaker["id"]
        genero = speaker.get("genero", "masculino")

        # Prioridade: voz_sugerida no JSON > padrao por genero
        if provedor == "edge-tts" and speaker.get("voz_sugerida"):
            mapa[speaker_id] = speaker["voz_sugerida"]
        elif provedor == "kokoro":
            mapa[speaker_id] = padrao.get(genero, padrao["masculino"])
        else:
            mapa[speaker_id] = padrao.get(genero, padrao["masculino"])

    return mapa


async def gerar_com_edge_tts(texto: str, voz: str, arquivo: Path):
    import edge_tts
    comm = edge_tts.Communicate(texto, voz)
    await comm.save(str(arquivo))


def gerar_com_kokoro(texto: str, voz: str, arquivo: Path):
    """Usa kokoro-onnx para gerar audio."""
    import warnings
    warnings.filterwarnings('ignore')
    from kokoro import KPipeline
    import soundfile as sf
    import numpy as np

    pipeline = KPipeline(lang_code='p', repo_id='hexgrad/Kokoro-82M')
    audio = []
    for _, _, chunk in pipeline(texto, voice=voz):
        audio.append(chunk)
    audio = np.concatenate(audio) if audio else np.array([], dtype=np.float32)
    sf.write(str(arquivo), audio, 24000)


async def gerar_episodio(episodio: dict, mapa_vozes: dict, pasta: Path, provedor: str):
    """Gera um MP3 por episodio, preservando disfluencias."""
    print(f"  Episodio {episodio['numero']}: {episodio['titulo']}")

    with tempfile.TemporaryDirectory() as tmp:
        ptmp = Path(tmp)
        audios = []

        for seg in episodio["segmentos"]:
            for fala in seg["falas"]:
                speaker = fala["speaker_id"]
                texto = fala["texto"]
                voz = mapa_vozes.get(speaker, list(mapa_vozes.values())[0])

                # Disfluencias sao intencionais - manter como estao
                arq = ptmp / f"fala_{len(audios):04d}.mp3"

                if provedor == "edge-tts":
                    await gerar_com_edge_tts(texto, voz, arq)
                elif provedor == "kokoro":
                    # Kokoro e sincrono, mas podemos rodar em executor
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(None, gerar_com_kokoro, texto, voz, arq)

                audios.append(arq)

        # Concatena
        saida = pasta / f"episodio_{episodio['numero']:02d}.mp3"
        lista = ptmp / "lista.txt"
        with open(lista, "w") as f:
            for a in audios:
                f.write(f"file '{a.resolve()}'\n")

        subprocess.run([
            FFMPEG, "-y", "-f", "concat", "-safe", "0",
            "-i", str(lista),
            "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
            str(saida)
        ], capture_output=True)

        print(f"    OK: {saida.name}")
        return saida


async def main():
    if len(sys.argv) < 2:
        print("Uso: python gerar_audio_do_json.py <caminho_do_json> [--tts provedor]")
        sys.exit(1)

    caminho_json = sys.argv[1]
    provedor = "edge-tts"
    if "--tts" in sys.argv:
        idx = sys.argv.index("--tts")
        if idx + 1 < len(sys.argv):
            provedor = sys.argv[idx + 1]

    if not os.path.exists(caminho_json):
        print(f"Erro: arquivo nao encontrado: {caminho_json}")
        sys.exit(1)

    roteiro = carregar_roteiro(caminho_json)
    mapa_vozes = mapear_vozes(roteiro, provedor)

    print(f"Provedor TTS: {provedor}")
    print(f"Vozes mapeadas: {mapa_vozes}")
    print(f"Total de episodios: {len(roteiro['episodios'])}")

    pasta_base = Path(caminho_json).parent / "audio_gerado"
    pasta_base.mkdir(exist_ok=True)
    pasta_episodios = pasta_base / "episodios_individuais"
    pasta_episodios.mkdir(exist_ok=True)

    arquivos_gerados = []
    for ep in roteiro["episodios"]:
        arq = await gerar_episodio(ep, mapa_vozes, pasta_episodios, provedor)
        if arq:
            arquivos_gerados.append(arq)

    # Podcast completo
    if arquivos_gerados:
        print("\nConcatenando podcast completo...")
        completo = pasta_base / "PODCAST_COMPLETO.mp3"
        with tempfile.TemporaryDirectory() as tmp:
            ptmp = Path(tmp)
            wavs = []
            for i, arq in enumerate(arquivos_gerados):
                wav = ptmp / f"w{i:04d}.wav"
                subprocess.run([FFMPEG, "-y", "-i", str(arq), "-ar", "24000", "-ac", "1", str(wav)], capture_output=True)
                if wav.exists():
                    wavs.append(wav)

            lista = ptmp / "final.txt"
            with open(lista, "w") as f:
                for w in wavs:
                    f.write(f"file '{w.resolve()}'\n")
            subprocess.run([
                FFMPEG, "-y", "-f", "concat", "-safe", "0",
                "-i", str(lista),
                "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
                str(completo)
            ], capture_output=True)

        print(f"Podcast completo: {completo}")
        tamanho_mb = os.path.getsize(completo) / (1024*1024)
        print(f"Tamanho: {tamanho_mb:.1f} MB")


if __name__ == "__main__":
    asyncio.run(main())
