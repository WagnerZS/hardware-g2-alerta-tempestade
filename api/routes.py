from fastapi import APIRouter, HTTPException, Request

from domain.models import Leitura, LeituraEntrada
from domain.service import LeituraService

router = APIRouter(prefix="/api/v1", tags=["leituras"])


def _service(request: Request) -> LeituraService:
    return request.app.state.leitura_service


@router.get("/health", tags=["sistema"])
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/leituras", response_model=Leitura, status_code=201)
def criar_leitura(entrada: LeituraEntrada, request: Request) -> Leitura:
    """Recebe uma leitura, calcula gravidade e disponibiliza o resultado."""
    return _service(request).processar(entrada)


@router.get("/leituras/ultima", response_model=Leitura)
def obter_ultima_leitura(request: Request) -> Leitura:
    leitura = _service(request).repository.obter_ultima()
    if leitura is None:
        raise HTTPException(status_code=404, detail="Nenhuma leitura recebida ainda")
    return leitura
