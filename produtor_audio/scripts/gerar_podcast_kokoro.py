#!/usr/bin/env python3
"""Gera audio do podcast a partir do roteiro MD usando Kokoro TTS com vozes PT-BR."""

import re
import os
import sys
import subprocess
import tempfile
from pathlib import Path

import soundfile as sf
import numpy as np
from kokoro_onnx import Kokoro

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

# Vozes PT-BR disponiveis no Kokoro:
#   pf_dora  -> feminina
#   pm_alex  -> masculino
#   pm_santa -> masculino (alternativo)
VOZES = {
    "Speaker A": "pm_alex",   # Rodrigo (masculino)
    "Speaker B": "pf_dora",   # Ana (feminino)
}

LANG = "pt-br"
SPEED = 1.0  # 1.0 = velocidade normal

# Caminhos
WORKSPACE = Path(__file__).parent
MODEL_ONNX  = WORKSPACE / "kokoro-v1.0.onnx"
VOICES_BIN  = WORKSPACE / "voices-v1.0.bin"
FFMPEG      = "ffmpeg"  # usa ffmpeg do PATH do sistema
PASTA_SAIDA = WORKSPACE / "podcast_audio_kokoro"
MD_PATH     = WORKSPACE / "uploads" / "podcast_completo.md"

PASTA_SAIDA.mkdir(exist_ok=True)

# Limite de caracteres por chunk (Kokoro tem limite interno ~500 tokens)
MAX_CHARS_CHUNK = 400


# ---------------------------------------------------------------------------
# Parsing do roteiro
# ---------------------------------------------------------------------------

def extrair_abertura(md_path: Path) -> list[dict]:
    """Extrai as falas da secao ABERTURA PADRAO do roteiro."""
    texto = md_path.read_text(encoding="utf-8")

    # Encontra a secao ABERTURA PADRAO (entre # ABERTURA e o primeiro # Episodio)
    m_inicio = re.search(r'^# ABERTURA', texto, flags=re.MULTILINE | re.IGNORECASE)
    m_fim    = re.search(r'^# Epis.dio \d+', texto, flags=re.MULTILINE | re.IGNORECASE)

    if not m_inicio or not m_fim:
        return []

    trecho = texto[m_inicio.end():m_fim.start()]
    return extrair_falas(trecho)


def extrair_falas(texto: str) -> list[dict]:
    """Extrai todas as falas de Speaker A/B do texto."""
    padrao = re.compile(r'\*\*(Speaker [AB]):\*\*')
    matches = list(padrao.finditer(texto))

    falas = []
    for i, match in enumerate(matches):
        speaker = match.group(1)
        inicio = match.end()
        fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)

        fala = texto[inicio:fim].strip()
        fala = re.sub(r'\[.*?\]', '', fala)
        fala = re.sub(r'^#+.*$', '', fala, flags=re.MULTILINE)
        fala = re.sub(r'^>.*$', '', fala, flags=re.MULTILINE)
        fala = re.sub(r'^[-]{3,}$', '', fala, flags=re.MULTILINE)
        fala = fala.replace('*', '').replace('_', '')
        fala = re.sub(r'\n{3,}', '\n\n', fala)
        fala = fala.strip()

        if fala:
            falas.append({"speaker": speaker, "texto": fala})

    return falas


def separar_episodios(md_path: Path) -> list[list[dict]]:
    """Separa as falas por episodio numerado (ignora Abertura e cabecalho)."""
    texto = md_path.read_text(encoding="utf-8")

    # Divide SOMENTE nos marcadores de episodio numerado
    padrao_ep = re.compile(
        r'^# Epis.dio \d+',
        flags=re.MULTILINE | re.IGNORECASE
    )
    matches = list(padrao_ep.finditer(texto))

    episodios = []
    for i, match in enumerate(matches):
        inicio = match.end()
        fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
        parte = texto[inicio:fim]

        # Remove a secao de Referencias no final de cada episodio
        parte = re.sub(r'##\s*Refer[e\xe9]ncias.*', '', parte, flags=re.DOTALL | re.IGNORECASE)

        falas = extrair_falas(parte)
        if falas:
            episodios.append(falas)

    return episodios


def chunkar_texto(texto: str, max_chars: int = MAX_CHARS_CHUNK) -> list[str]:
    """Divide texto longo em chunks menores respeitando limites de frase."""
    if len(texto) <= max_chars:
        return [texto]

    chunks = []
    sentencas = re.split(r'(?<=[.!?])\s+', texto)
    atual = ""
    for s in sentencas:
        if len(atual) + len(s) + 1 <= max_chars:
            atual = (atual + " " + s).strip() if atual else s
        else:
            if atual:
                chunks.append(atual)
            if len(s) > max_chars:
                sub = re.split(r'(?<=,)\s+', s)
                sub_atual = ""
                for part in sub:
                    if len(sub_atual) + len(part) + 1 <= max_chars:
                        sub_atual = (sub_atual + " " + part).strip() if sub_atual else part
                    else:
                        if sub_atual:
                            chunks.append(sub_atual)
                        sub_atual = part
                atual = sub_atual if sub_atual else ""
            else:
                atual = s
    if atual:
        chunks.append(atual)

    return chunks


