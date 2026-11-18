from .models import Leitura, LeituraEntrada, calcular_gravidade
from .repository import LeituraRepository


class LeituraService:
    def __init__(self, repository: LeituraRepository) -> None:
        self.repository = repository

    def processar(self, entrada: LeituraEntrada) -> Leitura:
        leitura = Leitura(
            temp=entrada.temp,
            umid=entrada.umid,
            mag=entrada.mag,
            gravidade=calcular_gravidade(entrada),
        )
        return self.repository.salvar(leitura)
