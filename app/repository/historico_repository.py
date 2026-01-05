from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from app.models.historico import HistoricoModel
from app.config.database import get_database


class HistoricoRepository:
    
    @property
    def collection(self):
        return get_database().historico

    # find_by_divida - Retorna todo o historico de uma divida
    async def find_by_divida(self, divida_id: str) -> List[dict]:
        print(f"Using method find_by_divida, in module historico_repository, with the variables: [divida_id: {divida_id}]")
        historicos = []
        cursor = self.collection.find({"id_divida": divida_id}).sort("created_at", 1)
        async for document in cursor:
            document["id"] = str(document["_id"])
            historicos.append(document)
        return historicos

    # find_by_cliente - Retorna todo o historico de um cliente (dividas e pagamentos diretos)
    async def find_by_cliente(self, cliente_id: str) -> List[dict]:
        print(f"Using method find_by_cliente, in module historico_repository, with the variables: [cliente_id: {cliente_id}]")
        from app.repository.divida_repository import DividaRepository
        divida_repository = DividaRepository()
        
        # Buscar todas as dividas do cliente
        dividas = await divida_repository.search_by_cliente(cliente_id)
        divida_ids = [divida["id"] for divida in dividas]
        
        # Buscar historico vinculado a dividas do cliente OU vinculado diretamente ao cliente
        historicos = []
        query = {
            "$or": [
                {"id_divida": {"$in": divida_ids}},
                {"id_cliente": cliente_id}
            ]
        }
        cursor = self.collection.find(query).sort("created_at", 1)
        async for document in cursor:
            document["id"] = str(document["_id"])
            historicos.append(document)
        return historicos

    # create - Cria um novo registro de historico
    async def create(self, historico_data: dict) -> dict:
        historico_print = historico_data.copy()
        if 'assinatura' in historico_print and historico_print['assinatura']:
            historico_print['assinatura'] = historico_print['assinatura'][:10] + "..."
        print(f"Using method create, in module historico_repository, with the variables: [historico_data: {historico_print}]")
        result = await self.collection.insert_one(historico_data)
        historico_data["id"] = str(result.inserted_id)
        historico_data["_id"] = result.inserted_id
        return historico_data
