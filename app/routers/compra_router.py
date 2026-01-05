from fastapi import APIRouter, HTTPException, status
from app.services.compra_service import CompraService
from app.dtos.compra_dto import CompraCreateDTO, CompraResponseDTO
from app.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/compras", tags=["Compras"])
compra_service = CompraService()


# create_compra - Registra uma compra normal
@router.post("", response_model=CompraResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_compra(compra: CompraCreateDTO):
    print(f"Using method create_compra, in module compra_router, with the variables: [compra: {compra.model_dump()}]")
    try:
        return await compra_service.create_compra(compra)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get_compra - Retorna os detalhes de uma compra especifica
@router.get("/{id}", response_model=CompraResponseDTO, status_code=status.HTTP_200_OK)
async def get_compra(id: str):
    print(f"Using method get_compra, in module compra_router, with the variables: [id: {id}]")
    try:
        return await compra_service.get_compra_by_id(id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
