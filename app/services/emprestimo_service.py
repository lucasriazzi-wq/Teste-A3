from app.exceptions import NaoEncontradoError, RegraNegocioError
from app.models import Emprestimo
from app.models.emprestimo import agora
from app.repositories.emprestimo_repository import EmprestimoRepository
from app.repositories.livro_repository import LivroRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas import EmprestimoCreate


class EmprestimoService:
    def __init__(
        self,
        repo: EmprestimoRepository,
        livros: LivroRepository,
        usuarios: UsuarioRepository,
    ):
        self.repo = repo
        self.livros = livros
        self.usuarios = usuarios

    def listar(self, livro_id, usuario_id, apenas_ativos) -> list[Emprestimo]:
        return self.repo.listar(livro_id, usuario_id, apenas_ativos)

    def obter(self, emprestimo_id: int) -> Emprestimo:
        emprestimo = self.repo.buscar_por_id(emprestimo_id)
        if emprestimo is None:
            raise NaoEncontradoError(f"Empréstimo {emprestimo_id} não encontrado.")
        return emprestimo

    def registrar_emprestimo(self, dados: EmprestimoCreate) -> Emprestimo:
        livro = self.livros.buscar_por_id(dados.livro_id)
        if livro is None:
            raise NaoEncontradoError(f"Livro {dados.livro_id} não encontrado.")
        if self.usuarios.buscar_por_id(dados.usuario_id) is None:
            raise NaoEncontradoError(f"Usuário {dados.usuario_id} não encontrado.")
        if livro.quantidade_disponivel < 1:
            raise RegraNegocioError("Não há exemplares disponíveis deste livro.")

        livro.quantidade_disponivel -= 1
        self.livros.salvar(livro)
        return self.repo.salvar(Emprestimo(**dados.model_dump()))

    def registrar_devolucao(self, emprestimo_id: int) -> Emprestimo:
        emprestimo = self.obter(emprestimo_id)
        if emprestimo.data_devolucao is not None:
            raise RegraNegocioError("Este empréstimo já foi devolvido.")

        livro = self.livros.buscar_por_id(emprestimo.livro_id)
        livro.quantidade_disponivel += 1
        self.livros.salvar(livro)

        emprestimo.data_devolucao = agora()
        return self.repo.salvar(emprestimo)
