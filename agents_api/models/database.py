"""
Database configuration and connection management
Using SQLAlchemy 2.0 with asyncpg for PostgreSQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
import os
from contextlib import asynccontextmanager

# AIDEV-NOTE: sqlalchemy-2.0-async; best practices from 2024 docs
# - Use postgresql+asyncpg:// dialect for async operations
# - AsyncSession with async context managers for proper cleanup
# - pool_size=20, max_overflow=0 for predictable connection count
# - pool_recycle=3600 to prevent timeout issues
# - pool_pre_ping=True to test connections before use
# - Avoid mixing sync and async code - use async throughout

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/julep"
)

# Create async engine with optimized pool settings
engine = create_async_engine(
    DATABASE_URL,
    # AIDEV-NOTE: connection-pool; tuned for high-concurrency API workload
    pool_size=20,  # Number of persistent connections
    max_overflow=0,  # No overflow connections - predictable resource usage
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Test connections before use
    echo=False,  # Set to True for SQL debugging
    # AIDEV-NOTE: performance-tip; statement cache improves prepared statement reuse
    connect_args={
        "statement_cache_size": 0,  # Disable if using pgbouncer
        "prepared_statement_cache_size": 0,
        "server_settings": {
            "application_name": "julep_v2",
            "jit": "off"  # Disable JIT for consistent query performance
        },
        # AIDEV-NOTE: pgvector-setup; register vector type for similarity search
        "init": register_vector_connection,
    }
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
    autoflush=False,  # Control flushing manually for better performance
)

# Base class for models
Base = declarative_base()

async def register_vector_connection(conn):
    """Register pgvector extension with asyncpg connection
    
    AIDEV-NOTE: vector-registration; required for pgvector 0.8.0+
    - Must be called for each new connection
    - Enables vector type handling in asyncpg
    """
    from pgvector.asyncpg import register_vector
    await register_vector(conn)

@asynccontextmanager
async def get_session() -> AsyncSession:
    """Async context manager for database sessions
    
    AIDEV-NOTE: session-pattern; ensures proper cleanup
    - Always use 'async with' to manage sessions
    - Automatic rollback on exceptions
    - Returns connection to pool after use
    
    Example:
        async with get_session() as session:
            result = await session.execute(select(Agent))
            agents = result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# AIDEV-TODO: migration-setup; implement Alembic async migrations
# AIDEV-TODO: connection-monitoring; add connection pool metrics
# AIDEV-TODO: read-replicas; implement read/write splitting for scale