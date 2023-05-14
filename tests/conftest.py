# from unittest.mock import MagicMock
from os import environ
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.main import app

# async def override_reddit_dependency() -> MagicMock:
#     mock = MagicMock()
#     reddit_stub = {
#         "recipes": [
#             "2085: the best chicken wings ever!! (https://i.redd.it/5iabdxh1jq381.jpg)",
#         ],
#         "easyrecipes": [
#             "74: Instagram accounts that post easy recipes? (https://www.reddit.com/r/easyrecipes/comments/rcluhd/instagram_accounts_that_post_easy_recipes/)",
#         ],
#         "TopSecretRecipes": [
#             "238: Halal guys red sauce - looking for recipe. Tried a recipe from a google search and it wasn’t nearly spicy enough. (https://i.redd.it/516yb30q9u381.jpg)",
#             "132: Benihana Diablo Sauce - THE AUTHENTIC RECIPE! (https://www.reddit.com/r/TopSecretRecipes/comments/rbcirf/benihana_diablo_sauce_the_authentic_recipe/)",
#         ],
#     }
#     mock.get_reddit_top.return_value = reddit_stub
#     return mock


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
async def aclient(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
