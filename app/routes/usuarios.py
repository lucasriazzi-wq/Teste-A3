from fastapi import APIRouter, Depends, status

from app.routes.dependencias import get_usuario_service
from app.schemas import ErroResposta, UsuarioCreate, UsuarioOut
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED,
             summary="Cadastrar usuário",
             responses={400: {"model": ErroResposta, "description": "Dados inválidos ou e-mail duplicado"}})
def cadastrar_usuario(dados: UsuarioCreate, service: UsuarioService = Depends(get_usuario_service)):
    return service.cadastrar(dados)


@router.get("", response_model=list[UsuarioOut], summary="Listar usuários")
def listar_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    return service.listar()


@router.get("/{usuario_id}", response_model=UsuarioOut, summary="Buscar usuário por ID",
            responses={404: {"model": ErroResposta, "description": "Usuário não encontrado"}})
def obter_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    return service.obter(usuario_id)
