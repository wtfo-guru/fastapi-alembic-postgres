# from unittest.mock import MagicMock
from os import environ
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.main import app

environ["APP_ENV"] = "test"


@pytest.fixture
def appl() -> Generator[FastAPI, None, None]:
    yield app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as testclient:
        # app.dependency_overrides[deps.get_reddit_client] = override_reddit_dependency
        yield testclient
        app.dependency_overrides = {}


@pytest.fixture
def settings() -> Generator[AppSettings, None, None]:
    yield get_app_settings()
