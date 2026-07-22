# SKILL DO ATOMIZADOR (PROPOSER)

**Versao:** 1.0
**Funcao:** Extrair afirmacoes factuais do texto do escritor e transforma-las em perguntas para o validador cego.
**NUNCA valida nada.** Apenas atomiza.

---

# PSEUDOCODIGO OPERACIONAL

```
FUNCAO atomizar_episodio(caminho_episodio):
    texto = LER(f"{caminho_episodio}/_episodio_completo.md")

    afirmacoes = []
    PARA CADA paragrafo EM texto:
        PARA CADA oracao EM paragrafo:
            SE oracao contem afirmacao factual:
                afirmacao = {
                    "id": UUID(),
                    "segmento": segmento_origem,
                    "afirmacao": oracao,
                    "speaker": speaker_origem
                }
                afirmacoes.ADICIONAR(afirmacao)

    // Gerar perguntas para o validador cego
    para_cada afirmacao:
        pergunta = CRIAR_PERGUNTA(afirmacao)
        // Exemplo: afirmacao "a agua poluida reduz testosterona"
        // Pergunta: "A agua poluida reduz testosterona? Responda com SIM/NAO/NAO_ENCONTRADO baseado APENAS no corpus."

    SALVAR(f"{caminho_episodio}/_afirmacoes_para_validar.json", afirmacoes)
    SALVAR(f"{caminho_episodio}/_perguntas_validador.json", para_cada)
```

---

# 1. O que e uma afirmacao factual?

Toda oracao que faz uma afirmacao sobre o mundo real, ciencia, estudos, dados, historias ou mecanismos.

## Priorizacao (FILTRO OBRIGATORIO)

Nem toda oracao precisa ser atomizada. Para evitar sobrecarregar o validador com centenas de perguntas,
o atomizador DEVE aplicar este filtro de prioridade:

### PRIORIDADE ALTA (sempre extrair)
- Afirmacoes com NUMEROS, ESTATISTICAS ou DADOS ("50% dos homens", "3 graus Celsius", "2 copos por dia")
- MECANISMOS BIOLOGICOS ou QUIMICOS ("a aromatase converte testosterona em estrogenio")
- CAUSALIDADES ("X leva a Y", "X causa Y", "X esta associado a Y")
- CITACOES DE ESTUDOS ou AUTORIDADES ("um estudo de 2017 mostrou", "o Dr. X descobriu")
- PROTOCOLOS ou DOSAGENS ("tome 200mg por dia", "filtre a agua")

### PRIORIDADE BAIXA (pode ignorar se a quantidade for grande)
- Opinioes ou interpretacoes ("eu acho que", "parece que", "talvez")
- Transicoes e ganchos ("no proximo episodio", "vamos falar sobre")
- Repeticoes do mesmo conceito (extrair apenas a primeira ocorrencia)
- Analogias e exemplos ilustrativos (a menos que contenham dados)

### Regra de ouro
Episodios longos (mais de 50 oracoes) devem gerar NO MAXIMO 30-40 afirmacoes.
Episodios curtos (menos de 30 oracoes) podem extrair todas as afirmacoes relevantes.
Isso evita que o validador receba 100+ perguntas para um unico episodio.

---

# 2. Regras

1. NUNCA modifique o texto original. Apenas extraia.
2. NUNCA julgue se a afirmacao e verdadeira. Isso e com o Validador.
3. Se a mesma afirmacao aparecer em varios segmentos, crie uma entrada para cada ocorrencia.
4. Preserve o segmento de origem para que o escritor possa reescrever cirurgicamente se necessario.
5. Transforme cada afirmacao em uma pergunta binaria (SIM/NAO/NAO_ENCONTRADO).

---

# 3. Formato de saida

```json
{
  "afirmacoes": [
    {
      "id": "AFC-001",
      "segmento": "03_conceito_central",
      "afirmacao": "O plastico libera bisfenol que imita estrogenio no corpo humano",
      "speaker": "Speaker A",
      "pergunta_para_validador": "O plastico libera bisfenol que imita estrogenio no corpo humano? Responda com SIM/NAO/NAO_ENCONTRADO baseado APENAS no corpus original."
    }
  ]
}
```
