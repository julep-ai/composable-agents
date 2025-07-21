"""
Julep V2 Core
Protocol-native co-agents with cognitive memory architecture
"""

# AIDEV-NOTE: version-management; semantic versioning from single source
__version__ = "2.0.0-alpha"

# AIDEV-NOTE: api-exports; public API surface
__all__ = [
    # Database
    "get_connection",
    "get_transaction",
    "execute_query",
    "fetch_one",
    "fetch_all",
    "fetch_value",
    
    # API
    "create_app",
    
    # Version
    "__version__",
]

# Import public API
from .database import (
    get_connection,
    get_transaction,
    execute_query,
    fetch_one,
    fetch_all,
    fetch_value,
)