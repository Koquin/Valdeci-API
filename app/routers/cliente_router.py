from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.services.cliente_service import ClienteService
from app.dtos.cliente_dto import ClienteCreateDTO, ClienteResponseDTO, ClienteUpdateDTO
from app.exceptions import BadRequestException, ConflictException

router = APIRouter(prefix="/clientes", tags=["Clientes"])
cliente_service = ClienteService()


# get_clientes - Retorna todos os clientes
@router.get("", response_model=List[ClienteResponseDTO], status_code=status.HTTP_200_OK)
async def get_clientes():
    print(f"Using method get_clientes, in module cliente_router, with the variables: []")
    try:
        return await cliente_service.get_all_clientes()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# search_clientes - Busca clientes por nome ou CPF
@router.get("/search", response_model=List[ClienteResponseDTO], status_code=status.HTTP_200_OK)
async def search_clientes(q: str = Query(..., description="Search text")):
    print(f"Using method search_clientes, in module cliente_router, with the variables: [q: {q}]")
    try:
        return await cliente_service.search_clientes(q)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# create_cliente - Cria um novo cliente
@router.post("", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_cliente(cliente: ClienteCreateDTO):
    print(f"Using method create_cliente, in module cliente_router, with the variables: [cliente: {cliente.model_dump()}]")
    try:
        return await cliente_service.create_cliente(cliente)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# update_cliente - Atualiza um cliente existente
@router.put("/{cliente_id}", response_model=ClienteResponseDTO, status_code=status.HTTP_200_OK)
async def update_cliente(cliente_id: str, cliente: ClienteUpdateDTO):
    print(f"Using method update_cliente, in module cliente_router, with the variables: [cliente_id: {cliente_id}, cliente: {cliente.model_dump()}]")
    try:
        result = await cliente_service.update_cliente(cliente_id, cliente)
        print(f"Method update_cliente finished successfully")
        return result
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# delete_cliente - Deleta um cliente
@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(cliente_id: str):
    print(f"Using method delete_cliente, in module cliente_router, with the variables: [cliente_id: {cliente_id}]")
    try:
        await cliente_service.delete_cliente(cliente_id)
        print(f"Method delete_cliente finished successfully")
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
