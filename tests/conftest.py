# from unittest.mock import MagicMock
from os import environ
from typing import AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

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


@pytest.fixture
async def initialized_app(appl: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        appl.state.pool = await FakeAsyncPool.create_pool(app.state.pool)
        yield appl


@pytest.fixture
async def aclient(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as the_client:
        yield the_client
