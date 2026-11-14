import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models  # noqa: F401  (registra as tabelas no metadata)
from app.database import Base, engine
from app.exceptions import NaoEncontradoError, RegraNegocioError
from app.routes import emprestimos, livros, usuarios

logger = logging.getLogger("biblioteca")

DESCRICAO = """
API REST para gerenciamento de uma biblioteca.

* **Livros**: cadastrar, buscar por título ou autor, atualizar e remover
* **Usuários**: cadastro de leitores
* **Empréstimos**: registrar empréstimos e devoluções

Códigos de status utilizados: **200**, **201**, **400**, **404** e **500**.
"""

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)  # cria as tabelas se não existirem
    yield


app = FastAPI(
    title="API de Biblioteca",
    description=DESCRICAO,
    version="1.0.0",
    lifespan=lifespan,
)


# ---------- tratamento centralizado de erros ----------
@app.exception_handler(NaoEncontradoError)
async def nao_encontrado_handler(request: Request, exc: NaoEncontradoError):
    return JSONResponse(status_code=404, content={"erro": str(exc)})


@app.exception_handler(RegraNegocioError)
async def regra_negocio_handler(request: Request, exc: RegraNegocioError):
    return JSONResponse(status_code=400, content={"erro": str(exc)})


@app.exception_handler(RequestValidationError)
async def validacao_handler(request: Request, exc: RequestValidationError):
    # Por padrão o FastAPI devolve 422; aqui padronizamos para 400.
    return JSONResponse(
        status_code=400,
        content={"erro": "Dados inválidos.", "detalhes": jsonable_encoder(exc.errors())},
    )


@app.exception_handler(Exception)
async def erro_interno_handler(request: Request, exc: Exception):
    logger.exception("Erro inesperado em %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"erro": "Erro interno do servidor."})


# ---------- rotas ----------
app.include_router(livros.router)
app.include_router(usuarios.router)
app.include_router(emprestimos.router)


@app.get("/", tags=["Sistema"], summary="Status da API")
def raiz():
    return {"api": "Biblioteca", "status": "ok", "documentacao": "/docs"}
