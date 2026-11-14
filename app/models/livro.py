from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), index=True)
    autor: Mapped[str] = mapped_column(String(150), index=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    ano_publicacao: Mapped[int | None] = mapped_column(Integer, nullable=True)
    quantidade_total: Mapped[int] = mapped_column(Integer, default=1)
    quantidade_disponivel: Mapped[int] = mapped_column(Integer, default=1)
