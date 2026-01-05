from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ItemCompraDTO(BaseModel):
    id_produto: str
    quantidade: float
    valor_total: float
    peso: Optional[float] = None


class CompraCreateDTO(BaseModel):
    itens: List[ItemCompraDTO]
    valor_compra: float
    data_compra: datetime


class CompraResponseDTO(BaseModel):
    id: str
    itens: List[ItemCompraDTO]
    valor_compra: float
    data_compra: datetime
    created_at: datetime


class ProdutoDetalheDTO(BaseModel):
    id: str
    nome: str
    valor: float
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    preco_por_peso: bool


class ItemCompraDetalhadoDTO(BaseModel):
    id_produto: str
    quantidade: float
    valor_total: float
    peso: Optional[float] = None
    produto: ProdutoDetalheDTO


class CompraDetalhadaResponseDTO(BaseModel):
    id: str
    itens: List[ItemCompraDetalhadoDTO]
    valor_compra: float
    data_compra: datetime
    created_at: datetime
