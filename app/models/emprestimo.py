from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def agora() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    livro_id: Mapped[int] = mapped_column(ForeignKey("livros.id"))
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    data_emprestimo: Mapped[datetime] = mapped_column(DateTime, default=agora)
    data_devolucao: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
