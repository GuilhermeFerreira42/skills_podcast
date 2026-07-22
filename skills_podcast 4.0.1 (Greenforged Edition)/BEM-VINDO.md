# 🎙️ Bem-vindo ao Podcast System

Este é um sistema de orquestração multiagente para transformar qualquer conteúdo
em podcast de alta profundidade, com validação automática e produção de áudio.

---

## 🚀 Como usar (para iniciar imediatamente)

### 1. Abra seu chat com a IA

Cole o comando abaixo. Não precisa decorar nada.

```
Inteligência Artificial, aja como o Orquestrador Geral do sistema Podcast System.

Para começar, leia e internalize rigorosamente estes arquivos:

1. README.md — para entender a arquitetura geral
2. orquestrador/BOOT_ORQUESTRADOR.md — suas instruções de inicialização
3. orquestrador/SKILL_ORQUESTRADOR.md — seu pseudocódigo operacional

Após ler, aguarde o corpus que vou enviar.

---

## 🎛️ Formatos disponíveis

Quando você enviar o corpus, a IA vai perguntar qual formato você quer:

| Formato | Descrição |
|---------|-----------|
| **Análise Detalhada** | Conversa animada que explica e conecta temas em profundidade |
| **Resumo** | Visão geral rápida das ideias principais |
| **Crítica** | Análise especializada com feedback construtivo |
| **Debate** | Perspectivas opostas em debate inteligente |

## 🎯 Foco personalizado

A IA também vai perguntar: "Em quais aspectos os apresentadores devem se concentrar?"
Você pode responder algo como "Foque nos estudos sobre plásticos e nas soluções práticas"
e o sistema vai priorizar exatamente esses pontos.
```

### 2. Envie o conteúdo bruto

Depois que a IA confirmar que leu, envie o arquivo de conteúdo. Pode ser:
- Um livro em Markdown ou TXT
- Transcrições de palestras
- Conjunto de artigos
- Qualquer material que você queira transformar em podcast

Digite algo como:

```
Aqui está o corpus. O arquivo se chama "meu_livro.md".
Produza o podcast completo seguindo o fluxo do Boot do Orquestrador.
```

### 3. A IA faz o resto

O sistema automaticamente:
1. Analisa o corpus e cria o plano de episódios
2. Invoca o Escritor para produzir cada episódio em segmentos
3. Invoca o Atomizador para extrair afirmações
4. Invoca o Validador Cego (MARCH) para checar contra as fontes
5. Se algo falhar, reescreve apenas o segmento problemático
6. Gera o JSON final padronizado
7. Consulta você sobre qual TTS usar (edge-tts, Kokoro, etc.)
8. Gera o MP3 final

---

## 📁 Estrutura da pasta

```
podcast_system/
├── BEM-VINDO.md              ← VOCÊ ESTÁ AQUI
├── README.md                 ← arquitetura detalhada
├── orquestrador/             ← agente que coordena tudo
│   ├── BOOT_ORQUESTRADOR.md  ← instruções de inicialização
│   └── SKILL_ORQUESTRADOR.md ← skill operacional
├── escritor/                 ← agente que escreve o conteúdo
│   ├── BOOT_ESCRITOR.md
│   └── SKILL_ESCRITOR_PROFUNDO.md
├── atomizador/               ← agente que extrai afirmações
│   ├── BOOT_ATOMIZADOR.md
│   └── SKILL_ATOMIZADOR.md
├── validador/                ← agente que valida (cego, MARCH)
│   ├── BOOT_VALIDADOR.md
│   └── SKILL_VALIDADOR_MARCH.md
├── produtor_audio/           ← agente que gera o MP3
│   ├── BOOT_PRODUTOR.md
│   ├── SKILL_PRODUCAO_AUDIO.md
│   └── scripts/
│       └── gerar_audio_do_json.py
├── formatos/
│   ├── FORMATO_ROTEIRO_PODCAST.json
│   └── TEMPLATE_ESTADO_DA_OBRA.md
├── esquema/
│   └── ESTRUTURA_DE_PROJETO.md
└── exemplos/
    └── FLUXO_COMPLETO.md
```

---

## 🔄 Se o processo for interrompido

O sistema salva o progresso em `estado_da_obra.md`.
Se a conexão cair, o limite de chamadas for atingido, ou você precisar parar,
basta reler o BOOT_ORQUESTRADOR.md que a IA continuará de onde parou.

---

## 🎛️ Escolhendo o TTS

Quando o roteiro estiver pronto, a IA vai perguntar qual TTS usar:

| Provedor | Custo | Qualidade | Requisitos |
|---|---|---|---|
| edge-tts (Microsoft) | Gratuito | Boa | Só internet |
| Kokoro-82M | Gratuito | Ótima | CPU, 4GB RAM |
| OpenAI TTS | ~$0.015/min | Excelente | API key |

Se não responder, o sistema usa edge-tts como padrão.

---

## ❓ Dúvidas comuns

**Preciso programar alguma coisa?**
Não. O sistema é todo baseado em instruções para a IA. Os scripts Python são
opcionais e usados apenas na produção de áudio.

**Quantos episódios o sistema consegue produzir?**
Quantos você quiser. O estado da obra garante que não haja perda de progresso,
mesmo em projetos com 30+ episódios.

**O que eu faço com o JSON final?**
O JSON pode ser lido por qualquer IA ou script. Use o produtor de áudio para
gerar o MP3, ou use o JSON como roteiro para gravação humana.

**Bem-vindo e boa produção! 🎧**
