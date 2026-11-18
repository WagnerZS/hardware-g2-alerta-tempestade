from threading import Lock

from .models import Leitura


class LeituraRepository:
    """Armazena a leitura mais recente de forma segura para as threads."""

    def __init__(self) -> None:
        self._ultima: Leitura | None = None
        self._lock = Lock()

    def salvar(self, leitura: Leitura) -> Leitura:
        with self._lock:
            self._ultima = leitura
        return leitura

    def obter_ultima(self) -> Leitura | None:
        with self._lock:
            return self._ultima
