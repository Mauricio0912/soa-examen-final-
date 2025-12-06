import os
from dataclasses import dataclass


@dataclass
class Settings:
    host: str = '0.0.0.0'
    port: int = 8002
    db_path: str = ':memory:'
    service_namespace: str = 'matricula.soap.service'
    debug: bool = False


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings(
            host=os.getenv('SOAP_HOST', '0.0.0.0'),
            port=int(os.getenv('SOAP_PORT', '8002')),
            db_path=os.getenv('DB_PATH', ':memory:'),
            service_namespace=os.getenv('SERVICE_NS', 'matricula.soap.service'),
            debug=os.getenv('DEBUG', 'false').lower() == 'true'
        )
    return _settings
