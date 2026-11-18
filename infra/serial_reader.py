import json
import logging
import threading
import time
from collections.abc import Callable

import serial
from pydantic import ValidationError

from domain.models import LeituraEntrada

logger = logging.getLogger(__name__)


class ArduinoSerialReader:
    """Lê uma linha JSON por vez e responde ALERTA quando necessário."""

    def __init__(
        self,
        port: str,
        baudrate: int,
        timeout: float,
        on_reading: Callable[[LeituraEntrada], None],
    ) -> None:
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.on_reading = on_reading
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._connection: serial.Serial | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, name="arduino-serial", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._connection and self._connection.is_open:
            self._connection.close()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                self._connection = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout,
                )
                logger.info("Serial conectada em %s", self.port)
                self._read_loop()
            except (serial.SerialException, OSError) as exc:
                logger.warning("Serial indisponível (%s). Nova tentativa em 5s", exc)
                time.sleep(5)
            finally:
                if self._connection and self._connection.is_open:
                    self._connection.close()
                self._connection = None

    def _read_loop(self) -> None:
        assert self._connection is not None
        while not self._stop_event.is_set():
            raw = self._connection.readline()
            if not raw:
                continue
            try:
                entrada = LeituraEntrada.model_validate_json(raw.decode("utf-8").strip())
                self.on_reading(entrada)
                # O callback processa a leitura e grava a resposta calculada.
                # A regra de envio é mantida aqui para a resposta física ao Arduino.
                if entrada.umid >= 35.0 and entrada.mag >= 800:
                    self._connection.write(b"ALERTA\\n")
            except (UnicodeDecodeError, json.JSONDecodeError, ValidationError) as exc:
                logger.warning("Leitura serial inválida: %s", exc)
            except serial.SerialException:
                raise
