from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(150), unique=True)