# ---------------------------------------------------------------------------
# Geracao de audio
# ---------------------------------------------------------------------------

def gerar_samples(kokoro: Kokoro, texto: str, voz: str) -> tuple:
    """Gera samples de audio para um texto, dividindo em chunks se necessario."""
    chunks = chunkar_texto(texto)
    todos_samples = []
    sample_rate = 24000

    for chunk in chunks:
        if not chunk.strip():
            continue
        samples, sr = kokoro.create(chunk, voice=voz, speed=SPEED, lang=LANG)
        sample_rate = sr
        todos_samples.append(samples)

        if len(chunks) > 1:
            silencio = np.zeros(int(sr * 0.2), dtype=samples.dtype)
            todos_samples.append(silencio)

    if not todos_samples:
        return np.zeros(1000, dtype=np.float32), sample_rate

    return np.concatenate(todos_samples), sample_rate


def gerar_fala_wav(kokoro: Kokoro, speaker: str, texto: str, idx: int, pasta: Path) -> Path:
    """Gera arquivo WAV para uma fala usando Kokoro."""
    voz = VOZES.get(speaker, "pf_dora")
    arquivo = pasta / f"fala_{idx:04d}.wav"

    samples, sr = gerar_samples(kokoro, texto, voz)
    sf.write(str(arquivo), samples, sr)
    return arquivo


def concatenar_wavs(arquivos: list, saida: Path):
    """Concatena varios WAVs em um unico MP3 usando ffmpeg."""
    if not arquivos:
        print("  Nenhum audio para concatenar.")
        return

    pasta = saida.parent
    lista_path = pasta / "_lista_wavs.txt"
    with open(lista_path, "w", encoding="utf-8") as f:
        for arq in arquivos:
            if arq.exists() and arq.stat().st_size > 100:
                f.write(f"file '{arq.resolve()}'\n")

    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(lista_path),
        "-c:a", "libmp3lame", "-b:a", "128k",
        str(saida)
    ]
    resultado = subprocess.run(cmd, capture_output=True, text=True)

    lista_path.unlink(missing_ok=True)

    if resultado.returncode != 0:
        print(f"  Erro ffmpeg: {resultado.stderr[-500:]}")
    else:
        tamanho = saida.stat().st_size
        print(f"  OK: {saida.name} ({tamanho/1024/1024:.1f} MB)")


# ---------------------------------------------------------------------------
# Orquestracao principal
# ---------------------------------------------------------------------------

def gerar_episodio(kokoro: Kokoro, nome: str, falas: list, pasta: Path):
    """Gera audio completo para um episodio."""
    print(f"\nGerando: {nome} ({len(falas)} falas)...")

    with tempfile.TemporaryDirectory() as tmp_dir:
        pasta_tmp = Path(tmp_dir)
        arquivos = []

        for i, fala in enumerate(falas):
            chars = len(fala['texto'])
            print(f"  {i+1:3d}/{len(falas)}: {fala['speaker']} ({chars} chars)", end="", flush=True)
            try:
                arq = gerar_fala_wav(kokoro, fala["speaker"], fala["texto"], i, pasta_tmp)
                arquivos.append(arq)
                print(" OK")
            except Exception as e:
                print(f" ERRO: {e}")

        saida = pasta / f"{nome}.mp3"
        print(f"  Concatenando {len(arquivos)} segmentos -> {saida.name}...")
        concatenar_wavs(arquivos, saida)


def main():
    if not MD_PATH.exists():
        print(f"Arquivo nao encontrado: {MD_PATH}")
        sys.exit(1)

    if not MODEL_ONNX.exists() or not VOICES_BIN.exists():
        print("Arquivos de modelo nao encontrados!")
        print(f"  Esperado: {MODEL_ONNX}")
        print(f"  Esperado: {VOICES_BIN}")
        sys.exit(1)

    print("Carregando modelo Kokoro...")
    kokoro = Kokoro(str(MODEL_ONNX), str(VOICES_BIN))
    print("Modelo carregado!")

    print("Analisando roteiro...")
    episodios = separar_episodios(MD_PATH)
    print(f"Encontrados {len(episodios)} episodios")

    # Permite gerar apenas episodios especificos via argumento: python script.py 1 2
    indices = None
    if len(sys.argv) > 1:
        indices = [int(x) for x in sys.argv[1:]]
        print(f"Gerando apenas episodios: {indices}")

    # Gera a abertura (a menos que o usuario tenha pedido episodios especificos)
    if not indices:
        falas_abertura = extrair_abertura(MD_PATH)
        if falas_abertura:
            gerar_episodio(kokoro, "Abertura", falas_abertura, PASTA_SAIDA)
        else:
            print("Abertura nao encontrada no roteiro.")

    for i, falas in enumerate(episodios, start=1):
        if indices and i not in indices:
            print(f"Pulando Episodio_{i}")
            continue
        gerar_episodio(kokoro, f"Episodio_{i}", falas, PASTA_SAIDA)

    print(f"\nConcluido! Arquivos em: {PASTA_SAIDA}")


if __name__ == "__main__":
    main()
