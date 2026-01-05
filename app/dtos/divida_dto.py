from datetime import datetime
from typing import List
from pydantic import BaseModel
from .compra_dto import ItemCompraDTO


class DividaCompraDTO(BaseModel):
    itens: List[ItemCompraDTO]
    valor_compra: float
    data_compra: datetime


class DividaCreateDTO(BaseModel):
    id_cliente: str
    compra: DividaCompraDTO
    assinatura: str


class DividaResponseDTO(BaseModel):
    id: str
    id_cliente: str
    id_compra: str
    valor_total: float
    valor_pago: float
    assinatura_compra: str
    status: str
    created_at: datetime
    updated_at: datetime


class DevedorResponseDTO(BaseModel):
    id: str
    nome_cliente: str
    cpf_cliente: str
    valor_total: float
    valor_pago: float
    valor_restante: float
    status: str
    created_at: datetime
