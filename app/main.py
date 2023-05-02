from fastapi import FastAPI

from app.core.config import get_app_settings
from app.routes.api import router as api_router

def create_application() -> FastAPI:
    """Create the application."""
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    return application


app = create_application()

app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
