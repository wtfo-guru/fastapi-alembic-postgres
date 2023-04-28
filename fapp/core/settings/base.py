from enum import Enum
from os import getenv

from pydantic import BaseSettings


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


def _environ_to_type() -> AppEnvTypes:
    env = getenv("APP_ENV", "")
    if env.startswith("test"):
        return AppEnvTypes.test
    elif env.startswith("dev"):
        return AppEnvTypes.dev
    return AppEnvTypes.prod


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = _environ_to_type()

    class Config:
        env_file = ".env"
