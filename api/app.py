import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes import router
from api.settings import Settings
from domain.repository import LeituraRepository
from domain.service import LeituraService
from infra.serial_reader import ArduinoSerialReader

logger = logging.getLogger(__name__)
settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = LeituraRepository()
    service = LeituraService(repository)
    reader = ArduinoSerialReader(
        port=settings.serial_port,
        baudrate=settings.serial_baudrate,
        timeout=settings.serial_timeout,
        on_reading=service.processar,
    )
    app.state.leitura_service = service
    app.state.serial_reader = reader
    reader.start()
    logger.info("Servidor iniciado; aguardando leituras em %s", settings.serial_port)
    yield
    reader.stop()
    logger.info("Servidor finalizado")


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(router)

static_dir = Path(__file__).resolve().parent.parent / "web" / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")
