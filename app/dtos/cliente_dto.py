from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ClienteCreateDTO(BaseModel):
    nome: str
    cpf: str


class ClienteUpdateDTO(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None


class ClienteResponseDTO(BaseModel):
    id: str
    nome: str
    cpf: str
    created_at: datetime
    divida_total: Optional[float] = 0.0
