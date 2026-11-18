from domain.models import LeituraEntrada, calcular_gravidade
from domain.repository import LeituraRepository
from domain.service import LeituraService


def test_alerta_quando_umidade_e_magnetismo_atingem_limites() -> None:
    leitura = LeituraEntrada(temp=25.0, umid=35.0, mag=800.0)
    assert calcular_gravidade(leitura) == "ALERTA"


def test_normal_quando_umidade_ou_magnetismo_ficam_abaixo() -> None:
    assert calcular_gravidade(LeituraEntrada(temp=25, umid=34.9, mag=900)) == "NORMAL"
    assert calcular_gravidade(LeituraEntrada(temp=25, umid=40, mag=799.9)) == "NORMAL"


def test_servico_salva_gravidade_na_leitura() -> None:
    service = LeituraService(LeituraRepository())
    resultado = service.processar(LeituraEntrada(temp=22, umid=40, mag=900))
    assert resultado.gravidade == "ALERTA"
    assert service.repository.obter_ultima() == resultado
