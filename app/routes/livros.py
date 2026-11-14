from fastapi import APIRouter, Depends, Query, status

from app.routes.dependencias import get_livro_service
from app.schemas import ErroResposta, LivroCreate, LivroOut, LivroUpdate, MensagemResposta
from app.services.livro_service import LivroService

router = APIRouter(prefix="/livros", tags=["Livros"])

ERRO_404 = {404: {"model": ErroResposta, "description": "Livro não encontrado"}}
ERRO_400 = {400: {"model": ErroResposta, "description": "Dados inválidos ou regra de negócio violada"}}
ERRO_500 = {500: {"model": ErroResposta, "description": "Erro interno do servidor"}}


@router.post("", response_model=LivroOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastrar livro", responses={**ERRO_400, **ERRO_500})
def cadastrar_livro(dados: LivroCreate, service: LivroService = Depends(get_livro_service)):
    return service.cadastrar(dados)


@router.get("", response_model=list[LivroOut], summary="Listar e buscar livros",
            responses={**ERRO_500})
def listar_livros(
    titulo: str | None = Query(default=None, description="Busca parcial por título"),
    autor: str | None = Query(default=None, description="Busca parcial por autor"),
    service: LivroService = Depends(get_livro_service),
):
    return service.listar(titulo, autor)


@router.get("/{livro_id}", response_model=LivroOut, summary="Buscar livro por ID",
            responses={**ERRO_404, **ERRO_500})
def obter_livro(livro_id: int, service: LivroService = Depends(get_livro_service)):
    return service.obter(livro_id)


@router.put("/{livro_id}", response_model=LivroOut, summary="Atualizar informações do livro",
            responses={**ERRO_400, **ERRO_404, **ERRO_500})
def atualizar_livro(livro_id: int, dados: LivroUpdate,
                    service: LivroService = Depends(get_livro_service)):
    return service.atualizar(livro_id, dados)


@router.delete("/{livro_id}", response_model=MensagemResposta, summary="Remover livro",
               responses={**ERRO_400, **ERRO_404, **ERRO_500})
def remover_livro(livro_id: int, service: LivroService = Depends(get_livro_service)):
    service.remover(livro_id)
    return MensagemResposta(mensagem=f"Livro {livro_id} removido com sucesso.")
