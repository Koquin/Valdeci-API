from .produto_router import router as produto_router
from .cliente_router import router as cliente_router
from .compra_router import router as compra_router
from .divida_router import router as divida_router
from .historico_router import router as historico_router

__all__ = [
    "produto_router",
    "cliente_router",
    "compra_router",
    "divida_router",
    "historico_router"
]
