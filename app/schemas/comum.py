from pydantic import BaseModel


class ErroResposta(BaseModel):
    erro: str
    detalhes: list | None = None


class MensagemResposta(BaseModel):
    mensagem: str
