from typing import Dict

from fastapi import APIRouter, status

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def hello_world() -> Dict[str, str]:
    """
    The root route which returns a JSON response.
    The JSON response is delivered as:
    {
      'message': 'Hello, World!'
    }
    """
    return {"message": "Hello, World!"}


@router.get("/healthcheck", status_code=status.HTTP_200_OK)
def perform_healthcheck() -> Dict[str, str]:
    """
    Simple route for the GitHub Actions to healthcheck on.
    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check
    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.
    Additionally, it also returns a JSON response in the form of:
    {
      'healthcheck': 'Everything OK!'
    }
    """
    return {"healthcheck": "Everything OK!"}
