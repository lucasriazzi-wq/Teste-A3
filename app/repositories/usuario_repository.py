from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self) -> list[Usuario]:
        return list(self.db.scalars(select(Usuario).order_by(Usuario.nome)))

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        return self.db.get(Usuario, usuario_id)

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.db.scalars(select(Usuario).where(Usuario.email == email)).first()

    def salvar(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
