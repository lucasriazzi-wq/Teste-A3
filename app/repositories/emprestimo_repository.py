from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Emprestimo


class EmprestimoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(
        self,
        livro_id: int | None = None,
        usuario_id: int | None = None,
        apenas_ativos: bool = False,
    ) -> list[Emprestimo]:
        consulta = select(Emprestimo).order_by(Emprestimo.id)
        if livro_id:
            consulta = consulta.where(Emprestimo.livro_id == livro_id)
        if usuario_id:
            consulta = consulta.where(Emprestimo.usuario_id == usuario_id)
        if apenas_ativos:
            consulta = consulta.where(Emprestimo.data_devolucao.is_(None))
        return list(self.db.scalars(consulta))

    def buscar_por_id(self, emprestimo_id: int) -> Emprestimo | None:
        return self.db.get(Emprestimo, emprestimo_id)

    def salvar(self, emprestimo: Emprestimo) -> Emprestimo:
        self.db.add(emprestimo)
        self.db.commit()
        self.db.refresh(emprestimo)
        return emprestimo
