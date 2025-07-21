# src Directory Guide

<!-- AIDEV-NOTE: src-overview; core implementation following database-centric architecture -->
This directory contains the core Julep V2 implementation using FastAPI and PostgreSQL as the single source of truth, without ORM dependencies.

## Directory Structure

- **api/**: FastAPI routes and endpoint handlers
- **memory/**: Cognitive memory system (episodic, semantic, implicit, prospective)
- **protocols/**: MCP and A2A protocol implementations
- **workflows/**: DBOS-based durable workflow orchestration
- **agents/**: Agent management and lifecycle
- **database/**: Database module with connection management and migrations
  - **connection.py**: Direct psycopg connection management (no ORM)
  - **migrations/**: SQL migration files (001-005)
- **database.py**: Backward compatibility re-export

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

## Database Migrations

<!-- AIDEV-NOTE: migration-location; migrations now live with application code -->
Database migrations are located in `src/database/migrations/`:
- Numbered sequentially (001, 002, etc.)
- Run automatically during Docker startup
- See `database/migrations/README.md` for migration guidelines

<!-- AIDEV-TODO: add-examples; include code examples for common patterns -->