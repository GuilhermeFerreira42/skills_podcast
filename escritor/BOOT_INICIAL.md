# BOOT DE INICIALIZAÇÃO — AGENTE ESCRITOR DE PODCAST

## Instruções para o Orquestrador Editorial

---

# Passo 1 — Leia os arquivos de configuração

1. **Skill operacional:** `SKILL_BOOK_FORGE_PODCAST.md`
2. **Arquivo de gênero:** `GENERO_PODCAST_*.md` (se houver)
3. **Formato de saída:** `FORMATO_ROTEIRO_PODCAST.json` (na pasta formatos/)

---

# Passo 2 — Identifique o corpus

Leia todos os arquivos fornecidos como conteúdo-base. Analise temas, estrutura, evidências, histórias e protocolos.

---

# Passo 3 — Planeje a estrutura

Defina:
- Quantos episódios?
- Um episódio por capítulo ou divisão temática?
- Quantos speakers? (1 a 4)
- Qual a duração aproximada?

Confirme com o Editor-Chefe se necessário.

---

# Passo 4 — Crie a pasta do projeto

Seguindo a estrutura da skill operacional.

---

# Passo 5 — Crie outline, escreva, costure, valide

Para cada episódio:
1. Outline JSON
2. Mapa de cobertura
3. Contexto anterior
4. Escrever segmentos
5. Costura editorial
6. **Gate de Validação (loop até aprovar)**

---

# Passo 6 — Gere o entregável final

Após todos os episódios validados, gere o arquivo `99_Roteiro_Final/roteiro_podcast.json` no formato definido em `FORMATO_ROTEIRO_PODCAST.json`.

**Regras do JSON de saída:**
- Texto das falas em PLAIN TEXT (sem markdown, sem negrito, sem itálico)
- Cada fala com `speaker_id` e `texto`
- Speakers listados no array `speakers[]`
- JSON válido e parseável

---

# Passo 7 — Entregue

Informe ao Editor-Chefe que o roteiro está pronto em `99_Roteiro_Final/roteiro_podcast.json`.

---

# Lembrete crítico

**O entregável é o JSON.** O markdown é opcional. O produtor de áudio só precisa do JSON para funcionar.
