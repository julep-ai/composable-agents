# Julep AI v2 - Protocol-Native Co-Agents
<!-- AIDEV-NOTE: main-readme; internal documentation for development team -->

PostgreSQL-centric AI agent platform with cognitive memory and native MCP/A2A protocol support.

## Quick Start

```bash
# Prerequisites: Docker, Docker Compose, Node.js 18+, Python 3.11+
git clone <repo-url>
cd julep-v2
docker-compose up -d postgres  # PostgreSQL with extensions
npm install -g @typespec/compiler
pip install -r requirements.txt
source .venv/bin/activate
```

## Architecture

**Database-Centric Design**: PostgreSQL as single source of truth
- **pgvector**: Vector similarity search for memory
- **pgmq**: Message queuing for protocols  
- **pgai**: LLM integration
- **pg_jsonschema**: Schema validation

**Key Design Decisions**:
- TypeSpec generates all schemas/APIs/clients
- DBOS for durable workflows (5-10 lines vs 100+ with Temporal)
- Hasura auto-exposes DB functions as GraphQL/REST
- 4 cognitive memory types: episodic, semantic, implicit, prospective

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Database | PostgreSQL 15+ | Single source of truth |
| API | FastAPI + psycopg | Async REST endpoints with direct SQL |
| Schema | TypeSpec | Code generation |
| Workflows | DBOS | Durable execution |
| GraphQL | Hasura | Auto-generated from DB |
| Vector Search | pgvector (HNSW) | Memory similarity |
| Message Queue | pgmq | Protocol messaging |

## Memory System

**4 Cognitive Memory Types**:
- **Episodic**: Temporal experiences with emotional valence
- **Semantic**: Factual knowledge graph (ConceptNet integration)
- **Implicit**: Unconscious patterns and biases
- **Prospective**: Goals, plans, future obligations

**Performance Targets**:
- Memory search: <50ms for 10k entries
- Agent operations: <100ms response time
- Concurrent ops: 1000+ agents

## Protocols

**MCP (Model Context Protocol)**:
- Tools, resources, prompts via DB registries
- PostgreSQL message store with pgmq queuing

**A2A (Agent-to-Agent)**:
- Extends MCP with task lifecycle management
- AgentCards for dynamic discovery
- Exactly-once delivery semantics

## Development Guidelines

**Critical Rules**:
1. **Human oversight**: AI generates code, humans own architecture/tests
2. **Ask before assuming**: Consult developer when uncertain  
3. **No touching tests**: Humans control test files and SPEC.md
4. **Anchor comments**: Add `AIDEV-NOTE:` for complex code
5. **Granular commits**: One logical change per commit

**Workflow**:
1. Check directory-specific `CLAUDE.md` files first
2. Use TypeSpec for schema changes
3. Run linters: `ruff`, `npm run lint`
4. Performance test with realistic data volumes

## Directory Structure

```
julep-v2/
├── CLAUDE.md              # AI assistant guidelines
├── IMPLEMENTATION_PLAN.md # Technical roadmap
├── TYPESPEC_REFERENCE.md  # Schema definitions
├── agents_api/           # Main API code (when created)
├── cli/src/              # CLI implementation  
├── integrations/         # Protocol integrations
├── schemas/              # TypeSpec definitions
└── tests/                # Human-owned tests
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `CLAUDE.md` | AI assistant behavior guidelines |
| `IMPLEMENTATION_PLAN.md` | 6-week development roadmap |
| `TYPESPEC_REFERENCE.md` | Schema-first API definitions |
| `OPEN_SOURCE_GUIDE.md` | Community documentation |
| `AGENTS.md` | Agent system documentation |

## Performance Targets

- **Sub-100ms** agent operations
- **Sub-50ms** memory search (10k entries)
- **1000+** concurrent agents
- **Exactly-once** protocol message delivery

## Development Timeline

**6-Week Rapid Prototype**:
- Week 1: Foundation (Docker, PostgreSQL, TypeSpec)
- Week 2: Core CRUD + basic memory
- Week 3: MCP/A2A protocols + advanced memory
- Week 4: Hasura integration + message routing
- Week 5: Multi-agent patterns + optimization
- Week 6: Testing + documentation + deployment

## Critical Notes

- **Disposable code**: Prototype focuses on proving concepts
- **PostgreSQL-first**: Avoid microservices complexity
- **Schema-driven**: TypeSpec generates 70% of boilerplate
- **Memory-centric**: 4 cognitive types essential for co-agents
- **Protocol-native**: MCP/A2A as first-class citizens

---

**For AI Assistants**: Always read `CLAUDE.md` before making changes. When uncertain, ask the developer.
