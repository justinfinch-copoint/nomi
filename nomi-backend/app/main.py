from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title="Nomi API", description="Personal Task Management & Inspiration Platform", version="0.1.0"
)

# Configure CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router with /api prefix
api_router = APIRouter(prefix="/api")


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@api_router.get("/health/db")
async def database_health_check(db: AsyncSession = Depends(get_db)):
    """Database health check endpoint - verifies database connectivity"""
    try:
        # Execute a simple query to test the connection
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "database_url": settings.database_url.split("@")[1] if "@" in settings.database_url else "configured",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }


@api_router.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Welcome to Nomi API", "version": "0.1.0"}


# Include API router
app.include_router(api_router)


@app.get("/")
async def app_root():
    """Application root endpoint"""
    return {"message": "Nomi API", "docs": "/docs", "api": "/api"}
