from typing import List
from datetime import datetime
from app.repository.produto_repository import ProdutoRepository
from app.dtos.produto_dto import ProdutoCreateDTO, ProdutoUpdateDTO, ProdutoResponseDTO
from app.exceptions import NotFoundException, BadRequestException


class ProdutoService:
    
    def __init__(self):
        self.repository = ProdutoRepository()

    # get_all_produtos - Retorna todos os produtos
    async def get_all_produtos(self) -> List[ProdutoResponseDTO]:
        print(f"Using method get_all_produtos, in module produto_service, with the variables: []")
        produtos = await self.repository.find_all()
        return [ProdutoResponseDTO(**produto) for produto in produtos]

    # search_produtos - Busca produtos por texto
    async def search_produtos(self, search_text: str) -> List[ProdutoResponseDTO]:
        print(f"Using method search_produtos, in module produto_service, with the variables: [search_text: {search_text}]")
        if not search_text or len(search_text.strip()) == 0:
            raise BadRequestException("Search text cannot be empty")
        produtos = await self.repository.search_by_text(search_text)
        return [ProdutoResponseDTO(**produto) for produto in produtos]

    # get_produto_by_codigo - Busca produto por codigo de barras
    async def get_produto_by_codigo(self, codigo: str) -> ProdutoResponseDTO:
        print(f"Using method get_produto_by_codigo, in module produto_service, with the variables: [codigo: {codigo}]")
        produto = await self.repository.find_by_codigo_barras(codigo)
        if not produto:
            raise NotFoundException("Produto not found")
        return ProdutoResponseDTO(**produto)

    # create_produto - Cria um novo produto
    async def create_produto(self, produto_dto: ProdutoCreateDTO) -> ProdutoResponseDTO:
        print(f"Using method create_produto, in module produto_service, with the variables: [produto_dto: {produto_dto.model_dump()}]")
        produto_data = produto_dto.model_dump()
        produto_data["created_at"] = datetime.utcnow()
        produto_data["updated_at"] = datetime.utcnow()
        produto = await self.repository.create(produto_data)
        return ProdutoResponseDTO(**produto)

    # update_produto - Atualiza um produto existente
    async def update_produto(self, produto_id: str, produto_dto: ProdutoUpdateDTO) -> ProdutoResponseDTO:
        print(f"Using method update_produto, in module produto_service, with the variables: [produto_id: {produto_id}, produto_dto: {produto_dto.model_dump()}]")
        existing_produto = await self.repository.find_by_id(produto_id)
        if not existing_produto:
            raise NotFoundException("Produto not found")
        produto_data = produto_dto.model_dump()
        produto_data["updated_at"] = datetime.utcnow()
        produto = await self.repository.update(produto_id, produto_data)
        return ProdutoResponseDTO(**produto)

    # delete_produto - Deleta um produto
    async def delete_produto(self, produto_id: str) -> None:
        print(f"Using method delete_produto, in module produto_service, with the variables: [produto_id: {produto_id}]")
        existing_produto = await self.repository.find_by_id(produto_id)
        if not existing_produto:
            raise NotFoundException("Produto not found")
        await self.repository.delete(produto_id)
