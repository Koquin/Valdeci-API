from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.cliente import ClienteModel
from app.config.database import get_database


class ClienteRepository:
    
    @property
    def collection(self):
        return get_database().clientes

    # find_all - Retorna todos os clientes
    async def find_all(self) -> List[dict]:
        print(f"Using method find_all, in module cliente_repository, with the variables: []")
        clientes = []
        cursor = self.collection.find()
        async for document in cursor:
            document["id"] = str(document["_id"])
            clientes.append(document)
        return clientes

    # find_by_id - Busca cliente por ID
    async def find_by_id(self, cliente_id: str) -> Optional[dict]:
        print(f"Using method find_by_id, in module cliente_repository, with the variables: [cliente_id: {cliente_id}]")
        if not ObjectId.is_valid(cliente_id):
            return None
        cliente = await self.collection.find_one({"_id": ObjectId(cliente_id)})
        if cliente:
            cliente["id"] = str(cliente["_id"])
        return cliente

    # search_by_text - Busca clientes por nome ou CPF
    async def search_by_text(self, search_text: str) -> List[dict]:
        print(f"Using method search_by_text, in module cliente_repository, with the variables: [search_text: {search_text}]")
        clientes = []
        query = {
            "$or": [
                {"nome": {"$regex": search_text, "$options": "i"}},
                {"cpf": {"$regex": search_text, "$options": "i"}}
            ]
        }
        cursor = self.collection.find(query)
        async for document in cursor:
            document["id"] = str(document["_id"])
            clientes.append(document)
        return clientes

    # find_by_cpf - Busca cliente por CPF exato
    async def find_by_cpf(self, cpf: str) -> Optional[dict]:
        print(f"Using method find_by_cpf, in module cliente_repository, with the variables: [cpf: {cpf}]")
        cliente = await self.collection.find_one({"cpf": cpf})
        if cliente:
            cliente["id"] = str(cliente["_id"])
        return cliente

    # create - Cria um novo cliente
    async def create(self, cliente_data: dict) -> dict:
        print(f"Using method create, in module cliente_repository, with the variables: [cliente_data: {cliente_data}]")
        result = await self.collection.insert_one(cliente_data)
        cliente_data["id"] = str(result.inserted_id)
        cliente_data["_id"] = result.inserted_id
        return cliente_data

    # update - Atualiza um cliente existente
    async def update(self, cliente_id: str, update_data: dict) -> Optional[dict]:
        print(f"Using method update, in module cliente_repository, with the variables: [cliente_id: {cliente_id}, update_data: {update_data}]")
        if not ObjectId.is_valid(cliente_id):
            return None
        result = await self.collection.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$set": update_data}
        )
        if result.modified_count == 0 and result.matched_count == 0:
            return None
        return await self.find_by_id(cliente_id)

    # delete - Deleta um cliente
    async def delete(self, cliente_id: str) -> bool:
        print(f"Using method delete, in module cliente_repository, with the variables: [cliente_id: {cliente_id}]")
        if not ObjectId.is_valid(cliente_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(cliente_id)})
        return result.deleted_count > 0
