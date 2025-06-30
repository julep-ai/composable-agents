# TypeSpec Directory Guide

<!-- AIDEV-NOTE: typespec-overview; schema-driven development reducing code by 70% -->
This directory contains TypeSpec definitions that generate PostgreSQL schemas, API contracts, and client SDKs.

**TypeSpec Version**: 1.1.0 (Latest stable release, June 2025)

## Directory Structure

- **models/**: Core data models (agents, memories, protocols)
- **contracts/**: API contracts and interfaces
- **generated/**: Output directory for generated code (gitignored)

## TypeSpec Benefits

<!-- AIDEV-NOTE: typespec-benefits; single source of truth for entire stack -->
1. **Single source of truth**: One definition generates everything
2. **Type safety**: End-to-end type checking from DB to client
3. **Auto-documentation**: OpenAPI specs generated automatically
4. **SDK generation**: Client libraries in multiple languages

## Key Models

<!-- AIDEV-NOTE: core-models; essential TypeSpec definitions -->
- `agent.tsp`: Agent definitions with MCP/A2A capabilities
- `memory.tsp`: Four cognitive memory types
- `protocol.tsp`: MCP and A2A message formats
- `workflow.tsp`: Task and workflow state models

## Development Workflow

1. Define or update TypeSpec models
2. Run generation: `npm run generate`
3. Generated code appears in:
   - `agents_api/models/` (SQLAlchemy)
   - `sdk/python/julep/` (Python SDK)
   - `sdk/typescript/` (TypeScript SDK)

<!-- AIDEV-TODO: generation-script; implement TypeSpec generation pipeline -->