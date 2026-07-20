#!/usr/bin/env python3
"""Gera audio do podcast a partir do roteiro MD usando edge-tts com multiplas vozes."""

import re
import os
import sys
import asyncio
import subprocess
import tempfile
from pathlib import Path

import edge_tts

# Mapeamento de speakers para vozes
VOZES = {
    "Speaker A": "pt-BR-AntonioNeural",
    "Speaker B": "pt-BR-FranciscaNeural",
}

FFMPEG = "/home/user/ffmpeg"
PASTA_SAIDA = Path("/home/user/podcast_audio")
PASTA_SAIDA.mkdir(exist_ok=True)


def extrair_falas(texto: str) -> list[dict]:
    """Extrai todas as falas de Speaker A/B do texto.
    
    Funciona encontrando todas as ocorrencias de **Speaker X:** e
    extraindo o texto ate a proxima ocorrencia ou fim do texto.
    """
    # Encontra todas as posicoes dos marcadores de speaker
    padrao_marcador = re.compile(r'\*\*(Speaker [AB]):\*\*')
    matches = list(padrao_marcador.finditer(texto))
    
    falas = []
    for i, match in enumerate(matches):
        speaker = match.group(1)
        inicio = match.end()
        # O texto vai ate o proximo marcador ou fim do arquivo
        if i + 1 < len(matches):
            fim = matches[i + 1].start()
        else:
            fim = len(texto)
        
        fala = texto[inicio:fim].strip()
        # Remove marcacoes de cena [TRILHA...], [SOBE...]
        fala = re.sub(r'\[.*?\]', '', fala)
        # Remove subtitulos markdown ## Linha
        fala = re.sub(r'^#+.*$', '', fala, flags=re.MULTILINE)
        # Remove linhas de citacao >
        fala = re.sub(r'^>.*$', '', fala, flags=re.MULTILINE)
        # Remove linhas de referencia (--- ou tracos)
        fala = re.sub(r'^[-]{3,}$', '', fala, flags=re.MULTILINE)
        # Remove formatacoes markdown
        fala = fala.replace('*', '').replace('_', '')
        # Remove linhas em branco excessivas
        fala = re.sub(r'\n{3,}', '\n\n', fala)
        fala = fala.strip()
        
        if fala:
            falas.append({"speaker": speaker, "texto": fala})
    
    return falas


def separar_episodios(md_path: str) -> list[list[dict]]:
    """Separa as falas por episodio."""
    with open(md_path, "r", encoding="utf-8") as f:
        texto = f.read()
    
    # Divide pelos marcadores de episodio
    partes = re.split(r'^# Episódio \d+', texto, flags=re.MULTILINE)
    
    episodios = []
    for parte in partes:
        if not parte.strip():
            continue
        # Pula se for so o cabecalho/referencias
        if parte.strip().startswith('---') or 'Referências' in parte[:200]:
            continue
        falas = extrair_falas(parte)
        if falas:
            episodios.append(falas)
    
    return episodios


async def gerar_fala_audio(speaker: str, texto: str, idx: int, pasta: Path) -> Path:
    """Gera arquivo MP3 para uma fala usando edge-tts."""
    voz = VOZES.get(speaker, "pt-BR-FranciscaNeural")
    arquivo = pasta / f"fala_{idx:04d}.mp3"
    communicate = edge_tts.Communicate(texto, voz)
    await communicate.save(str(arquivo))
    return arquivo


def concatenar_audios(arquivos: list[Path], saida: Path):
    """Concatena varios MP3 em um unico MP3 usando ffmpeg.
    
    Abordagem: converte todos para WAV, concatena WAVs, depois converte para MP3.
    """
    if not arquivos:
        print("  Nenhum audio para concatenar.")
        return
    
    pasta = saida.parent
    wav_dir = pasta / "_wavs"
    wav_dir.mkdir(exist_ok=True)
    
    # Converte cada MP3 para WAV (mesmo formato: 24000 Hz, mono)
    wavs = []
    for i, arq in enumerate(arquivos):
        if not arq.exists() or arq.stat().st_size < 100:
            print(f"  Aviso: arquivo {arq.name} muito pequeno ou inexistente, pulando")
            continue
        wav = wav_dir / f"{i:04d}.wav"
        r = subprocess.run([
            FFMPEG, "-y", "-i", str(arq),
            "-ar", "24000", "-ac", "1",
            str(wav)
        ], capture_output=True)
        if wav.exists() and wav.stat().st_size > 100:
            wavs.append(wav)
        else:
            print(f"  Aviso: falha ao converter {arq.name} para WAV, pulando")
    
    # Cria lista de WAVs para concatenacao
    lista_path = pasta / "_lista_wavs.txt"
    with open(lista_path, "w") as f:
        for w in wavs:
            f.write(f"file '{w.resolve()}'\n")
    
    # Concatena WAVs e converte para MP3
    cmd = [
        FFMPEG, "-y", "-f", "concat", "-safe", "0",
        "-i", str(lista_path),
        "-c:a", "libmp3lame", "-b:a", "48k", "-ar", "24000", "-ac", "1",
        str(saida)
    ]
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    
    # Limpeza (ignora arquivos que nao existem)
    lista_path.unlink(missing_ok=True)
    for w in wavs:
        try:
            w.unlink(missing_ok=True)
        except:
            pass
    try:
        wav_dir.rmdir()
    except:
        pass
    
    if resultado.returncode != 0:
        print(f"  Erro ffmpeg: {resultado.stderr}")


async def gerar_episodio(nome: str, falas: list[dict], pasta: Path):
    """Gera audio completo para um conjunto de falas."""
    print(f"Gerando: {nome} ({len(falas)} falas)...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        pasta_tmp = Path(tmp_dir)
        arquivos = []
        
        for i, fala in enumerate(falas):
            print(f"  {i+1}/{len(falas)}: {fala['speaker']} ({len(fala['texto'])} chars)")
            arq = await gerar_fala_audio(fala["speaker"], fala["texto"], i, pasta_tmp)
            arquivos.append(arq)
        
        # Sem pausas extras - os audios sao concatenados direto
        # (as pausas naturais da fala ja sao suficientes)
        arquivos_com_pausa = arquivos
        
        saida = pasta / f"{nome}.mp3"
        print(f"  Concatenando {len(arquivos_com_pausa)} segmentos...")
        concatenar_audios(arquivos_com_pausa, saida)
        
        tamanho = os.path.getsize(saida)
        print(f"  OK: {saida.name} ({tamanho/1024:.0f} KB)")


async def main():
    md_path = "/home/user/uploads/podcast_completo.md"
    
    if not os.path.exists(md_path):
        print(f"Arquivo nao encontrado: {md_path}")
        sys.exit(1)
    
    print("Analisando roteiro...")
    episodios = separar_episodios(md_path)
    print(f"Encontrados {len(episodios)} blocos com falas de speaker")
    
    for i, falas in enumerate(episodios):
        nome = f"Episodio_{i+1}"
        await gerar_episodio(nome, falas, PASTA_SAIDA)
    
    print(f"\nConcluido! {len(episodios)} episodios em: {PASTA_SAIDA}")


if __name__ == "__main__":
    asyncio.run(main())
