from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.divida import DividaModel
from app.config.database import get_database


class DividaRepository:
    
    @property
    def collection(self):
        return get_database().dividas

    # find_all_open - Retorna todas as dividas em aberto
    async def find_all_open(self) -> List[dict]:
        print(f"Using method find_all_open, in module divida_repository, with the variables: []")
        dividas = []
        cursor = self.collection.find({"status": "aberta"})
        async for document in cursor:
            document["id"] = str(document["_id"])
            dividas.append(document)
        return dividas

    # find_by_id - Busca divida por ID
    async def find_by_id(self, divida_id: str) -> Optional[dict]:
        print(f"Using method find_by_id, in module divida_repository, with the variables: [divida_id: {divida_id}]")
        if not ObjectId.is_valid(divida_id):
            return None
        divida = await self.collection.find_one({"_id": ObjectId(divida_id)})
        if divida:
            divida["id"] = str(divida["_id"])
        return divida

    # search_by_cliente - Busca dividas por ID do cliente
    async def search_by_cliente(self, cliente_id: str) -> List[dict]:
        print(f"Using method search_by_cliente, in module divida_repository, with the variables: [cliente_id: {cliente_id}]")
        dividas = []
        cursor = self.collection.find({"id_cliente": cliente_id, "status": "aberta"})
        async for document in cursor:
            document["id"] = str(document["_id"])
            dividas.append(document)
        return dividas

    # create - Cria uma nova divida
    async def create(self, divida_data: dict) -> dict:
        divida_print = divida_data.copy()
        if 'assinatura_compra' in divida_print and divida_print['assinatura_compra']:
            divida_print['assinatura_compra'] = divida_print['assinatura_compra'][:10] + "..."
        print(f"Using method create, in module divida_repository, with the variables: [divida_data: {divida_print}]")
        result = await self.collection.insert_one(divida_data)
        divida_data["id"] = str(result.inserted_id)
        divida_data["_id"] = result.inserted_id
        return divida_data

    # update - Atualiza uma divida existente
    async def update(self, divida_id: str, divida_data: dict) -> Optional[dict]:
        print(f"Using method update, in module divida_repository, with the variables: [divida_id: {divida_id}, divida_data: {divida_data}]")
        if not ObjectId.is_valid(divida_id):
            return None
        result = await self.collection.update_one(
            {"_id": ObjectId(divida_id)},
            {"$set": divida_data}
        )
        if result.modified_count > 0:
            return await self.find_by_id(divida_id)
        return None
