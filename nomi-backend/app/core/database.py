"""Database configuration and session management for SQLAlchemy async."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.core.config import settings

# Get database URL from settings
DATABASE_URL = settings.database_url

# Create async engine with connection pooling
# Development: echo=True logs SQL queries for debugging
# Production: set echo=False for performance
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=5,  # Minimum number of connections in pool
    max_overflow=15,  # Maximum connections beyond pool_size (total max = 20)
    pool_pre_ping=True,  # Verify connections before using them
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (better for async)
)

# Declarative base for ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function for FastAPI endpoints.
    Yields an async database session and ensures cleanup.

    Usage in FastAPI endpoints:
        @app.get("/items")
        async def read_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
