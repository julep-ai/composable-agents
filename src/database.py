"""
Backward compatibility module
Database functionality has been moved to src.database module
"""

# AIDEV-NOTE: backward-compat; re-export from database module to maintain API
from .database import (
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