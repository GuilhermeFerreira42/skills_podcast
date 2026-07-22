# Adaptador de Dominio: CODIGO

**Material de Origem:** Repositorio, docs API, testes existentes, linters
**Verificador:** Compilador + linter + testes unitarios + revisao de diff

## Exemplo de UATs

1. "Criar funcao de autenticacao JWT"
2. "Escrever testes para a rota /login"
3. "Refatorar modulo de banco de dados"

## Exemplo de Assercoes

- "A funcao `gerar_token()` usa a biblioteca `PyJWT`"
- "A rota `/login` retorna 401 para credenciais invalidas"
- "O modulo `db.py` nao importa bibliotecas nao utilizadas"

## Verificador

O Checker de codigo pode usar:
- Compilador (TypeScript, Python, etc.) para verificar sintaxe
- Linter (ESLint, Pylint) para verificar padroes
- Testes existentes para verificar regressao
- Revisao manual do diff
