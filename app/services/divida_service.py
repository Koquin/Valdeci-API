from typing import List
from datetime import datetime
from app.repository.divida_repository import DividaRepository
from app.repository.cliente_repository import ClienteRepository
from app.repository.compra_repository import CompraRepository
from app.repository.historico_repository import HistoricoRepository
from app.repository.produto_repository import ProdutoRepository
from app.dtos.divida_dto import DividaCreateDTO, DividaResponseDTO, DevedorResponseDTO
from app.dtos.compra_dto import CompraResponseDTO, CompraDetalhadaResponseDTO, ItemCompraDetalhadoDTO, ProdutoDetalheDTO
from app.exceptions import NotFoundException, BadRequestException


class DividaService:
    
    def __init__(self):
        self.repository = DividaRepository()
        self.cliente_repository = ClienteRepository()
        self.compra_repository = CompraRepository()
        self.historico_repository = HistoricoRepository()
        self.produto_repository = ProdutoRepository()

    # get_compra_by_divida_id - Retorna a compra associada a uma divida com detalhes dos produtos
    async def get_compra_by_divida_id(self, divida_id: str) -> CompraDetalhadaResponseDTO:
        print(f"Using method get_compra_by_divida_id, in module divida_service, with the variables: [divida_id: {divida_id}]")
        divida = await self.repository.find_by_id(divida_id)
        if not divida:
            raise NotFoundException("Divida not found")
        compra = await self.compra_repository.find_by_id(divida["id_compra"])
        if not compra:
            raise NotFoundException("Compra not found")
        
        # Buscar detalhes de cada produto
        itens_detalhados = []
        for item in compra["itens"]:
            produto = await self.produto_repository.find_by_id(item["id_produto"])
            if produto:
                item_detalhado = ItemCompraDetalhadoDTO(
                    id_produto=item["id_produto"],
                    quantidade=item["quantidade"],
                    valor_total=item["valor_total"],
                    peso=item.get("peso"),
                    produto=ProdutoDetalheDTO(
                        id=produto["id"],
                        nome=produto["nome"],
                        valor=produto["valor"],
                        descricao=produto.get("descricao"),
                        codigo_barras=produto.get("codigo_barras"),
                        preco_por_peso=produto["preco_por_peso"]
                    )
                )
                itens_detalhados.append(item_detalhado)
        
        return CompraDetalhadaResponseDTO(
            id=compra["id"],
            itens=itens_detalhados,
            valor_compra=compra["valor_compra"],
            data_compra=compra["data_compra"],
            created_at=compra["created_at"]
        )

    # get_all_devedores - Retorna todos os clientes com dividas em aberto
    async def get_all_devedores(self) -> List[DevedorResponseDTO]:
        print(f"Using method get_all_devedores, in module divida_service, with the variables: []")
        dividas = await self.repository.find_all_open()
        devedores = []
        for divida in dividas:
            cliente = await self.cliente_repository.find_by_id(divida["id_cliente"])
            if cliente:
                devedor = DevedorResponseDTO(
                    id=divida["id"],
                    nome_cliente=cliente["nome"],
                    cpf_cliente=cliente["cpf"],
                    valor_total=divida["valor_total"],
                    valor_pago=divida["valor_pago"],
                    valor_restante=divida["valor_total"] - divida["valor_pago"],
                    status=divida["status"],
                    created_at=divida["created_at"]
                )
                devedores.append(devedor)
        return devedores

    # search_devedores - Busca devedores por texto
    async def search_devedores(self, search_text: str) -> List[DevedorResponseDTO]:
        print(f"Using method search_devedores, in module divida_service, with the variables: [search_text: {search_text}]")
        if not search_text or len(search_text.strip()) == 0:
            raise BadRequestException("Search text cannot be empty")
        clientes = await self.cliente_repository.search_by_text(search_text)
        devedores = []
        for cliente in clientes:
            dividas = await self.repository.search_by_cliente(cliente["id"])
            for divida in dividas:
                devedor = DevedorResponseDTO(
                    id=divida["id"],
                    nome_cliente=cliente["nome"],
                    cpf_cliente=cliente["cpf"],
                    valor_total=divida["valor_total"],
                    valor_pago=divida["valor_pago"],
                    valor_restante=divida["valor_total"] - divida["valor_pago"],
                    status=divida["status"],
                    created_at=divida["created_at"]
                )
                devedores.append(devedor)
        return devedores

    # create_divida - Cria uma nova divida com compra e historico
    async def create_divida(self, divida_dto: DividaCreateDTO) -> DividaResponseDTO:
        divida_dict = divida_dto.model_dump()
        if 'assinatura' in divida_dict and divida_dict['assinatura']:
            divida_dict['assinatura'] = divida_dict['assinatura'][:10] + "..."
        print(f"Using method create_divida, in module divida_service, with the variables: [divida_dto: {divida_dict}]")
        cliente = await self.cliente_repository.find_by_id(divida_dto.id_cliente)
        if not cliente:
            raise NotFoundException("Cliente not found")
        compra_data = divida_dto.compra.model_dump()
        compra_data["created_at"] = datetime.utcnow()
        compra = await self.compra_repository.create(compra_data)
        divida_data = {
            "id_cliente": divida_dto.id_cliente,
            "id_compra": compra["id"],
            "valor_total": divida_dto.compra.valor_compra,
            "valor_pago": 0.0,
            "assinatura_compra": divida_dto.assinatura,
            "status": "aberta",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        divida = await self.repository.create(divida_data)
        historico_data = {
            "id_divida": divida["id"],
            "tipo": "compra_fiada",
            "valor": divida_dto.compra.valor_compra,
            "assinatura": divida_dto.assinatura,
            "data": divida_dto.compra.data_compra,
            "created_at": datetime.utcnow()
        }
        await self.historico_repository.create(historico_data)
        return DividaResponseDTO(**divida)
