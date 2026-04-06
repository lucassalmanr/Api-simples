from pydantic import BaseModel

class EmpreendimentoRequest(BaseModel):
    name: str
    description: str
    type: str
    stats: str
    area: int


class EmpreendimentoResponse(BaseModel):
    id:int
    message: str
    data: dict
