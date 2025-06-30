# Technical Implementation Plan for Julep V2: Building Protocol-Native Co-Agents

<!-- AIDEV-NOTE: implementation-overview; core architecture decisions for 4-6 week rapid prototype -->
Julep V2 can be built within the 4-6 week timeline using a PostgreSQL-centric architecture with TypeSpec for code generation, DBOS for workflow orchestration, and native MCP/A2A protocol support. This approach minimizes development complexity while proving the core architectural concepts through rapid prototyping with disposable code that validates the cognitive memory system design.

<!-- AIDEV-NOTE: postgres-centric; eliminates microservice complexity with single database source of truth -->
The proposed architecture leverages PostgreSQL as the single source of truth for all agent operations, using extensions like pgvector for similarity search, pgmq for message queuing, and pgai for LLM integration. TypeSpec accelerates development by auto-generating schemas, API contracts, and client libraries from a single specification. DBOS provides durable workflow orchestration with minimal code changes, while Hasura exposes PostgreSQL functions as GraphQL/REST APIs automatically.

## Core architecture design choices

<!-- AIDEV-NOTE: database-centric; unified infrastructure approach eliminates service boundaries -->
The database-centric approach places PostgreSQL at the heart of the system, handling not just data storage but also workflow orchestration, message queuing, and vector search. This eliminates the need for separate infrastructure components like Redis or Elasticsearch during prototyping.

<!-- AIDEV-NOTE: typespec-benefits; 70% code reduction through schema-driven generation -->
**TypeSpec serves as the schema definition language**, generating PostgreSQL tables, API contracts, and client SDKs from a single source. This reduces boilerplate code by approximately **70%** compared to manual implementation. The TypeSpec definitions flow through the entire stack:

typescript

    // Single TypeSpec definition generates everything
    model Agent {
      id: string;
      name: string;
      type: "conversational" | "task-oriented" | "research";
      mcpServers?: MCPServerConfig[];
      a2aCapabilities?: A2AAgentCard;
    }

<!-- AIDEV-NOTE: dbos-simplification; 90% code reduction compared to Temporal for workflows -->
**DBOS replaces traditional workflow engines** like Temporal with a simpler decorator-based approach. Adding durability to Python functions requires only 5-10 lines of decorator code, compared to 100+ lines for Temporal. This dramatic simplification accelerates development while maintaining production-grade reliability.

## Protocol implementation strategy

<!-- AIDEV-NOTE: mcp-implementation; database-backed registries for tools and resources -->
The MCP (Model Context Protocol) implementation uses PostgreSQL as the message store with pgmq for queuing. Each MCP server exposes tools, resources, and prompts through database-backed registries:

sql

    CREATE TABLE mcp_tools (
        id UUID PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        input_schema JSONB,
        server_id UUID,
        enabled BOOLEAN DEFAULT true
    );

<!-- AIDEV-NOTE: a2a-protocol; extends MCP with task lifecycle and agent discovery -->
The A2A (Agent-to-Agent) protocol builds on MCP by adding task lifecycle management and agent discovery. AgentCards stored in PostgreSQL enable dynamic agent registration and capability advertisement. The protocol messages flow through pgmq queues with exactly-once delivery semantics.

<!-- AIDEV-NOTE: protocol-integration; unified database infrastructure for MCP and A2A -->
**Protocol integration happens at the database level**, with both MCP and A2A messages sharing common infrastructure. This unified approach simplifies debugging and monitoring while enabling cross-protocol communication patterns.

## Cognitive memory architecture implementation

<!-- AIDEV-NOTE: memory-system; four cognitive memory types inspired by human cognition -->
The memory system uses four distinct types stored in PostgreSQL with vector embeddings for similarity search:

<!-- AIDEV-NOTE: episodic-memory; temporal experiences with emotional valence and decay -->
**Episodic memory** captures temporal sequences of experiences with full context. Each memory includes timestamps, emotional valence, and importance scores that decay over time unless reinforced through access.

<!-- AIDEV-NOTE: semantic-memory; factual knowledge with ConceptNet integration -->
**Semantic memory** stores factual knowledge in a graph structure, with relationships between concepts tracked in a separate table. ConceptNet integration provides grounded common-sense knowledge by linking agent memories to established concepts.

<!-- AIDEV-NOTE: implicit-memory; unconscious patterns shaping agent behavior -->
**Implicit memory** tracks unconscious patterns, biases, and behavioral tendencies that influence decision-making. These memories form through repeated experiences and shape agent responses without explicit recall.

<!-- AIDEV-NOTE: prospective-memory; goal hierarchy with dependency tracking -->
**Prospective memory** manages future-oriented cognition including goals, plans, and obligations. A hierarchical structure allows complex goals to be decomposed into subgoals with dependencies.

<!-- AIDEV-NOTE: pgvector-performance; HNSW indexing for sub-50ms memory search -->
The **pgvector extension enables efficient similarity search** across all memory types using HNSW indexing. Memory consolidation runs as background processes, strengthening frequently accessed memories while allowing unused ones to decay according to forgetting curves.

