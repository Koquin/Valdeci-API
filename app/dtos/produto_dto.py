from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProdutoCreateDTO(BaseModel):
    nome: str
    valor: float
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    preco_por_peso: bool = False


class ProdutoUpdateDTO(BaseModel):
    nome: str
    valor: float
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    preco_por_peso: bool = False


class ProdutoResponseDTO(BaseModel):
    id: str
    nome: str
    valor: float
    descricao: Optional[str] = None
    codigo_barras: Optional[str] = None
    preco_por_peso: bool
    created_at: datetime
    updated_at: datetime
