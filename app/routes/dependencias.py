"""Montagem das camadas via injeção de dependências."""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.emprestimo_repository import EmprestimoRepository
from app.repositories.livro_repository import LivroRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.emprestimo_service import EmprestimoService
from app.services.livro_service import LivroService
from app.services.usuario_service import UsuarioService


def get_livro_service(db: Session = Depends(get_db)) -> LivroService:
    return LivroService(LivroRepository(db))


def get_usuario_service(db: Session = Depends(get_db)) -> UsuarioService:
    return UsuarioService(UsuarioRepository(db))


def get_emprestimo_service(db: Session = Depends(get_db)) -> EmprestimoService:
    return EmprestimoService(EmprestimoRepository(db), LivroRepository(db), UsuarioRepository(db))