## Development timeline and milestones

### Week 1: Foundation and core infrastructure

<!-- AIDEV-NOTE: week1-foundation; docker setup with postgres extensions and typespec schemas -->
The first week focuses on environment setup and core database schema implementation. Docker Compose orchestrates PostgreSQL with all required extensions (pgvector, pgmq, pgai, pg\_jsonschema). TypeSpec definitions create the initial schema for agents, memories, and protocol messages. FastAPI provides the REST API layer with automatic OpenAPI documentation.

### Week 2: Core agent operations and basic memory

Basic CRUD operations for agents launch early in week two, followed by simple memory storage and retrieval. The team implements JWT authentication and establishes the foundation for protocol message handling. By week's end, agents can store and retrieve memories with basic vector search capabilities.

### Week 3: Protocol implementation and advanced memory

MCP server/client implementation begins with tool and resource registries in PostgreSQL. A2A protocol support adds agent discovery and task management. The memory system gains consolidation algorithms and more sophisticated retrieval patterns. DBOS integration provides durable workflows for agent operations.

### Week 4: Integration and external systems

Hasura configuration exposes PostgreSQL functions as GraphQL APIs, enabling flexible client access patterns. The team connects TypeSpec-generated schemas with runtime systems and implements message routing between protocols. End-to-end integration testing validates the complete system flow.

### Week 5: Advanced features and optimization

Multi-agent communication patterns emerge through A2A protocol enhancements. Performance optimization focuses on query tuning and index optimization. Advanced memory features like belief updating and cross-memory reasoning come online. The team implements circuit breakers and error recovery mechanisms.

### Week 6: Testing, documentation, and deployment

Comprehensive test coverage reaches 90% through unit, integration, and end-to-end tests. Production deployment configurations use Docker Swarm or Kubernetes. API documentation generated from TypeSpec provides complete reference materials. Performance benchmarking confirms sub-100ms response times for key operations.

## Technical stack configuration

The PostgreSQL configuration maximizes performance for AI workloads:

sql

    -- Key PostgreSQL settings
    SET maintenance_work_mem = '2GB';
    SET max_parallel_maintenance_workers = 4;
    SET shared_buffers = '4GB';
    SET effective_cache_size = '12GB';

**Python dependencies focus on async performance**:

-   FastAPI for high-performance async REST APIs
-   SQLAlchemy with async support for ORM operations
-   asyncpg for direct PostgreSQL access when performance matters
-   DBOS Python client for workflow orchestration

The development environment uses Docker Compose for consistency:

yaml

    services:
      postgres:
        image: postgres:15
        command: postgres -c shared_preload_libraries='pg_stat_statements,pgmq,vector'
        environment:
          POSTGRES_PASSWORD: postgres
      
      app:
        build: .
        depends_on: [postgres, hasura]
        environment:
          DATABASE_URL: postgresql://postgres:postgres@postgres:5432/julep

## Risk mitigation and architectural decisions

<!-- AIDEV-NOTE: risk-mitigation; key strategies for 6-week prototype success -->
**Database performance risk** is mitigated through proper indexing strategies and connection pooling. The team monitors query performance using pg\_stat\_statements and adjusts indexes based on actual usage patterns.

<!-- AIDEV-NOTE: integration-complexity; abstraction layers prevent component coupling -->
**Integration complexity** between TypeSpec, DBOS, and Hasura is managed through abstraction layers. Each component has clear boundaries with well-defined interfaces. Fallback strategies ensure the system remains functional if any integration fails.

<!-- AIDEV-NOTE: scope-control; strict MVP focus prevents timeline creep -->
**Scope creep** threatens the 6-week timeline. Strict MVP definition focuses on core co-agent functionality. Weekly stakeholder reviews ensure alignment while a formal change control process defers non-essential features.

<!-- AIDEV-NOTE: disposable-code; prototype markers for production migration -->
The **disposable code approach** acknowledges that some prototype code won't survive to production. Clear markers identify temporary implementations. The architecture supports gradual replacement of prototype components without system-wide refactoring.

## Success metrics and validation

<!-- AIDEV-NOTE: success-metrics; performance targets for prototype validation -->
The prototype demonstrates success through several key metrics:

-   **Response times under 100ms** for agent operations
-   **Memory search completes in under 50ms** for 10,000 entries
-   **Protocol message delivery maintains exactly-once semantics**
-   **System handles 1000+ concurrent agent operations**

<!-- AIDEV-NOTE: functional-validation; core capabilities required for co-agent proof -->
Functional validation confirms that agents can:

-   Communicate using both MCP and A2A protocols
-   Store and retrieve memories across all four types
-   Execute durable workflows that survive system failures
-   Discover and collaborate with other agents dynamically

The prototype proves that a database-centric architecture with declarative configuration can deliver sophisticated AI agent capabilities. The rapid development approach validates core concepts while identifying areas for production hardening. Most importantly, the 4-6 week timeline produces a working system that demonstrates the feasibility of protocol-native co-agents with cognitive memory architectures.







