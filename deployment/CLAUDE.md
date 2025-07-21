# Deployment Architecture Context for AI Assistants

<!-- AIDEV-NOTE: deployment-context; comprehensive guide for AI assistants working on Julep V2 deployment -->

## Overview

Julep V2 uses a **database-centric architecture** where PostgreSQL is the single source of truth, handling:
- Data storage (with pgvector for embeddings)
- Message queuing (with pgmq)
- Full-text and vector search
- ACID transactions for consistency

## Technology Stack

<!-- AIDEV-NOTE: tech-stack; core technologies and versions -->

### Core Infrastructure
- **PostgreSQL 15** with extensions:
  - `pgvector` 0.8.0 - Vector similarity search with HNSW indexing
  - `pgmq` - Native message queuing in PostgreSQL
  - `pg_jsonschema` - JSON schema validation
  - `uuid-ossp` - UUID generation

- **Hasura GraphQL Engine** v2.36.0
  - Instant GraphQL API over PostgreSQL
  - Real-time subscriptions
  - Row-level security integration
  - No custom resolvers needed

### Application Layer
- **Python 3.11** with:
  - `FastAPI` - Async web framework
  - `psycopg` - PostgreSQL async driver (v3)
  - `pydantic` - Data validation
  - `httpx` - Async HTTP client

### Optional Services
- **Redis 7** - Caching layer (profile: full)
- **Prometheus + Grafana** - Monitoring (profile: monitoring)

## Database Schema Design

<!-- AIDEV-NOTE: schema-design; critical understanding for database operations -->

### Schema Organization
```sql
-- Logical separation by schema
CREATE SCHEMA agents;      -- Agent management
CREATE SCHEMA memory;      -- Cognitive memory system  
CREATE SCHEMA protocols;   -- MCP/A2A protocol support
CREATE SCHEMA workflows;   -- Workflow orchestration
```

### Key Design Patterns

1. **UUID Primary Keys**: All tables use UUID PKs for distributed systems compatibility
2. **JSONB for Flexibility**: Configuration and metadata stored as JSONB
3. **Materialized Views**: For complex queries (memory type views)
4. **Function-based Logic**: Complex operations in PostgreSQL functions
5. **Trigger-based Updates**: Automatic timestamp updates

### Memory System Architecture

<!-- AIDEV-NOTE: memory-architecture; 4-layer cognitive memory system -->

The memory system implements four distinct types:

1. **Episodic Memory** (`memory.episodic_memories` view)
   - Personal experiences with temporal context
   - Emotional valence tracking
   - Sensory details storage

2. **Semantic Memory** (`memory.semantic_memories` view)
   - Facts and concepts
   - Relationship networks
   - ConceptNet integration

3. **Implicit Memory** (`memory.implicit_memories` view)
   - Patterns and habits
   - Frequency tracking
   - Automatic triggers

4. **Prospective Memory** (`memory.prospective_memories` view)
   - Future intentions and goals
   - Deadline management
   - Dependency tracking

### Vector Search Strategy

<!-- AIDEV-NOTE: vector-search; pgvector HNSW configuration -->

```sql
-- HNSW index configuration for optimal performance
CREATE INDEX ON memory.memories 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Key settings:
-- m = 16: Number of bi-directional links (higher = better quality, more memory)
-- ef_construction = 64: Size of dynamic candidate list (higher = better quality, slower build)
```

Performance targets:
- 10k vectors: <50ms search time
- 100k vectors: <100ms search time
- 1M vectors: <500ms search time

## Protocol Implementation

<!-- AIDEV-NOTE: protocol-implementation; MCP and A2A protocol details -->

### MCP (Model Context Protocol)
- Servers registry in `protocols.mcp_servers`
- Tools, resources, and prompts per server
- Message queuing via pgmq
- Automatic tool discovery and validation

### A2A (Agent-to-Agent)
- AgentCard registry in `protocols.a2a_agents`
- Task-based communication model
- Artifact sharing support
- Public/private agent discovery

## Deployment Patterns

<!-- AIDEV-NOTE: deployment-patterns; how services interact -->

### Service Communication
```
User Request → FastAPI App → PostgreSQL ← Hasura GraphQL
                    ↓              ↑
                 psycopg      pgmq queues
```

### Connection Pooling
- App maintains 10-20 connections via psycopg pool
- Hasura uses its own connection pool
- Total connections should not exceed `max_connections` (default: 200)

### Environment Variable Strategy
- **No defaults for secrets** - Forces explicit configuration
- Sensitive vars: passwords, API keys, secrets
- Non-sensitive vars: ports, feature flags, tuning parameters

## Common Tasks and Patterns

<!-- AIDEV-NOTE: common-patterns; frequently needed code patterns -->

### Direct SQL Query Pattern
```python
from src.database import get_connection, get_transaction

# Simple query
async with get_connection() as conn:
    agents = await conn.fetch(
        "SELECT * FROM agents.agents WHERE is_active = $1", 
        True
    )

# Transaction with multiple operations
async with get_transaction() as conn:
    agent_id = await conn.fetchval(
        "INSERT INTO agents.agents (name, type) VALUES ($1, $2) RETURNING id",
        name, agent_type
    )
    await conn.execute(
        "INSERT INTO agents.sessions (agent_id) VALUES ($1)",
        agent_id
    )
```

