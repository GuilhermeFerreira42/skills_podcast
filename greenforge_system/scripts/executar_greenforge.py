#!/usr/bin/env python3
"""
Script de exemplo para execucao do Greenforge System.
Uso: python executar_greenforge.py <caminho_do_plano>

Este script e um esqueleto. A logica real de orquestracao
e feita pela IA seguindo as skills.
"""

import json
import sys
from pathlib import Path


def carregar_plano(caminho: str) -> dict:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if len(sys.argv) < 2:
        print("Uso: python executar_greenforge.py <caminho_do_plano>")
        sys.exit(1)

    caminho = sys.argv[1]
    if not Path(caminho).exists():
        print(f"Erro: arquivo nao encontrado: {caminho}")
        sys.exit(1)

    print("=== Greenforge System ===")
    print(f"Plano: {caminho}")
    print("A execucao real e feita pela IA seguindo as skills.")
    print("Este script e apenas um esqueleto de referencia.")
    print()
    print("Para usar, de o comando a IA:")
    print('  "Inteligencia Artificial, aja como o Orquestrador Mestre do Greenforge System."')
    print('  "Leia o BOOT_ORQUESTRADOR_GREENFORGE.md e a SKILL_ORQUESTRADOR_GREENFORGE.md."')


if __name__ == "__main__":
    main()
