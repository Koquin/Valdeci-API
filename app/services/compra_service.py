from datetime import datetime
from app.repository.compra_repository import CompraRepository
from app.dtos.compra_dto import CompraCreateDTO, CompraResponseDTO
from app.exceptions import NotFoundException


class CompraService:
    
    def __init__(self):
        self.repository = CompraRepository()

    # get_compra_by_id - Retorna uma compra por ID
    async def get_compra_by_id(self, compra_id: str) -> CompraResponseDTO:
        print(f"Using method get_compra_by_id, in module compra_service, with the variables: [compra_id: {compra_id}]")
        compra = await self.repository.find_by_id(compra_id)
        if not compra:
            raise NotFoundException("Compra not found")
        return CompraResponseDTO(**compra)

    # create_compra - Cria uma nova compra
    async def create_compra(self, compra_dto: CompraCreateDTO) -> CompraResponseDTO:
        print(f"Using method create_compra, in module compra_service, with the variables: [compra_dto: {compra_dto.model_dump()}]")
        compra_data = compra_dto.model_dump()
        compra_data["created_at"] = datetime.utcnow()
        compra = await self.repository.create(compra_data)
        return CompraResponseDTO(**compra)
