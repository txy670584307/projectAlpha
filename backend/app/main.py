import logging
import os
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import tickets, tags


def setup_logging():
    log_dir = settings.LOG_DIR
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    root_logger.addHandler(console_handler)


setup_logging()

app = FastAPI(
    title="projectAlpha API",
    description="基于标签分类的 Ticket 管理工具 API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tickets.router, prefix="/api", tags=["tickets"])
app.include_router(tags.router, prefix="/api", tags=["tags"])


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy", "database": "connected"}


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to projectAlpha API",
        "docs": "/docs" if settings.DEBUG else "API documentation disabled in production",
        "redoc": "/redoc" if settings.DEBUG else None,
    }
