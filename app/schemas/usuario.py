from pydantic import BaseModel, ConfigDict, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150, examples=["Maria Silva"])
    email: str = Field(
        min_length=5, max_length=150, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        examples=["maria@email.com"],
    )


class UsuarioOut(UsuarioCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
