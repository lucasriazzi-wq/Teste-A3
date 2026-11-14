"""Configuração do banco de dados.

Por padrão usa SQLite (zero configuração). Para usar PostgreSQL, defina a
variável de ambiente DATABASE_URL, por exemplo:
    postgresql+psycopg2://usuario:senha@localhost:5432/biblioteca
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./biblioteca.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """Dependência do FastAPI: abre e fecha a sessão a cada requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
