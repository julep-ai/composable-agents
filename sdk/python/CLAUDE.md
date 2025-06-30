# Python SDK Directory Guide

<!-- AIDEV-NOTE: sdk-overview; TypeSpec-generated Python client library -->
This directory contains the Python SDK for Julep V2, providing a high-level interface for interacting with agents and their cognitive memory systems.

## Directory Structure

- **julep/**: Main SDK package
  - **client.py**: Async client with connection pooling
  - **models/**: TypeSpec-generated Pydantic models
  - **agents/**: Agent management operations
  - **memory/**: Memory system interfaces
  - **protocols/**: MCP and A2A client implementations

## SDK Design Principles

<!-- AIDEV-NOTE: sdk-patterns; async-first Python client design -->
1. **Async-First**: All operations use async/await
2. **Type-Safe**: Full type hints with Pydantic models
3. **Resource Management**: Context managers for proper cleanup
4. **Streaming Support**: Async iterators for real-time updates
5. **Error Handling**: Rich exception hierarchy

## Usage Example

```python
from julep import JulepClient
from julep.models import Agent, MemoryQuery

async def main():
    # AIDEV-NOTE: client-usage; async context manager pattern
    async with JulepClient(api_key="...") as client:
        # Create an agent
        agent = await client.agents.create(
            name="Research Assistant",
            type="research"
        )
        
        # Store a memory
        await agent.memories.store(
            content="User prefers concise summaries",
            memory_type="semantic"
        )
        
        # Query memories with vector search
        memories = await agent.memories.search(
            query="communication preferences",
            limit=5
        )
```

## Performance Considerations

- Connection pooling with httpx for efficient API calls
- Automatic retry with exponential backoff
- Request batching for bulk operations
- Local caching of frequently accessed data

<!-- AIDEV-TODO: sdk-generation; implement TypeSpec->Python generation -->
<!-- AIDEV-TODO: streaming-client; add SSE support for real-time updates -->