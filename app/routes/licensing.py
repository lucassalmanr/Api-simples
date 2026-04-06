from fastapi import APIRouter
from app.schemas.licensing import EmpreendimentoRequest, EmpreendimentoResponse
from app.services.licensing_service import LicensingService

router = APIRouter()
service = LicensingService()


@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/mostrarsucesso")
def mostrarsucesso():
    return {"API Funcionando"}
    


@router.post("/empreendimentos-teste", response_model=EmpreendimentoResponse)
def criar_empreendimento_teste(payload: EmpreendimentoRequest):
    return service.processar_empreendimento(payload)


@router.post("/empreendimentos-teste-2", response_model=EmpreendimentoResponse)
def criar_empreendimento_teste2(payload: EmpreendimentoRequest):
    return service.processar_empreendimento2(payload)



