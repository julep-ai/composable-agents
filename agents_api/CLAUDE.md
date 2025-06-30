# agents_api Directory Guide

<!-- AIDEV-NOTE: agents-api-overview; core API implementation following database-centric architecture -->
This directory contains the core Julep V2 API implementation using FastAPI and PostgreSQL as the single source of truth.

## Directory Structure

- **api/**: FastAPI routes and endpoint handlers
- **models/**: TypeSpec-generated SQLAlchemy models
- **memory/**: Cognitive memory system (episodic, semantic, implicit, prospective)
- **protocols/**: MCP and A2A protocol implementations
- **workflows/**: DBOS-based durable workflow orchestration
- **utils/**: Shared utilities and helpers

## Key Principles

<!-- AIDEV-NOTE: db-centric-principle; PostgreSQL handles storage, queuing, and search -->
1. **Database-centric**: PostgreSQL with extensions (pgvector, pgmq, pgai) handles all infrastructure needs
2. **TypeSpec-driven**: Models and contracts generated from TypeSpec definitions
3. **Async-first**: Use asyncio throughout for high concurrency
4. **Protocol-native**: Built-in support for MCP and A2A protocols

## Development Guidelines

<!-- AIDEV-NOTE: dev-guidelines; critical patterns for maintaining consistency -->
- Always use async/await for database operations
- Implement proper error handling with custom exceptions
- Add AIDEV-NOTE comments for complex logic
- Follow the 4-layer memory architecture strictly
- Use DBOS decorators for any stateful operations

## Performance Targets

- API response time: <100ms
- Memory search: <50ms for 10k entries
- Concurrent operations: 1000+ agents

<!-- AIDEV-TODO: add-examples; include code examples for common patterns -->