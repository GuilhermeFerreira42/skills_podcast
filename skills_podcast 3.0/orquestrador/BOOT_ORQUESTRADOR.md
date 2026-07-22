# BOOT DO ORQUESTRADOR GERAL

## Instrucoes de Inicializacao

---

# Passo 1 — Identifique o projeto

Leia a pasta fornecida pelo usuario.

Identifique:
- Corpus (arquivo de conteudo bruto, livro, transcricao, etc.)
- Genero (arquivo GENERO_*.md, se houver)
- Configuracoes adicionais (formato JSON, scripts, etc.)

Se nao houver arquivo de genero, use o genero padrao narrativo-educacional.

---

# Passo 2 — Carregue o estado anterior

Procure por `estado_da_obra.md` na pasta do projeto.

SE existir:
- Leia o estado
- Identifique o ultimo episodio concluido
- Continue de onde parou

SE nao existir:
- Crie o estado vazio
- Inicie do zero

---

# Passo 3 — Consulte o usuario sobre formato e foco

## 3.1 Selecione o formato

Pergunte ao usuario:

"Qual o formato desejado para o podcast?

1. Analise Detalhada (Deep Dive) — conversa animada, explica e conecta temas
2. Resumo (Brief) — visao geral rapida das ideias principais
3. Critica — analise especializada com feedback construtivo
4. Debate — perspectivas opostas em debate inteligente
5. Personalizado — voce descreve o formato que quer"

## 3.2 Capture o foco do usuario

Pergunte ao usuario:

"Em quais aspectos os apresentadores devem se concentrar neste episodio?
(Texto livre. Ex: 'Foque nos estudos sobre plasticos e na solucao pratica')"

Registre a resposta no campo `foco_do_usuario` do JSON final.

## 3.3 Carregue o genero

Conforme o formato, carregue o arquivo da pasta generos/:
- Detalhado -> generos/GENERO_DETALHADO.md
- Resumo -> generos/GENERO_RESUMO.md
- Critica -> generos/GENERO_CRITICA.md
- Debate -> generos/GENERO_DEBATE.md
- Personalizado -> crie um arquivo temporario com a descricao do usuario

## 3.4 Analise o corpus

Leia TODO o corpus fornecido. Identifique:
- Temas centrais
- Numero de capitulos ou secoes
- Estrutura narrativa
- Conceitos tecnicos, historias, protocolos
- Evidencias e seus niveis (humano, animal, observacional)

Produza um plano de serie com:
- Numero de episodios, Titulos provisorios, Ordem narrativa

---

# Passo 4 — Execute o loop de producao

Siga rigorosamente o pseudocodigo da SKILL_ORQUESTRADOR.md.

PARA CADA episodio no plano:
1. Invoque o Escritor com o corpus + genero + numero do episodio + foco_do_usuario
2. Apos o escritor terminar, invoque o Atomizador
3. Invoque o Validador (cego ao texto do escritor)
4. Se validado: marque como concluido e salve estado
5. Se reprovado: devolva ao escritor com as falhas especificas

---

# Passo 5 — Apos todos os episodios

1. Consolide o JSON final
2. Invoque o Produtor de Audio com o JSON + configuracao de TTS
3. Entregue ao usuario

---

# Lembrete

**O orquestrador nao escreve. O orquestrador coordena.**
Cada subagente recebe apenas o insumo necessario, nunca o projeto inteiro.
O estado da obra e o checkpoint unico. Escreva e leia sempre.
