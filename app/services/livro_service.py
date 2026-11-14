from app.exceptions import NaoEncontradoError, RegraNegocioError
from app.models import Livro
from app.repositories.livro_repository import LivroRepository
from app.schemas import LivroCreate, LivroUpdate


class LivroService:
    def __init__(self, repo: LivroRepository):
        self.repo = repo

    def listar(self, titulo: str | None, autor: str | None) -> list[Livro]:
        return self.repo.listar(titulo, autor)

    def obter(self, livro_id: int) -> Livro:
        livro = self.repo.buscar_por_id(livro_id)
        if livro is None:
            raise NaoEncontradoError(f"Livro {livro_id} não encontrado.")
        return livro

    def cadastrar(self, dados: LivroCreate) -> Livro:
        if self.repo.buscar_por_isbn(dados.isbn):
            raise RegraNegocioError(f"Já existe um livro com o ISBN {dados.isbn}.")
        livro = Livro(**dados.model_dump(), quantidade_disponivel=dados.quantidade_total)
        return self.repo.salvar(livro)

    def atualizar(self, livro_id: int, dados: LivroUpdate) -> Livro:
        livro = self.obter(livro_id)

        outro = self.repo.buscar_por_isbn(dados.isbn)
        if outro and outro.id != livro.id:
            raise RegraNegocioError(f"Já existe um livro com o ISBN {dados.isbn}.")

        emprestados = livro.quantidade_total - livro.quantidade_disponivel
        if dados.quantidade_total < emprestados:
            raise RegraNegocioError(
                f"Quantidade total não pode ser menor que os {emprestados} exemplares emprestados."
            )

        for campo, valor in dados.model_dump().items():
            setattr(livro, campo, valor)
        livro.quantidade_disponivel = dados.quantidade_total - emprestados
        return self.repo.salvar(livro)

    def remover(self, livro_id: int) -> None:
        livro = self.obter(livro_id)
        if self.repo.contar_emprestimos_ativos(livro_id) > 0:
            raise RegraNegocioError("Não é possível remover um livro com empréstimos em aberto.")
        self.repo.remover(livro)
