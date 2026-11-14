from pydantic import BaseModel, ConfigDict, Field


class LivroBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=200, examples=["Dom Casmurro"])
    autor: str = Field(min_length=1, max_length=150, examples=["Machado de Assis"])
    isbn: str = Field(min_length=10, max_length=20, examples=["9788535914849"])
    ano_publicacao: int | None = Field(default=None, ge=0, le=2100, examples=[1899])
    quantidade_total: int = Field(default=1, ge=1, examples=[3])


class LivroCreate(LivroBase):
    pass


class LivroUpdate(LivroBase):
    """PUT substitui todos os campos editáveis do livro."""


class LivroOut(LivroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quantidade_disponivel: int
