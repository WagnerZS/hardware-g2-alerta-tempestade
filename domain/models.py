from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Gravidade = Literal["NORMAL", "ALERTA"]


class LeituraEntrada(BaseModel):
    """Payload enviado pelo Arduino ou por um cliente da API."""

    model_config = ConfigDict(extra="forbid")

    temp: float = Field(..., description="Temperatura medida")
    umid: float = Field(..., description="Umidade medida")
    mag: float = Field(..., description="Magnitude/campo magnético medido")


class Leitura(BaseModel):
    """Leitura normalizada, incluindo a gravidade calculada pelo servidor."""

    model_config = ConfigDict(extra="forbid")

    temp: float
    umid: float
    mag: float
    gravidade: Gravidade
    recebido_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


def calcular_gravidade(leitura: LeituraEntrada) -> Gravidade:
    """Retorna ALERTA quando umidade e magnetismo atingem os limites definidos."""

    if leitura.umid >= 35.0 and leitura.mag >= 800:
        return "ALERTA"
    return "NORMAL"
