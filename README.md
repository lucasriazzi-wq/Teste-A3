# API de Biblioteca

API REST em **FastAPI** para gerenciar livros, usuários e empréstimos de uma biblioteca.
Projeto da **A3 de Sistemas Distribuídos** (UniBH).

O documento inicial do projeto (tema, escopo, arquitetura e endpoints) está em [`docs/documento-inicial.md`](docs/documento-inicial.md).

## Requisitos

- Python 3.10+

## Como executar

```bash
# 1. criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. subir a API
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

As tabelas são criadas automaticamente na primeira execução (arquivo `biblioteca.db`, SQLite).

### Usando PostgreSQL (opcional)

```bash
pip install psycopg2-binary
export DATABASE_URL="postgresql+psycopg2://usuario:senha@localhost:5432/biblioteca"
uvicorn app.main:app --reload
```

## Testes

```bash
pytest -v
```

## Estrutura

```
app/
├── main.py            # app FastAPI, handlers de erro (400/404/500)
├── database.py        # conexão com o banco
├── exceptions.py      # exceções de domínio
├── routes/            # camada HTTP
├── schemas/           # validação e contratos (Pydantic)
├── services/          # regras de negócio
├── repositories/      # acesso ao banco
└── models/            # tabelas (SQLAlchemy)
tests/                 # testes automatizados
docs/                  # documentação do projeto
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/livros` | Cadastrar livro |
| GET | `/livros?titulo=&autor=` | Listar / buscar por título ou autor |
| GET | `/livros/{id}` | Buscar livro |
| PUT | `/livros/{id}` | Atualizar livro |
| DELETE | `/livros/{id}` | Remover livro |
| POST | `/usuarios` | Cadastrar usuário |
| GET | `/usuarios`, `/usuarios/{id}` | Listar / buscar usuário |
| POST | `/emprestimos` | Registrar empréstimo |
| GET | `/emprestimos`, `/emprestimos/{id}` | Listar / buscar empréstimos |
| PUT | `/emprestimos/{id}/devolucao` | Registrar devolução |

## Exemplo rápido

```bash
curl -X POST http://127.0.0.1:8000/livros -H "Content-Type: application/json" \
  -d '{"titulo":"Dom Casmurro","autor":"Machado de Assis","isbn":"9788535914849","ano_publicacao":1899,"quantidade_total":2}'

curl "http://127.0.0.1:8000/livros?autor=machado"
```

## Códigos de status

`200` sucesso · `201` criado · `400` dados inválidos / regra de negócio · `404` não encontrado · `500` erro interno
