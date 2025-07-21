"""
Database module for Julep V2
Handles connections, migrations, and database utilities
"""

# AIDEV-NOTE: database-module; re-export public API for backward compatibility
from .connection import (
    init_pool,
    close_pool,
    get_connection,
    get_transaction,
    execute_query,
    fetch_one,
    fetch_all,
    fetch_value,
)

__all__ = [
    "init_pool",
    "close_pool",
    "get_connection",
    "get_transaction",
    "execute_query",
    "fetch_one",
    "fetch_all",
    "fetch_value",
]