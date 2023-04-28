from functools import lru_cache
from typing import Dict, Type

from fapp.core.settings.app import AppSettings
from fapp.core.settings.base import AppEnvTypes, BaseAppSettings
from fapp.core.settings.development import DevAppSettings
from fapp.core.settings.production import ProdAppSettings
from fapp.core.settings.test import TestAppSettings

environments: Dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}


@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
