from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "arduino-monitor"
    host: str = "0.0.0.0"
    port: int = 5000
    serial_port: str = "/dev/ttyACM0"
    serial_baudrate: int = 9600
    serial_timeout: float = 1.0
    cors_origins: str = "http://localhost:5000,http://127.0.0.1:5000,http://10.1.25.130:5000,null"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
