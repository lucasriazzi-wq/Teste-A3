from fastapi import APIRouter, Depends, Query, status

from app.routes.dependencias import get_emprestimo_service
from app.schemas import EmprestimoCreate, EmprestimoOut, ErroResposta
from app.services.emprestimo_service import EmprestimoService

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])

ERRO_400 = {400: {"model": ErroResposta, "description": "Regra de negócio violada"}}
ERRO_404 = {404: {"model": ErroResposta, "description": "Recurso não encontrado"}}


@router.post("", response_model=EmprestimoOut, status_code=status.HTTP_201_CREATED,
             summary="Registrar empréstimo", responses={**ERRO_400, **ERRO_404})
def registrar_emprestimo(dados: EmprestimoCreate,
                         service: EmprestimoService = Depends(get_emprestimo_service)):
    return service.registrar_emprestimo(dados)


@router.get("", response_model=list[EmprestimoOut], summary="Listar empréstimos")
def listar_emprestimos(
    livro_id: int | None = Query(default=None),
    usuario_id: int | None = Query(default=None),
    apenas_ativos: bool = Query(default=False, description="Somente não devolvidos"),
    service: EmprestimoService = Depends(get_emprestimo_service),
):
    return service.listar(livro_id, usuario_id, apenas_ativos)


@router.get("/{emprestimo_id}", response_model=EmprestimoOut, summary="Buscar empréstimo por ID",
            responses={**ERRO_404})
def obter_emprestimo(emprestimo_id: int,
                     service: EmprestimoService = Depends(get_emprestimo_service)):
    return service.obter(emprestimo_id)


@router.put("/{emprestimo_id}/devolucao", response_model=EmprestimoOut,
            summary="Registrar devolução", responses={**ERRO_400, **ERRO_404})
def registrar_devolucao(emprestimo_id: int,
                        service: EmprestimoService = Depends(get_emprestimo_service)):
    return service.registrar_devolucao(emprestimo_id)
