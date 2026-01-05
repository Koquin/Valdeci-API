from typing import List
from fastapi import APIRouter, HTTPException, status
from app.services.historico_service import HistoricoService
from app.dtos.historico_dto import PagamentoCreateDTO, HistoricoResponseDTO
from app.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/historico", tags=["Historico"])
historico_service = HistoricoService()


# get_historico - Retorna todo o historico de uma divida
@router.get("/divida/{id_divida}", response_model=List[HistoricoResponseDTO], status_code=status.HTTP_200_OK)
async def get_historico(id_divida: str):
    print(f"Using method get_historico, in module historico_router, with the variables: [id_divida: {id_divida}]")
    try:
        return await historico_service.get_historico_by_divida(id_divida)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# get_historico_by_cliente - Retorna todo o historico de um cliente
@router.get("/cliente/{id_cliente}", response_model=List[HistoricoResponseDTO], status_code=status.HTTP_200_OK)
async def get_historico_by_cliente(id_cliente: str):
    print(f"Using method get_historico_by_cliente, in module historico_router, with the variables: [id_cliente: {id_cliente}]")
    try:
        result = await historico_service.get_historico_by_cliente(id_cliente)
        result_print = []
        for h in result:
            h_dict = h.model_dump()
            if 'assinatura' in h_dict and h_dict['assinatura']:
                h_dict['assinatura'] = h_dict['assinatura'][:10] + "..."
            result_print.append(h_dict)
        print(f"[RETURN] get_historico_by_cliente returning: {result_print}")
        return result
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# create_pagamento - Registra um pagamento com assinatura
@router.post("/pagamento", response_model=HistoricoResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_pagamento(pagamento: PagamentoCreateDTO):
    pagamento_dict = pagamento.model_dump()
    if 'assinatura' in pagamento_dict and pagamento_dict['assinatura']:
        pagamento_dict['assinatura'] = pagamento_dict['assinatura'][:10] + "..."
    print(f"Using method create_pagamento, in module historico_router, with the variables: [pagamento: {pagamento_dict}]")
    try:
        return await historico_service.create_pagamento(pagamento)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