### Vector Search Pattern
```python
# Generate embedding (would use actual embedding service)
embedding = await generate_embedding(query_text)

# Search similar memories
memories = await conn.fetch("""
    SELECT id, content, 1 - (embedding <=> $1) as similarity
    FROM memory.memories
    WHERE agent_id = $2
      AND 1 - (embedding <=> $1) > $3
    ORDER BY similarity DESC
    LIMIT $4
""", embedding, agent_id, threshold, limit)
```

### Message Queue Pattern
```python
# Send message via pgmq
await conn.execute(
    "SELECT pgmq.send('mcp_messages', $1)",
    json.dumps(message_data)
)

# Receive messages
messages = await conn.fetch(
    "SELECT * FROM pgmq.read('mcp_messages', 10, 30)"
)
```

## Performance Optimization

<!-- AIDEV-NOTE: performance-tips; critical for production -->

1. **Index Usage**
   - Always check query plans with `EXPLAIN ANALYZE`
   - Create indexes AFTER bulk data loads
   - Use partial indexes for filtered queries

2. **Connection Management**
   - Reuse connections from pool
   - Use transactions for related operations
   - Close connections promptly

3. **Query Optimization**
   - Use prepared statements for repeated queries
   - Batch operations when possible
   - Avoid N+1 query problems

4. **Vector Search Optimization**
   - Pre-filter with WHERE before vector search
   - Use appropriate HNSW parameters
   - Consider quantization for very large datasets

## Migration Management

<!-- AIDEV-NOTE: migration-strategy; database evolution approach -->

Migrations are located in `src/database/migrations/` and run in sequence:
1. `001_initial_schema.sql` - Core agent tables
2. `002_memory_system.sql` - Memory system
3. `003_protocols.sql` - Protocol support
4. `004_workflows.sql` - Workflow tables
5. `005_functions.sql` - Helper functions

**Future migrations** should:
- Follow the `NNN_description.sql` naming pattern
- Be idempotent (safe to run multiple times)
- Include rollback procedures in comments
- Update documentation
- Test on staging first

See `src/database/migrations/README.md` for detailed migration guidelines.

## Monitoring and Debugging

<!-- AIDEV-NOTE: debugging-tips; troubleshooting guidance -->

### Key Metrics to Watch
- Connection pool saturation
- Query execution time (p50, p95, p99)
- Vector search performance
- Message queue depth
- Memory usage by index

### Useful Queries
```sql
-- Active connections
SELECT count(*) FROM pg_stat_activity;

-- Slow queries
SELECT query, mean_exec_time 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- Table sizes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables 
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan;
```

## Security Considerations

<!-- AIDEV-NOTE: security-critical; must be maintained -->

1. **No hardcoded secrets** - All sensitive data from environment
2. **Parameterized queries** - Never concatenate SQL strings
3. **Row-level security** - Hasura policies for multi-tenancy
4. **Connection encryption** - SSL/TLS in production
5. **Least privilege** - App user has only necessary permissions

## Development Workflow

<!-- AIDEV-NOTE: dev-workflow; standard development process -->

1. **Local Development**
   ```bash
   cp .env.example .env
   # Fill in required values
   docker-compose up -d
   ```

2. **Making Changes**
   - Database changes: Create new migration file
   - API changes: Update src/ code
   - Test locally before committing

3. **Testing**
   - Unit tests: Direct function tests
   - Integration tests: With test database
   - E2E tests: Full stack with Docker Compose

## Known Limitations and TODOs

<!-- AIDEV-NOTE: limitations; areas needing attention -->

1. **No built-in migration tool** - Using numbered SQL files
2. **Basic connection pooling** - May need pgBouncer at scale
3. **Limited caching** - Redis integration is optional
4. **No automatic failover** - Single PostgreSQL instance

## Future Enhancements

<!-- AIDEV-NOTE: roadmap-items; planned improvements -->

1. **Production Readiness**
   - Kubernetes manifests
   - Horizontal scaling strategy
   - Multi-region deployment

2. **Performance**
   - Query result caching
   - Read replica support
   - Prepared statement optimization

3. **Observability**
   - OpenTelemetry integration
   - Custom Grafana dashboards
   - Alerting rules

## Quick Reference

<!-- AIDEV-NOTE: quick-ref; most commonly needed information -->

### File Locations
- SQL migrations: `src/database/migrations/`
- Docker config: `deployment/docker/docker-compose.yml`
- Environment template: `.env.example`
- App code: `src/`
- Database module: `src/database/`

### Default Ports
- PostgreSQL: 5432
- Hasura: 8080
- App API: 8000
- Redis: 6379
- Prometheus: 9090
- Grafana: 3000

### Key Commands
```bash
# Start everything
docker-compose --profile full --profile monitoring up -d

# View logs
docker-compose logs -f [service]

# Database shell
docker-compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# Restart service
docker-compose restart app
```

Remember: When in doubt, check the SQL migrations for the source of truth on schema design!