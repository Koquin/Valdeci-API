from typing import List
from fastapi import APIRouter, HTTPException, Query, status
from app.services.produto_service import ProdutoService
from app.dtos.produto_dto import ProdutoCreateDTO, ProdutoUpdateDTO, ProdutoResponseDTO
from app.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/produtos", tags=["Produtos"])
produto_service = ProdutoService()


# get_produtos - Retorna todos os produtos
@router.get("", response_model=List[ProdutoResponseDTO], status_code=status.HTTP_200_OK)
async def get_produtos():
    print(f"Using method get_produtos, in module produto_router, with the variables: []")
    try:
        return await produto_service.get_all_produtos()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# search_produtos - Busca produtos por nome ou codigo de barras
@router.get("/search", response_model=List[ProdutoResponseDTO], status_code=status.HTTP_200_OK)
async def search_produtos(q: str = Query(..., description="Search text")):
    print(f"Using method search_produtos, in module produto_router, with the variables: [q: {q}]")
    try:
        return await produto_service.search_produtos(q)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get_produto_by_codigo - Busca produto por codigo de barras
@router.get("/codigo/{codigo}", response_model=ProdutoResponseDTO, status_code=status.HTTP_200_OK)
async def get_produto_by_codigo(codigo: str):
    print(f"Using method get_produto_by_codigo, in module produto_router, with the variables: [codigo: {codigo}]")
    try:
        return await produto_service.get_produto_by_codigo(codigo)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# create_produto - Cria um novo produto
@router.post("", response_model=ProdutoResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_produto(produto: ProdutoCreateDTO):
    print(f"Using method create_produto, in module produto_router, with the variables: [produto: {produto.model_dump()}]")
    try:
        return await produto_service.create_produto(produto)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# update_produto - Atualiza um produto existente
@router.put("/{id}", response_model=ProdutoResponseDTO, status_code=status.HTTP_200_OK)
async def update_produto(id: str, produto: ProdutoUpdateDTO):
    print(f"Using method update_produto, in module produto_router, with the variables: [id: {id}, produto: {produto.model_dump()}]")
    try:
        return await produto_service.update_produto(id, produto)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# delete_produto - Deleta um produto
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_produto(id: str):
    print(f"Using method delete_produto, in module produto_router, with the variables: [id: {id}]")
    try:
        await produto_service.delete_produto(id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
