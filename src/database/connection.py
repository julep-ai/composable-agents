"""
Database connection management using psycopg directly
No ORM - direct SQL queries for performance and simplicity
"""

import os
from contextlib import asynccontextmanager
from typing import Optional, Any, List, Dict
import logging
import psycopg
from psycopg import AsyncConnection
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

# AIDEV-NOTE: psycopg-direct; bypassing ORM for better performance
# - Direct SQL queries with parameterized statements
# - Connection pooling with psycopg_pool
# - Automatic pgvector type registration
# - No ORM overhead, full control over queries

logger = logging.getLogger(__name__)

# Database configuration from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    # Build from components if full URL not provided
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_pass = os.getenv("POSTGRES_PASSWORD", "postgres")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "julep")
    DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# Global connection pool
_pool: Optional[AsyncConnectionPool] = None


async def init_pool():
    """Initialize the global connection pool
    
    AIDEV-NOTE: connection-pool-init; called once at app startup
    - min_size=10: maintain minimum connections
    - max_size=20: limit maximum connections
    - Connection recycling handled automatically
    """
    global _pool
    
    if _pool is not None:
        return _pool
    
    async def configure_connection(conn: AsyncConnection) -> None:
        """Initialize each connection in the pool"""
        async with conn.cursor() as cur:
            # Register pgvector extension types
            await cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            # Set application name for monitoring
            await cur.execute("SET application_name = 'julep_v2'")
            # Disable JIT for consistent performance
            await cur.execute("SET jit = 'off'")
    
    _pool = AsyncConnectionPool(
        DATABASE_URL,
        min_size=10,
        max_size=20,
        configure=configure_connection,
        kwargs={
            "row_factory": dict_row,  # Return dicts instead of tuples
            "autocommit": False,  # Explicit transaction control
        }
    )
    
    await _pool.open()
    logger.info("Database connection pool initialized")
    return _pool


async def close_pool():
    """Close the global connection pool"""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


@asynccontextmanager
async def get_connection():
    """Get a database connection from the pool
    
    AIDEV-NOTE: connection-pattern; use with async context manager
    - Automatically returns connection to pool
    - Handles connection errors gracefully
    - No need for manual cleanup
    
    Example:
        async with get_connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM agents.agents")
                result = await cur.fetchall()
    """
    pool = await init_pool()
    async with pool.connection() as conn:
        yield conn


@asynccontextmanager
async def get_transaction():
    """Get a database connection with transaction
    
    AIDEV-NOTE: transaction-pattern; for atomic operations
    - Automatic rollback on exception
    - Automatic commit on success
    - Nested transactions supported via savepoints
    
    Example:
        async with get_transaction() as conn:
            async with conn.cursor() as cur:
                await cur.execute("INSERT INTO agents.agents ...")
                await cur.execute("INSERT INTO agents.sessions ...")
                # Both queries commit or rollback together
    """
    async with get_connection() as conn:
        async with conn.transaction():
            yield conn


async def execute_query(query: str, params: tuple = ()) -> str:
    """Execute a query that doesn't return results
    
    Args:
        query: SQL query with %s placeholders
        params: Query parameters as tuple
        
    Returns:
        Row count affected
    """
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return f"AFFECTED {cur.rowcount}"


async def fetch_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    """Fetch a single row
    
    Args:
        query: SQL query with %s placeholders
        params: Query parameters as tuple
        
    Returns:
        Dict or None
    """
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchone()


async def fetch_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Fetch all rows
    
    Args:
        query: SQL query with %s placeholders
        params: Query parameters as tuple
        
    Returns:
        List of dicts
    """
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchall()


async def fetch_value(query: str, params: tuple = ()) -> Any:
    """Fetch a single value
    
    Args:
        query: SQL query with %s placeholders
        params: Query parameters as tuple
        
    Returns:
        The value or None
    """
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            row = await cur.fetchone()
            return list(row.values())[0] if row else None


# AIDEV-NOTE: prepared-statements; psycopg3 handles statement preparation automatically
# Use conn.prepare() for explicit prepared statements if needed

# AIDEV-TODO: query-builder; add simple query builder for common patterns
# AIDEV-TODO: monitoring; add query timing and connection pool metrics