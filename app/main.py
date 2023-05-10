from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.api.api_v1.api import api_router
from app.core.config import get_app_settings

# Project Directories
ROOT = Path(__file__).resolve().parent.parent
BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


def create_application() -> FastAPI:
    """Create the application."""
    settings = get_app_settings()
    settings.configure_logging()
    return FastAPI(**settings.fastapi_kwargs)


app = create_application()
app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn  # noqa: WPS433

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")  # noqa: WPS432, S104
