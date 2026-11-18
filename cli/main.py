import uvicorn

from api.settings import Settings


def main() -> None:
    settings = Settings()
    uvicorn.run("api.app:app", host=settings.host, port=settings.port, reload=False)


if __name__ == "__main__":
    main()
