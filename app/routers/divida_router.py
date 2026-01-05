from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.services.divida_service import DividaService
from app.dtos.divida_dto import DividaCreateDTO, DividaResponseDTO, DevedorResponseDTO
from app.dtos.compra_dto import CompraDetalhadaResponseDTO
from app.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/dividas", tags=["Dividas"])
divida_service = DividaService()


# get_dividas - Lista todos os clientes que possuem dividas em aberto
@router.get("", response_model=List[DevedorResponseDTO], status_code=status.HTTP_200_OK)
async def get_dividas():
    print(f"Using method get_dividas, in module divida_router, with the variables: []")
    try:
        return await divida_service.get_all_devedores()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# search_dividas - Busca devedores pelo nome ou CPF
@router.get("/search", response_model=List[DevedorResponseDTO], status_code=status.HTTP_200_OK)
async def search_dividas(q: str = Query(..., description="Search text")):
    print(f"Using method search_dividas, in module divida_router, with the variables: [q: {q}]")
    try:
        return await divida_service.search_devedores(q)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get_compra_by_divida - Retorna a compra associada a uma divida com detalhes dos produtos
@router.get("/{id_divida}/compra", response_model=CompraDetalhadaResponseDTO, status_code=status.HTTP_200_OK)
async def get_compra_by_divida(id_divida: str):
    print(f"Using method get_compra_by_divida, in module divida_router, with the variables: [id_divida: {id_divida}]")
    try:
        return await divida_service.get_compra_by_divida_id(id_divida)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# create_divida - Registra uma compra fiada com cliente e assinatura
@router.post("", response_model=DividaResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_divida(divida: DividaCreateDTO):
    divida_dict = divida.model_dump()
    if 'assinatura' in divida_dict and divida_dict['assinatura']:
        divida_dict['assinatura'] = divida_dict['assinatura'][:10] + "..."
    print(f"Using method create_divida, in module divida_router, with the variables: [divida: {divida_dict}]")
    try:
        return await divida_service.create_divida(divida)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
