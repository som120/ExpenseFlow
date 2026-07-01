from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.bot.manager import telegram_bot_manager
from app.core.config import settings
from app.core.exceptions import add_exception_handlers
from app.core.logging import configure_logging
from app.routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    await telegram_bot_manager.configure_commands()
    yield
    await telegram_bot_manager.shutdown()


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_exception_handlers(application)
    application.include_router(api_router, prefix=settings.api_v1_str)
    return application


app = create_application()
