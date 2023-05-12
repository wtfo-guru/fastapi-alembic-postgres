import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.core.settings.app import AppSettings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "rpath, key, valor",
    (
        ("/", "message", "Hello, World!"),
        ("/healthcheck", "healthcheck", "Everything OK!"),
    ),
)
async def test_exposed_routes(
    client: TestClient,
    settings: AppSettings,
    rpath: str,
    key: str,
    valor: str,
) -> None:
    # When
    response = client.get("{0}/".format(rpath))
    rdata = response.json()

    # Then
    assert response.status_code == status.HTTP_200_OK
    # print(rdata)  # noqa: WPS421
    assert key in rdata
    assert rdata.get(key, "") == valor
