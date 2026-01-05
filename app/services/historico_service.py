from typing import List
from datetime import datetime
from app.repository.historico_repository import HistoricoRepository
from app.repository.divida_repository import DividaRepository
from app.repository.cliente_repository import ClienteRepository
from app.dtos.historico_dto import PagamentoCreateDTO, HistoricoResponseDTO
from app.exceptions import NotFoundException, BadRequestException


class HistoricoService:
    
    def __init__(self):
        self.repository = HistoricoRepository()
        self.divida_repository = DividaRepository()
        self.cliente_repository = ClienteRepository()

    # get_historico_by_divida - Retorna o historico de uma divida
    async def get_historico_by_divida(self, divida_id: str) -> List[HistoricoResponseDTO]:
        print(f"Using method get_historico_by_divida, in module historico_service, with the variables: [divida_id: {divida_id}]")
        divida = await self.divida_repository.find_by_id(divida_id)
        if not divida:
            raise NotFoundException("Divida not found")
        historicos = await self.repository.find_by_divida(divida_id)
        return [HistoricoResponseDTO(**historico) for historico in historicos]

    # get_historico_by_cliente - Retorna o historico de um cliente
    async def get_historico_by_cliente(self, cliente_id: str) -> List[HistoricoResponseDTO]:
        print(f"Using method get_historico_by_cliente, in module historico_service, with the variables: [cliente_id: {cliente_id}]")
        cliente = await self.cliente_repository.find_by_id(cliente_id)
        if not cliente:
            raise NotFoundException("Cliente not found")
        historicos = await self.repository.find_by_cliente(cliente_id)
        return [HistoricoResponseDTO(**historico) for historico in historicos]

    # create_pagamento - Registra um pagamento sem vincular a dívida específica
    async def create_pagamento(self, pagamento_dto: PagamentoCreateDTO) -> HistoricoResponseDTO:
        pagamento_dict = pagamento_dto.model_dump()
        if 'assinatura' in pagamento_dict and pagamento_dict['assinatura']:
            pagamento_dict['assinatura'] = pagamento_dict['assinatura'][:10] + "..."
        print(f"Using method create_pagamento, in module historico_service, with the variables: [pagamento_dto: {pagamento_dict}]")
        
        # Validar se o cliente existe
        cliente = await self.cliente_repository.find_by_id(pagamento_dto.id_cliente)
        if not cliente:
            raise NotFoundException("Cliente not found")
        
        # Validar valor
        if pagamento_dto.valor <= 0:
            raise BadRequestException("Payment value must be greater than zero")
        
        # Registrar o pagamento no histórico sem vincular a dívida específica
        historico_data = {
            "id_cliente": pagamento_dto.id_cliente,
            "tipo": "pagamento",
            "valor": pagamento_dto.valor,
            "assinatura": pagamento_dto.assinatura,
            "data": datetime.utcnow(),
            "created_at": datetime.utcnow()
        }
        historico = await self.repository.create(historico_data)
        
        return HistoricoResponseDTO(**historico)
