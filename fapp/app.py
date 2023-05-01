
from fastapi import FastAPI
from fapp.core.config import get_app_settings

def pre_create_app():
    """Called before app startup."""

def create_application():
    """Create the application."""
    settings = get_app_settings()

    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    return application

app = create_application()
