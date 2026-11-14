# A3 – Sistemas Distribuídos: API de Biblioteca

**Disciplina:** Sistemas Distribuídos
**Professor:** Fabrício Valadares
**Instituição:** UniBH – Campus Estoril
**Integrantes do grupo:** _(preencher com os nomes)_

---

## 1. Tema

**API de Biblioteca** – serviço REST para gerenciar o acervo e a circulação de livros de uma biblioteca.

## 2. Descrição

A API permite que um sistema cliente (site, aplicativo ou o projeto da UC de Usabilidade) cadastre livros, pesquise o acervo por título ou autor, atualize informações e controle empréstimos e devoluções, mantendo a quantidade de exemplares disponíveis sempre consistente.

## 3. Objetivos

- Disponibilizar operações de CRUD para livros e usuários.
- Permitir busca de livros por título ou autor.
- Registrar empréstimos e devoluções, aplicando regras de negócio.
- Documentar todos os endpoints com Swagger (OpenAPI).
- Retornar códigos de status HTTP adequados (200, 201, 400, 404, 500).

## 4. Funcionalidades (escopo)

| # | Funcionalidade | Descrição |
|---|---|---|
| 1 | Cadastrar livros | Registra título, autor, ISBN, ano e quantidade de exemplares |
| 2 | Buscar por título ou autor | Busca parcial, sem diferenciar maiúsculas/minúsculas |
| 3 | Atualizar informações | Altera os dados do livro |
| 4 | Remover livros | Só permitido se não houver empréstimo em aberto |
| 5 | Cadastrar usuários | Leitores que podem pegar livros emprestados |
| 6 | Registrar empréstimo | Reduz em 1 o número de exemplares disponíveis |
| 7 | Registrar devolução | Aumenta em 1 o número de exemplares disponíveis |

## 5. Tecnologias

| Item | Escolha |
|---|---|
| Linguagem | Python 3.10+ |
| Framework | FastAPI |
| Documentação | Swagger UI (`/docs`) e ReDoc (`/redoc`), gerados automaticamente |
| ORM | SQLAlchemy 2.0 |
| Banco de dados | SQLite (desenvolvimento) / PostgreSQL (opcional, via `DATABASE_URL`) |
| Testes | Pytest + TestClient |
| Versionamento | Git / GitHub |

## 6. Arquitetura em camadas

```
Cliente HTTP
    │
    ▼
┌─────────────┐  validação de entrada/saída (Pydantic), status HTTP
│  routes     │
└─────┬───────┘
      ▼
┌─────────────┐  regras de negócio (ex.: não emprestar sem exemplar)
│  services   │
└─────┬───────┘
      ▼
┌─────────────┐  consultas e persistência
│ repositories│
└─────┬───────┘
      ▼
┌─────────────┐
│ models / BD │
└─────────────┘
```

| Camada | Pasta | Responsabilidade |
|---|---|---|
| Rotas | `app/routes` | Recebe a requisição, chama o service, devolve a resposta |
| Schemas | `app/schemas` | Contratos de entrada e saída (Pydantic) |
| Serviços | `app/services` | Regras de negócio e lançamento de exceções de domínio |
| Repositórios | `app/repositories` | Acesso ao banco de dados |
| Modelos | `app/models` | Tabelas (SQLAlchemy) |

## 7. Modelo de dados

**livros**: `id`, `titulo`, `autor`, `isbn` (único), `ano_publicacao`, `quantidade_total`, `quantidade_disponivel`

**usuarios**: `id`, `nome`, `email` (único)

**emprestimos**: `id`, `livro_id` (FK), `usuario_id` (FK), `data_emprestimo`, `data_devolucao` (nula enquanto não devolvido)

Relacionamentos: um livro pode ter vários empréstimos; um usuário pode ter vários empréstimos.

## 8. Endpoints

| Método | Rota | Descrição | Status |
|---|---|---|---|
| POST | `/livros` | Cadastrar livro | 201, 400 |
| GET | `/livros?titulo=&autor=` | Listar/buscar livros | 200 |
| GET | `/livros/{id}` | Buscar livro por ID | 200, 404 |
| PUT | `/livros/{id}` | Atualizar livro | 200, 400, 404 |
| DELETE | `/livros/{id}` | Remover livro | 200, 400, 404 |
| POST | `/usuarios` | Cadastrar usuário | 201, 400 |
| GET | `/usuarios` | Listar usuários | 200 |
| GET | `/usuarios/{id}` | Buscar usuário | 200, 404 |
| POST | `/emprestimos` | Registrar empréstimo | 201, 400, 404 |
| GET | `/emprestimos` | Listar empréstimos (`livro_id`, `usuario_id`, `apenas_ativos`) | 200 |
| GET | `/emprestimos/{id}` | Buscar empréstimo | 200, 404 |
| PUT | `/emprestimos/{id}/devolucao` | Registrar devolução | 200, 400, 404 |

## 9. Códigos de status HTTP

| Código | Quando ocorre |
|---|---|
| 200 | Consulta, atualização, remoção ou devolução bem-sucedida |
| 201 | Recurso criado (livro, usuário, empréstimo) |
| 400 | Dados inválidos, ISBN/e-mail duplicado, livro sem exemplares, devolução repetida |
| 404 | Livro, usuário ou empréstimo inexistente |
| 500 | Erro inesperado no servidor (resposta padronizada, sem expor detalhes internos) |

Formato padrão de erro: `{"erro": "mensagem", "detalhes": [...]}`

## 10. Regras de negócio

1. O ISBN de cada livro é único.
2. O e-mail de cada usuário é único.
3. Só é possível emprestar um livro se houver exemplar disponível.
4. A devolução de um empréstimo só pode ser registrada uma vez.
5. Um livro com empréstimo em aberto não pode ser removido.
6. A quantidade total de um livro não pode ficar menor que o número de exemplares emprestados.

## 11. Divisão de tarefas sugerida

| Integrante | Responsabilidade |
|---|---|
| _(nome)_ | Livros (rotas, service, repository) |
| _(nome)_ | Empréstimos e devoluções |
| _(nome)_ | Usuários, banco de dados e testes |
| _(nome)_ | Documentação, README e integração com o projeto de Usabilidade |

## 12. Repositório

- Repositório no GitHub: _(inserir o link)_
- Acesso: público ou compartilhado com o usuário `fvaladares`.
