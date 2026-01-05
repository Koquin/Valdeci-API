from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.compra import CompraModel
from app.config.database import get_database


class CompraRepository:
    
    @property
    def collection(self):
        return get_database().compras

    # find_by_id - Busca compra por ID
    async def find_by_id(self, compra_id: str) -> Optional[dict]:
        print(f"Using method find_by_id, in module compra_repository, with the variables: [compra_id: {compra_id}]")
        if not ObjectId.is_valid(compra_id):
            return None
        compra = await self.collection.find_one({"_id": ObjectId(compra_id)})
        if compra:
            compra["id"] = str(compra["_id"])
        return compra

    # create - Cria uma nova compra
    async def create(self, compra_data: dict) -> dict:
        print(f"Using method create, in module compra_repository, with the variables: [compra_data: {compra_data}]")
        result = await self.collection.insert_one(compra_data)
        compra_data["id"] = str(result.inserted_id)
        compra_data["_id"] = result.inserted_id
        return compra_data
