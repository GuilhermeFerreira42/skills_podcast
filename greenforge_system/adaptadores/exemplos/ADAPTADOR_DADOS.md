# Adaptador de Dominio: DADOS

**Material de Origem:** Schema, documentacao de dados, amostras, dicionario de variaveis
**Verificador:** Validacao de tipos + integridade referencial + testes estatisticos

## Exemplo de UATs

1. "Validar schema da tabela usuarios"
2. "Identificar valores nulos no dataset"
3. "Calcular correlacao entre idade e colesterol"
4. "Detectar outliers na distribuicao de renda"

## Exemplo de Assercoes

- "A coluna `email` e do tipo VARCHAR(255) e nao permite nulos"
- "A correlacao entre idade e colesterol e de 0.65 na amostra"
- "5% dos registros tem valores nulos na coluna `telefone`"
- "Nao ha outliers alem de 3 desvios padrao na distribuicao de renda"

## Verificador

O Checker de dados pode usar:
- Validacao de schema (tipos, nulos, chaves)
- Testes estatisticos (correlacao, distribuicao)
- Integridade referencial entre tabelas
