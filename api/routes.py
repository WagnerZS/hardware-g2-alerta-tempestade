from fastapi import APIRouter, HTTPException, Request

from domain.models import Leitura, LeituraEntrada
from domain.service import LeituraService

router = APIRouter(prefix="/api/monitor", tags=["leituras"])


def _service(request: Request) -> LeituraService:
    return request.app.state.leitura_service


@router.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/leituras/ultima", response_model=Leitura)
def obter_ultima_leitura(request: Request) -> Leitura:
    leitura = _service(request).repository.obter_ultima()
    if leitura is None:
        raise HTTPException(status_code=404, detail="Nenhuma leitura recebida ainda")
    return leitura
