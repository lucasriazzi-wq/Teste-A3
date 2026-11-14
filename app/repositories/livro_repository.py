from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Emprestimo, Livro


class LivroRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, titulo: str | None = None, autor: str | None = None) -> list[Livro]:
        consulta = select(Livro).order_by(Livro.titulo)
        if titulo:
            consulta = consulta.where(Livro.titulo.ilike(f"%{titulo}%"))
        if autor:
            consulta = consulta.where(Livro.autor.ilike(f"%{autor}%"))
        return list(self.db.scalars(consulta))

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return self.db.get(Livro, livro_id)

    def buscar_por_isbn(self, isbn: str) -> Livro | None:
        return self.db.scalars(select(Livro).where(Livro.isbn == isbn)).first()

    def contar_emprestimos_ativos(self, livro_id: int) -> int:
        consulta = select(Emprestimo).where(
            Emprestimo.livro_id == livro_id, Emprestimo.data_devolucao.is_(None)
        )
        return len(list(self.db.scalars(consulta)))

    def salvar(self, livro: Livro) -> Livro:
        self.db.add(livro)
        self.db.commit()
        self.db.refresh(livro)
        return livro

    def remover(self, livro: Livro) -> None:
        self.db.delete(livro)
        self.db.commit()
