import logging

from pydantic import AnyUrl

from fapp.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev FastAPI example application"

    logging_level: int = logging.DEBUG

    database_url: AnyUrl

    class Config(AppSettings.Config):
        env_file = ".env.dev"
