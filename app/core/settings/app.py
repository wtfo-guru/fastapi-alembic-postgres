import logging
import sys
from typing import Any, Dict, List, Tuple, Union

from loguru import logger
from pydantic import AnyHttpUrl, SecretStr, validator

from app.core.logging import InterceptHandler
from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI example application"
    version: str = "0.1.0-dev1"

    # database_url: PostgresDsn
    database_url: str
    first_superuser: str

    max_connection_count: int = 10
    min_connection_count: int = 10

    secret_key: SecretStr

    api_prefix: str = "/api/v1"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    backend_cores_origins: List[AnyHttpUrl] = []

    @validator("backend_cores_origins", pre=True)  # 3
    def assemble_cors_origins(
        cls,  # noqa: N805
        vv: Union[str, List[str]],
    ) -> Union[List[str], str]:
        if isinstance(vv, str) and not vv.startswith("["):
            return [ii.strip() for ii in vv.split(",")]
        elif isinstance(vv, (list, str)):
            return vv
        raise ValueError(vv)

    jwt_token_prefix: str = "Token"

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])
