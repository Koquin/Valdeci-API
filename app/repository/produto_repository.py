from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.produto import ProdutoModel
from app.config.database import get_database


class ProdutoRepository:
    
    @property
    def collection(self):
        return get_database().produtos

    # find_all - Retorna todos os produtos
    async def find_all(self) -> List[dict]:
        print(f"Using method find_all, in module produto_repository, with the variables: []")
        produtos = []
        cursor = self.collection.find()
        async for document in cursor:
            document["id"] = str(document["_id"])
            produtos.append(document)
        print(f"[RETURN] find_all returning: {produtos}")
        return produtos

    # find_by_id - Busca produto por ID
    async def find_by_id(self, produto_id: str) -> Optional[dict]:
        print(f"Using method find_by_id, in module produto_repository, with the variables: [produto_id: {produto_id}]")
        if not ObjectId.is_valid(produto_id):
            print(f"[RETURN] find_by_id returning: None (invalid ObjectId)")
            return None
        produto = await self.collection.find_one({"_id": ObjectId(produto_id)})
        if produto:
            produto["id"] = str(produto["_id"])
        print(f"[RETURN] find_by_id returning: {produto}")
        return produto

    # search_by_text - Busca produtos por nome ou codigo de barras
    async def search_by_text(self, search_text: str) -> List[dict]:
        print(f"Using method search_by_text, in module produto_repository, with the variables: [search_text: {search_text}]")
        produtos = []
        query = {
            "$or": [
                {"nome": {"$regex": search_text, "$options": "i"}},
                {"codigo_barras": {"$regex": search_text, "$options": "i"}}
            ]
        }
        cursor = self.collection.find(query)
        async for document in cursor:
            document["id"] = str(document["_id"])
            produtos.append(document)
        print(f"[RETURN] search_by_text returning: {len(produtos)} produtos")
        return produtos

    # find_by_codigo_barras - Busca produto por codigo de barras exato
    async def find_by_codigo_barras(self, codigo: str) -> Optional[dict]:
        print(f"Using method find_by_codigo_barras, in module produto_repository, with the variables: [codigo: {codigo}]")
        produto = await self.collection.find_one({"codigo_barras": codigo})
        if produto:
            produto["id"] = str(produto["_id"])
        print(f"[RETURN] find_by_codigo_barras returning: {produto}")
        return produto

    # create - Cria um novo produto
    async def create(self, produto_data: dict) -> dict:
        print(f"Using method create, in module produto_repository, with the variables: [produto_data: {produto_data}]")
        result = await self.collection.insert_one(produto_data)
        produto_data["id"] = str(result.inserted_id)
        produto_data["_id"] = result.inserted_id
        print(f"[RETURN] create returning: {produto_data}")
        return produto_data

    # update - Atualiza um produto existente
    async def update(self, produto_id: str, produto_data: dict) -> Optional[dict]:
        print(f"Using method update, in module produto_repository, with the variables: [produto_id: {produto_id}, produto_data: {produto_data}]")
        if not ObjectId.is_valid(produto_id):
            print(f"[RETURN] update returning: None (invalid ObjectId)")
            return None
        result = await self.collection.update_one(
            {"_id": ObjectId(produto_id)},
            {"$set": produto_data}
        )
        if result.modified_count > 0:
            updated_produto = await self.find_by_id(produto_id)
            print(f"[RETURN] update returning: {updated_produto}")
            return updated_produto
        print(f"[RETURN] update returning: None (modified_count = 0)")
        return None

    # delete - Deleta um produto
    async def delete(self, produto_id: str) -> bool:
        print(f"Using method delete, in module produto_repository, with the variables: [produto_id: {produto_id}]")
        if not ObjectId.is_valid(produto_id):
            print(f"[RETURN] delete returning: False (invalid ObjectId)")
            return False
        result = await self.collection.delete_one({"_id": ObjectId(produto_id)})
        deleted = result.deleted_count > 0
        print(f"[RETURN] delete returning: {deleted} (deleted_count: {result.deleted_count})")
        return deleted
