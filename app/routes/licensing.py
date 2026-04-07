
from fastapi import APIRouter, HTTPException
import httpx
from app.clients.licensing_client import LicensingClient
from app.schemas.licensing import DevelopmentCreateRequest
from app.services.licensing_service import LicensingService
from app.schemas.licensing import EmpreendimentoRequest, EmpreendimentoResponse



router = APIRouter(prefix="/api/v1/licenciamento", tags=["Licenciamento"])
service = LicensingService()
service2 = LicensingClient()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/empreendimentos-teste", response_model=EmpreendimentoResponse)
def criar_empreendimento_teste(payload: EmpreendimentoRequest):
    return service.processar_empreendimento(payload)

# tirei o response_model e rodou, isso ta certo? 
@router.post("/criar-empreendimento")
async def criar_empreendimento(payload: DevelopmentCreateRequest):
    try:
        return await service2.create_development(
            payload.name,
            payload.description
        )

    # 🔴 Erro HTTP vindo do httpx (API externa respondeu erro)
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code

        if status_code == 422:
            raise HTTPException(
                status_code=422,
                detail="Erro de validação na API externa"
            )

        elif status_code == 500:
            raise HTTPException(
                status_code=500,
                detail="Erro interno na API externa"
            )
        
        elif status_code == 401:
            raise HTTPException(
                status_code=401,
                detail="Não autorizado: Verifique sua chave de API"
            )

        elif status_code == 201:
            raise HTTPException(
                status_code=201,
                detail="Empreendimento criado com sucesso"
            )
        
        elif status_code == 200:
            raise HTTPException(
                status_code=200,
                detail="Empreendimento atualizado com sucesso"
            )

        else:
            raise HTTPException(
                status_code=status_code,
                detail=f"Erro HTTP inesperado: {e.response.text}"
            )

    # 🌐 Erro de conexão (timeout, API fora do ar, etc.)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Erro de conexão com a API externa"
        )

    # 💣 Qualquer outro erro
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )        

