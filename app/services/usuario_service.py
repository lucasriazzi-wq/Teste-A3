from app.exceptions import NaoEncontradoError, RegraNegocioError
from app.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas import UsuarioCreate


class UsuarioService:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def listar(self) -> list[Usuario]:
        return self.repo.listar()

    def obter(self, usuario_id: int) -> Usuario:
        usuario = self.repo.buscar_por_id(usuario_id)
        if usuario is None:
            raise NaoEncontradoError(f"Usuário {usuario_id} não encontrado.")
        return usuario

    def cadastrar(self, dados: UsuarioCreate) -> Usuario:
        if self.repo.buscar_por_email(dados.email):
            raise RegraNegocioError(f"Já existe um usuário com o e-mail {dados.email}.")
        return self.repo.salvar(Usuario(**dados.model_dump()))
