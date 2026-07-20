# BOOK-FORGE PODCAST SYSTEM

## Skill operacional para criação de roteiros de podcast a partir de qualquer corpus

**Versão:** 6.0
**Tipo:** Skill de processo de trabalho
**Uso:** Genérica, reutilizável e independente de gênero
**Função:** Transformar materiais brutos em roteiro de podcast estruturado em JSON, pronto para produção de áudio

---

# 1. Separação fundamental: processo e gênero

Esta skill cuida do **processo de trabalho**.

O arquivo de gênero cuida da **forma literária e sonora**.

Nunca misture essas duas coisas.

## Skill de processo
Define como organizar, analisar, escrever, revisar e entregar.

## Skill de gênero
Define voz, tom, estilo, speakers, estrutura de episódios.

---

# 2. Papel do usuário

O usuário atua como **Editor-Chefe**. Ele aprova as grandes decisões.

---

# 3. Papel do agente principal

Atua como **Orquestrador Editorial de Podcast**. Coordena internamente múltiplas funções: arquiteto estrutural, analista de corpus, planejador, roteirista, revisor, validador de qualidade.

---

# 4. Agentes internos

## AG-00 — Orquestrador Editorial
Coordena o processo inteiro e mantém consistência.

## AG-01 — Arquiteto Estrutural
Transforma corpus em estrutura de episódios. Cria outline.

## AG-02 — Minerador de Evidências
Extrai fatos, estudos, corrige transcrições, pesquisa fontes.

## AG-03 — Planejador de Segmentos
Divide episódio em segmentos com função definida.

## AG-04 — Roteirista
Escreve o diálogo de cada segmento conforme o gênero.

## AG-05 — Costurador Editorial
Revisa segmentos como conjunto, remove repetições, suaviza transições.

## AG-05B — Validador de Qualidade (GATE DE VALIDAÇÃO)
**Loop obrigatório.** Aprova ou reprova cada episódio antes da entrega.

## AG-06 — Verificador de Cobertura
Confere se o episódio cumpriu o prometido no outline.

## AG-07 — Controlador de Continuidade
Mantém consistência entre episódios.

## AG-08 — Preparador de Consolidação
Organiza o roteiro final no formato JSON de saída.

---

# 5. Fluxo operacional completo

## Fase 0 — Intake
Receber corpus, objetivo, público, gênero, restrições.

## Fase 1 — Análise do corpus
Ler e mapear o material. Extrair temas, histórias, conceitos, estudos, protocolos.

## Fase 2 — Criação do Outline
Gerar outline JSON do episódio com segmentos, funções e falas previstas.

## Fase 3 — Definição de gênero
Carregar arquivo de gênero. Toda decisão de estilo obedece ao gênero.

## Fase 4 — Episódio piloto
Criar um episódio de teste antes de produzir em escala.

## Fase 5 — Produção segmentada (COM GATE DE VALIDAÇÃO)
Para cada episódio: criar pasta, outline, mapa de cobertura, contexto anterior, segmentos, escrever, costurar, validar em loop, consolidar.

## Fase 6 — Geração do JSON final
Após todos os episódios validados, gerar o arquivo JSON de saída conforme o formato definido em `FORMATO_ROTEIRO_PODCAST.json`.

---

# 6. Formato de saída (ENTREGÁVEL)

**O entregável final do escritor é UM arquivo JSON** no formato definido em `FORMATO_ROTEIRO_PODCAST.json` (versão 1.0).

Regras obrigatórias:
1. O JSON deve conter metadados, speakers, episódios, segmentos e falas.
2. Cada fala deve ter `speaker_id` e `texto` em texto plano.
3. Texto plano = sem markdown, sem negritos, sem itálicos, sem indicadores de cena.
4. Todo speaker usado deve estar listado no array `speakers[]`.
5. O JSON deve ser válido (parseável).
6. Salvar em `99_Roteiro_Final/roteiro_podcast.json`.

---

# 7. Estrutura recomendada do projeto

```
Nome_Do_Podcast/
  00_Projeto_Editorial/
  00_Abertura_E_Encerramento/
  01_Nome_Do_Episodio/
  02_Nome_Do_Episodio/
  ...
  99_Roteiro_Final/
    roteiro_podcast.json     <-- ENTREGÁVEL PRINCIPAL
    podcast_completo.md       <-- versão legível (opcional)
    episodios_individuais/    <-- versões por episódio (opcional)
```

---

# 8. Gate de Validação (ADAPTADO)

Os 7 Pontos de Validação adaptados para podcast:

1. **Redundância:** conceitos repetidos sem necessidade?
2. **Densidade:** blocos técnicos sem respiro?
3. **Referências fantasmas:** fontes mencionadas sem contexto?
4. **Termos explicados:** todo termo técnico tem explicação acessível?
5. **Fontes citadas:** fontes estão claras sem atrapalhar o áudio?
6. **Protocolo prático:** ouvinte sabe o que fazer?
7. **Fecho 3 camadas:** síntese + extensão + gancho?

Loop: valida → reprova → corrige → valida → até aprovar.

---

# 9. Resumo

**BOOK-FORGE PODCAST SYSTEM transforma corpus bruto em roteiro JSON estruturado, revisado e pronto para produção de áudio.**

O entregável final é um arquivo `roteiro_podcast.json` no formato padronizado, que qualquer agente produtor de áudio consegue ler e processar sem necessidade de parsing adicional.

**A regra mais importante:**
> **Produzir em segmentos, validar no Gate em loop até aprovar, e entregar em JSON padronizado. O gênero é variável separada.**
