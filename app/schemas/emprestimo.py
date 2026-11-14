from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmprestimoCreate(BaseModel):
    livro_id: int = Field(ge=1, examples=[1])
    usuario_id: int = Field(ge=1, examples=[1])


class EmprestimoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    livro_id: int
    usuario_id: int
    data_emprestimo: datetime
    data_devolucao: datetime | None
