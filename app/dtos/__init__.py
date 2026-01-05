from .produto_dto import ProdutoCreateDTO, ProdutoUpdateDTO, ProdutoResponseDTO
from .cliente_dto import ClienteCreateDTO, ClienteResponseDTO
from .compra_dto import CompraCreateDTO, CompraResponseDTO, ItemCompraDTO
from .divida_dto import DividaCreateDTO, DividaResponseDTO, DevedorResponseDTO, DividaCompraDTO
from .historico_dto import PagamentoCreateDTO, HistoricoResponseDTO

__all__ = [
    "ProdutoCreateDTO",
    "ProdutoUpdateDTO",
    "ProdutoResponseDTO",
    "ClienteCreateDTO",
    "ClienteResponseDTO",
    "CompraCreateDTO",
    "CompraResponseDTO",
    "ItemCompraDTO",
    "DividaCreateDTO",
    "DividaResponseDTO",
    "DevedorResponseDTO",
    "DividaCompraDTO",
    "PagamentoCreateDTO",
    "HistoricoResponseDTO"
]
