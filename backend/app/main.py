import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import tickets, tags


logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="projectAlpha API",
    description="基于标签分类的 Ticket 管理工具 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
    return {
        "status": "healthy",
        "database": "connected"
    }


@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to projectAlpha API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
