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

# Passo 3 — Analise o corpus

Leia TODO o corpus fornecido. Identifique:
- Temas centrais
- Numero de capitulos ou secoes
- Estrutura narrativa
- Conceitos tecnicos, historias, protocolos
- Evidencias e seus niveis (humano, animal, observacional)

Produza um plano de serie com:
- Numero de episodios
- Titulos provisorios
- Ordem narrativa

---

# Passo 4 — Execute o loop de producao

Siga rigorosamente o pseudocodigo da SKILL_ORQUESTRADOR.md.

PARA CADA episodio no plano:
1. Invoque o Escritor com o corpus + genero + numero do episodio
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
