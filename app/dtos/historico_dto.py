from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PagamentoCreateDTO(BaseModel):
    id_cliente: str
    valor: float
    assinatura: str


class HistoricoResponseDTO(BaseModel):
    id: str
    id_divida: Optional[str] = None
    id_cliente: Optional[str] = None
    tipo: str
    valor: float
    assinatura: Optional[str] = None
    data: datetime
    created_at: datetime
