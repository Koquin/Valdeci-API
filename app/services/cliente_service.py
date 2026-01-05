from typing import List
from datetime import datetime
from app.repository.cliente_repository import ClienteRepository
from app.repository.divida_repository import DividaRepository
from app.repository.historico_repository import HistoricoRepository
from app.dtos.cliente_dto import ClienteCreateDTO, ClienteResponseDTO, ClienteUpdateDTO
from app.exceptions import BadRequestException, ConflictException


class ClienteService:
    
    def __init__(self):
        self.repository = ClienteRepository()
        self.divida_repository = DividaRepository()
        self.historico_repository = HistoricoRepository()

    # get_all_clientes - Retorna todos os clientes
    async def get_all_clientes(self) -> List[ClienteResponseDTO]:
        print(f"Using method get_all_clientes, in module cliente_service, with the variables: []")
        clientes = await self.repository.find_all()
        
        # Para cada cliente, calcular divida total (dividas - pagamentos)
        clientes_com_dividas = []
        for cliente in clientes:
            # Buscar todas as dívidas do cliente
            dividas = await self.divida_repository.search_by_cliente(cliente["id"])
            total_dividas = sum(divida["valor_total"] for divida in dividas)
            
            # Buscar todos os pagamentos do cliente no histórico
            historicos = await self.historico_repository.find_by_cliente(cliente["id"])
            total_pagamentos = sum(h["valor"] for h in historicos if h["tipo"] == "pagamento")
            
            # Calcular dívida total
            divida_total = total_dividas - total_pagamentos
            cliente["divida_total"] = max(0, divida_total)  # Não permitir valores negativos
            clientes_com_dividas.append(ClienteResponseDTO(**cliente))
        
        return clientes_com_dividas

    # search_clientes - Busca clientes por texto
    async def search_clientes(self, search_text: str) -> List[ClienteResponseDTO]:
        print(f"Using method search_clientes, in module cliente_service, with the variables: [search_text: {search_text}]")
        if not search_text or len(search_text.strip()) == 0:
            raise BadRequestException("Search text cannot be empty")
        clientes = await self.repository.search_by_text(search_text)
        
        # Para cada cliente, calcular divida total (dividas - pagamentos)
        clientes_com_dividas = []
        for cliente in clientes:
            # Buscar todas as dívidas do cliente
            dividas = await self.divida_repository.search_by_cliente(cliente["id"])
            total_dividas = sum(divida["valor_total"] for divida in dividas)
            
            # Buscar todos os pagamentos do cliente no histórico
            historicos = await self.historico_repository.find_by_cliente(cliente["id"])
            total_pagamentos = sum(h["valor"] for h in historicos if h["tipo"] == "pagamento")
            
            # Calcular dívida total
            divida_total = total_dividas - total_pagamentos
            cliente["divida_total"] = max(0, divida_total)  # Não permitir valores negativos
            clientes_com_dividas.append(ClienteResponseDTO(**cliente))
        
        return clientes_com_dividas

    # create_cliente - Cria um novo cliente
    async def create_cliente(self, cliente_dto: ClienteCreateDTO) -> ClienteResponseDTO:
        print(f"Using method create_cliente, in module cliente_service, with the variables: [cliente_dto: {cliente_dto.model_dump()}]")
        existing_cliente = await self.repository.find_by_cpf(cliente_dto.cpf)
        if existing_cliente:
            raise ConflictException("Cliente with this CPF already exists")
        cliente_data = cliente_dto.model_dump()
        cliente_data["created_at"] = datetime.utcnow()
        cliente = await self.repository.create(cliente_data)
        cliente["divida_total"] = 0.0
        return ClienteResponseDTO(**cliente)

    # update_cliente - Atualiza um cliente existente
    async def update_cliente(self, cliente_id: str, cliente_dto: ClienteUpdateDTO) -> ClienteResponseDTO:
        print(f"Using method update_cliente, in module cliente_service, with the variables: [cliente_id: {cliente_id}, cliente_dto: {cliente_dto.model_dump()}]")
        
        # Verifica se o cliente existe
        existing_cliente = await self.repository.find_by_id(cliente_id)
        if not existing_cliente:
            raise BadRequestException("Cliente not found")
        
        # Prepara os dados para atualização (apenas os campos fornecidos)
        update_data = cliente_dto.model_dump(exclude_unset=True)
        
        if not update_data:
            raise BadRequestException("No fields to update")
        
        # Se o CPF foi fornecido, verifica se já existe outro cliente com esse CPF
        if "cpf" in update_data:
            cpf_cliente = await self.repository.find_by_cpf(update_data["cpf"])
            if cpf_cliente and cpf_cliente["id"] != cliente_id:
                raise ConflictException("Another cliente with this CPF already exists")
        
        # Atualiza o cliente
        cliente = await self.repository.update(cliente_id, update_data)
        
        # Calcular dívida total (dividas - pagamentos)
        dividas = await self.divida_repository.search_by_cliente(cliente_id)
        total_dividas = sum(divida["valor_total"] for divida in dividas)
        
        historicos = await self.historico_repository.find_by_cliente(cliente_id)
        total_pagamentos = sum(h["valor"] for h in historicos if h["tipo"] == "pagamento")
        
        divida_total = total_dividas - total_pagamentos
        cliente["divida_total"] = max(0, divida_total)
        
        return ClienteResponseDTO(**cliente)

    # delete_cliente - Deleta um cliente
    async def delete_cliente(self, cliente_id: str) -> None:
        print(f"Using method delete_cliente, in module cliente_service, with the variables: [cliente_id: {cliente_id}]")
        
        # Verifica se o cliente existe
        existing_cliente = await self.repository.find_by_id(cliente_id)
        if not existing_cliente:
            raise BadRequestException("Cliente not found")
        
        # Verifica se o cliente tem dívidas pendentes
        dividas = await self.divida_repository.search_by_cliente(cliente_id)
        dividas_pendentes = [d for d in dividas if d["valor_total"] > d["valor_pago"]]
        
        if dividas_pendentes:
            raise BadRequestException("Cannot delete cliente with pending debts")
        
        # Deleta o cliente
        deleted = await self.repository.delete(cliente_id)
        if not deleted:
            raise BadRequestException("Failed to delete cliente")
