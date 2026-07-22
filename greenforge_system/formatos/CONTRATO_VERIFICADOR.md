# Contrato do Verificador (Interface Universal)

Qualquer verificador plugado DEVE seguir este contrato:

## Entrada

```json
{
  "assertions": [
    {"id": "ASS-001", "assertion": "Afirmacao a ser verificada"},
    {"id": "ASS-002", "assertion": "Outra afirmacao"}
  ],
  "material_origem": "Caminho ou conteudo do material de referencia"
}
```

## Saida

```json
{
  "uat_id": "UAT-001",
  "total_assertions": 10,
  "confirmados": 9,
  "contraditos": 0,
  "nao_encontrados": 1,
  "taxa_confirmados": 0.9,
  "resultados": [
    {"id": "ASS-001", "status": "CONFIRMADO", "evidencia": "Trecho do material que confirma"},
    {"id": "ASS-002", "status": "NAO_ENCONTRADO", "evidencia": null}
  ],
  "status_geral": "APROVADO | REPROVADO"
}
```

## Regras do Contrato

1. O Orquestrador NAO sabe o que esta sendo verificado. Ele so aplica as travas duras.
2. O Checker DEVE retornar todos os campos obrigatorios.
3. O status_geral DEVE ser APROVADO ou REPROVADO.
4. A taxa_confirmados DEVE ser um float entre 0 e 1.
