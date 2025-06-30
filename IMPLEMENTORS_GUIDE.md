# Julep V2 Complete Implementor's Guide

<!-- AIDEV-NOTE: implementors-guide; comprehensive technical implementation documentation -->
## Table of Contents

1.  [Prerequisites and Environment Setup](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#prerequisites)
2.  [Project Structure and Initial Configuration](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#project-structure)
3.  [PostgreSQL Database Setup](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#postgresql-setup)
4.  [TypeSpec Schema Definition](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#typespec-schema)
5.  [Database Schema Implementation](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#database-schema)
6.  [Memory System Implementation](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#memory-system)
7.  [MCP Protocol Implementation](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#mcp-protocol)
8.  [A2A Protocol Implementation](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#a2a-protocol)
9.  [DBOS Workflow Integration](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#dbos-workflows)
10.  [FastAPI Application Layer](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#fastapi-layer)
11.  [Hasura Configuration](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#hasura-setup)
12.  [Testing Strategy](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#testing)
13.  [Deployment and Operations](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#deployment)
14.  [Troubleshooting Guide](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#troubleshooting)
15.  [Performance Optimization](https://claude.ai/public/artifacts/900a94aa-0e48-44ba-8478-b8a791cff089#performance)

* * *

## 1\. Prerequisites and Environment Setup {#prerequisites}

### Required Software

-   Python 3.11+ (for async performance improvements)
-   PostgreSQL 15+ with development headers
-   Docker and Docker Compose
-   Node.js 18+ (for TypeSpec)
-   Git

### Development Machine Setup

bash

    # Clone the repository
    git clone https://github.com/julep-ai/julep-v2-prototype.git
    cd julep-v2-prototype
    
    # Create Python virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    # Install TypeSpec globally
    npm install -g @typespec/compiler
    
    # Install PostgreSQL extensions build tools
    sudo apt-get install postgresql-server-dev-15 build-essential

### Directory Structure Creation

bash

    mkdir -p {src/{agents,memory,protocols,workflows,api},tests,schemas,docker,scripts,docs}
    touch .env .env.example docker-compose.yml README.md

* * *

## 2\. Project Structure and Initial Configuration {#project-structure}

### Project Layout

    julep-v2-prototype/
    ├── docker/
    │   ├── postgres/
    │   │   ├── Dockerfile
    │   │   └── init.sql
    │   ├── app/
    │   │   └── Dockerfile
    │   └── hasura/
    │       └── metadata/
    ├── schemas/
    │   ├── typespec/
    │   │   ├── main.tsp
    │   │   ├── agents.tsp
    │   │   ├── memory.tsp
    │   │   └── protocols.tsp
    │   └── generated/
    ├── src/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database.py
    │   ├── agents/
    │   │   ├── __init__.py
    │   │   ├── models.py
    │   │   ├── crud.py
    │   │   └── schemas.py
    │   ├── memory/
    │   │   ├── __init__.py
    │   │   ├── episodic.py
    │   │   ├── semantic.py
    │   │   ├── implicit.py
    │   │   └── prospective.py
    │   ├── protocols/
    │   │   ├── __init__.py
    │   │   ├── mcp/
    │   │   └── a2a/
    │   ├── workflows/
    │   │   ├── __init__.py
    │   │   └── dbos_workflows.py
    │   └── api/
    │       ├── __init__.py
    │       ├── main.py
    │       └── routers/
    ├── tests/
    ├── scripts/
    │   ├── setup_extensions.sh
    │   └── generate_schemas.sh
    ├── docker-compose.yml
    ├── .env.example
    ├── requirements.txt
    ├── pyproject.toml
    └── README.md

### Initial Configuration Files

**`.env.example`**

env

    # Database
    DATABASE_URL=postgresql://postgres:postgres@localhost:5432/julep_v2
    DATABASE_POOL_SIZE=20
    DATABASE_MAX_OVERFLOW=40
    
    # Redis (for pgmq)
    REDIS_URL=redis://localhost:6379
    
    # API Keys
    OPENAI_API_KEY=sk-...
    ANTHROPIC_API_KEY=sk-ant-...
    
    # Hasura
    HASURA_GRAPHQL_ENDPOINT=http://localhost:8080/v1/graphql
    HASURA_ADMIN_SECRET=myadminsecret
    
    # Application
    SECRET_KEY=your-secret-key-here
    ENVIRONMENT=development
    LOG_LEVEL=INFO
    
    # DBOS
    DBOS_DATABASE_URL=${DATABASE_URL}
    DBOS_NAMESPACE=julep_v2
    
    # Vector dimensions
    EMBEDDING_DIMENSIONS=1536

**`pyproject.toml`**

toml

    [tool.poetry]
    name = "julep-v2-prototype"
    version = "0.1.0"
    description = "Protocol-native co-agents with cognitive memory"
    authors = ["Julep Team"]
    python = "^3.11"
    
    [tool.poetry.dependencies]
    python = "^3.11"
    fastapi = "^0.109.0"
    uvicorn = {extras = ["standard"], version = "^0.25.0"}
    sqlalchemy = {extras = ["asyncio"], version = "^2.0.25"}
    asyncpg = "^0.29.0"
    alembic = "^1.13.1"
    pydantic = "^2.5.3"
    pydantic-settings = "^2.1.0"
    dbos = "^0.1.0"
    openai = "^1.6.1"
    anthropic = "^0.8.1"
    httpx = "^0.25.2"
    python-jose = {extras = ["cryptography"], version = "^3.3.0"}
    passlib = {extras = ["bcrypt"], version = "^1.7.4"}
    python-multipart = "^0.0.6"
    pytest = "^7.4.4"
    pytest-asyncio = "^0.21.1"
    black = "^23.12.1"
    mypy = "^1.8.0"
    ruff = "^0.1.11"
    
    [build-system]
    requires = ["poetry-core"]
    build-backend = "poetry.core.masonry.api"
    
    [tool.black]
    line-length = 88
    target-version = ['py311']
    
    [tool.ruff]
    line-length = 88
    select = ["E", "F", "I", "N", "W"]
    ignore = ["E501"]
    
    [tool.mypy]
    python_version = "3.11"
    warn_return_any = true
    warn_unused_configs = true
    ignore_missing_imports = true

**`docker-compose.yml`**

yaml

    version: '3.8'
    
    services:
      postgres:
        build: ./docker/postgres
        environment:
          POSTGRES_DB: julep_v2
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 5s
          timeout: 5s
          retries: 5
    
      hasura:
        image: hasura/graphql-engine:v2.36.0
        ports:
          - "8080:8080"
        depends_on:
          postgres:
            condition: service_healthy
        restart: always
        environment:
          HASURA_GRAPHQL_DATABASE_URL: postgres://postgres:postgres@postgres:5432/julep_v2
          HASURA_GRAPHQL_ENABLE_CONSOLE: "true"
          HASURA_GRAPHQL_DEV_MODE: "true"
          HASURA_GRAPHQL_ENABLED_LOG_TYPES: startup, http-log, webhook-log, websocket-log, query-log
          HASURA_GRAPHQL_ADMIN_SECRET: myadminsecret
          HASURA_GRAPHQL_METADATA_DATABASE_URL: postgres://postgres:postgres@postgres:5432/julep_v2
    
      app:
        build: ./docker/app
        ports:
          - "8000:8000"
        depends_on:
          postgres:
            condition: service_healthy
        environment:
          DATABASE_URL: postgresql://postgres:postgres@postgres:5432/julep_v2
          ENVIRONMENT: development
        volumes:
          - ./src:/app/src
          - ./schemas:/app/schemas
        command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
    
    volumes:
      postgres_data:

* * *

## 3\. PostgreSQL Database Setup {#postgresql-setup}

### PostgreSQL Dockerfile with Extensions

**`docker/postgres/Dockerfile`**

dockerfile

    FROM postgres:15
    
    # Install build dependencies
    RUN apt-get update && apt-get install -y \
        build-essential \
        git \
        postgresql-server-dev-15 \
        curl \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*
    
    # Install pgvector
    RUN cd /tmp && \
        git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git && \
        cd pgvector && \
        make && \
        make install
    
    # Install pgmq
    RUN cd /tmp && \
        git clone https://github.com/pgmq/pgmq.git && \
        cd pgmq && \
        make && \
        make install
    
    # Install pg_jsonschema
    RUN cd /tmp && \
        git clone https://github.com/supabase/pg_jsonschema.git && \
        cd pg_jsonschema && \
        make && \
        make install
    
    # Install pgai (placeholder - use actual installation when available)
    # For now, we'll create functions that call external APIs
    
    # Copy initialization script
    COPY init.sql /docker-entrypoint-initdb.d/

### Database Initialization Script

**`docker/postgres/init.sql`**

sql

    -- Enable required extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";
    CREATE EXTENSION IF NOT EXISTS "vector";
    CREATE EXTENSION IF NOT EXISTS "pgmq";
    CREATE EXTENSION IF NOT EXISTS "pg_jsonschema";
    
    -- Create schemas for organization
    CREATE SCHEMA IF NOT EXISTS agents;
    CREATE SCHEMA IF NOT EXISTS memory;
    CREATE SCHEMA IF NOT EXISTS protocols;
    CREATE SCHEMA IF NOT EXISTS workflows;
    
    -- Set default search path
    ALTER DATABASE julep_v2 SET search_path TO public, agents, memory, protocols, workflows;
    
    -- Create custom types
    CREATE TYPE agent_type AS ENUM ('conversational', 'task_oriented', 'research', 'coordinator');
    CREATE TYPE memory_type AS ENUM ('episodic', 'semantic', 'implicit', 'prospective');
    CREATE TYPE task_status AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');
    
    -- pgai function placeholders (replace with actual pgai when available)
    CREATE OR REPLACE FUNCTION ai_generate_embedding(
        model TEXT,
        content TEXT
    ) RETURNS vector(1536) AS $$
    DECLARE
        -- This is a placeholder implementation
        -- In production, this would call the actual pgai function
        embedding vector(1536);
    BEGIN
        -- Generate a dummy embedding for now
        SELECT ARRAY_AGG(random()::real)::vector(1536)
        INTO embedding
        FROM generate_series(1, 1536);
        
        RETURN embedding;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE OR REPLACE FUNCTION ai_chat_completion(
        model TEXT,
        messages JSONB
    ) RETURNS JSONB AS $$
    DECLARE
        -- Placeholder for actual LLM call
        response JSONB;
    BEGIN
        response := jsonb_build_object(
            'id', gen_random_uuid()::text,
            'model', model,
            'choices', jsonb_build_array(
                jsonb_build_object(
                    'message', jsonb_build_object(
                        'role', 'assistant',
                        'content', 'This is a placeholder response'
                    ),
                    'finish_reason', 'stop'
                )
            ),
            'usage', jsonb_build_object(
                'prompt_tokens', 10,
                'completion_tokens', 10,
                'total_tokens', 20
            )
        );
        
        RETURN response;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Create message queues
    SELECT pgmq.create_queue('mcp_messages');
    SELECT pgmq.create_queue('a2a_tasks');
    SELECT pgmq.create_queue('memory_consolidation');
    SELECT pgmq.create_queue('workflow_events');
    
    -- Performance settings
    ALTER SYSTEM SET shared_buffers = '4GB';
    ALTER SYSTEM SET effective_cache_size = '12GB';
    ALTER SYSTEM SET maintenance_work_mem = '2GB';
    ALTER SYSTEM SET max_parallel_workers_per_gather = 4;
    ALTER SYSTEM SET max_parallel_maintenance_workers = 4;
    ALTER SYSTEM SET random_page_cost = 1.1;
    ALTER SYSTEM SET effective_io_concurrency = 200;
    
    -- Configure pgvector
    ALTER SYSTEM SET max_wal_size = '2GB';
    ALTER SYSTEM SET min_wal_size = '1GB';

* * *

## 4\. TypeSpec Schema Definition {#typespec-schema}

### Main TypeSpec Configuration

**`schemas/typespec/main.tsp`**

typescript

    import "@typespec/http";
    import "@typespec/rest";
    import "@typespec/openapi3";
    
    using TypeSpec.Http;
    using TypeSpec.Rest;
    
    @service({
      title: "Julep V2 API",
      version: "0.1.0",
    })
    @server("http://localhost:8000", "Development server")
    namespace JulepV2;
    
    // Import sub-schemas
    import "./agents.tsp";
    import "./memory.tsp";
    import "./protocols.tsp";
    
    // Common models
    model UUID extends string {
      @format("uuid")
      @pattern("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
    }
    
    model Timestamp extends string {
      @format("date-time")
    }
    
    model PaginationParams {
      @query limit?: int32 = 20;
      @query offset?: int32 = 0;
    }
    
    model PaginatedResponse<T> {
      items: T[];
      total: int32;
      limit: int32;
      offset: int32;
    }

### Agent TypeSpec Definitions

**`schemas/typespec/agents.tsp`**

typescript

    using TypeSpec.Http;
    using TypeSpec.Rest;
    
    namespace JulepV2.Agents;
    
    enum AgentType {
      conversational,
      task_oriented,
      research,
      coordinator,
    }
    
    model AgentBase {
      name: string;
      description?: string;
      type: AgentType;
      model: string = "gpt-4";
      temperature?: float32 = 0.7;
      maxTokens?: int32 = 4096;
      systemPrompt?: string;
      metadata?: Record<unknown>;
    }
    
    model Agent extends AgentBase {
      @key
      id: UUID;
      
      createdAt: Timestamp;
      updatedAt: Timestamp;
      isActive: boolean = true;
      
      // Protocol configurations
      mcpServers?: MCPServerConfig[];
      a2aCapabilities?: A2AAgentCard;
      
      // Memory configuration
      memoryConfig?: MemoryConfig;
    }
    
    model MCPServerConfig {
      name: string;
      transport: "stdio" | "http";
      command?: string;
      args?: string[];
      env?: Record<string>;
      url?: string;
      headers?: Record<string>;
    }
    
    model A2AAgentCard {
      capabilities: string[];
      protocols: string[] = ["a2a/v1"];
      authentication?: AuthConfig;
      endpoints?: Record<string>;
    }
    
    model AuthConfig {
      type: "none" | "apiKey" | "oauth2" | "jwt";
      config?: Record<unknown>;
    }
    
    model MemoryConfig {
      enableEpisodic: boolean = true;
      enableSemantic: boolean = true;
      enableImplicit: boolean = true;
      enableProspective: boolean = true;
      
      consolidationInterval?: int32 = 3600; // seconds
      decayRate?: float32 = 0.95;
      importanceThreshold?: float32 = 0.3;
    }
    
    @route("/agents")
    interface AgentsAPI {
      @get
      list(...PaginationParams): PaginatedResponse<Agent>;
      
      @post
      create(@body agent: AgentBase): Agent;
      
      @get
      @route("/{id}")
      get(@path id: UUID): Agent;
      
      @put
      @route("/{id}")
      update(@path id: UUID, @body agent: AgentBase): Agent;
      
      @delete
      @route("/{id}")
      delete(@path id: UUID): void;
      
      @post
      @route("/{id}/activate")
      activate(@path id: UUID): Agent;
      
      @post
      @route("/{id}/deactivate")
      deactivate(@path id: UUID): Agent;
    }

### Memory TypeSpec Definitions

**`schemas/typespec/memory.tsp`**

typescript

    using TypeSpec.Http;
    using TypeSpec.Rest;
    
    namespace JulepV2.Memory;
    
    enum MemoryType {
      episodic,
      semantic,
      implicit,
      prospective,
    }
    
    model MemoryBase {
      agentId: UUID;
      type: MemoryType;
      content: string;
      importance: float32 = 0.5;
      metadata?: Record<unknown>;
    }
    
    model Memory extends MemoryBase {
      @key
      id: UUID;
      
      embedding?: float32[];
      createdAt: Timestamp;
      lastAccessedAt: Timestamp;
      accessCount: int32 = 0;
      decayedImportance?: float32;
      
      // Relationships
      relatedMemories?: UUID[];
      sourceContext?: ContextInfo;
    }
    
    model EpisodicMemory extends Memory {
      emotionalValence?: float32; // -1 to 1
      sensoryDetails?: Record<string>;
      temporalContext?: TemporalContext;
    }
    
    model SemanticMemory extends Memory {
      concepts?: string[];
      relationships?: Relationship[];
      confidence: float32 = 1.0;
    }
    
    model ImplicitMemory extends Memory {
      pattern?: string;
      frequency: int32 = 1;
      lastTriggered?: Timestamp;
    }
    
    model ProspectiveMemory extends Memory {
      goalId?: UUID;
      deadline?: Timestamp;
      priority: int32 = 5; // 1-10
      status: "active" | "completed" | "failed" | "deferred";
      dependencies?: UUID[];
    }
    
    model ContextInfo {
      conversationId?: UUID;
      taskId?: UUID;
      environment?: Record<string>;
    }
    
    model TemporalContext {
      timestamp: Timestamp;
      duration?: int32; // seconds
      precedingEvent?: string;
      followingEvent?: string;
    }
    
    model Relationship {
      type: "is_a" | "part_of" | "related_to" | "causes" | "precedes";
      target: string;
      strength: float32 = 1.0;
    }
    
    @route("/memory")
    interface MemoryAPI {
      @post
      store(@body memory: MemoryBase): Memory;
      
      @post
      @route("/search")
      search(@body query: SearchQuery): SearchResults;
      
      @get
      @route("/{id}")
      retrieve(@path id: UUID): Memory;
      
      @post
      @route("/consolidate")
      consolidate(@body params: ConsolidationParams): ConsolidationResult;
    }
    
    model SearchQuery {
      agentId: UUID;
      query: string;
      types?: MemoryType[];
      limit?: int32 = 10;
      threshold?: float32 = 0.7;
      includeDecayed?: boolean = false;
    }
    
    model SearchResults {
      memories: Memory[];
      scores: float32[];
      totalCount: int32;
    }
    
    model ConsolidationParams {
      agentId: UUID;
      types?: MemoryType[];
      minImportance?: float32 = 0.3;
    }
    
    model ConsolidationResult {
      consolidated: int32;
      strengthened: int32;
      decayed: int32;
      removed: int32;
    }

### Protocol TypeSpec Definitions

**`schemas/typespec/protocols.tsp`**

typescript

    using TypeSpec.Http;
    using TypeSpec.Rest;
    
    namespace JulepV2.Protocols;
    
    // MCP Protocol Models
    model MCPTool {
      name: string;
      description?: string;
      inputSchema: Record<unknown>;
      serverId: UUID;
      enabled: boolean = true;
    }
    
    model MCPResource {
      uri: string;
      name: string;
      description?: string;
      mimeType?: string;
      serverId: UUID;
    }
    
    model MCPPrompt {
      name: string;
      description?: string;
      arguments?: PromptArgument[];
      serverId: UUID;
    }
    
    model PromptArgument {
      name: string;
      description?: string;
      required: boolean = false;
      type: "string" | "number" | "boolean";
    }
    
    model MCPMessage {
      @key
      id: UUID;
      
      type: "request" | "response" | "notification";
      method: string;
      params?: Record<unknown>;
      result?: Record<unknown>;
      error?: MCPError;
      
      sourceAgent: UUID;
      targetAgent?: UUID;
      timestamp: Timestamp;
    }
    
    model MCPError {
      code: int32;
      message: string;
      data?: Record<unknown>;
    }
    
    // A2A Protocol Models
    model A2ATask {
      @key
      id: UUID;
      
      clientAgent: UUID;
      remoteAgent: UUID;
      
      name: string;
      description?: string;
      input?: Record<unknown>;
      
      status: TaskStatus;
      progress?: float32; // 0-1
      
      artifacts?: A2AArtifact[];
      messages?: A2AMessage[];
      
      createdAt: Timestamp;
      updatedAt: Timestamp;
      completedAt?: Timestamp;
    }
    
    enum TaskStatus {
      pending,
      running,
      completed,
      failed,
      cancelled,
    }
    
    model A2AArtifact {
      id: UUID;
      name: string;
      type: string;
      content?: string;
      url?: string;
      metadata?: Record<unknown>;
    }
    
    model A2AMessage {
      id: UUID;
      taskId: UUID;
      sender: "client" | "remote";
      content: string;
      parts?: MessagePart[];
      timestamp: Timestamp;
    }
    
    model MessagePart {
      type: "text" | "image" | "file" | "code";
      content: string;
      metadata?: Record<unknown>;
    }
    
    @route("/mcp")
    interface MCPAPI {
      @post
      @route("/tools")
      registerTool(@body tool: MCPTool): MCPTool;
      
      @get
      @route("/tools")
      listTools(@query serverId?: UUID): MCPTool[];
      
      @post
      @route("/execute")
      executeTool(@body execution: ToolExecution): ToolResult;
      
      @post
      @route("/messages")
      sendMessage(@body message: MCPMessage): MCPMessage;
    }
    
    model ToolExecution {
      toolName: string;
      input: Record<unknown>;
      agentId: UUID;
    }
    
    model ToolResult {
      output: Record<unknown>;
      error?: MCPError;
      duration: int32; // milliseconds
    }
    
    @route("/a2a")
    interface A2AAPI {
      @post
      @route("/tasks")
      createTask(@body task: TaskCreation): A2ATask;
      
      @get
      @route("/tasks/{id}")
      getTask(@path id: UUID): A2ATask;
      
      @put
      @route("/tasks/{id}")
      updateTask(@path id: UUID, @body update: TaskUpdate): A2ATask;
      
      @post
      @route("/tasks/{id}/messages")
      sendMessage(@path id: UUID, @body message: MessageCreation): A2AMessage;
      
      @get
      @route("/agents")
      discoverAgents(@query capabilities?: string[]): A2AAgentCard[];
    }
    
    model TaskCreation {
      remoteAgent: UUID;
      name: string;
      description?: string;
      input?: Record<unknown>;
    }
    
    model TaskUpdate {
      status?: TaskStatus;
      progress?: float32;
      artifacts?: A2AArtifact[];
    }
    
    model MessageCreation {
      content: string;
      parts?: MessagePart[];
    }

### TypeSpec Build Configuration

**`schemas/typespec/tspconfig.yaml`**

yaml

    extends: ["@typespec/openapi3/openapi.yaml"]
    emit:
      - "@typespec/openapi3"
      - "@typespec/json-schema"
      - "./typespec-postgres"  # Custom emitter for PostgreSQL
      - "./typespec-python"    # Custom emitter for Python
    
    options:
      "@typespec/openapi3":
        output-file: "{output-dir}/openapi.yaml"
      
      "@typespec/json-schema":
        output-dir: "{output-dir}/json-schemas"
      
      "./typespec-postgres":
        output-file: "{output-dir}/schema.sql"
        schema-prefix: "julep_v2"
      
      "./typespec-python":
        output-dir: "{output-dir}/python"
        package-name: "julep_v2_types"

* * *

## 5\. Database Schema Implementation {#database-schema}

### Core Agent Tables

**`src/database/schema/01_agents.sql`**

sql

    -- Agent main table
    CREATE TABLE agents.agents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        description TEXT,
        type agent_type NOT NULL DEFAULT 'conversational',
        model VARCHAR(100) NOT NULL DEFAULT 'gpt-4',
        temperature FLOAT DEFAULT 0.7 CHECK (temperature >= 0 AND temperature <= 2),
        max_tokens INTEGER DEFAULT 4096 CHECK (max_tokens > 0),
        system_prompt TEXT,
        metadata JSONB DEFAULT '{}',
        
        -- Protocol configurations
        mcp_servers JSONB DEFAULT '[]',
        a2a_capabilities JSONB,
        
        -- Memory configuration
        memory_config JSONB DEFAULT '{
            "enableEpisodic": true,
            "enableSemantic": true,
            "enableImplicit": true,
            "enableProspective": true,
            "consolidationInterval": 3600,
            "decayRate": 0.95,
            "importanceThreshold": 0.3
        }',
        
        -- Metadata
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Constraints
        CONSTRAINT valid_mcp_servers CHECK (jsonb_matches_schema(
            mcp_server_array_schema(), mcp_servers
        )),
        CONSTRAINT valid_a2a_capabilities CHECK (
            a2a_capabilities IS NULL OR 
            jsonb_matches_schema(a2a_capabilities_schema(), a2a_capabilities)
        ),
        CONSTRAINT valid_memory_config CHECK (jsonb_matches_schema(
            memory_config_schema(), memory_config
        ))
    );
    
    -- Indexes for agents
    CREATE INDEX idx_agents_type ON agents.agents(type);
    CREATE INDEX idx_agents_active ON agents.agents(is_active) WHERE is_active = true;
    CREATE INDEX idx_agents_metadata ON agents.agents USING GIN(metadata);
    CREATE INDEX idx_agents_created ON agents.agents(created_at DESC);
    
    -- Update trigger
    CREATE TRIGGER update_agents_updated_at
        BEFORE UPDATE ON agents.agents
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
    
    -- Agent sessions table
    CREATE TABLE agents.sessions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        user_id UUID,
        
        -- Session configuration
        context_window INTEGER DEFAULT 4096,
        max_messages INTEGER DEFAULT 100,
        
        -- State
        is_active BOOLEAN DEFAULT true,
        message_count INTEGER DEFAULT 0,
        total_tokens_used INTEGER DEFAULT 0,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        ended_at TIMESTAMPTZ,
        
        -- Indexes
        CONSTRAINT valid_context_window CHECK (context_window > 0),
        CONSTRAINT valid_session_state CHECK (
            (is_active = true AND ended_at IS NULL) OR
            (is_active = false AND ended_at IS NOT NULL)
        )
    );
    
    CREATE INDEX idx_sessions_agent ON agents.sessions(agent_id);
    CREATE INDEX idx_sessions_user ON agents.sessions(user_id);
    CREATE INDEX idx_sessions_active ON agents.sessions(agent_id, is_active) WHERE is_active = true;
    
    -- Messages table
    CREATE TABLE agents.messages (
        id SERIAL PRIMARY KEY,
        session_id UUID NOT NULL REFERENCES agents.sessions(id) ON DELETE CASCADE,
        role VARCHAR(20) NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'function')),
        content TEXT NOT NULL,
        
        -- Token counting
        token_count INTEGER,
        
        -- Function calls
        function_call JSONB,
        function_response JSONB,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- For memory integration
        embedding vector(1536),
        importance_score FLOAT DEFAULT 0.5
    );
    
    CREATE INDEX idx_messages_session ON agents.messages(session_id, created_at DESC);
    CREATE INDEX idx_messages_embedding ON agents.messages 
        USING hnsw (embedding vector_cosine_ops) 
        WHERE embedding IS NOT NULL;
    
    -- Helper functions for JSON schema validation
    CREATE OR REPLACE FUNCTION mcp_server_array_schema() RETURNS JSONB AS $$
    BEGIN
        RETURN '{
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "transport": {"enum": ["stdio", "http"]},
                    "command": {"type": "string"},
                    "args": {"type": "array", "items": {"type": "string"}},
                    "env": {"type": "object"},
                    "url": {"type": "string"},
                    "headers": {"type": "object"}
                },
                "required": ["name", "transport"]
            }
        }'::jsonb;
    END;
    $$ LANGUAGE plpgsql IMMUTABLE;
    
    CREATE OR REPLACE FUNCTION a2a_capabilities_schema() RETURNS JSONB AS $$
    BEGIN
        RETURN '{
            "type": "object",
            "properties": {
                "capabilities": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "protocols": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["a2a/v1"]
                },
                "authentication": {
                    "type": "object",
                    "properties": {
                        "type": {"enum": ["none", "apiKey", "oauth2", "jwt"]},
                        "config": {"type": "object"}
                    },
                    "required": ["type"]
                },
                "endpoints": {"type": "object"}
            },
            "required": ["capabilities"]
        }'::jsonb;
    END;
    $$ LANGUAGE plpgsql IMMUTABLE;
    
    CREATE OR REPLACE FUNCTION memory_config_schema() RETURNS JSONB AS $$
    BEGIN
        RETURN '{
            "type": "object",
            "properties": {
                "enableEpisodic": {"type": "boolean"},
                "enableSemantic": {"type": "boolean"},
                "enableImplicit": {"type": "boolean"},
                "enableProspective": {"type": "boolean"},
                "consolidationInterval": {"type": "integer", "minimum": 60},
                "decayRate": {"type": "number", "minimum": 0, "maximum": 1},
                "importanceThreshold": {"type": "number", "minimum": 0, "maximum": 1}
            }
        }'::jsonb;
    END;
    $$ LANGUAGE plpgsql IMMUTABLE;

### Memory System Tables

**`src/database/schema/02_memory.sql`**

sql

    -- Base memory table
    CREATE TABLE memory.memories (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        type memory_type NOT NULL,
        
        -- Core content
        content TEXT NOT NULL,
        embedding vector(1536),
        
        -- Importance and decay
        importance FLOAT DEFAULT 0.5 CHECK (importance >= 0 AND importance <= 1),
        decayed_importance FLOAT,
        decay_rate FLOAT DEFAULT 0.95,
        
        -- Access patterns
        access_count INTEGER DEFAULT 0,
        last_accessed_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        source_context JSONB,
        
        -- Timestamps
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Relationships
        related_memories UUID[] DEFAULT '{}',
        
        -- Type-specific data stored in JSONB
        type_data JSONB DEFAULT '{}'
    );
    
    -- Indexes for memory
    CREATE INDEX idx_memories_agent_type ON memory.memories(agent_id, type);
    CREATE INDEX idx_memories_importance ON memory.memories(agent_id, decayed_importance DESC)
        WHERE decayed_importance > 0.3;
    CREATE INDEX idx_memories_embedding ON memory.memories 
        USING hnsw (embedding vector_cosine_ops);
    CREATE INDEX idx_memories_created ON memory.memories(created_at DESC);
    CREATE INDEX idx_memories_metadata ON memory.memories USING GIN(metadata);
    
    -- Episodic memory specific
    CREATE VIEW memory.episodic_memories AS
    SELECT 
        m.*,
        (type_data->>'emotionalValence')::FLOAT as emotional_valence,
        type_data->'sensoryDetails' as sensory_details,
        type_data->'temporalContext' as temporal_context
    FROM memory.memories m
    WHERE m.type = 'episodic';
    
    -- Semantic memory specific
    CREATE VIEW memory.semantic_memories AS
    SELECT 
        m.*,
        (type_data->>'confidence')::FLOAT as confidence,
        type_data->'concepts' as concepts,
        type_data->'relationships' as relationships
    FROM memory.memories m
    WHERE m.type = 'semantic';
    
    -- Implicit memory specific
    CREATE VIEW memory.implicit_memories AS
    SELECT 
        m.*,
        type_data->>'pattern' as pattern,
        (type_data->>'frequency')::INTEGER as frequency,
        (type_data->>'lastTriggered')::TIMESTAMPTZ as last_triggered
    FROM memory.memories m
    WHERE m.type = 'implicit';
    
    -- Prospective memory specific
    CREATE VIEW memory.prospective_memories AS
    SELECT 
        m.*,
        (type_data->>'goalId')::UUID as goal_id,
        (type_data->>'deadline')::TIMESTAMPTZ as deadline,
        (type_data->>'priority')::INTEGER as priority,
        type_data->>'status' as status,
        (type_data->'dependencies')::UUID[] as dependencies
    FROM memory.memories m
    WHERE m.type = 'prospective';
    
    -- Memory relationships table
    CREATE TABLE memory.relationships (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_memory UUID NOT NULL REFERENCES memory.memories(id) ON DELETE CASCADE,
        target_memory UUID NOT NULL REFERENCES memory.memories(id) ON DELETE CASCADE,
        relationship_type VARCHAR(50) NOT NULL,
        strength FLOAT DEFAULT 1.0 CHECK (strength >= 0 AND strength <= 1),
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_relationship UNIQUE(source_memory, target_memory, relationship_type)
    );
    
    CREATE INDEX idx_relationships_source ON memory.relationships(source_memory);
    CREATE INDEX idx_relationships_target ON memory.relationships(target_memory);
    CREATE INDEX idx_relationships_type ON memory.relationships(relationship_type);
    
    -- ConceptNet integration table
    CREATE TABLE memory.concepts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        concept VARCHAR(255) NOT NULL UNIQUE,
        embedding vector(1536),
        conceptnet_uri VARCHAR(500),
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX idx_concepts_embedding ON memory.concepts 
        USING hnsw (embedding vector_cosine_ops);
    
    -- Memory consolidation log
    CREATE TABLE memory.consolidation_log (
        id SERIAL PRIMARY KEY,
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        started_at TIMESTAMPTZ DEFAULT NOW(),
        completed_at TIMESTAMPTZ,
        memories_processed INTEGER DEFAULT 0,
        memories_consolidated INTEGER DEFAULT 0,
        memories_strengthened INTEGER DEFAULT 0,
        memories_decayed INTEGER DEFAULT 0,
        memories_removed INTEGER DEFAULT 0,
        error TEXT,
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX idx_consolidation_agent ON memory.consolidation_log(agent_id, started_at DESC);
    
    -- Memory search function
    CREATE OR REPLACE FUNCTION memory.search_memories(
        p_agent_id UUID,
        p_query TEXT,
        p_types memory_type[] DEFAULT NULL,
        p_limit INTEGER DEFAULT 10,
        p_threshold FLOAT DEFAULT 0.7,
        p_include_decayed BOOLEAN DEFAULT false
    ) RETURNS TABLE(
        memory_id UUID,
        content TEXT,
        type memory_type,
        similarity FLOAT,
        importance FLOAT,
        metadata JSONB
    ) AS $$
    DECLARE
        query_embedding vector(1536);
    BEGIN
        -- Generate embedding for query
        query_embedding := ai_generate_embedding('text-embedding-3-small', p_query);
        
        RETURN QUERY
        SELECT 
            m.id,
            m.content,
            m.type,
            1 - (m.embedding <=> query_embedding) as similarity,
            COALESCE(m.decayed_importance, m.importance) as importance,
            m.metadata
        FROM memory.memories m
        WHERE m.agent_id = p_agent_id
            AND (p_types IS NULL OR m.type = ANY(p_types))
            AND m.embedding IS NOT NULL
            AND (p_include_decayed OR COALESCE(m.decayed_importance, m.importance) > 0.1)
            AND (1 - (m.embedding <=> query_embedding)) > p_threshold
        ORDER BY similarity DESC, importance DESC
        LIMIT p_limit;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Memory consolidation function
    CREATE OR REPLACE FUNCTION memory.consolidate_memories(
        p_agent_id UUID,
        p_types memory_type[] DEFAULT NULL,
        p_min_importance FLOAT DEFAULT 0.3
    ) RETURNS JSONB AS $$
    DECLARE
        v_log_id INTEGER;
        v_processed INTEGER := 0;
        v_consolidated INTEGER := 0;
        v_strengthened INTEGER := 0;
        v_decayed INTEGER := 0;
        v_removed INTEGER := 0;
        v_memory RECORD;
        v_related RECORD;
        v_similarity FLOAT;
    BEGIN
        -- Create consolidation log entry
        INSERT INTO memory.consolidation_log (agent_id)
        VALUES (p_agent_id)
        RETURNING id INTO v_log_id;
        
        -- Process each memory
        FOR v_memory IN
            SELECT * FROM memory.memories
            WHERE agent_id = p_agent_id
                AND (p_types IS NULL OR type = ANY(p_types))
            ORDER BY created_at DESC
        LOOP
            v_processed := v_processed + 1;
            
            -- Apply decay
            UPDATE memory.memories
            SET decayed_importance = importance * POWER(decay_rate, 
                EXTRACT(EPOCH FROM (NOW() - last_accessed_at)) / 86400)
            WHERE id = v_memory.id;
            
            -- Check if memory should be removed
            IF v_memory.decayed_importance < p_min_importance THEN
                DELETE FROM memory.memories WHERE id = v_memory.id;
                v_removed := v_removed + 1;
                CONTINUE;
            END IF;
            
            -- Find similar memories to consolidate
            FOR v_related IN
                SELECT m2.*, 
                       1 - (v_memory.embedding <=> m2.embedding) as similarity
                FROM memory.memories m2
                WHERE m2.agent_id = p_agent_id
                    AND m2.id != v_memory.id
                    AND m2.type = v_memory.type
                    AND 1 - (v_memory.embedding <=> m2.embedding) > 0.9
                ORDER BY similarity DESC
                LIMIT 5
            LOOP
                -- Merge highly similar memories
                IF v_related.similarity > 0.95 THEN
                    -- Strengthen the more important memory
                    IF v_memory.importance > v_related.importance THEN
                        UPDATE memory.memories
                        SET importance = LEAST(1.0, importance + 0.1),
                            access_count = access_count + v_related.access_count
                        WHERE id = v_memory.id;
                        
                        DELETE FROM memory.memories WHERE id = v_related.id;
                        v_consolidated := v_consolidated + 1;
                    END IF;
                ELSE
                    -- Create relationship for related memories
                    INSERT INTO memory.relationships (
                        source_memory, target_memory, 
                        relationship_type, strength
                    ) VALUES (
                        v_memory.id, v_related.id,
                        'similar_to', v_related.similarity
                    ) ON CONFLICT DO NOTHING;
                END IF;
            END LOOP;
        END LOOP;
        
        -- Update consolidation log
        UPDATE memory.consolidation_log
        SET completed_at = NOW(),
            memories_processed = v_processed,
            memories_consolidated = v_consolidated,
            memories_strengthened = v_strengthened,
            memories_decayed = v_decayed,
            memories_removed = v_removed
        WHERE id = v_log_id;
        
        RETURN jsonb_build_object(
            'processed', v_processed,
            'consolidated', v_consolidated,
            'strengthened', v_strengthened,
            'decayed', v_decayed,
            'removed', v_removed
        );
    END;
    $$ LANGUAGE plpgsql;

### Protocol Tables

**`src/database/schema/03_protocols.sql`**

sql

    -- MCP Protocol Tables
    
    -- MCP servers registry
    CREATE TABLE protocols.mcp_servers (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        transport VARCHAR(20) NOT NULL CHECK (transport IN ('stdio', 'http')),
        
        -- Connection details
        command TEXT,
        args TEXT[],
        env JSONB DEFAULT '{}',
        url TEXT,
        headers JSONB DEFAULT '{}',
        
        -- State
        is_active BOOLEAN DEFAULT true,
        last_heartbeat TIMESTAMPTZ,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_server_per_agent UNIQUE(agent_id, name),
        CONSTRAINT valid_transport_config CHECK (
            (transport = 'stdio' AND command IS NOT NULL) OR
            (transport = 'http' AND url IS NOT NULL)
        )
    );
    
    CREATE INDEX idx_mcp_servers_agent ON protocols.mcp_servers(agent_id);
    CREATE INDEX idx_mcp_servers_active ON protocols.mcp_servers(is_active) WHERE is_active = true;
    
    -- MCP tools registry
    CREATE TABLE protocols.mcp_tools (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        input_schema JSONB NOT NULL,
        enabled BOOLEAN DEFAULT true,
        
        -- Usage statistics
        usage_count INTEGER DEFAULT 0,
        last_used_at TIMESTAMPTZ,
        avg_duration_ms INTEGER,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_tool_per_server UNIQUE(server_id, name),
        CONSTRAINT valid_input_schema CHECK (
            jsonb_typeof(input_schema) = 'object' AND
            input_schema ? 'type' AND
            input_schema->>'type' = 'object'
        )
    );
    
    CREATE INDEX idx_mcp_tools_server ON protocols.mcp_tools(server_id);
    CREATE INDEX idx_mcp_tools_enabled ON protocols.mcp_tools(enabled) WHERE enabled = true;
    
    -- MCP resources registry
    CREATE TABLE protocols.mcp_resources (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
        uri TEXT NOT NULL,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        mime_type VARCHAR(100),
        
        -- Caching
        cached_content TEXT,
        cached_at TIMESTAMPTZ,
        cache_ttl INTEGER DEFAULT 3600, -- seconds
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_resource_per_server UNIQUE(server_id, uri)
    );
    
    CREATE INDEX idx_mcp_resources_server ON protocols.mcp_resources(server_id);
    
    -- MCP prompts registry
    CREATE TABLE protocols.mcp_prompts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        arguments JSONB DEFAULT '[]',
        template TEXT NOT NULL,
        
        -- Usage
        usage_count INTEGER DEFAULT 0,
        last_used_at TIMESTAMPTZ,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_prompt_per_server UNIQUE(server_id, name)
    );
    
    CREATE INDEX idx_mcp_prompts_server ON protocols.mcp_prompts(server_id);
    
    -- MCP message log (uses pgmq for actual queuing)
    CREATE TABLE protocols.mcp_messages (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        type VARCHAR(20) NOT NULL CHECK (type IN ('request', 'response', 'notification')),
        method VARCHAR(255) NOT NULL,
        params JSONB,
        result JSONB,
        error JSONB,
        
        source_agent UUID NOT NULL REFERENCES agents.agents(id),
        target_agent UUID REFERENCES agents.agents(id),
        
        -- Message tracking
        correlation_id UUID,
        queue_message_id BIGINT, -- pgmq message id
        
        -- Timing
        created_at TIMESTAMPTZ DEFAULT NOW(),
        processed_at TIMESTAMPTZ,
        duration_ms INTEGER,
        
        -- Status
        status VARCHAR(20) DEFAULT 'pending' CHECK (
            status IN ('pending', 'queued', 'processing', 'completed', 'failed')
        )
    );
    
    CREATE INDEX idx_mcp_messages_source ON protocols.mcp_messages(source_agent);
    CREATE INDEX idx_mcp_messages_target ON protocols.mcp_messages(target_agent);
    CREATE INDEX idx_mcp_messages_correlation ON protocols.mcp_messages(correlation_id);
    CREATE INDEX idx_mcp_messages_created ON protocols.mcp_messages(created_at DESC);
    
    -- A2A Protocol Tables
    
    -- A2A agent registry (AgentCards)
    CREATE TABLE protocols.a2a_agents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        
        -- AgentCard data
        capabilities TEXT[] NOT NULL,
        protocols TEXT[] DEFAULT ARRAY['a2a/v1'],
        authentication JSONB,
        endpoints JSONB DEFAULT '{}',
        
        -- Discovery
        is_public BOOLEAN DEFAULT false,
        discovery_metadata JSONB DEFAULT '{}',
        
        -- State
        is_active BOOLEAN DEFAULT true,
        last_seen TIMESTAMPTZ DEFAULT NOW(),
        
        -- Metadata
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        
        CONSTRAINT unique_a2a_agent UNIQUE(agent_id)
    );
    
    CREATE INDEX idx_a2a_agents_public ON protocols.a2a_agents(is_public) WHERE is_public = true;
    CREATE INDEX idx_a2a_agents_capabilities ON protocols.a2a_agents USING GIN(capabilities);
    
    -- A2A tasks
    CREATE TABLE protocols.a2a_tasks (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        client_agent UUID NOT NULL REFERENCES agents.agents(id),
        remote_agent UUID NOT NULL REFERENCES agents.agents(id),
        
        -- Task details
        name VARCHAR(255) NOT NULL,
        description TEXT,
        input JSONB,
        
        -- Status tracking
        status task_status NOT NULL DEFAULT 'pending',
        progress FLOAT DEFAULT 0 CHECK (progress >= 0 AND progress <= 1),
        
        -- Timing
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        started_at TIMESTAMPTZ,
        completed_at TIMESTAMPTZ,
        
        -- Results
        output JSONB,
        error JSONB,
        
        -- Metadata
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX idx_a2a_tasks_client ON protocols.a2a_tasks(client_agent);
    CREATE INDEX idx_a2a_tasks_remote ON protocols.a2a_tasks(remote_agent);
    CREATE INDEX idx_a2a_tasks_status ON protocols.a2a_tasks(status);
    CREATE INDEX idx_a2a_tasks_created ON protocols.a2a_tasks(created_at DESC);
    
    -- A2A artifacts
    CREATE TABLE protocols.a2a_artifacts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        task_id UUID NOT NULL REFERENCES protocols.a2a_tasks(id) ON DELETE CASCADE,
        
        name VARCHAR(255) NOT NULL,
        type VARCHAR(100) NOT NULL,
        content TEXT,
        url TEXT,
        size_bytes BIGINT,
        
        -- Metadata
        metadata JSONB DEFAULT '{}',
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX idx_a2a_artifacts_task ON protocols.a2a_artifacts(task_id);
    
    -- A2A messages
    CREATE TABLE protocols.a2a_messages (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        task_id UUID NOT NULL REFERENCES protocols.a2a_tasks(id) ON DELETE CASCADE,
        sender VARCHAR(10) NOT NULL CHECK (sender IN ('client', 'remote')),
        
        content TEXT NOT NULL,
        parts JSONB DEFAULT '[]',
        
        -- Tracking
        queue_message_id BIGINT, -- pgmq message id
        
        -- Timestamps
        created_at TIMESTAMPTZ DEFAULT NOW(),
        delivered_at TIMESTAMPTZ
    );
    
    CREATE INDEX idx_a2a_messages_task ON protocols.a2a_messages(task_id, created_at);
    
    -- Protocol integration functions
    
    -- Function to execute MCP tool
    CREATE OR REPLACE FUNCTION protocols.execute_mcp_tool(
        p_tool_name VARCHAR,
        p_input JSONB,
        p_agent_id UUID
    ) RETURNS JSONB AS $$
    DECLARE
        v_tool RECORD;
        v_message_id UUID;
        v_result JSONB;
        v_start_time TIMESTAMPTZ;
        v_duration_ms INTEGER;
    BEGIN
        v_start_time := clock_timestamp();
        
        -- Find the tool
        SELECT t.*, s.transport, s.url, s.command, s.args
        INTO v_tool
        FROM protocols.mcp_tools t
        JOIN protocols.mcp_servers s ON t.server_id = s.id
        WHERE t.name = p_tool_name
            AND t.enabled = true
            AND s.is_active = true
            AND s.agent_id = p_agent_id
        LIMIT 1;
        
        IF NOT FOUND THEN
            RAISE EXCEPTION 'Tool % not found for agent %', p_tool_name, p_agent_id;
        END IF;
        
        -- Validate input against schema
        IF NOT jsonb_matches_schema(v_tool.input_schema, p_input) THEN
            RAISE EXCEPTION 'Invalid input for tool %', p_tool_name;
        END IF;
        
        -- Create MCP message
        INSERT INTO protocols.mcp_messages (
            type, method, params, source_agent
        ) VALUES (
            'request', 'tools/execute', 
            jsonb_build_object('tool', p_tool_name, 'input', p_input),
            p_agent_id
        ) RETURNING id INTO v_message_id;
        
        -- Queue the message
        SELECT pgmq.send(
            'mcp_messages',
            jsonb_build_object(
                'message_id', v_message_id,
                'tool_id', v_tool.id,
                'server_id', v_tool.server_id,
                'input', p_input
            )
        );
        
        -- For prototype, simulate execution
        -- In production, this would wait for actual execution
        v_result := jsonb_build_object(
            'output', jsonb_build_object('result', 'Tool executed successfully'),
            'duration_ms', 100
        );
        
        -- Update tool usage statistics
        v_duration_ms := EXTRACT(MILLISECONDS FROM clock_timestamp() - v_start_time);
        
        UPDATE protocols.mcp_tools
        SET usage_count = usage_count + 1,
            last_used_at = NOW(),
            avg_duration_ms = CASE
                WHEN avg_duration_ms IS NULL THEN v_duration_ms
                ELSE (avg_duration_ms * usage_count + v_duration_ms) / (usage_count + 1)
            END
        WHERE id = v_tool.id;
        
        -- Update message
        UPDATE protocols.mcp_messages
        SET status = 'completed',
            result = v_result,
            processed_at = NOW(),
            duration_ms = v_duration_ms
        WHERE id = v_message_id;
        
        RETURN v_result;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Function to discover A2A agents
    CREATE OR REPLACE FUNCTION protocols.discover_a2a_agents(
        p_capabilities TEXT[] DEFAULT NULL
    ) RETURNS TABLE(
        agent_id UUID,
        name VARCHAR,
        capabilities TEXT[],
        protocols TEXT[],
        endpoints JSONB
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT 
            a.id,
            ag.name,
            a.capabilities,
            a.protocols,
            a.endpoints
        FROM protocols.a2a_agents a
        JOIN agents.agents ag ON a.agent_id = ag.id
        WHERE a.is_public = true
            AND a.is_active = true
            AND ag.is_active = true
            AND (p_capabilities IS NULL OR 
                 a.capabilities && p_capabilities) -- Array overlap
        ORDER BY a.last_seen DESC;
    END;
    $$ LANGUAGE plpgsql;

### Workflow Tables (DBOS)

**`src/database/schema/04_workflows.sql`**

sql

    -- DBOS workflow tables (simplified version)
    -- In production, use actual DBOS schema
    
    -- Workflow definitions
    CREATE TABLE workflows.workflow_definitions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL UNIQUE,
        version INTEGER NOT NULL DEFAULT 1,
        
        -- Workflow configuration
        steps JSONB NOT NULL,
        retry_policy JSONB DEFAULT '{
            "max_attempts": 3,
            "backoff_multiplier": 2,
            "initial_interval": 1000
        }',
        
        -- Metadata
        description TEXT,
        tags TEXT[] DEFAULT '{}',
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    CREATE INDEX idx_workflow_defs_name ON workflows.workflow_definitions(name);
    CREATE INDEX idx_workflow_defs_active ON workflows.workflow_definitions(is_active) WHERE is_active = true;
    
    -- Workflow instances
    CREATE TABLE workflows.workflow_instances (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        definition_id UUID NOT NULL REFERENCES workflows.workflow_definitions(id),
        agent_id UUID NOT NULL REFERENCES agents.agents(id),
        
        -- State
        status VARCHAR(20) DEFAULT 'pending' CHECK (
            status IN ('pending', 'running', 'completed', 'failed', 'cancelled', 'suspended')
        ),
        current_step VARCHAR(255),
        context JSONB DEFAULT '{}',
        
        -- Timing
        created_at TIMESTAMPTZ DEFAULT NOW(),
        started_at TIMESTAMPTZ,
        completed_at TIMESTAMPTZ,
        
        -- Error handling
        error JSONB,
        retry_count INTEGER DEFAULT 0,
        
        -- Results
        output JSONB,
        
        -- Metadata
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX idx_workflow_instances_agent ON workflows.workflow_instances(agent_id);
    CREATE INDEX idx_workflow_instances_status ON workflows.workflow_instances(status);
    CREATE INDEX idx_workflow_instances_created ON workflows.workflow_instances(created_at DESC);
    
    -- Workflow step executions
    CREATE TABLE workflows.step_executions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        instance_id UUID NOT NULL REFERENCES workflows.workflow_instances(id) ON DELETE CASCADE,
        step_name VARCHAR(255) NOT NULL,
        
        -- Execution details
        status VARCHAR(20) DEFAULT 'pending' CHECK (
            status IN ('pending', 'running', 'completed', 'failed', 'skipped')
        ),
        input JSONB,
        output JSONB,
        error JSONB,
        
        -- Timing
        started_at TIMESTAMPTZ,
        completed_at TIMESTAMPTZ,
        duration_ms INTEGER,
        
        -- Metadata
        metadata JSONB DEFAULT '{}'
    );
    
    CREATE INDEX idx_step_executions_instance ON workflows.step_executions(instance_id);
    CREATE INDEX idx_step_executions_status ON workflows.step_executions(status);
    
    -- Common workflow: Memory consolidation
    INSERT INTO workflows.workflow_definitions (name, description, steps) VALUES (
        'memory_consolidation',
        'Consolidate and organize agent memories',
        '{
            "steps": [
                {
                    "name": "fetch_memories",
                    "type": "function",
                    "function": "memory.fetch_recent_memories",
                    "next": "calculate_importance"
                },
                {
                    "name": "calculate_importance",
                    "type": "function", 
                    "function": "memory.calculate_importance_scores",
                    "next": "apply_decay"
                },
                {
                    "name": "apply_decay",
                    "type": "function",
                    "function": "memory.apply_decay_function",
                    "next": "find_similar"
                },
                {
                    "name": "find_similar",
                    "type": "function",
                    "function": "memory.find_similar_memories",
                    "next": "consolidate"
                },
                {
                    "name": "consolidate",
                    "type": "function",
                    "function": "memory.consolidate_similar",
                    "next": "update_graph"
                },
                {
                    "name": "update_graph",
                    "type": "function",
                    "function": "memory.update_relationship_graph",
                    "next": null
                }
            ]
        }'::jsonb
    );
    
    -- Common workflow: Agent conversation
    INSERT INTO workflows.workflow_definitions (name, description, steps) VALUES (
        'agent_conversation',
        'Handle a conversation turn with memory integration',
        '{
            "steps": [
                {
                    "name": "retrieve_context",
                    "type": "function",
                    "function": "memory.retrieve_relevant_memories",
                    "next": "generate_response"
                },
                {
                    "name": "generate_response",
                    "type": "function",
                    "function": "agents.generate_llm_response",
                    "next": "extract_memories"
                },
                {
                    "name": "extract_memories",
                    "type": "function",
                    "function": "memory.extract_memories_from_response",
                    "next": "store_memories"
                },
                {
                    "name": "store_memories",
                    "type": "function",
                    "function": "memory.store_new_memories",
                    "next": "update_goals"
                },
                {
                    "name": "update_goals",
                    "type": "function",
                    "function": "memory.update_prospective_memories",
                    "next": null
                }
            ]
        }'::jsonb
    );

### Helper Functions and Triggers

**`src/database/schema/05_functions.sql`**

sql

    -- Update timestamp trigger function
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Token counting function (placeholder - use tiktoken in Python)
    CREATE OR REPLACE FUNCTION count_tokens(
        p_model VARCHAR,
        p_text TEXT
    ) RETURNS INTEGER AS $$
    BEGIN
        -- Rough approximation: 1 token per 4 characters
        -- In production, call Python tiktoken via plpython3u
        RETURN CEIL(LENGTH(p_text) / 4.0);
    END;
    $$ LANGUAGE plpgsql;
    
    -- Generate embedding with caching
    CREATE OR REPLACE FUNCTION generate_embedding_cached(
        p_model VARCHAR,
        p_content TEXT
    ) RETURNS vector(1536) AS $$
    DECLARE
        v_cache_key VARCHAR;
        v_embedding vector(1536);
    BEGIN
        -- Create cache key
        v_cache_key := MD5(p_model || ':' || p_content);
        
        -- Check cache (in production, use a proper cache table)
        -- For now, always generate
        v_embedding := ai_generate_embedding(p_model, p_content);
        
        RETURN v_embedding;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Agent activity tracking
    CREATE OR REPLACE FUNCTION track_agent_activity()
    RETURNS TRIGGER AS $$
    BEGIN
        -- Update agent last activity
        UPDATE agents.agents
        SET updated_at = NOW(),
            metadata = metadata || jsonb_build_object(
                'last_activity', NOW(),
                'total_sessions', COALESCE((metadata->>'total_sessions')::int, 0) + 1
            )
        WHERE id = NEW.agent_id;
        
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    
    CREATE TRIGGER track_session_activity
        AFTER INSERT ON agents.sessions
        FOR EACH ROW
        EXECUTE FUNCTION track_agent_activity();
    
    -- Memory importance calculation
    CREATE OR REPLACE FUNCTION calculate_memory_importance(
        p_content TEXT,
        p_emotional_valence FLOAT DEFAULT NULL,
        p_access_count INTEGER DEFAULT 0,
        p_age_days FLOAT DEFAULT 0
    ) RETURNS FLOAT AS $$
    DECLARE
        v_base_importance FLOAT;
        v_emotion_factor FLOAT;
        v_access_factor FLOAT;
        v_recency_factor FLOAT;
    BEGIN
        -- Base importance from content length and complexity
        v_base_importance := LEAST(1.0, LENGTH(p_content) / 1000.0);
        
        -- Emotional factor (stronger emotions = higher importance)
        v_emotion_factor := CASE
            WHEN p_emotional_valence IS NULL THEN 1.0
            ELSE 1.0 + ABS(p_emotional_valence) * 0.5
        END;
        
        -- Access factor (more access = higher importance)
        v_access_factor := 1.0 + LOG(GREATEST(1, p_access_count)) * 0.1;
        
        -- Recency factor (newer = higher importance)
        v_recency_factor := EXP(-p_age_days / 30.0); -- Decay over 30 days
        
        -- Combine factors
        RETURN LEAST(1.0, v_base_importance * v_emotion_factor * 
                          v_access_factor * v_recency_factor);
    END;
    $$ LANGUAGE plpgsql;
    
    -- Workflow orchestration helper
    CREATE OR REPLACE FUNCTION execute_workflow_step(
        p_instance_id UUID,
        p_step_name VARCHAR
    ) RETURNS JSONB AS $$
    DECLARE
        v_workflow RECORD;
        v_step JSONB;
        v_result JSONB;
        v_step_id UUID;
    BEGIN
        -- Get workflow instance and current step
        SELECT wi.*, wd.steps
        INTO v_workflow
        FROM workflows.workflow_instances wi
        JOIN workflows.workflow_definitions wd ON wi.definition_id = wd.id
        WHERE wi.id = p_instance_id;
        
        -- Find step definition
        SELECT value INTO v_step
        FROM jsonb_array_elements(v_workflow.steps->'steps') 
        WHERE value->>'name' = p_step_name;
        
        IF v_step IS NULL THEN
            RAISE EXCEPTION 'Step % not found in workflow', p_step_name;
        END IF;
        
        -- Create step execution record
        INSERT INTO workflows.step_executions (
            instance_id, step_name, status, started_at
        ) VALUES (
            p_instance_id, p_step_name, 'running', NOW()
        ) RETURNING id INTO v_step_id;
        
        -- Execute step based on type
        CASE v_step->>'type'
            WHEN 'function' THEN
                -- Execute function (simplified - in production use DBOS)
                v_result := jsonb_build_object('output', 'Function executed');
            WHEN 'tool' THEN
                -- Execute MCP tool
                v_result := protocols.execute_mcp_tool(
                    v_step->>'tool', 
                    v_step->'input', 
                    v_workflow.agent_id
                );
            ELSE
                RAISE EXCEPTION 'Unknown step type: %', v_step->>'type';
        END CASE;
        
        -- Update step execution
        UPDATE workflows.step_executions
        SET status = 'completed',
            output = v_result,
            completed_at = NOW(),
            duration_ms = EXTRACT(MILLISECONDS FROM NOW() - started_at)
        WHERE id = v_step_id;
        
        -- Update workflow instance
        UPDATE workflows.workflow_instances
        SET current_step = v_step->>'next',
            context = context || v_result
        WHERE id = p_instance_id;
        
        RETURN v_result;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Create materialized views for performance
    
    -- Active agents summary
    CREATE MATERIALIZED VIEW agents.active_agents_summary AS
    SELECT 
        a.id,
        a.name,
        a.type,
        COUNT(DISTINCT s.id) as total_sessions,
        COUNT(DISTINCT m.id) as total_messages,
        MAX(m.created_at) as last_activity,
        AVG(LENGTH(m.content)) as avg_message_length
    FROM agents.agents a
    LEFT JOIN agents.sessions s ON a.id = s.agent_id
    LEFT JOIN agents.messages m ON s.id = m.session_id
    WHERE a.is_active = true
    GROUP BY a.id, a.name, a.type;
    
    CREATE UNIQUE INDEX idx_active_agents_summary_id ON agents.active_agents_summary(id);
    
    -- Memory statistics
    CREATE MATERIALIZED VIEW memory.memory_statistics AS
    SELECT 
        agent_id,
        type,
        COUNT(*) as count,
        AVG(importance) as avg_importance,
        AVG(access_count) as avg_access_count,
        MAX(created_at) as newest_memory,
        MIN(created_at) as oldest_memory
    FROM memory.memories
    GROUP BY agent_id, type;
    
    CREATE UNIQUE INDEX idx_memory_statistics ON memory.memory_statistics(agent_id, type);
    
    -- Refresh materialized views function
    CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
    RETURNS void AS $$
    BEGIN
        REFRESH MATERIALIZED VIEW CONCURRENTLY agents.active_agents_summary;
        REFRESH MATERIALIZED VIEW CONCURRENTLY memory.memory_statistics;
    END;
    $$ LANGUAGE plpgsql;

* * *

## 6\. Memory System Implementation {#memory-system}

### Base Memory Module

**`src/memory/__init__.py`**

python

    from typing import List, Optional, Dict, Any, Union
    from enum import Enum
    from datetime import datetime
    from pydantic import BaseModel, Field
    import numpy as np
    
    class MemoryType(str, Enum):
        EPISODIC = "episodic"
        SEMANTIC = "semantic"
        IMPLICIT = "implicit"
        PROSPECTIVE = "prospective"
    
    class MemoryBase(BaseModel):
        agent_id: str
        type: MemoryType
        content: str
        importance: float = Field(default=0.5, ge=0, le=1)
        metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Memory(MemoryBase):
        id: str
        embedding: Optional[List[float]] = None
        created_at: datetime
        last_accessed_at: datetime
        access_count: int = 0
        decayed_importance: Optional[float] = None
        related_memories: List[str] = Field(default_factory=list)
        source_context: Optional[Dict[str, Any]] = None
    
    class EpisodicMemory(Memory):
        emotional_valence: Optional[float] = Field(None, ge=-1, le=1)
        sensory_details: Optional[Dict[str, Any]] = None
        temporal_context: Optional[Dict[str, Any]] = None
    
    class SemanticMemory(Memory):
        concepts: List[str] = Field(default_factory=list)
        relationships: List[Dict[str, Any]] = Field(default_factory=list)
        confidence: float = Field(default=1.0, ge=0, le=1)
    
    class ImplicitMemory(Memory):
        pattern: Optional[str] = None
        frequency: int = 1
        last_triggered: Optional[datetime] = None
    
    class ProspectiveMemory(Memory):
        goal_id: Optional[str] = None
        deadline: Optional[datetime] = None
        priority: int = Field(default=5, ge=1, le=10)
        status: str = Field(default="active")
        dependencies: List[str] = Field(default_factory=list)

### Episodic Memory Implementation

**`src/memory/episodic.py`**

python

    import asyncio
    from typing import List, Optional, Dict, Any
    from datetime import datetime, timedelta
    import numpy as np
    from sqlalchemy import select, and_, func
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.memory import EpisodicMemory, MemoryType
    from src.utils.embeddings import generate_embedding
    from src.utils.emotions import analyze_emotional_content
    
    class EpisodicMemoryManager:
        def __init__(self, db_session: AsyncSession):
            self.db = db_session
        
        async def store_episode(
            self,
            agent_id: str,
            content: str,
            context: Dict[str, Any],
            emotional_valence: Optional[float] = None,
            sensory_details: Optional[Dict[str, Any]] = None
        ) -> EpisodicMemory:
            """Store a new episodic memory with full context."""
            
            # Generate embedding
            embedding = await generate_embedding(content)
            
            # Analyze emotional content if not provided
            if emotional_valence is None:
                emotional_valence = await analyze_emotional_content(content)
            
            # Calculate initial importance
            importance = self._calculate_importance(
                content, emotional_valence, context
            )
            
            # Create temporal context
            temporal_context = {
                "timestamp": datetime.utcnow().isoformat(),
                "day_of_week": datetime.utcnow().strftime("%A"),
                "time_of_day": self._get_time_of_day(),
                "context_before": context.get("previous_event"),
                "context_after": None  # Will be updated later
            }
            
            # Store in database
            query = """
            INSERT INTO memory.memories (
                agent_id, type, content, embedding, importance,
                type_data, source_context, metadata
            ) VALUES (
                :agent_id, :type, :content, :embedding, :importance,
                :type_data, :source_context, :metadata
            ) RETURNING *
            """
            
            type_data = {
                "emotionalValence": emotional_valence,
                "sensoryDetails": sensory_details or {},
                "temporalContext": temporal_context
            }
            
            result = await self.db.execute(
                query,
                {
                    "agent_id": agent_id,
                    "type": MemoryType.EPISODIC,
                    "content": content,
                    "embedding": embedding,
                    "importance": importance,
                    "type_data": type_data,
                    "source_context": context,
                    "metadata": {"tags": self._extract_tags(content)}
                }
            )
            
            memory_data = result.fetchone()
            
            # Find and link related memories
            related = await self._find_related_episodes(
                agent_id, embedding, memory_data["id"]
            )
            
            if related:
                await self._link_memories(memory_data["id"], related)
            
            return EpisodicMemory(**memory_data)
        
        async def retrieve_episodes(
            self,
            agent_id: str,
            query: str,
            limit: int = 10,
            time_range: Optional[timedelta] = None,
            emotional_filter: Optional[str] = None
        ) -> List[EpisodicMemory]:
            """Retrieve relevant episodic memories."""
            
            query_embedding = await generate_embedding(query)
            
            sql = """
            SELECT m.*, 
                   1 - (m.embedding <=> :query_embedding) as similarity
            FROM memory.memories m
            WHERE m.agent_id = :agent_id
              AND m.type = 'episodic'
              AND COALESCE(m.decayed_importance, m.importance) > 0.2
            """
            
            params = {
                "agent_id": agent_id,
                "query_embedding": query_embedding
            }
            
            # Add time range filter
            if time_range:
                cutoff = datetime.utcnow() - time_range
                sql += " AND m.created_at > :cutoff"
                params["cutoff"] = cutoff
            
            # Add emotional filter
            if emotional_filter:
                if emotional_filter == "positive":
                    sql += " AND (m.type_data->>'emotionalValence')::float > 0"
                elif emotional_filter == "negative":
                    sql += " AND (m.type_data->>'emotionalValence')::float < 0"
            
            sql += """
            ORDER BY similarity DESC, m.importance DESC
            LIMIT :limit
            """
            params["limit"] = limit
            
            result = await self.db.execute(sql, params)
            memories = result.fetchall()
            
            # Update access counts
            for memory in memories:
                await self._update_access(memory["id"])
            
            return [EpisodicMemory(**m) for m in memories]
        
        async def consolidate_episodes(
            self,
            agent_id: str,
            min_similarity: float = 0.85
        ) -> Dict[str, int]:
            """Consolidate similar episodic memories."""
            
            # Get all active episodic memories
            sql = """
            SELECT id, content, embedding, importance, type_data
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND type = 'episodic'
              AND COALESCE(decayed_importance, importance) > 0.3
            ORDER BY created_at DESC
            """
            
            result = await self.db.execute(sql, {"agent_id": agent_id})
            memories = result.fetchall()
            
            consolidated = 0
            strengthened = 0
            
            # Compare each memory with others
            for i, mem1 in enumerate(memories):
                for mem2 in memories[i+1:]:
                    similarity = 1 - np.dot(
                        np.array(mem1["embedding"]), 
                        np.array(mem2["embedding"])
                    )
                    
                    if similarity > min_similarity:
                        # Check if memories are from similar time periods
                        time_diff = abs(
                            datetime.fromisoformat(
                                mem1["type_data"]["temporalContext"]["timestamp"]
                            ) - datetime.fromisoformat(
                                mem2["type_data"]["temporalContext"]["timestamp"]
                            )
                        )
                        
                        if time_diff < timedelta(hours=24):
                            # Merge memories
                            await self._merge_episodes(mem1, mem2)
                            consolidated += 1
                        else:
                            # Link as related but don't merge
                            await self._link_memories(
                                mem1["id"], [mem2["id"]], 
                                relationship_type="similar_episode"
                            )
                            strengthened += 1
            
            return {
                "consolidated": consolidated,
                "strengthened": strengthened
            }
        
        async def _find_related_episodes(
            self,
            agent_id: str,
            embedding: List[float],
            exclude_id: str,
            limit: int = 5
        ) -> List[str]:
            """Find episodes similar to the given embedding."""
            
            sql = """
            SELECT id
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND type = 'episodic'
              AND id != :exclude_id
              AND 1 - (embedding <=> :embedding) > 0.7
            ORDER BY embedding <=> :embedding
            LIMIT :limit
            """
            
            result = await self.db.execute(
                sql,
                {
                    "agent_id": agent_id,
                    "embedding": embedding,
                    "exclude_id": exclude_id,
                    "limit": limit
                }
            )
            
            return [row["id"] for row in result.fetchall()]
        
        async def _merge_episodes(
            self,
            memory1: Dict[str, Any],
            memory2: Dict[str, Any]
        ):
            """Merge two similar episodic memories."""
            
            # Create merged content
            merged_content = f"{memory1['content']}\n\n[Consolidated with:]\n{memory2['content']}"
            
            # Average emotional valence
            valence1 = float(memory1["type_data"].get("emotionalValence", 0))
            valence2 = float(memory2["type_data"].get("emotionalValence", 0))
            merged_valence = (valence1 + valence2) / 2
            
            # Combine sensory details
            sensory1 = memory1["type_data"].get("sensoryDetails", {})
            sensory2 = memory2["type_data"].get("sensoryDetails", {})
            merged_sensory = {**sensory1, **sensory2}
            
            # Update the more important memory
            if memory1["importance"] >= memory2["importance"]:
                keep_id, remove_id = memory1["id"], memory2["id"]
            else:
                keep_id, remove_id = memory2["id"], memory1["id"]
            
            # Update kept memory
            sql = """
            UPDATE memory.memories
            SET content = :content,
                importance = LEAST(1.0, importance + 0.1),
                type_data = type_data || :new_data
            WHERE id = :id
            """
            
            await self.db.execute(
                sql,
                {
                    "content": merged_content,
                    "new_data": {
                        "emotionalValence": merged_valence,
                        "sensoryDetails": merged_sensory,
                        "consolidated": True
                    },
                    "id": keep_id
                }
            )
            
            # Remove the other memory
            await self.db.execute(
                "DELETE FROM memory.memories WHERE id = :id",
                {"id": remove_id}
            )
        
        def _calculate_importance(
            self,
            content: str,
            emotional_valence: float,
            context: Dict[str, Any]
        ) -> float:
            """Calculate initial importance score for episodic memory."""
            
            # Base importance from content length
            base = min(1.0, len(content) / 500)
            
            # Emotional factor
            emotion_factor = 1.0 + abs(emotional_valence) * 0.5
            
            # Context factors
            context_factor = 1.0
            if context.get("is_goal_related"):
                context_factor *= 1.5
            if context.get("involves_other_agents"):
                context_factor *= 1.3
            
            return min(1.0, base * emotion_factor * context_factor)
        
        def _get_time_of_day(self) -> str:
            """Get descriptive time of day."""
            hour = datetime.utcnow().hour
            if 5 <= hour < 12:
                return "morning"
            elif 12 <= hour < 17:
                return "afternoon"
            elif 17 <= hour < 21:
                return "evening"
            else:
                return "night"
        
        def _extract_tags(self, content: str) -> List[str]:
            """Extract relevant tags from content."""
            # Simple implementation - in production use NLP
            tags = []
            
            # Extract mentioned entities, actions, emotions
            # This is a placeholder implementation
            if "goal" in content.lower():
                tags.append("goal-related")
            if any(word in content.lower() for word in ["happy", "joy", "excited"]):
                tags.append("positive-emotion")
            if any(word in content.lower() for word in ["sad", "angry", "frustrated"]):
                tags.append("negative-emotion")
            
            return tags
        
        async def _update_access(self, memory_id: str):
            """Update memory access statistics."""
            sql = """
            UPDATE memory.memories
            SET access_count = access_count + 1,
                last_accessed_at = NOW()
            WHERE id = :id
            """
            await self.db.execute(sql, {"id": memory_id})
        
        async def _link_memories(
            self,
            source_id: str,
            target_ids: List[str],
            relationship_type: str = "related_to"
        ):
            """Create relationships between memories."""
            for target_id in target_ids:
                sql = """
                INSERT INTO memory.relationships (
                    source_memory, target_memory, relationship_type
                ) VALUES (:source, :target, :type)
                ON CONFLICT DO NOTHING
                """
                
                await self.db.execute(
                    sql,
                    {
                        "source": source_id,
                        "target": target_id,
                        "type": relationship_type
                    }
                )

### Semantic Memory Implementation

**`src/memory/semantic.py`**

python

    import asyncio
    from typing import List, Optional, Dict, Any, Tuple
    from datetime import datetime
    import numpy as np
    from sqlalchemy.ext.asyncio import AsyncSession
    import networkx as nx
    
    from src.database import get_db
    from src.memory import SemanticMemory, MemoryType
    from src.utils.embeddings import generate_embedding
    from src.utils.knowledge import extract_concepts, query_conceptnet
    
    class SemanticMemoryManager:
        def __init__(self, db_session: AsyncSession):
            self.db = db_session
            self.concept_graph = nx.DiGraph()
        
        async def store_fact(
            self,
            agent_id: str,
            content: str,
            concepts: Optional[List[str]] = None,
            confidence: float = 1.0,
            source: Optional[str] = None
        ) -> SemanticMemory:
            """Store a semantic fact with concept extraction."""
            
            # Extract concepts if not provided
            if concepts is None:
                concepts = await extract_concepts(content)
            
            # Generate embedding
            embedding = await generate_embedding(content)
            
            # Build relationships
            relationships = await self._build_concept_relationships(concepts)
            
            # Calculate importance based on concept centrality
            importance = self._calculate_semantic_importance(
                concepts, relationships, confidence
            )
            
            # Store in database
            query = """
            INSERT INTO memory.memories (
                agent_id, type, content, embedding, importance,
                type_data, metadata
            ) VALUES (
                :agent_id, :type, :content, :embedding, :importance,
                :type_data, :metadata
            ) RETURNING *
            """
            
            type_data = {
                "concepts": concepts,
                "relationships": relationships,
                "confidence": confidence
            }
            
            metadata = {
                "source": source or "direct_learning",
                "concept_count": len(concepts),
                "verified": False
            }
            
            result = await self.db.execute(
                query,
                {
                    "agent_id": agent_id,
                    "type": MemoryType.SEMANTIC,
                    "content": content,
                    "embedding": embedding,
                    "importance": importance,
                    "type_data": type_data,
                    "metadata": metadata
                }
            )
            
            memory_data = result.fetchone()
            
            # Update concept graph
            await self._update_concept_graph(agent_id, concepts, relationships)
            
            # Link to related facts
            related = await self._find_related_facts(
                agent_id, embedding, concepts, memory_data["id"]
            )
            
            if related:
                await self._link_facts(memory_data["id"], related)
            
            return SemanticMemory(**memory_data)
        
        async def query_knowledge(
            self,
            agent_id: str,
            query: str,
            concept_filter: Optional[List[str]] = None,
            min_confidence: float = 0.7
        ) -> List[SemanticMemory]:
            """Query semantic knowledge base."""
            
            # Extract concepts from query
            query_concepts = await extract_concepts(query)
            query_embedding = await generate_embedding(query)
            
            sql = """
            WITH concept_matches AS (
                SELECT m.id,
                       ARRAY_LENGTH(
                           ARRAY(
                               SELECT unnest(ARRAY[:query_concepts]::text[])
                               INTERSECT
                               SELECT unnest((m.type_data->'concepts')::text[])
                           ), 1
                       ) as concept_overlap
                FROM memory.memories m
                WHERE m.agent_id = :agent_id
                  AND m.type = 'semantic'
            )
            SELECT m.*,
                   1 - (m.embedding <=> :query_embedding) as similarity,
                   cm.concept_overlap
            FROM memory.memories m
            JOIN concept_matches cm ON m.id = cm.id
            WHERE (m.type_data->>'confidence')::float >= :min_confidence
            """
            
            params = {
                "agent_id": agent_id,
                "query_embedding": query_embedding,
                "query_concepts": query_concepts,
                "min_confidence": min_confidence
            }
            
            # Add concept filter
            if concept_filter:
                sql += """
                  AND m.type_data->'concepts' ?| ARRAY[:concept_filter]::text[]
                """
                params["concept_filter"] = concept_filter
            
            sql += """
            ORDER BY 
                cm.concept_overlap DESC,
                similarity DESC,
                m.importance DESC
            LIMIT 20
            """
            
            result = await self.db.execute(sql, params)
            facts = result.fetchall()
            
            # Post-process results with inference
            enriched_facts = await self._apply_inference(facts, query_concepts)
            
            return [SemanticMemory(**f) for f in enriched_facts]
        
        async def build_knowledge_graph(
            self,
            agent_id: str,
            max_depth: int = 3
        ) -> nx.DiGraph:
            """Build a knowledge graph from semantic memories."""
            
            # Load all semantic memories
            sql = """
            SELECT id, content, type_data
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND type = 'semantic'
              AND COALESCE(decayed_importance, importance) > 0.3
            """
            
            result = await self.db.execute(sql, {"agent_id": agent_id})
            memories = result.fetchall()
            
            # Build graph
            graph = nx.DiGraph()
            
            for memory in memories:
                concepts = memory["type_data"]["concepts"]
                relationships = memory["type_data"]["relationships"]
                
                # Add concepts as nodes
                for concept in concepts:
                    if not graph.has_node(concept):
                        graph.add_node(
                            concept,
                            type="concept",
                            memories=[memory["id"]]
                        )
                    else:
                        graph.nodes[concept]["memories"].append(memory["id"])
                
                # Add relationships as edges
                for rel in relationships:
                    if rel["type"] == "is_a":
                        graph.add_edge(
                            rel["source"],
                            rel["target"],
                            relation="is_a",
                            weight=rel.get("strength", 1.0)
                        )
                    elif rel["type"] == "part_of":
                        graph.add_edge(
                            rel["source"],
                            rel["target"],
                            relation="part_of",
                            weight=rel.get("strength", 1.0)
                        )
            
            # Add ConceptNet relationships
            await self._enrich_with_conceptnet(graph, max_depth)
            
            return graph
        
        async def infer_new_facts(
            self,
            agent_id: str,
            max_inferences: int = 10
        ) -> List[Dict[str, Any]]:
            """Infer new facts from existing knowledge."""
            
            graph = await self.build_knowledge_graph(agent_id)
            inferences = []
            
            # Rule-based inference
            for node in graph.nodes():
                # Transitive inference (A is_a B, B is_a C => A is_a C)
                if graph.out_degree(node) > 0:
                    for child in graph.successors(node):
                        if graph[node][child].get("relation") == "is_a":
                            for grandchild in graph.successors(child):
                                if graph[child][grandchild].get("relation") == "is_a":
                                    if not graph.has_edge(node, grandchild):
                                        inferences.append({
                                            "type": "transitive_is_a",
                                            "content": f"{node} is a {grandchild}",
                                            "concepts": [node, grandchild],
                                            "confidence": 0.8,
                                            "source": "inference"
                                        })
                
                # Part-whole inference
                parts = [n for n in graph.predecessors(node) 
                        if graph[n][node].get("relation") == "part_of"]
                if len(parts) > 1:
                    for i, part1 in enumerate(parts):
                        for part2 in parts[i+1:]:
                            inferences.append({
                                "type": "shared_whole",
                                "content": f"{part1} and {part2} are both parts of {node}",
                                "concepts": [part1, part2, node],
                                "confidence": 0.9,
                                "source": "inference"
                            })
            
            # Store top inferences
            for inference in inferences[:max_inferences]:
                await self.store_fact(
                    agent_id,
                    inference["content"],
                    inference["concepts"],
                    inference["confidence"],
                    inference["source"]
                )
            
            return inferences[:max_inferences]
        
        async def _build_concept_relationships(
            self,
            concepts: List[str]
        ) -> List[Dict[str, Any]]:
            """Build relationships between concepts."""
            
            relationships = []
            
            # Query ConceptNet for relationships
            for concept in concepts:
                cn_data = await query_conceptnet(concept)
                
                for edge in cn_data.get("edges", []):
                    if edge["end"]["label"] in concepts:
                        relationships.append({
                            "type": edge["rel"]["label"],
                            "source": concept,
                            "target": edge["end"]["label"],
                            "strength": edge["weight"]
                        })
            
            # Add basic relationships based on patterns
            # This is simplified - in production use more sophisticated NLP
            for i, c1 in enumerate(concepts):
                for c2 in concepts[i+1:]:
                    if c1.lower() in c2.lower():
                        relationships.append({
                            "type": "part_of",
                            "source": c1,
                            "target": c2,
                            "strength": 0.7
                        })
            
            return relationships
        
        async def _update_concept_graph(
            self,
            agent_id: str,
            concepts: List[str],
            relationships: List[Dict[str, Any]]
        ):
            """Update the agent's concept graph."""
            
            # Store concepts if new
            for concept in concepts:
                sql = """
                INSERT INTO memory.concepts (concept, embedding)
                VALUES (:concept, :embedding)
                ON CONFLICT (concept) DO UPDATE
                SET embedding = COALESCE(concepts.embedding, :embedding)
                """
                
                embedding = await generate_embedding(concept)
                await self.db.execute(
                    sql,
                    {"concept": concept, "embedding": embedding}
                )
            
            # Update in-memory graph
            for concept in concepts:
                self.concept_graph.add_node(concept)
            
            for rel in relationships:
                self.concept_graph.add_edge(
                    rel["source"],
                    rel["target"],
                    relation=rel["type"],
                    weight=rel["strength"]
                )
        
        async def _find_related_facts(
            self,
            agent_id: str,
            embedding: List[float],
            concepts: List[str],
            exclude_id: str
        ) -> List[str]:
            """Find facts related by embedding or concepts."""
            
            sql = """
            WITH concept_overlap AS (
                SELECT m.id,
                       ARRAY_LENGTH(
                           ARRAY(
                               SELECT unnest(ARRAY[:concepts]::text[])
                               INTERSECT
                               SELECT unnest((m.type_data->'concepts')::text[])
                           ), 1
                       ) as overlap_count
                FROM memory.memories m
                WHERE m.agent_id = :agent_id
                  AND m.type = 'semantic'
                  AND m.id != :exclude_id
            )
            SELECT m.id
            FROM memory.memories m
            JOIN concept_overlap co ON m.id = co.id
            WHERE m.agent_id = :agent_id
              AND m.type = 'semantic'
              AND m.id != :exclude_id
              AND (
                  1 - (m.embedding <=> :embedding) > 0.8
                  OR co.overlap_count > 0
              )
            ORDER BY 
                co.overlap_count DESC,
                m.embedding <=> :embedding
            LIMIT 10
            """
            
            result = await self.db.execute(
                sql,
                {
                    "agent_id": agent_id,
                    "embedding": embedding,
                    "concepts": concepts,
                    "exclude_id": exclude_id
                }
            )
            
            return [row["id"] for row in result.fetchall()]
        
        async def _link_facts(
            self,
            source_id: str,
            target_ids: List[str]
        ):
            """Create relationships between semantic facts."""
            
            for target_id in target_ids:
                # Determine relationship type based on content
                sql = """
                INSERT INTO memory.relationships (
                    source_memory, target_memory, 
                    relationship_type, strength
                )
                SELECT :source, :target, 
                       CASE
                           WHEN m1.type_data->'concepts' @> m2.type_data->'concepts'
                           THEN 'generalizes'
                           WHEN m2.type_data->'concepts' @> m1.type_data->'concepts'
                           THEN 'specializes'
                           ELSE 'related_to'
                       END,
                       GREATEST(
                           0.5,
                           1 - (m1.embedding <=> m2.embedding)
                       )
                FROM memory.memories m1, memory.memories m2
                WHERE m1.id = :source AND m2.id = :target
                ON CONFLICT DO NOTHING
                """
                
                await self.db.execute(
                    sql,
                    {"source": source_id, "target": target_id}
                )
        
        def _calculate_semantic_importance(
            self,
            concepts: List[str],
            relationships: List[Dict[str, Any]],
            confidence: float
        ) -> float:
            """Calculate importance for semantic memory."""
            
            # Base importance from concept count
            base = min(1.0, len(concepts) / 5)
            
            # Relationship factor
            rel_factor = min(1.5, 1.0 + len(relationships) * 0.1)
            
            # Confidence factor
            conf_factor = 0.5 + confidence * 0.5
            
            # Check for important concept types
            important_concepts = [
                "goal", "rule", "principle", "law", 
                "definition", "theorem", "axiom"
            ]
            
            importance_boost = 1.0
            for concept in concepts:
                if any(imp in concept.lower() for imp in important_concepts):
                    importance_boost = 1.5
                    break
            
            return min(1.0, base * rel_factor * conf_factor * importance_boost)
        
        async def _apply_inference(
            self,
            facts: List[Dict[str, Any]],
            query_concepts: List[str]
        ) -> List[Dict[str, Any]]:
            """Apply logical inference to enrich query results."""
            
            enriched = []
            
            for fact in facts:
                fact_dict = dict(fact)
                inferred_relations = []
                
                # Check for transitive relations
                for rel in fact["type_data"]["relationships"]:
                    if rel["type"] == "is_a" and rel["target"] in query_concepts:
                        # This fact's subject IS-A query concept
                        inferred_relations.append({
                            "type": "answers_query",
                            "confidence": 0.9
                        })
                
                fact_dict["inferred_relations"] = inferred_relations
                enriched.append(fact_dict)
            
            return enriched
        
        async def _enrich_with_conceptnet(
            self,
            graph: nx.DiGraph,
            max_depth: int
        ):
            """Enrich knowledge graph with ConceptNet data."""
            
            # Get all concepts
            concepts = [n for n in graph.nodes() 
                       if graph.nodes[n].get("type") == "concept"]
            
            for concept in concepts[:50]:  # Limit for performance
                cn_data = await query_conceptnet(concept)
                
                for edge in cn_data.get("edges", [])[:10]:
                    rel_type = edge["rel"]["label"]
                    target = edge["end"]["label"]
                    
                    if rel_type in ["IsA", "PartOf", "HasA", "UsedFor"]:
                        graph.add_edge(
                            concept,
                            target,
                            relation=rel_type.lower(),
                            weight=edge["weight"],
                            source="conceptnet"
                        )

### Implicit Memory Implementation

**`src/memory/implicit.py`**

python

    import asyncio
    from typing import List, Optional, Dict, Any
    from datetime import datetime, timedelta
    from collections import defaultdict
    import numpy as np
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.memory import ImplicitMemory, MemoryType
    from src.utils.patterns import extract_behavioral_patterns
    
    class ImplicitMemoryManager:
        def __init__(self, db_session: AsyncSession):
            self.db = db_session
            self.pattern_cache = defaultdict(list)
        
        async def record_behavior(
            self,
            agent_id: str,
            action: str,
            context: Dict[str, Any],
            outcome: Optional[str] = None
        ) -> ImplicitMemory:
            """Record behavioral pattern for implicit learning."""
            
            # Extract pattern from action and context
            pattern = await self._extract_pattern(action, context)
            
            # Check if pattern already exists
            existing = await self._find_existing_pattern(agent_id, pattern)
            
            if existing:
                # Update frequency and recency
                await self._update_pattern_frequency(existing["id"])
                return ImplicitMemory(**existing)
            
            # Create new implicit memory
            content = self._format_pattern_content(pattern, action, context)
            
            query = """
            INSERT INTO memory.memories (
                agent_id, type, content, importance,
                type_data, source_context, metadata
            ) VALUES (
                :agent_id, :type, :content, :importance,
                :type_data, :source_context, :metadata
            ) RETURNING *
            """
            
            type_data = {
                "pattern": pattern,
                "frequency": 1,
                "lastTriggered": datetime.utcnow().isoformat(),
                "outcomes": [outcome] if outcome else []
            }
            
            metadata = {
                "action_type": self._classify_action(action),
                "context_features": self._extract_context_features(context),
                "confidence": 0.5  # Initial confidence
            }
            
            result = await self.db.execute(
                query,
                {
                    "agent_id": agent_id,
                    "type": MemoryType.IMPLICIT,
                    "content": content,
                    "importance": 0.3,  # Start with low importance
                    "type_data": type_data,
                    "source_context": context,
                    "metadata": metadata
                }
            )
            
            memory_data = result.fetchone()
            return ImplicitMemory(**memory_data)
        
        async def get_behavioral_tendencies(
            self,
            agent_id: str,
            context: Dict[str, Any],
            min_frequency: int = 3
        ) -> List[Dict[str, Any]]:
            """Get behavioral tendencies for given context."""
            
            context_features = self._extract_context_features(context)
            
            sql = """
            SELECT m.*,
                   (m.type_data->>'frequency')::int as frequency,
                   (m.type_data->>'lastTriggered')::timestamp as last_triggered
            FROM memory.memories m
            WHERE m.agent_id = :agent_id
              AND m.type = 'implicit'
              AND (m.type_data->>'frequency')::int >= :min_frequency
              AND m.metadata->'context_features' ?| ARRAY[:features]::text[]
            ORDER BY frequency DESC, last_triggered DESC
            LIMIT 10
            """
            
            result = await self.db.execute(
                sql,
                {
                    "agent_id": agent_id,
                    "min_frequency": min_frequency,
                    "features": list(context_features.keys())
                }
            )
            
            patterns = result.fetchall()
            
            # Calculate tendency scores
            tendencies = []
            for pattern in patterns:
                score = self._calculate_tendency_score(
                    pattern, context_features
                )
                
                tendencies.append({
                    "pattern": pattern["type_data"]["pattern"],
                    "action": self._extract_action_from_pattern(pattern),
                    "frequency": pattern["frequency"],
                    "confidence": pattern["metadata"]["confidence"],
                    "score": score,
                    "outcomes": pattern["type_data"]["outcomes"]
                })
            
            return sorted(tendencies, key=lambda x: x["score"], reverse=True)
        
        async def learn_from_outcome(
            self,
            agent_id: str,
            action: str,
            context: Dict[str, Any],
            outcome: str,
            success: bool
        ):
            """Update implicit memories based on action outcomes."""
            
            pattern = await self._extract_pattern(action, context)
            
            # Find the pattern
            existing = await self._find_existing_pattern(agent_id, pattern)
            
            if not existing:
                # Create new pattern with outcome
                await self.record_behavior(agent_id, action, context, outcome)
                return
            
            # Update pattern with outcome
            sql = """
            UPDATE memory.memories
            SET type_data = type_data || jsonb_build_object(
                    'outcomes', 
                    (type_data->'outcomes')::jsonb || to_jsonb(:outcome)
                ),
                importance = CASE
                    WHEN :success THEN LEAST(1.0, importance + 0.1)
                    ELSE GREATEST(0.0, importance - 0.05)
                END,
                metadata = metadata || jsonb_build_object(
                    'confidence',
                    CASE
                        WHEN :success THEN 
                            LEAST(1.0, (metadata->>'confidence')::float + 0.1)
                        ELSE 
                            GREATEST(0.0, (metadata->>'confidence')::float - 0.05)
                    END,
                    'success_rate',
                    CASE
                        WHEN metadata ? 'success_rate' THEN
                            ((metadata->>'success_rate')::float * 
                             (metadata->>'total_outcomes')::int + 
                             CASE WHEN :success THEN 1 ELSE 0 END) /
                            ((metadata->>'total_outcomes')::int + 1)
                        ELSE
                            CASE WHEN :success THEN 1.0 ELSE 0.0 END
                    END,
                    'total_outcomes',
                    COALESCE((metadata->>'total_outcomes')::int, 0) + 1
                )
            WHERE id = :id
            """
            
            await self.db.execute(
                sql,
                {
                    "id": existing["id"],
                    "outcome": outcome,
                    "success": success
                }
            )
        
        async def extract_habits(
            self,
            agent_id: str,
            time_window: timedelta = timedelta(days=30),
            min_frequency: int = 10
        ) -> List[Dict[str, Any]]:
            """Extract habitual patterns from implicit memories."""
            
            cutoff = datetime.utcnow() - time_window
            
            sql = """
            WITH time_patterns AS (
                SELECT 
                    m.*,
                    EXTRACT(HOUR FROM (m.type_data->>'lastTriggered')::timestamp) as hour,
                    EXTRACT(DOW FROM (m.type_data->>'lastTriggered')::timestamp) as dow,
                    (m.type_data->>'frequency')::int as frequency
                FROM memory.memories m
                WHERE m.agent_id = :agent_id
                  AND m.type = 'implicit'
                  AND (m.type_data->>'lastTriggered')::timestamp > :cutoff
                  AND (m.type_data->>'frequency')::int >= :min_frequency
            )
            SELECT 
                type_data->>'pattern' as pattern,
                COUNT(*) as occurrence_count,
                AVG(frequency) as avg_frequency,
                MODE() WITHIN GROUP (ORDER BY hour) as typical_hour,
                MODE() WITHIN GROUP (ORDER BY dow) as typical_day,
                AVG((metadata->>'confidence')::float) as avg_confidence
            FROM time_patterns
            GROUP BY type_data->>'pattern'
            HAVING COUNT(*) > 3
            ORDER BY occurrence_count DESC
            """
            
            result = await self.db.execute(
                sql,
                {
                    "agent_id": agent_id,
                    "cutoff": cutoff,
                    "min_frequency": min_frequency
                }
            )
            
            habits = []
            for row in result.fetchall():
                habits.append({
                    "pattern": row["pattern"],
                    "strength": min(1.0, row["avg_frequency"] / 50),
                    "regularity": row["occurrence_count"] / time_window.days,
                    "typical_time": {
                        "hour": int(row["typical_hour"]),
                        "day_of_week": int(row["typical_day"])
                    },
                    "confidence": row["avg_confidence"]
                })
            
            return habits
        
        async def _extract_pattern(
            self,
            action: str,
            context: Dict[str, Any]
        ) -> str:
            """Extract behavioral pattern from action and context."""
            
            # Extract key features
            features = []
            
            # Action type
            action_type = self._classify_action(action)
            features.append(f"action:{action_type}")
            
            # Context features
            if context.get("emotional_state"):
                features.append(f"emotion:{context['emotional_state']}")
            
            if context.get("time_pressure"):
                features.append("time_pressure:high")
            
            if context.get("social_context"):
                features.append(f"social:{context['social_context']}")
            
            # Environmental features
            if context.get("location"):
                features.append(f"location:{context['location']}")
            
            # Combine into pattern
            pattern = " AND ".join(sorted(features))
            return pattern
        
        async def _find_existing_pattern(
            self,
            agent_id: str,
            pattern: str
        ) -> Optional[Dict[str, Any]]:
            """Find existing implicit memory with same pattern."""
            
            sql = """
            SELECT *
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND type = 'implicit'
              AND type_data->>'pattern' = :pattern
            LIMIT 1
            """
            
            result = await self.db.execute(
                sql,
                {"agent_id": agent_id, "pattern": pattern}
            )
            
            row = result.fetchone()
            return dict(row) if row else None
        
        async def _update_pattern_frequency(self, memory_id: str):
            """Update frequency and recency of a pattern."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = type_data || jsonb_build_object(
                    'frequency', (type_data->>'frequency')::int + 1,
                    'lastTriggered', :now
                ),
                importance = LEAST(1.0, importance + 0.02),
                last_accessed_at = NOW()
            WHERE id = :id
            """
            
            await self.db.execute(
                sql,
                {"id": memory_id, "now": datetime.utcnow().isoformat()}
            )
        
        def _format_pattern_content(
            self,
            pattern: str,
            action: str,
            context: Dict[str, Any]
        ) -> str:
            """Format pattern into human-readable content."""
            
            parts = pattern.split(" AND ")
            conditions = []
            
            for part in parts:
                key, value = part.split(":", 1)
                if key == "action":
                    conditions.append(f"performing {value} actions")
                elif key == "emotion":
                    conditions.append(f"when feeling {value}")
                elif key == "social":
                    conditions.append(f"in {value} social contexts")
                elif key == "location":
                    conditions.append(f"at {value}")
                else:
                    conditions.append(f"with {key}={value}")
            
            content = f"Tendency to {action} "
            content += " and ".join(conditions)
            
            return content
        
        def _classify_action(self, action: str) -> str:
            """Classify action into categories."""
            
            action_lower = action.lower()
            
            # Simple classification - in production use NLP
            if any(word in action_lower for word in ["say", "tell", "ask", "speak"]):
                return "communication"
            elif any(word in action_lower for word in ["think", "consider", "analyze"]):
                return "cognitive"
            elif any(word in action_lower for word in ["move", "go", "travel"]):
                return "movement"
            elif any(word in action_lower for word in ["help", "assist", "support"]):
                return "prosocial"
            elif any(word in action_lower for word in ["avoid", "refuse", "decline"]):
                return "avoidance"
            else:
                return "general"
        
        def _extract_context_features(
            self,
            context: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Extract relevant features from context."""
            
            features = {}
            
            # Time features
            now = datetime.utcnow()
            features["hour_of_day"] = now.hour
            features["day_of_week"] = now.weekday()
            
            # Context features
            if context.get("emotional_state"):
                features["emotional_state"] = context["emotional_state"]
            
            if context.get("energy_level"):
                features["energy_level"] = context["energy_level"]
            
            if context.get("social_context"):
                features["social_presence"] = bool(context["social_context"])
            
            if context.get("task_complexity"):
                features["task_complexity"] = context["task_complexity"]
            
            return features
        
        def _calculate_tendency_score(
            self,
            pattern: Dict[str, Any],
            context_features: Dict[str, Any]
        ) -> float:
            """Calculate how likely a pattern is in current context."""
            
            base_score = pattern["frequency"] / 100.0  # Normalize frequency
            
            # Context match score
            pattern_features = pattern["metadata"]["context_features"]
            matches = sum(
                1 for k, v in context_features.items()
                if k in pattern_features and pattern_features[k] == v
            )
            
            context_score = matches / max(len(context_features), 1)
            
            # Recency score
            last_triggered = datetime.fromisoformat(
                pattern["type_data"]["lastTriggered"]
            )
            days_ago = (datetime.utcnow() - last_triggered).days
            recency_score = np.exp(-days_ago / 7)  # Decay over a week
            
            # Confidence factor
            confidence = pattern["metadata"]["confidence"]
            
            # Combine scores
            final_score = (
                base_score * 0.3 +
                context_score * 0.4 +
                recency_score * 0.2 +
                confidence * 0.1
            )
            
            return min(1.0, final_score)
        
        def _extract_action_from_pattern(
            self,
            pattern: Dict[str, Any]
        ) -> str:
            """Extract the likely action from a pattern."""
            
            # Parse pattern string
            pattern_str = pattern["type_data"]["pattern"]
            parts = pattern_str.split(" AND ")
            
            for part in parts:
                if part.startswith("action:"):
                    return part.split(":", 1)[1]
            
            return "unspecified action"

### Prospective Memory Implementation

**`src/memory/prospective.py`**

python

    import asyncio
    from typing import List, Optional, Dict, Any, Tuple
    from datetime import datetime, timedelta
    from enum import Enum
    import networkx as nx
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.memory import ProspectiveMemory, MemoryType
    from src.utils.planning import decompose_goal, estimate_duration
    
    class GoalStatus(str, Enum):
        ACTIVE = "active"
        COMPLETED = "completed"
        FAILED = "failed"
        DEFERRED = "deferred"
        CANCELLED = "cancelled"
    
    class ProspectiveMemoryManager:
        def __init__(self, db_session: AsyncSession):
            self.db = db_session
            self.goal_graph = nx.DiGraph()
        
        async def create_goal(
            self,
            agent_id: str,
            goal: str,
            deadline: Optional[datetime] = None,
            priority: int = 5,
            parent_goal_id: Optional[str] = None
        ) -> ProspectiveMemory:
            """Create a new goal or subgoal."""
            
            # Decompose goal into subgoals if complex
            subgoals = await decompose_goal(goal)
            
            # Estimate duration if no deadline
            if deadline is None and subgoals:
                estimated_duration = await estimate_duration(goal)
                deadline = datetime.utcnow() + timedelta(hours=estimated_duration)
            
            # Calculate importance
            importance = self._calculate_goal_importance(priority, deadline)
            
            # Create main goal
            query = """
            INSERT INTO memory.memories (
                agent_id, type, content, importance,
                type_data, metadata
            ) VALUES (
                :agent_id, :type, :content, :importance,
                :type_data, :metadata
            ) RETURNING *
            """
            
            type_data = {
                "goalId": parent_goal_id,
                "deadline": deadline.isoformat() if deadline else None,
                "priority": priority,
                "status": GoalStatus.ACTIVE,
                "dependencies": [],
                "progress": 0.0,
                "subgoals": []
            }
            
            metadata = {
                "created_by": "user" if parent_goal_id is None else "system",
                "category": self._categorize_goal(goal),
                "estimated_effort": len(subgoals) * 2,  # hours
                "checkpoints": []
            }
            
            result = await self.db.execute(
                query,
                {
                    "agent_id": agent_id,
                    "type": MemoryType.PROSPECTIVE,
                    "content": goal,
                    "importance": importance,
                    "type_data": type_data,
                    "metadata": metadata
                }
            )
            
            goal_data = result.fetchone()
            goal_memory = ProspectiveMemory(**goal_data)
            
            # Create subgoals
            if subgoals:
                subgoal_ids = []
                for i, subgoal in enumerate(subgoals):
                    sub_memory = await self.create_goal(
                        agent_id,
                        subgoal["description"],
                        deadline=subgoal.get("deadline"),
                        priority=priority - 1,
                        parent_goal_id=goal_memory.id
                    )
                    subgoal_ids.append(sub_memory.id)
                    
                    # Add dependencies
                    if i > 0 and subgoal.get("depends_on_previous"):
                        await self.add_dependency(
                            sub_memory.id, subgoal_ids[i-1]
                        )
                
                # Update parent with subgoals
                await self._update_goal_subgoals(goal_memory.id, subgoal_ids)
            
            # Update goal graph
            await self._update_goal_graph(agent_id)
            
            return goal_memory
        
        async def get_active_goals(
            self,
            agent_id: str,
            include_subgoals: bool = True,
            sort_by: str = "priority"
        ) -> List[ProspectiveMemory]:
            """Get all active goals for an agent."""
            
            sql = """
            SELECT m.*,
                   (type_data->>'priority')::int as priority,
                   (type_data->>'deadline')::timestamp as deadline,
                   (type_data->>'progress')::float as progress
            FROM memory.memories m
            WHERE m.agent_id = :agent_id
              AND m.type = 'prospective'
              AND type_data->>'status' = 'active'
            """
            
            if not include_subgoals:
                sql += " AND type_data->>'goalId' IS NULL"
            
            # Add sorting
            if sort_by == "priority":
                sql += " ORDER BY priority DESC, deadline ASC NULLS LAST"
            elif sort_by == "deadline":
                sql += " ORDER BY deadline ASC NULLS LAST, priority DESC"
            elif sort_by == "progress":
                sql += " ORDER BY progress DESC, priority DESC"
            
            result = await self.db.execute(sql, {"agent_id": agent_id})
            goals = result.fetchall()
            
            # Check for overdue goals
            now = datetime.utcnow()
            processed_goals = []
            
            for goal in goals:
                goal_dict = dict(goal)
                
                # Check if overdue
                if goal["deadline"] and goal["deadline"] < now:
                    goal_dict["metadata"]["is_overdue"] = True
                    goal_dict["importance"] = min(1.0, goal_dict["importance"] * 1.5)
                
                processed_goals.append(ProspectiveMemory(**goal_dict))
            
            return processed_goals
        
        async def update_goal_progress(
            self,
            goal_id: str,
            progress: float,
            checkpoint: Optional[str] = None
        ):
            """Update goal progress and optionally add checkpoint."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = type_data || jsonb_build_object('progress', :progress),
                metadata = CASE
                    WHEN :checkpoint IS NOT NULL THEN
                        metadata || jsonb_build_object(
                            'checkpoints',
                            COALESCE(metadata->'checkpoints', '[]'::jsonb) || 
                            jsonb_build_array(jsonb_build_object(
                                'description', :checkpoint,
                                'progress', :progress,
                                'timestamp', :now
                            ))
                        )
                    ELSE metadata
                END,
                updated_at = NOW()
            WHERE id = :goal_id
            RETURNING type_data->>'status' as status, 
                      type_data->'subgoals' as subgoals
            """
            
            result = await self.db.execute(
                sql,
                {
                    "goal_id": goal_id,
                    "progress": progress,
                    "checkpoint": checkpoint,
                    "now": datetime.utcnow().isoformat()
                }
            )
            
            goal_info = result.fetchone()
            
            # Check if goal is complete
            if progress >= 1.0 and goal_info["status"] == GoalStatus.ACTIVE:
                await self.complete_goal(goal_id)
            
            # Update parent goal progress if this is a subgoal
            await self._update_parent_progress(goal_id)
        
        async def complete_goal(self, goal_id: str):
            """Mark a goal as completed."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = type_data || jsonb_build_object(
                    'status', :status,
                    'completedAt', :completed_at,
                    'progress', 1.0
                ),
                importance = importance * 0.7  -- Reduce importance after completion
            WHERE id = :goal_id
            """
            
            await self.db.execute(
                sql,
                {
                    "goal_id": goal_id,
                    "status": GoalStatus.COMPLETED,
                    "completed_at": datetime.utcnow().isoformat()
                }
            )
            
            # Trigger any dependent goals
            await self._activate_dependent_goals(goal_id)
        
        async def defer_goal(
            self,
            goal_id: str,
            new_deadline: Optional[datetime] = None,
            reason: Optional[str] = None
        ):
            """Defer a goal to a later time."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = type_data || jsonb_build_object(
                    'status', :status,
                    'deadline', :deadline,
                    'deferredAt', :deferred_at
                ),
                metadata = metadata || jsonb_build_object(
                    'deferral_reason', :reason,
                    'deferral_count', 
                    COALESCE((metadata->>'deferral_count')::int, 0) + 1
                )
            WHERE id = :goal_id
            """
            
            await self.db.execute(
                sql,
                {
                    "goal_id": goal_id,
                    "status": GoalStatus.DEFERRED,
                    "deadline": new_deadline.isoformat() if new_deadline else None,
                    "deferred_at": datetime.utcnow().isoformat(),
                    "reason": reason
                }
            )
        
        async def add_dependency(
            self,
            goal_id: str,
            depends_on: str
        ):
            """Add a dependency between goals."""
            
            # Update goal dependencies
            sql = """
            UPDATE memory.memories
            SET type_data = jsonb_set(
                type_data,
                '{dependencies}',
                COALESCE(type_data->'dependencies', '[]'::jsonb) || 
                to_jsonb(:depends_on)
            )
            WHERE id = :goal_id
            """
            
            await self.db.execute(
                sql,
                {"goal_id": goal_id, "depends_on": depends_on}
            )
            
            # Create relationship
            await self.db.execute(
                """
                INSERT INTO memory.relationships (
                    source_memory, target_memory, relationship_type
                ) VALUES (:source, :target, 'depends_on')
                ON CONFLICT DO NOTHING
                """,
                {"source": goal_id, "target": depends_on}
            )
        
        async def suggest_next_actions(
            self,
            agent_id: str,
            context: Dict[str, Any],
            max_suggestions: int = 5
        ) -> List[Dict[str, Any]]:
            """Suggest next actions based on active goals."""
            
            # Get active goals
            goals = await self.get_active_goals(agent_id, sort_by="priority")
            
            suggestions = []
            
            for goal in goals[:10]:  # Consider top 10 goals
                # Check dependencies
                if await self._has_unmet_dependencies(goal.id):
                    continue
                
                # Calculate action priority
                priority_score = self._calculate_action_priority(
                    goal, context
                )
                
                # Generate action suggestion
                suggestion = {
                    "goal_id": goal.id,
                    "goal": goal.content,
                    "action": self._generate_action_suggestion(goal, context),
                    "priority_score": priority_score,
                    "deadline": goal.deadline,
                    "progress": goal.progress,
                    "estimated_duration": self._estimate_action_duration(goal)
                }
                
                suggestions.append(suggestion)
            
            # Sort by priority score
            suggestions.sort(key=lambda x: x["priority_score"], reverse=True)
            
            return suggestions[:max_suggestions]
        
        async def review_goals(
            self,
            agent_id: str,
            review_period: timedelta = timedelta(days=7)
        ) -> Dict[str, Any]:
            """Review goal progress and suggest adjustments."""
            
            cutoff = datetime.utcnow() - review_period
            
            sql = """
            WITH goal_stats AS (
                SELECT 
                    m.*,
                    (type_data->>'status')::text as status,
                    (type_data->>'priority')::int as priority,
                    (type_data->>'progress')::float as progress,
                    (type_data->>'deadline')::timestamp as deadline,
                    (metadata->>'checkpoints')::jsonb as checkpoints
                FROM memory.memories m
                WHERE m.agent_id = :agent_id
                  AND m.type = 'prospective'
                  AND m.created_at > :cutoff
            )
            SELECT 
                COUNT(*) FILTER (WHERE status = 'completed') as completed_count,
                COUNT(*) FILTER (WHERE status = 'active') as active_count,
                COUNT(*) FILTER (WHERE status = 'failed') as failed_count,
                COUNT(*) FILTER (WHERE status = 'deferred') as deferred_count,
                AVG(progress) FILTER (WHERE status = 'active') as avg_progress,
                COUNT(*) FILTER (
                    WHERE status = 'active' 
                    AND deadline < NOW()
                ) as overdue_count
            FROM goal_stats
            """
            
            result = await self.db.execute(
                sql,
                {"agent_id": agent_id, "cutoff": cutoff}
            )
            
            stats = dict(result.fetchone())
            
            # Get struggling goals (low progress, approaching deadline)
            struggling_sql = """
            SELECT *
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND type = 'prospective'
              AND type_data->>'status' = 'active'
              AND (type_data->>'progress')::float < 0.3
              AND (type_data->>'deadline')::timestamp < :deadline_threshold
            """
            
            deadline_threshold = datetime.utcnow() + timedelta(days=3)
            struggling_result = await self.db.execute(
                struggling_sql,
                {
                    "agent_id": agent_id,
                    "deadline_threshold": deadline_threshold
                }
            )
            
            struggling_goals = [
                ProspectiveMemory(**row) for row in struggling_result.fetchall()
            ]
            
            # Generate recommendations
            recommendations = []
            
            if stats["overdue_count"] > 0:
                recommendations.append({
                    "type": "overdue_goals",
                    "message": f"{stats['overdue_count']} goals are overdue",
                    "action": "Review and update deadlines or mark as failed"
                })
            
            if stats["avg_progress"] and stats["avg_progress"] < 0.5:
                recommendations.append({
                    "type": "low_progress",
                    "message": f"Average progress is only {stats['avg_progress']:.1%}",
                    "action": "Break down complex goals into smaller subgoals"
                })
            
            for goal in struggling_goals:
                recommendations.append({
                    "type": "struggling_goal",
                    "goal_id": goal.id,
                    "message": f"Goal '{goal.content}' has low progress",
                    "action": "Consider deferring or decomposing into smaller tasks"
                })
            
            return {
                "statistics": stats,
                "struggling_goals": struggling_goals,
                "recommendations": recommendations
            }
        
        async def _update_goal_graph(self, agent_id: str):
            """Update the agent's goal dependency graph."""
            
            sql = """
            SELECT 
                m.id,
                m.content,
                type_data->>'status' as status,
                type_data->'dependencies' as dependencies,
                type_data->'subgoals' as subgoals
            FROM memory.memories m
            WHERE m.agent_id = :agent_id
              AND m.type = 'prospective'
              AND type_data->>'status' IN ('active', 'deferred')
            """
            
            result = await self.db.execute(sql, {"agent_id": agent_id})
            goals = result.fetchall()
            
            # Clear and rebuild graph
            self.goal_graph.clear()
            
            for goal in goals:
                self.goal_graph.add_node(
                    goal["id"],
                    content=goal["content"],
                    status=goal["status"]
                )
                
                # Add dependency edges
                if goal["dependencies"]:
                    for dep_id in goal["dependencies"]:
                        self.goal_graph.add_edge(dep_id, goal["id"])
                
                # Add subgoal edges
                if goal["subgoals"]:
                    for subgoal_id in goal["subgoals"]:
                        self.goal_graph.add_edge(goal["id"], subgoal_id)
        
        async def _update_parent_progress(self, subgoal_id: str):
            """Update parent goal progress based on subgoals."""
            
            # Find parent goal
            sql = """
            SELECT 
                (type_data->>'goalId')::uuid as parent_id,
                (type_data->>'progress')::float as progress
            FROM memory.memories
            WHERE id = :subgoal_id
            """
            
            result = await self.db.execute(sql, {"subgoal_id": subgoal_id})
            subgoal_info = result.fetchone()
            
            if not subgoal_info or not subgoal_info["parent_id"]:
                return
            
            # Calculate parent progress from all subgoals
            parent_sql = """
            WITH subgoal_progress AS (
                SELECT 
                    (type_data->>'progress')::float as progress
                FROM memory.memories
                WHERE (type_data->>'goalId')::uuid = :parent_id
            )
            UPDATE memory.memories
            SET type_data = jsonb_set(
                type_data,
                '{progress}',
                to_jsonb((SELECT AVG(progress) FROM subgoal_progress))
            )
            WHERE id = :parent_id
            """
            
            await self.db.execute(
                parent_sql,
                {"parent_id": subgoal_info["parent_id"]}
            )
        
        async def _activate_dependent_goals(self, completed_goal_id: str):
            """Activate goals that were waiting on this one."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = jsonb_set(
                type_data,
                '{status}',
                to_jsonb('active'::text)
            )
            WHERE type = 'prospective'
              AND type_data->>'status' = 'deferred'
              AND type_data->'dependencies' ? :completed_goal_id
              AND NOT EXISTS (
                  -- Check if all other dependencies are also complete
                  SELECT 1
                  FROM jsonb_array_elements_text(type_data->'dependencies') dep
                  JOIN memory.memories m2 ON m2.id = dep::uuid
                  WHERE dep != :completed_goal_id
                    AND (m2.type_data->>'status') != 'completed'
              )
            """
            
            await self.db.execute(
                sql,
                {"completed_goal_id": completed_goal_id}
            )
        
        async def _has_unmet_dependencies(self, goal_id: str) -> bool:
            """Check if a goal has unmet dependencies."""
            
            sql = """
            SELECT EXISTS (
                SELECT 1
                FROM memory.memories m1
                JOIN LATERAL jsonb_array_elements_text(
                    m1.type_data->'dependencies'
                ) dep ON true
                JOIN memory.memories m2 ON m2.id = dep::uuid
                WHERE m1.id = :goal_id
                  AND (m2.type_data->>'status') != 'completed'
            )
            """
            
            result = await self.db.execute(sql, {"goal_id": goal_id})
            return result.scalar()
        
        def _calculate_goal_importance(
            self,
            priority: int,
            deadline: Optional[datetime]
        ) -> float:
            """Calculate goal importance score."""
            
            # Base importance from priority
            base = priority / 10.0
            
            # Urgency factor
            if deadline:
                days_until = (deadline - datetime.utcnow()).days
                if days_until < 1:
                    urgency = 2.0
                elif days_until < 7:
                    urgency = 1.5
                elif days_until < 30:
                    urgency = 1.2
                else:
                    urgency = 1.0
            else:
                urgency = 0.8
            
            return min(1.0, base * urgency)
        
        def _categorize_goal(self, goal: str) -> str:
            """Categorize goal into types."""
            
            goal_lower = goal.lower()
            
            if any(word in goal_lower for word in ["learn", "study", "understand"]):
                return "learning"
            elif any(word in goal_lower for word in ["create", "build", "make"]):
                return "creation"
            elif any(word in goal_lower for word in ["fix", "solve", "resolve"]):
                return "problem_solving"
            elif any(word in goal_lower for word in ["meet", "talk", "communicate"]):
                return "social"
            elif any(word in goal_lower for word in ["organize", "plan", "schedule"]):
                return "organization"
            else:
                return "general"
        
        def _calculate_action_priority(
            self,
            goal: ProspectiveMemory,
            context: Dict[str, Any]
        ) -> float:
            """Calculate priority score for taking action on a goal."""
            
            # Base priority from goal
            base_priority = goal.priority / 10.0
            
            # Urgency based on deadline
            if goal.deadline:
                hours_until = (goal.deadline - datetime.utcnow()).total_seconds() / 3600
                if hours_until < 24:
                    urgency = 2.0
                elif hours_until < 72:
                    urgency = 1.5
                else:
                    urgency = 1.0
            else:
                urgency = 0.8
            
            # Context appropriateness
            context_score = 1.0
            if context.get("available_time", 60) < 30 and goal.priority < 7:
                context_score = 0.5  # Deprioritize if limited time
            
            if context.get("energy_level", "normal") == "low" and \
               goal.metadata.get("category") in ["creation", "problem_solving"]:
                context_score *= 0.7  # Deprioritize demanding tasks when tired
            
            # Progress factor (prioritize goals that are closer to completion)
            progress_factor = 1.0 + goal.progress * 0.5
            
            return base_priority * urgency * context_score * progress_factor
        
        def _generate_action_suggestion(
            self,
            goal: ProspectiveMemory,
            context: Dict[str, Any]
        ) -> str:
            """Generate specific action suggestion for a goal."""
            
            if goal.progress == 0:
                return f"Start working on: {goal.content}"
            elif goal.progress < 0.3:
                return f"Continue initial work on: {goal.content}"
            elif goal.progress < 0.7:
                return f"Make progress on: {goal.content}"
            elif goal.progress < 1.0:
                return f"Complete final steps for: {goal.content}"
            else:
                return f"Review and finalize: {goal.content}"
        
        def _estimate_action_duration(
            self,
            goal: ProspectiveMemory
        ) -> int:
            """Estimate duration in minutes for next action."""
            
            # Simple estimation based on goal complexity
            remaining_effort = goal.metadata.get("estimated_effort", 2) * (1 - goal.progress)
            
            if remaining_effort < 0.5:
                return 15
            elif remaining_effort < 2:
                return 30
            elif remaining_effort < 5:
                return 60
            else:
                return 120
        
        async def _update_goal_subgoals(
            self,
            goal_id: str,
            subgoal_ids: List[str]
        ):
            """Update goal with its subgoals."""
            
            sql = """
            UPDATE memory.memories
            SET type_data = jsonb_set(
                type_data,
                '{subgoals}',
                to_jsonb(:subgoal_ids)
            )
            WHERE id = :goal_id
            """
    
    ---
    
    ## 7. MCP Protocol Implementation {#mcp-protocol}
    
    ### MCP Server Implementation
    
    **`src/protocols/mcp/server.py`**
    ```python
    import asyncio
    import json
    from typing import Dict, Any, Optional, List, Callable
    from dataclasses import dataclass
    from enum import Enum
    import uuid
    from datetime import datetime
    
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.database import get_db
    
    class TransportType(str, Enum):
        STDIO = "stdio"
        HTTP = "http"
    
    @dataclass
    class MCPTool:
        name: str
        description: str
        input_schema: Dict[str, Any]
        handler: Callable
        server_id: str
    
    @dataclass
    class MCPResource:
        uri: str
        name: str
        description: str
        mime_type: str
        server_id: str
        handler: Optional[Callable] = None
    
    @dataclass
    class MCPPrompt:
        name: str
        description: str
        template: str
        arguments: List[Dict[str, Any]]
        server_id: str
    
    class MCPServer:
        def __init__(
            self,
            name: str,
            agent_id: str,
            transport: TransportType,
            db_session: AsyncSession
        ):
            self.name = name
            self.agent_id = agent_id
            self.transport = transport
            self.db = db_session
            self.server_id = str(uuid.uuid4())
            
            self.tools: Dict[str, MCPTool] = {}
            self.resources: Dict[str, MCPResource] = {}
            self.prompts: Dict[str, MCPPrompt] = {}
            
            self._running = False
            self._message_handlers = {
                "initialize": self._handle_initialize,
                "tools/list": self._handle_list_tools,
                "tools/execute": self._handle_execute_tool,
                "resources/list": self._handle_list_resources,
                "resources/get": self._handle_get_resource,
                "prompts/list": self._handle_list_prompts,
                "prompts/get": self._handle_get_prompt
            }
        
        async def start(self):
            """Start the MCP server."""
            # Register server in database
            await self._register_server()
            
            self._running = True
            
            if self.transport == TransportType.STDIO:
                await self._start_stdio()
            else:
                await self._start_http()
        
        async def stop(self):
            """Stop the MCP server."""
            self._running = False
            
            # Update server status
            sql = """
            UPDATE protocols.mcp_servers
            SET is_active = false,
                last_heartbeat = NOW()
            WHERE id = :server_id
            """
            
            await self.db.execute(sql, {"server_id": self.server_id})
            await self.db.commit()
        
        def register_tool(
            self,
            name: str,
            description: str,
            input_schema: Dict[str, Any],
            handler: Callable
        ):
            """Register a tool with the server."""
            tool = MCPTool(
                name=name,
                description=description,
                input_schema=input_schema,
                handler=handler,
                server_id=self.server_id
            )
            
            self.tools[name] = tool
            
            # Store in database (async operation queued)
            asyncio.create_task(self._store_tool(tool))
        
        def register_resource(
            self,
            uri: str,
            name: str,
            description: str,
            mime_type: str = "text/plain",
            handler: Optional[Callable] = None
        ):
            """Register a resource with the server."""
            resource = MCPResource(
                uri=uri,
                name=name,
                description=description,
                mime_type=mime_type,
                server_id=self.server_id,
                handler=handler
            )
            
            self.resources[uri] = resource
            
            # Store in database
            asyncio.create_task(self._store_resource(resource))
        
        def register_prompt(
            self,
            name: str,
            description: str,
            template: str,
            arguments: List[Dict[str, Any]] = None
        ):
            """Register a prompt template."""
            prompt = MCPPrompt(
                name=name,
                description=description,
                template=template,
                arguments=arguments or [],
                server_id=self.server_id
            )
            
            self.prompts[name] = prompt
            
            # Store in database
            asyncio.create_task(self._store_prompt(prompt))
        
        async def _start_stdio(self):
            """Start STDIO transport."""
            import sys
            
            reader = asyncio.StreamReader()
            protocol = asyncio.StreamReaderProtocol(reader)
            await asyncio.get_event_loop().connect_read_pipe(
                lambda: protocol, sys.stdin
            )
            
            writer = asyncio.StreamWriter(
                sys.stdout,
                protocol,
                reader,
                asyncio.get_event_loop()
            )
            
            while self._running:
                try:
                    # Read message
                    line = await reader.readline()
                    if not line:
                        break
                    
                    message = json.loads(line.decode())
                    response = await self._handle_message(message)
                    
                    # Write response
                    writer.write(json.dumps(response).encode() + b'\n')
                    await writer.drain()
                    
                except Exception as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }
                    writer.write(json.dumps(error_response).encode() + b'\n')
                    await writer.drain()
        
        async def _start_http(self):
            """Start HTTP transport."""
            from aiohttp import web
            
            async def handle_request(request):
                try:
                    message = await request.json()
                    response = await self._handle_message(message)
                    return web.json_response(response)
                except Exception as e:
                    return web.json_response({
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32603,
                            "message": str(e)
                        }
                    }, status=500)
            
            app = web.Application()
            app.router.add_post("/", handle_request)
            
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, 'localhost', 8081)
            await site.start()
            
            # Keep running
            while self._running:
                await asyncio.sleep(1)
                await self._send_heartbeat()
        
        async def _handle_message(
            self,
            message: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Handle incoming JSON-RPC message."""
            
            method = message.get("method")
            params = message.get("params", {})
            msg_id = message.get("id")
            
            # Log message
            await self._log_message(message, "request")
            
            try:
                handler = self._message_handlers.get(method)
                if not handler:
                    raise ValueError(f"Unknown method: {method}")
                
                result = await handler(params)
                
                response = {
                    "jsonrpc": "2.0",
                    "result": result
                }
                
                if msg_id:
                    response["id"] = msg_id
                
                # Log response
                await self._log_message(response, "response")
                
                return response
                
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": str(e),
                        "data": {"method": method}
                    }
                }
                
                if msg_id:
                    error_response["id"] = msg_id
                
                await self._log_message(error_response, "response")
                
                return error_response
        
        async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Handle initialization request."""
            return {
                "protocolVersion": "1.0",
                "capabilities": {
                    "tools": True,
                    "resources": True,
                    "prompts": True,
                    "sampling": False
                },
                "serverInfo": {
                    "name": self.name,
                    "version": "0.1.0"
                }
            }
        
        async def _handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """List available tools."""
            tools = []
            
            for name, tool in self.tools.items():
                tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema
                })
            
            return {"tools": tools}
        
        async def _handle_execute_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Execute a tool."""
            tool_name = params.get("name")
            tool_input = params.get("input", {})
            
            tool = self.tools.get(tool_name)
            if not tool:
                raise ValueError(f"Tool not found: {tool_name}")
            
            # Validate input
            # In production, use proper JSON schema validation
            
            # Execute tool
            start_time = datetime.utcnow()
            
            try:
                result = await tool.handler(tool_input)
                
                duration_ms = int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                )
                
                # Update usage statistics
                await self._update_tool_usage(tool_name, duration_ms)
                
                return {
                    "output": result,
                    "duration": duration_ms
                }
                
            except Exception as e:
                return {
                    "error": str(e),
                    "duration": int(
                        (datetime.utcnow() - start_time).total_seconds() * 1000
                    )
                }
        
        async def _handle_list_resources(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """List available resources."""
            resources = []
            
            for uri, resource in self.resources.items():
                resources.append({
                    "uri": resource.uri,
                    "name": resource.name,
                    "description": resource.description,
                    "mimeType": resource.mime_type
                })
            
            return {"resources": resources}
        
        async def _handle_get_resource(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Get a resource."""
            uri = params.get("uri")
            
            resource = self.resources.get(uri)
            if not resource:
                raise ValueError(f"Resource not found: {uri}")
            
            # Get content
            if resource.handler:
                content = await resource.handler()
            else:
                # Check cache
                content = await self._get_cached_resource(uri)
            
            return {
                "uri": uri,
                "mimeType": resource.mime_type,
                "content": content
            }
        
        async def _handle_list_prompts(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """List available prompts."""
            prompts = []
            
            for name, prompt in self.prompts.items():
                prompts.append({
                    "name": prompt.name,
                    "description": prompt.description,
                    "arguments": prompt.arguments
                })
            
            return {"prompts": prompts}
        
        async def _handle_get_prompt(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Get a prompt template."""
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            prompt = self.prompts.get(name)
            if not prompt:
                raise ValueError(f"Prompt not found: {name}")
            
            # Format template with arguments
            try:
                formatted = prompt.template.format(**arguments)
            except KeyError as e:
                raise ValueError(f"Missing argument: {e}")
            
            return {
                "name": name,
                "content": formatted
            }
        
        async def _register_server(self):
            """Register server in database."""
            sql = """
            INSERT INTO protocols.mcp_servers (
                id, agent_id, name, transport, is_active, last_heartbeat
            ) VALUES (
                :id, :agent_id, :name, :transport, true, NOW()
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": self.server_id,
                    "agent_id": self.agent_id,
                    "name": self.name,
                    "transport": self.transport.value
                }
            )
            await self.db.commit()
        
        async def _store_tool(self, tool: MCPTool):
            """Store tool in database."""
            sql = """
            INSERT INTO protocols.mcp_tools (
                server_id, name, description, input_schema, enabled
            ) VALUES (
                :server_id, :name, :description, :input_schema, true
            ) ON CONFLICT (server_id, name) DO UPDATE SET
                description = EXCLUDED.description,
                input_schema = EXCLUDED.input_schema
            """
            
            await self.db.execute(
                sql,
                {
                    "server_id": tool.server_id,
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema
                }
            )
            await self.db.commit()
        
        async def _store_resource(self, resource: MCPResource):
            """Store resource in database."""
            sql = """
            INSERT INTO protocols.mcp_resources (
                server_id, uri, name, description, mime_type
            ) VALUES (
                :server_id, :uri, :name, :description, :mime_type
            ) ON CONFLICT (server_id, uri) DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                mime_type = EXCLUDED.mime_type
            """
            
            await self.db.execute(
                sql,
                {
                    "server_id": resource.server_id,
                    "uri": resource.uri,
                    "name": resource.name,
                    "description": resource.description,
                    "mime_type": resource.mime_type
                }
            )
            await self.db.commit()
        
        async def _store_prompt(self, prompt: MCPPrompt):
            """Store prompt in database."""
            sql = """
            INSERT INTO protocols.mcp_prompts (
                server_id, name, description, template, arguments
            ) VALUES (
                :server_id, :name, :description, :template, :arguments
            ) ON CONFLICT (server_id, name) DO UPDATE SET
                description = EXCLUDED.description,
                template = EXCLUDED.template,
                arguments = EXCLUDED.arguments
            """
            
            await self.db.execute(
                sql,
                {
                    "server_id": prompt.server_id,
                    "name": prompt.name,
                    "description": prompt.description,
                    "template": prompt.template,
                    "arguments": prompt.arguments
                }
            )
            await self.db.commit()
        
        async def _send_heartbeat(self):
            """Send heartbeat to database."""
            sql = """
            UPDATE protocols.mcp_servers
            SET last_heartbeat = NOW()
            WHERE id = :server_id
            """
            
            await self.db.execute(sql, {"server_id": self.server_id})
            await self.db.commit()
        
        async def _log_message(
            self,
            message: Dict[str, Any],
            msg_type: str
        ):
            """Log MCP message."""
            sql = """
            INSERT INTO protocols.mcp_messages (
                type, method, params, result, error,
                source_agent, status
            ) VALUES (
                :type, :method, :params, :result, :error,
                :source_agent, :status
            )
            """
            
            method = message.get("method", "")
            
            await self.db.execute(
                sql,
                {
                    "type": msg_type,
                    "method": method,
                    "params": message.get("params"),
                    "result": message.get("result"),
                    "error": message.get("error"),
                    "source_agent": self.agent_id,
                    "status": "completed" if "result" in message else "failed"
                }
            )
            await self.db.commit()
        
        async def _update_tool_usage(self, tool_name: str, duration_ms: int):
            """Update tool usage statistics."""
            sql = """
            UPDATE protocols.mcp_tools
            SET usage_count = usage_count + 1,
                last_used_at = NOW(),
                avg_duration_ms = CASE
                    WHEN avg_duration_ms IS NULL THEN :duration
                    ELSE (avg_duration_ms * usage_count + :duration) / (usage_count + 1)
                END
            WHERE server_id = :server_id AND name = :name
            """
            
            await self.db.execute(
                sql,
                {
                    "server_id": self.server_id,
                    "name": tool_name,
                    "duration": duration_ms
                }
            )
            await self.db.commit()
        
        async def _get_cached_resource(self, uri: str) -> Optional[str]:
            """Get cached resource content."""
            sql = """
            SELECT cached_content
            FROM protocols.mcp_resources
            WHERE server_id = :server_id 
              AND uri = :uri
              AND cached_at > NOW() - INTERVAL '1 hour' * cache_ttl / 3600
            """
            
            result = await self.db.execute(
                sql,
                {"server_id": self.server_id, "uri": uri}
            )
            
            row = result.fetchone()
            return row["cached_content"] if row else None







### MCP Client Implementation

**`src/protocols/mcp/client.py`**

python

    import asyncio
    import json
    from typing import Dict, Any, Optional, List, Callable
    from dataclasses import dataclass
    import httpx
    import uuid
    from datetime import datetime
    
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.database import get_db
    
    class MCPClient:
        def __init__(
            self,
            agent_id: str,
            db_session: AsyncSession
        ):
            self.agent_id = agent_id
            self.db = db_session
            self._servers: Dict[str, Dict[str, Any]] = {}
            self._http_client = httpx.AsyncClient()
            
        async def connect_to_server(
            self,
            server_name: str,
            transport: str,
            **kwargs
        ) -> str:
            """Connect to an MCP server."""
            
            server_id = str(uuid.uuid4())
            
            if transport == "stdio":
                connection = await self._connect_stdio(
                    server_name,
                    kwargs.get("command"),
                    kwargs.get("args", []),
                    kwargs.get("env", {})
                )
            elif transport == "http":
                connection = await self._connect_http(
                    server_name,
                    kwargs.get("url"),
                    kwargs.get("headers", {})
                )
            else:
                raise ValueError(f"Unsupported transport: {transport}")
            
            self._servers[server_id] = {
                "name": server_name,
                "transport": transport,
                "connection": connection,
                "capabilities": await self._initialize_server(connection)
            }
            
            # Store server configuration
            await self._store_server_config(server_id, server_name, transport, kwargs)
            
            return server_id
        
        async def list_tools(self, server_id: Optional[str] = None) -> List[Dict[str, Any]]:
            """List available tools from connected servers."""
            
            if server_id:
                servers = [(server_id, self._servers[server_id])]
            else:
                servers = list(self._servers.items())
            
            all_tools = []
            
            for sid, server in servers:
                connection = server["connection"]
                
                response = await self._send_request(
                    connection,
                    "tools/list",
                    {}
                )
                
                tools = response.get("result", {}).get("tools", [])
                for tool in tools:
                    tool["server_id"] = sid
                    tool["server_name"] = server["name"]
                    all_tools.append(tool)
            
            return all_tools
        
        async def execute_tool(
            self,
            tool_name: str,
            tool_input: Dict[str, Any],
            server_id: Optional[str] = None
        ) -> Dict[str, Any]:
            """Execute a tool on an MCP server."""
            
            # Find the server that has this tool
            if not server_id:
                server_id = await self._find_tool_server(tool_name)
                if not server_id:
                    raise ValueError(f"Tool not found: {tool_name}")
            
            server = self._servers[server_id]
            connection = server["connection"]
            
            # Log tool execution
            execution_id = await self._log_tool_execution_start(
                tool_name, tool_input, server_id
            )
            
            try:
                # Send execution request
                response = await self._send_request(
                    connection,
                    "tools/execute",
                    {
                        "name": tool_name,
                        "input": tool_input
                    }
                )
                
                result = response.get("result", {})
                
                # Log success
                await self._log_tool_execution_end(
                    execution_id, result, None
                )
                
                return result
                
            except Exception as e:
                # Log failure
                await self._log_tool_execution_end(
                    execution_id, None, str(e)
                )
                raise
        
        async def get_resource(
            self,
            uri: str,
            server_id: Optional[str] = None
        ) -> Dict[str, Any]:
            """Get a resource from an MCP server."""
            
            if not server_id:
                # Try to find server with this resource
                for sid, server in self._servers.items():
                    resources = await self.list_resources(sid)
                    if any(r["uri"] == uri for r in resources):
                        server_id = sid
                        break
                
                if not server_id:
                    raise ValueError(f"Resource not found: {uri}")
            
            server = self._servers[server_id]
            connection = server["connection"]
            
            response = await self._send_request(
                connection,
                "resources/get",
                {"uri": uri}
            )
            
            return response.get("result", {})
        
        async def list_resources(
            self,
            server_id: Optional[str] = None
        ) -> List[Dict[str, Any]]:
            """List available resources."""
            
            if server_id:
                servers = [(server_id, self._servers[server_id])]
            else:
                servers = list(self._servers.items())
            
            all_resources = []
            
            for sid, server in servers:
                connection = server["connection"]
                
                response = await self._send_request(
                    connection,
                    "resources/list",
                    {}
                )
                
                resources = response.get("result", {}).get("resources", [])
                for resource in resources:
                    resource["server_id"] = sid
                    resource["server_name"] = server["name"]
                    all_resources.append(resource)
            
            return all_resources
        
        async def get_prompt(
            self,
            prompt_name: str,
            arguments: Dict[str, Any],
            server_id: Optional[str] = None
        ) -> str:
            """Get a formatted prompt from an MCP server."""
            
            if not server_id:
                # Find server with this prompt
                for sid, server in self._servers.items():
                    prompts = await self.list_prompts(sid)
                    if any(p["name"] == prompt_name for p in prompts):
                        server_id = sid
                        break
                
                if not server_id:
                    raise ValueError(f"Prompt not found: {prompt_name}")
            
            server = self._servers[server_id]
            connection = server["connection"]
            
            response = await self._send_request(
                connection,
                "prompts/get",
                {
                    "name": prompt_name,
                    "arguments": arguments
                }
            )
            
            return response.get("result", {}).get("content", "")
        
        async def list_prompts(
            self,
            server_id: Optional[str] = None
        ) -> List[Dict[str, Any]]:
            """List available prompts."""
            
            if server_id:
                servers = [(server_id, self._servers[server_id])]
            else:
                servers = list(self._servers.items())
            
            all_prompts = []
            
            for sid, server in servers:
                connection = server["connection"]
                
                response = await self._send_request(
                    connection,
                    "prompts/list",
                    {}
                )
                
                prompts = response.get("result", {}).get("prompts", [])
                for prompt in prompts:
                    prompt["server_id"] = sid
                    prompt["server_name"] = server["name"]
                    all_prompts.append(prompt)
            
            return all_prompts
        
        async def disconnect(self, server_id: str):
            """Disconnect from an MCP server."""
            
            if server_id not in self._servers:
                return
            
            server = self._servers[server_id]
            connection = server["connection"]
            
            if server["transport"] == "stdio":
                await self._disconnect_stdio(connection)
            
            del self._servers[server_id]
            
            # Update database
            await self._update_server_status(server_id, False)
        
        async def _connect_stdio(
            self,
            server_name: str,
            command: str,
            args: List[str],
            env: Dict[str, str]
        ) -> Dict[str, Any]:
            """Connect to STDIO-based MCP server."""
            
            import subprocess
            
            # Start the process
            process = await asyncio.create_subprocess_exec(
                command,
                *args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, **env}
            )
            
            return {
                "type": "stdio",
                "process": process,
                "reader": process.stdout,
                "writer": process.stdin
            }
        
        async def _connect_http(
            self,
            server_name: str,
            url: str,
            headers: Dict[str, str]
        ) -> Dict[str, Any]:
            """Connect to HTTP-based MCP server."""
            
            # Test connection
            response = await self._http_client.post(
                url,
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "params": {},
                    "id": 1
                },
                headers=headers
            )
            
            response.raise_for_status()
            
            return {
                "type": "http",
                "url": url,
                "headers": headers
            }
        
        async def _initialize_server(
            self,
            connection: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Initialize connection with MCP server."""
            
            response = await self._send_request(
                connection,
                "initialize",
                {
                    "clientInfo": {
                        "name": "julep-agent",
                        "version": "0.1.0"
                    }
                }
            )
            
            return response.get("result", {}).get("capabilities", {})
        
        async def _send_request(
            self,
            connection: Dict[str, Any],
            method: str,
            params: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Send request to MCP server."""
            
            request = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": str(uuid.uuid4())
            }
            
            if connection["type"] == "stdio":
                return await self._send_stdio_request(connection, request)
            else:
                return await self._send_http_request(connection, request)
        
        async def _send_stdio_request(
            self,
            connection: Dict[str, Any],
            request: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Send request over STDIO."""
            
            writer = connection["writer"]
            reader = connection["reader"]
            
            # Write request
            writer.write(json.dumps(request).encode() + b'\n')
            await writer.drain()
            
            # Read response
            line = await reader.readline()
            if not line:
                raise ConnectionError("Server disconnected")
            
            return json.loads(line.decode())
        
        async def _send_http_request(
            self,
            connection: Dict[str, Any],
            request: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Send request over HTTP."""
            
            response = await self._http_client.post(
                connection["url"],
                json=request,
                headers=connection["headers"]
            )
            
            response.raise_for_status()
            return response.json()
        
        async def _disconnect_stdio(self, connection: Dict[str, Any]):
            """Disconnect STDIO connection."""
            
            process = connection["process"]
            
            # Send terminate signal
            process.terminate()
            
            # Wait for process to end
            try:
                await asyncio.wait_for(process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                # Force kill if needed
                process.kill()
                await process.wait()
        
        async def _find_tool_server(self, tool_name: str) -> Optional[str]:
            """Find which server provides a tool."""
            
            for server_id in self._servers:
                tools = await self.list_tools(server_id)
                if any(t["name"] == tool_name for t in tools):
                    return server_id
            
            return None
        
        async def _store_server_config(
            self,
            server_id: str,
            server_name: str,
            transport: str,
            config: Dict[str, Any]
        ):
            """Store server configuration in database."""
            
            sql = """
            INSERT INTO protocols.mcp_servers (
                id, agent_id, name, transport,
                command, args, env, url, headers,
                is_active, last_heartbeat
            ) VALUES (
                :id, :agent_id, :name, :transport,
                :command, :args, :env, :url, :headers,
                true, NOW()
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": server_id,
                    "agent_id": self.agent_id,
                    "name": server_name,
                    "transport": transport,
                    "command": config.get("command"),
                    "args": config.get("args", []),
                    "env": config.get("env", {}),
                    "url": config.get("url"),
                    "headers": config.get("headers", {})
                }
            )
            await self.db.commit()
        
        async def _update_server_status(self, server_id: str, is_active: bool):
            """Update server status in database."""
            
            sql = """
            UPDATE protocols.mcp_servers
            SET is_active = :is_active,
                last_heartbeat = NOW()
            WHERE id = :server_id
            """
            
            await self.db.execute(
                sql,
                {"server_id": server_id, "is_active": is_active}
            )
            await self.db.commit()
        
        async def _log_tool_execution_start(
            self,
            tool_name: str,
            tool_input: Dict[str, Any],
            server_id: str
        ) -> str:
            """Log start of tool execution."""
            
            execution_id = str(uuid.uuid4())
            
            sql = """
            INSERT INTO protocols.mcp_messages (
                id, type, method, params,
                source_agent, status, created_at
            ) VALUES (
                :id, 'request', 'tools/execute', :params,
                :agent_id, 'processing', NOW()
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": execution_id,
                    "params": {
                        "tool": tool_name,
                        "input": tool_input,
                        "server_id": server_id
                    },
                    "agent_id": self.agent_id
                }
            )
            await self.db.commit()
            
            return execution_id
        
        async def _log_tool_execution_end(
            self,
            execution_id: str,
            result: Optional[Dict[str, Any]],
            error: Optional[str]
        ):
            """Log end of tool execution."""
            
            sql = """
            UPDATE protocols.mcp_messages
            SET result = :result,
                error = :error,
                status = :status,
                processed_at = NOW(),
                duration_ms = EXTRACT(MILLISECONDS FROM NOW() - created_at)
            WHERE id = :id
            """
            
            await self.db.execute(
                sql,
                {
                    "id": execution_id,
                    "result": result,
                    "error": {"message": error} if error else None,
                    "status": "failed" if error else "completed"
                }
            )
            await self.db.commit()

### MCP Integration Manager

**`src/protocols/mcp/manager.py`**

python

    from typing import Dict, Any, List, Optional, Callable
    import asyncio
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.protocols.mcp.server import MCPServer
    from src.protocols.mcp.client import MCPClient
    from src.database import get_db
    
    class MCPManager:
        """Manages MCP servers and clients for an agent."""
        
        def __init__(self, agent_id: str, db_session: AsyncSession):
            self.agent_id = agent_id
            self.db = db_session
            self.servers: Dict[str, MCPServer] = {}
            self.client = MCPClient(agent_id, db_session)
        
        async def initialize(self):
            """Initialize MCP manager from agent configuration."""
            
            # Load agent configuration
            agent_config = await self._load_agent_config()
            
            # Start configured MCP servers
            for server_config in agent_config.get("mcp_servers", []):
                await self.start_server(
                    server_config["name"],
                    server_config["transport"]
                )
            
            # Connect to external MCP servers
            for connection in agent_config.get("mcp_connections", []):
                await self.client.connect_to_server(
                    connection["name"],
                    connection["transport"],
                    **connection["config"]
                )
        
        async def start_server(
            self,
            name: str,
            transport: str
        ) -> MCPServer:
            """Start an MCP server for this agent."""
            
            server = MCPServer(
                name=name,
                agent_id=self.agent_id,
                transport=transport,
                db_session=self.db
            )
            
            # Register default tools
            await self._register_default_tools(server)
            
            # Start server
            await server.start()
            
            self.servers[server.server_id] = server
            return server
        
        async def register_tool(
            self,
            server_name: str,
            tool_name: str,
            description: str,
            input_schema: Dict[str, Any],
            handler: Callable
        ):
            """Register a tool with a server."""
            
            server = self._get_server_by_name(server_name)
            if not server:
                raise ValueError(f"Server not found: {server_name}")
            
            server.register_tool(
                tool_name,
                description,
                input_schema,
                handler
            )
        
        async def execute_tool(
            self,
            tool_name: str,
            tool_input: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Execute a tool (local or remote)."""
            
            # Check local servers first
            for server in self.servers.values():
                if tool_name in server.tools:
                    tool = server.tools[tool_name]
                    return await tool.handler(tool_input)
            
            # Try remote servers
            return await self.client.execute_tool(tool_name, tool_input)
        
        async def list_all_tools(self) -> List[Dict[str, Any]]:
            """List all available tools (local and remote)."""
            
            all_tools = []
            
            # Local tools
            for server in self.servers.values():
                for name, tool in server.tools.items():
                    all_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.input_schema,
                        "server": server.name,
                        "type": "local"
                    })
            
            # Remote tools
            remote_tools = await self.client.list_tools()
            for tool in remote_tools:
                tool["type"] = "remote"
                all_tools.append(tool)
            
            return all_tools
        
        async def get_resource(self, uri: str) -> Dict[str, Any]:
            """Get a resource (local or remote)."""
            
            # Check local servers
            for server in self.servers.values():
                if uri in server.resources:
                    resource = server.resources[uri]
                    if resource.handler:
                        content = await resource.handler()
                    else:
                        content = await self._get_cached_resource(
                            server.server_id, uri
                        )
                    
                    return {
                        "uri": uri,
                        "mimeType": resource.mime_type,
                        "content": content
                    }
            
            # Try remote servers
            return await self.client.get_resource(uri)
        
        async def shutdown(self):
            """Shutdown all MCP connections."""
            
            # Stop local servers
            for server in self.servers.values():
                await server.stop()
            
            # Disconnect from remote servers
            for server_id in list(self.client._servers.keys()):
                await self.client.disconnect(server_id)
        
        async def _load_agent_config(self) -> Dict[str, Any]:
            """Load agent configuration from database."""
            
            sql = """
            SELECT mcp_servers, metadata
            FROM agents.agents
            WHERE id = :agent_id
            """
            
            result = await self.db.execute(sql, {"agent_id": self.agent_id})
            agent = result.fetchone()
            
            if not agent:
                raise ValueError(f"Agent not found: {self.agent_id}")
            
            return {
                "mcp_servers": agent["mcp_servers"] or [],
                "mcp_connections": agent["metadata"].get("mcp_connections", [])
            }
        
        async def _register_default_tools(self, server: MCPServer):
            """Register default tools with server."""
            
            # Memory search tool
            server.register_tool(
                "search_memory",
                "Search agent's memory",
                {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "memory_types": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["episodic", "semantic", "implicit", "prospective"]
                            }
                        },
                        "limit": {"type": "integer", "default": 10}
                    },
                    "required": ["query"]
                },
                self._search_memory_handler
            )
            
            # Goal management tool
            server.register_tool(
                "manage_goals",
                "Create, update, or query goals",
                {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["create", "update", "list", "complete"]
                        },
                        "goal": {"type": "string"},
                        "goal_id": {"type": "string"},
                        "priority": {"type": "integer", "minimum": 1, "maximum": 10},
                        "deadline": {"type": "string", "format": "date-time"}
                    },
                    "required": ["action"]
                },
                self._manage_goals_handler
            )
            
            # Agent state tool
            server.register_tool(
                "get_agent_state",
                "Get current agent state and context",
                {
                    "type": "object",
                    "properties": {
                        "include_memory_stats": {"type": "boolean", "default": false},
                        "include_active_goals": {"type": "boolean", "default": true}
                    }
                },
                self._get_agent_state_handler
            )
            
            # Default resources
            server.register_resource(
                f"agent://{self.agent_id}/profile",
                "Agent Profile",
                "Agent configuration and capabilities",
                "application/json",
                self._get_agent_profile_handler
            )
            
            server.register_resource(
                f"agent://{self.agent_id}/memories",
                "Agent Memories",
                "Recent agent memories",
                "application/json",
                self._get_recent_memories_handler
            )
        
        async def _search_memory_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Handle memory search requests."""
            
            from src.memory import search_memories
            
            results = await search_memories(
                self.db,
                self.agent_id,
                params["query"],
                memory_types=params.get("memory_types"),
                limit=params.get("limit", 10)
            )
            
            return {
                "memories": [
                    {
                        "id": m.id,
                        "type": m.type,
                        "content": m.content,
                        "importance": m.importance,
                        "created_at": m.created_at.isoformat()
                    }
                    for m in results
                ],
                "count": len(results)
            }
        
        async def _manage_goals_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Handle goal management requests."""
            
            from src.memory.prospective import ProspectiveMemoryManager
            
            pmm = ProspectiveMemoryManager(self.db)
            
            action = params["action"]
            
            if action == "create":
                goal = await pmm.create_goal(
                    self.agent_id,
                    params["goal"],
                    deadline=params.get("deadline"),
                    priority=params.get("priority", 5)
                )
                return {"goal_id": goal.id, "status": "created"}
            
            elif action == "update":
                await pmm.update_goal_progress(
                    params["goal_id"],
                    params.get("progress", 0),
                    params.get("checkpoint")
                )
                return {"status": "updated"}
            
            elif action == "list":
                goals = await pmm.get_active_goals(self.agent_id)
                return {
                    "goals": [
                        {
                            "id": g.id,
                            "content": g.content,
                            "priority": g.priority,
                            "progress": g.progress,
                            "deadline": g.deadline.isoformat() if g.deadline else None
                        }
                        for g in goals
                    ]
                }
            
            elif action == "complete":
                await pmm.complete_goal(params["goal_id"])
                return {"status": "completed"}
        
        async def _get_agent_state_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
            """Handle agent state requests."""
            
            state = {
                "agent_id": self.agent_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            if params.get("include_memory_stats"):
                sql = """
                SELECT type, COUNT(*) as count,
                       AVG(importance) as avg_importance
                FROM memory.memories
                WHERE agent_id = :agent_id
                GROUP BY type
                """
                
                result = await self.db.execute(sql, {"agent_id": self.agent_id})
                stats = result.fetchall()
                
                state["memory_stats"] = {
                    row["type"]: {
                        "count": row["count"],
                        "avg_importance": float(row["avg_importance"])
                    }
                    for row in stats
                }
            
            if params.get("include_active_goals", True):
                from src.memory.prospective import ProspectiveMemoryManager
                
                pmm = ProspectiveMemoryManager(self.db)
                goals = await pmm.get_active_goals(self.agent_id)
                
                state["active_goals"] = [
                    {
                        "id": g.id,
                        "content": g.content,
                        "priority": g.priority,
                        "progress": g.progress
                    }
                    for g in goals[:5]  # Top 5 goals
                ]
            
            return state
        
        async def _get_agent_profile_handler(self) -> str:
            """Get agent profile as JSON."""
            
            sql = """
            SELECT name, type, model, metadata, mcp_servers, a2a_capabilities
            FROM agents.agents
            WHERE id = :agent_id
            """
            
            result = await self.db.execute(sql, {"agent_id": self.agent_id})
            agent = result.fetchone()
            
            profile = {
                "id": self.agent_id,
                "name": agent["name"],
                "type": agent["type"],
                "model": agent["model"],
                "capabilities": {
                    "mcp_servers": len(agent["mcp_servers"] or []),
                    "a2a_enabled": agent["a2a_capabilities"] is not None
                },
                "metadata": agent["metadata"]
            }
            
            return json.dumps(profile, indent=2)
        
        async def _get_recent_memories_handler(self) -> str:
            """Get recent memories as JSON."""
            
            sql = """
            SELECT id, type, content, importance, created_at
            FROM memory.memories
            WHERE agent_id = :agent_id
            ORDER BY created_at DESC
            LIMIT 20
            """
            
            result = await self.db.execute(sql, {"agent_id": self.agent_id})
            memories = result.fetchall()
            
            memory_list = [
                {
                    "id": m["id"],
                    "type": m["type"],
                    "content": m["content"],
                    "importance": float(m["importance"]),
                    "created_at": m["created_at"].isoformat()
                }
                for m in memories
            ]
            
            return json.dumps(memory_list, indent=2)
        
        def _get_server_by_name(self, name: str) -> Optional[MCPServer]:
            """Get server by name."""
            
            for server in self.servers.values():
                if server.name == name:
                    return server
            return None
        
        async def _get_cached_resource(
            self,
            server_id: str,
            uri: str
        ) -> Optional[str]:
            """Get cached resource content."""
            
            sql = """
            SELECT cached_content
            FROM protocols.mcp_resources
            WHERE server_id = :server_id AND uri = :uri
              AND cached_at > NOW() - INTERVAL '1 hour'
            """
            
            result = await self.db.execute(
                sql,
                {"server_id": server_id, "uri": uri}
            )
            
            row = result.fetchone()
            return row["cached_content"] if row else None

* * *

## 8\. A2A Protocol Implementation {#a2a-protocol}

### A2A Agent Implementation

**`src/protocols/a2a/agent.py`**

python

    import asyncio
    from typing import Dict, Any, List, Optional, Callable
    from dataclasses import dataclass
    from enum import Enum
    import uuid
    from datetime import datetime
    
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.database import get_db
    
    class TaskStatus(str, Enum):
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"
        CANCELLED = "cancelled"
    
    @dataclass
    class A2AAgentCard:
        agent_id: str
        name: str
        capabilities: List[str]
        protocols: List[str] = None
        authentication: Optional[Dict[str, Any]] = None
        endpoints: Optional[Dict[str, str]] = None
        metadata: Optional[Dict[str, Any]] = None
    
    @dataclass
    class A2ATask:
        id: str
        client_agent: str
        remote_agent: str
        name: str
        description: Optional[str]
        input: Optional[Dict[str, Any]]
        status: TaskStatus
        progress: float = 0.0
        created_at: datetime = None
        updated_at: datetime = None
        completed_at: Optional[datetime] = None
        output: Optional[Dict[str, Any]] = None
        error: Optional[str] = None
        artifacts: List[Dict[str, Any]] = None
        messages: List[Dict[str, Any]] = None
    
    class A2AAgent:
        """Agent-to-Agent protocol implementation."""
        
        def __init__(
            self,
            agent_id: str,
            db_session: AsyncSession
        ):
            self.agent_id = agent_id
            self.db = db_session
            self._task_handlers: Dict[str, Callable] = {}
            self._running_tasks: Dict[str, asyncio.Task] = {}
            self._agent_card: Optional[A2AAgentCard] = None
        
        async def initialize(self):
            """Initialize A2A agent from configuration."""
            
            # Load agent card
            self._agent_card = await self._load_agent_card()
            
            # Register default task handlers
            self._register_default_handlers()
            
            # Start task processor
            asyncio.create_task(self._process_tasks())
        
        async def register_capability(
            self,
            capability: str,
            handler: Callable[[A2ATask], None]
        ):
            """Register a capability handler."""
            
            self._task_handlers[capability] = handler
            
            # Update agent card
            if capability not in self._agent_card.capabilities:
                self._agent_card.capabilities.append(capability)
                await self._update_agent_card()
        
        async def create_task(
            self,
            remote_agent: str,
            task_name: str,
            task_input: Optional[Dict[str, Any]] = None,
            description: Optional[str] = None
        ) -> A2ATask:
            """Create a new task for a remote agent."""
            
            # Verify remote agent exists and is capable
            remote_card = await self._get_remote_agent_card(remote_agent)
            if not remote_card:
                raise ValueError(f"Remote agent not found: {remote_agent}")
            
            # Create task
            task = A2ATask(
                id=str(uuid.uuid4()),
                client_agent=self.agent_id,
                remote_agent=remote_agent,
                name=task_name,
                description=description,
                input=task_input,
                status=TaskStatus.PENDING,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Store in database
            await self._store_task(task)
            
            # Queue task for remote agent
            await self._queue_task_for_remote(task)
            
            return task
        
        async def get_task(self, task_id: str) -> Optional[A2ATask]:
            """Get task by ID."""
            
            sql = """
            SELECT t.*, 
                   ARRAY_AGG(DISTINCT a.*) as artifacts,
                   ARRAY_AGG(DISTINCT m.*) as messages
            FROM protocols.a2a_tasks t
            LEFT JOIN protocols.a2a_artifacts a ON t.id = a.task_id
            LEFT JOIN protocols.a2a_messages m ON t.id = m.task_id
            WHERE t.id = :task_id
            GROUP BY t.id
            """
            
            result = await self.db.execute(sql, {"task_id": task_id})
            row = result.fetchone()
            
            if not row:
                return None
            
            return self._row_to_task(row)
        
        async def update_task_progress(
            self,
            task_id: str,
            progress: float,
            message: Optional[str] = None
        ):
            """Update task progress."""
            
            sql = """
            UPDATE protocols.a2a_tasks
            SET progress = :progress,
                updated_at = NOW()
            WHERE id = :task_id
            """
            
            await self.db.execute(
                sql,
                {"task_id": task_id, "progress": progress}
            )
            
            if message:
                await self.send_task_message(task_id, message)
            
            await self.db.commit()
        
        async def complete_task(
            self,
            task_id: str,
            output: Dict[str, Any],
            artifacts: Optional[List[Dict[str, Any]]] = None
        ):
            """Complete a task successfully."""
            
            sql = """
            UPDATE protocols.a2a_tasks
            SET status = :status,
                progress = 1.0,
                output = :output,
                completed_at = NOW(),
                updated_at = NOW()
            WHERE id = :task_id
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "status": TaskStatus.COMPLETED,
                    "output": output
                }
            )
            
            # Store artifacts
            if artifacts:
                for artifact in artifacts:
                    await self._store_artifact(task_id, artifact)
            
            await self.db.commit()
            
            # Notify client
            await self._notify_task_completion(task_id)
        
        async def fail_task(
            self,
            task_id: str,
            error: str
        ):
            """Fail a task with error."""
            
            sql = """
            UPDATE protocols.a2a_tasks
            SET status = :status,
                error = :error,
                completed_at = NOW(),
                updated_at = NOW()
            WHERE id = :task_id
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "status": TaskStatus.FAILED,
                    "error": error
                }
            )
            
            await self.db.commit()
            
            # Notify client
            await self._notify_task_failure(task_id)
        
        async def send_task_message(
            self,
            task_id: str,
            content: str,
            parts: Optional[List[Dict[str, Any]]] = None
        ):
            """Send a message about a task."""
            
            sql = """
            INSERT INTO protocols.a2a_messages (
                task_id, sender, content, parts, created_at
            ) VALUES (
                :task_id, :sender, :content, :parts, NOW()
            )
            """
            
            # Determine if we're client or remote
            task = await self.get_task(task_id)
            sender = "client" if task.client_agent == self.agent_id else "remote"
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "sender": sender,
                    "content": content,
                    "parts": parts or []
                }
            )
            
            await self.db.commit()
            
            # Queue message for delivery
            await self._queue_message_delivery(task_id, content, parts)
        
        async def discover_agents(
            self,
            capabilities: Optional[List[str]] = None
        ) -> List[A2AAgentCard]:
            """Discover available agents."""
            
            sql = """
            SELECT a.*, ag.name
            FROM protocols.a2a_agents a
            JOIN agents.agents ag ON a.agent_id = ag.id
            WHERE a.is_public = true
              AND a.is_active = true
              AND ag.is_active = true
            """
            
            params = {}
            
            if capabilities:
                sql += " AND a.capabilities && :capabilities"
                params["capabilities"] = capabilities
            
            sql += " ORDER BY a.last_seen DESC"
            
            result = await self.db.execute(sql, params)
            rows = result.fetchall()
            
            return [
                A2AAgentCard(
                    agent_id=row["agent_id"],
                    name=row["name"],
                    capabilities=row["capabilities"],
                    protocols=row["protocols"],
                    authentication=row["authentication"],
                    endpoints=row["endpoints"],
                    metadata=row["discovery_metadata"]
                )
                for row in rows
            ]
        
        async def _process_tasks(self):
            """Background task processor."""
            
            while True:
                try:
                    # Get pending tasks for this agent
                    sql = """
                    SELECT *
                    FROM protocols.a2a_tasks
                    WHERE remote_agent = :agent_id
                      AND status = 'pending'
                    ORDER BY created_at
                    LIMIT 10
                    """
                    
                    result = await self.db.execute(
                        sql, {"agent_id": self.agent_id}
                    )
                    tasks = result.fetchall()
                    
                    for task_row in tasks:
                        task = self._row_to_task(task_row)
                        
                        # Find appropriate handler
                        handler = self._find_task_handler(task)
                        if handler:
                            # Start task processing
                            asyncio_task = asyncio.create_task(
                                self._execute_task(task, handler)
                            )
                            self._running_tasks[task.id] = asyncio_task
                        else:
                            # No handler found
                            await self.fail_task(
                                task.id,
                                f"No handler found for task: {task.name}"
                            )
                    
                    # Wait before next check
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    # Log error and continue
                    print(f"Task processor error: {e}")
                    await asyncio.sleep(5)
        
        async def _execute_task(
            self,
            task: A2ATask,
            handler: Callable
        ):
            """Execute a task with handler."""
            
            try:
                # Update status to running
                await self._update_task_status(task.id, TaskStatus.RUNNING)
                
                # Execute handler
                await handler(task)
                
                # Handler should call complete_task or fail_task
                
            except Exception as e:
                # Task failed
                await self.fail_task(task.id, str(e))
            
            finally:
                # Remove from running tasks
                self._running_tasks.pop(task.id, None)
        
        def _register_default_handlers(self):
            """Register default task handlers."""
            
            # Memory search handler
            self._task_handlers["memory_search"] = self._handle_memory_search
            
            # Question answering handler
            self._task_handlers["question_answer"] = self._handle_question_answer
            
            # Collaboration request handler
            self._task_handlers["collaborate"] = self._handle_collaboration
        
        async def _handle_memory_search(self, task: A2ATask):
            """Handle memory search tasks."""
            
            from src.memory import search_memories
            
            query = task.input.get("query", "")
            memory_types = task.input.get("memory_types")
            limit = task.input.get("limit", 10)
            
            # Search memories
            results = await search_memories(
                self.db,
                self.agent_id,
                query,
                memory_types=memory_types,
                limit=limit
            )
            
            # Format results
            output = {
                "memories": [
                    {
                        "id": m.id,
                        "type": m.type,
                        "content": m.content,
                        "importance": m.importance,
                        "metadata": m.metadata
                    }
                    for m in results
                ],
                "count": len(results)
            }
            
            await self.complete_task(task.id, output)
        
        async def _handle_question_answer(self, task: A2ATask):
            """Handle question answering tasks."""
            
            question = task.input.get("question", "")
            context = task.input.get("context", {})
            
            # Update progress
            await self.update_task_progress(task.id, 0.2, "Processing question")
            
            # Search relevant memories
            from src.memory import search_memories
            
            memories = await search_memories(
                self.db,
                self.agent_id,
                question,
                limit=5
            )
            
            await self.update_task_progress(task.id, 0.5, "Generating answer")
            
            # Generate answer using LLM
            # This is a placeholder - integrate with actual LLM
            answer = f"Based on my knowledge: {question} [Generated answer]"
            
            sources = [
                {
                    "type": m.type,
                    "content": m.content[:200] + "...",
                    "relevance": 0.8  # Placeholder
                }
                for m in memories
            ]
            
            output = {
                "answer": answer,
                "sources": sources,
                "confidence": 0.85
            }
            
            await self.complete_task(task.id, output)
        
        async def _handle_collaboration(self, task: A2ATask):
            """Handle collaboration requests."""
            
            collab_type = task.input.get("type", "general")
            
            if collab_type == "brainstorm":
                await self._handle_brainstorm(task)
            elif collab_type == "review":
                await self._handle_review(task)
            else:
                await self.send_task_message(
                    task.id,
                    f"Starting collaboration of type: {collab_type}"
                )
                
                # Simulate collaboration
                await asyncio.sleep(2)
                
                output = {
                    "result": "Collaboration completed",
                    "contributions": ["Idea 1", "Idea 2", "Idea 3"]
                }
                
                await self.complete_task(task.id, output)
        
        async def _handle_brainstorm(self, task: A2ATask):
            """Handle brainstorming collaboration."""
            
            topic = task.input.get("topic", "")
            
            await self.send_task_message(
                task.id,
                f"Starting brainstorm session on: {topic}"
            )
            
            # Generate ideas (placeholder)
            ideas = [
                f"Idea about {topic} #1",
                f"Idea about {topic} #2",
                f"Idea about {topic} #3"
            ]
            
            # Send ideas as messages
            for i, idea in enumerate(ideas):
                await self.update_task_progress(
                    task.id,
                    (i + 1) / len(ideas),
                    f"Generated idea: {idea}"
                )
                await asyncio.sleep(1)
            
            output = {
                "topic": topic,
                "ideas": ideas,
                "session_duration": 5
            }
            
            await self.complete_task(task.id, output)
        
        async def _handle_review(self, task: A2ATask):
            """Handle review collaboration."""
            
            content = task.input.get("content", "")
            review_type = task.input.get("review_type", "general")
            
            await self.send_task_message(
                task.id,
                f"Reviewing content for: {review_type}"
            )
            
            # Simulate review process
            await asyncio.sleep(3)
            
            feedback = {
                "overall": "Good work with minor improvements needed",
                "strengths": ["Clear structure", "Good examples"],
                "improvements": ["Add more detail in section 2", "Fix typo on line 15"],
                "rating": 4.2
            }
            
            await self.complete_task(task.id, {"feedback": feedback})
        
        async def _load_agent_card(self) -> A2AAgentCard:
            """Load agent card from database."""
            
            sql = """
            SELECT a.*, ag.name
            FROM protocols.a2a_agents a
            JOIN agents.agents ag ON a.agent_id = ag.id
            WHERE a.agent_id = :agent_id
            """
            
            result = await self.db.execute(sql, {"agent_id": self.agent_id})
            row = result.fetchone()
            
            if row:
                return A2AAgentCard(
                    agent_id=row["agent_id"],
                    name=row["name"],
                    capabilities=row["capabilities"],
                    protocols=row["protocols"],
                    authentication=row["authentication"],
                    endpoints=row["endpoints"]
                )
            else:
                # Create default agent card
                card = A2AAgentCard(
                    agent_id=self.agent_id,
                    name=f"Agent-{self.agent_id[:8]}",
                    capabilities=["memory_search", "question_answer"],
                    protocols=["a2a/v1"]
                )
                
                await self._create_agent_card(card)
                return card
        
        async def _create_agent_card(self, card: A2AAgentCard):
            """Create agent card in database."""
            
            sql = """
            INSERT INTO protocols.a2a_agents (
                agent_id, capabilities, protocols,
                authentication, endpoints, is_public, is_active
            ) VALUES (
                :agent_id, :capabilities, :protocols,
                :authentication, :endpoints, :is_public, true
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "agent_id": card.agent_id,
                    "capabilities": card.capabilities,
                    "protocols": card.protocols or ["a2a/v1"],
                    "authentication": card.authentication,
                    "endpoints": card.endpoints,
                    "is_public": True  # Default to public for prototype
                }
            )
            await self.db.commit()
        
        async def _update_agent_card(self):
            """Update agent card in database."""
            
            sql = """
            UPDATE protocols.a2a_agents
            SET capabilities = :capabilities,
                last_seen = NOW()
            WHERE agent_id = :agent_id
            """
            
            await self.db.execute(
                sql,
                {
                    "agent_id": self.agent_id,
                    "capabilities": self._agent_card.capabilities
                }
            )
            await self.db.commit()
        
        async def _get_remote_agent_card(
            self,
            agent_id: str
        ) -> Optional[A2AAgentCard]:
            """Get remote agent's card."""
            
            sql = """
            SELECT a.*, ag.name
            FROM protocols.a2a_agents a
            JOIN agents.agents ag ON a.agent_id = ag.id
            WHERE a.agent_id = :agent_id
              AND a.is_active = true
            """
            
            result = await self.db.execute(sql, {"agent_id": agent_id})
            row = result.fetchone()
            
            if not row:
                return None
            
            return A2AAgentCard(
                agent_id=row["agent_id"],
                name=row["name"],
                capabilities=row["capabilities"],
                protocols=row["protocols"],
                authentication=row["authentication"],
                endpoints=row["endpoints"]
            )
        
        async def _store_task(self, task: A2ATask):
            """Store task in database."""
            
            sql = """
            INSERT INTO protocols.a2a_tasks (
                id, client_agent, remote_agent,
                name, description, input,
                status, progress,
                created_at, updated_at
            ) VALUES (
                :id, :client_agent, :remote_agent,
                :name, :description, :input,
                :status, :progress,
                :created_at, :updated_at
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": task.id,
                    "client_agent": task.client_agent,
                    "remote_agent": task.remote_agent,
                    "name": task.name,
                    "description": task.description,
                    "input": task.input,
                    "status": task.status,
                    "progress": task.progress,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
            )
            await self.db.commit()
        
        async def _store_artifact(
            self,
            task_id: str,
            artifact: Dict[str, Any]
        ):
            """Store task artifact."""
            
            sql = """
            INSERT INTO protocols.a2a_artifacts (
                task_id, name, type, content, url, metadata
            ) VALUES (
                :task_id, :name, :type, :content, :url, :metadata
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "name": artifact["name"],
                    "type": artifact["type"],
                    "content": artifact.get("content"),
                    "url": artifact.get("url"),
                    "metadata": artifact.get("metadata", {})
                }
            )
            await self.db.commit()
        
        async def _queue_task_for_remote(self, task: A2ATask):
            """Queue task for remote agent processing."""
            
            # Use pgmq to queue task
            sql = """
            SELECT pgmq.send(
                'a2a_tasks',
                jsonb_build_object(
                    'task_id', :task_id,
                    'remote_agent', :remote_agent,
                    'notification_type', 'new_task'
                )
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task.id,
                    "remote_agent": task.remote_agent
                }
            )
            await self.db.commit()
        
        async def _queue_message_delivery(
            self,
            task_id: str,
            content: str,
            parts: Optional[List[Dict[str, Any]]]
        ):
            """Queue message for delivery."""
            
            # Get task to determine recipient
            task = await self.get_task(task_id)
            recipient = (
                task.client_agent
                if task.remote_agent == self.agent_id
                else task.remote_agent
            )
            
            sql = """
            SELECT pgmq.send(
                'a2a_messages',
                jsonb_build_object(
                    'task_id', :task_id,
                    'recipient', :recipient,
                    'content', :content,
                    'parts', :parts,
                    'sender', :sender
                )
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "recipient": recipient,
                    "content": content,
                    "parts": parts or [],
                    "sender": self.agent_id
                }
            )
            await self.db.commit()
        
        async def _notify_task_completion(self, task_id: str):
            """Notify client of task completion."""
            
            task = await self.get_task(task_id)
            
            sql = """
            SELECT pgmq.send(
                'a2a_notifications',
                jsonb_build_object(
                    'task_id', :task_id,
                    'recipient', :recipient,
                    'type', 'task_completed',
                    'data', jsonb_build_object(
                        'output', :output,
                        'artifacts', :artifacts
                    )
                )
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "recipient": task.client_agent,
                    "output": task.output,
                    "artifacts": task.artifacts
                }
            )
            await self.db.commit()
        
        async def _notify_task_failure(self, task_id: str):
            """Notify client of task failure."""
            
            task = await self.get_task(task_id)
            
            sql = """
            SELECT pgmq.send(
                'a2a_notifications',
                jsonb_build_object(
                    'task_id', :task_id,
                    'recipient', :recipient,
                    'type', 'task_failed',
                    'data', jsonb_build_object('error', :error)
                )
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "task_id": task_id,
                    "recipient": task.client_agent,
                    "error": task.error
                }
            )
            await self.db.commit()
        
        async def _update_task_status(
            self,
            task_id: str,
            status: TaskStatus
        ):
            """Update task status."""
            
            sql = """
            UPDATE protocols.a2a_tasks
            SET status = :status,
                updated_at = NOW()
            WHERE id = :task_id
            """
            
            await self.db.execute(
                sql,
                {"task_id": task_id, "status": status}
            )
            await self.db.commit()
        
        def _find_task_handler(
            self,
            task: A2ATask
        ) -> Optional[Callable]:
            """Find handler for task."""
            
            # Direct capability match
            if task.name in self._task_handlers:
                return self._task_handlers[task.name]
            
            # Check if task name contains capability
            for capability, handler in self._task_handlers.items():
                if capability in task.name:
                    return handler
            
            return None
        
        def _row_to_task(self, row: Any) -> A2ATask:
            """Convert database row to Task object."""
            
            return A2ATask(
                id=row["id"],
                client_agent=row["client_agent"],
                remote_agent=row["remote_agent"],
                name=row["name"],
                description=row["description"],
                input=row["input"],
                status=TaskStatus(row["status"]),
                progress=row["progress"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                completed_at=row["completed_at"],
                output=row["output"],
                error=row["error"],
                artifacts=row.get("artifacts", []),
                messages=row.get("messages", [])
            )

* * *

## 9\. DBOS Workflow Integration {#dbos-workflows}

### DBOS Workflow Base

**`src/workflows/base.py`**

python

    from typing import Any, Dict, Optional, TypeVar, Generic, Callable
    from datetime import datetime, timedelta
    import asyncio
    from functools import wraps
    from dataclasses import dataclass
    from enum import Enum
    
    from dbos import DBOS, workflow, step, scheduled
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    
    T = TypeVar('T')
    
    class WorkflowStatus(str, Enum):
        PENDING = "pending"
        RUNNING = "running"
        COMPLETED = "completed"
        FAILED = "failed"
        SUSPENDED = "suspended"
        CANCELLED = "cancelled"
    
    @dataclass
    class WorkflowContext:
        workflow_id: str
        agent_id: str
        input_data: Dict[str, Any]
        state: Dict[str, Any]
        created_at: datetime
        metadata: Dict[str, Any]
    
    class DBOSWorkflow(Generic[T]):
        """Base class for DBOS workflows."""
        
        def __init__(
            self,
            name: str,
            agent_id: str,
            db_session: AsyncSession
        ):
            self.name = name
            self.agent_id = agent_id
            self.db = db_session
            self._context: Optional[WorkflowContext] = None
        
        @property
        def context(self) -> WorkflowContext:
            """Get current workflow context."""
            if not self._context:
                raise RuntimeError("Workflow context not initialized")
            return self._context
        
        async def initialize_context(
            self,
            workflow_id: str,
            input_data: Dict[str, Any]
        ):
            """Initialize workflow context."""
            self._context = WorkflowContext(
                workflow_id=workflow_id,
                agent_id=self.agent_id,
                input_data=input_data,
                state={},
                created_at=datetime.utcnow(),
                metadata={}
            )
            
            # Store in database
            await self._store_workflow_instance()
        
        async def update_state(self, key: str, value: Any):
            """Update workflow state."""
            self.context.state[key] = value
            
            # Update in database
            sql = """
            UPDATE workflows.workflow_instances
            SET context = context || jsonb_build_object(:key, :value),
                updated_at = NOW()
            WHERE id = :workflow_id
            """
            
            await self.db.execute(
                sql,
                {
                    "workflow_id": self.context.workflow_id,
                    "key": key,
                    "value": value
                }
            )
            await self.db.commit()
        
        async def get_state(self, key: str, default: Any = None) -> Any:
            """Get value from workflow state."""
            return self.context.state.get(key, default)
        
        async def log_step(
            self,
            step_name: str,
            message: str,
            data: Optional[Dict[str, Any]] = None
        ):
            """Log workflow step execution."""
            sql = """
            INSERT INTO workflows.step_executions (
                instance_id, step_name, status,
                started_at, metadata
            ) VALUES (
                :instance_id, :step_name, 'running',
                NOW(), :metadata
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "instance_id": self.context.workflow_id,
                    "step_name": step_name,
                    "metadata": {
                        "message": message,
                        "data": data or {}
                    }
                }
            )
            await self.db.commit()
        
        async def _store_workflow_instance(self):
            """Store workflow instance in database."""
            
            # Get workflow definition ID
            definition_id = await self._get_or_create_definition()
            
            sql = """
            INSERT INTO workflows.workflow_instances (
                id, definition_id, agent_id,
                status, context, created_at
            ) VALUES (
                :id, :definition_id, :agent_id,
                'running', :context, :created_at
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": self.context.workflow_id,
                    "definition_id": definition_id,
                    "agent_id": self.agent_id,
                    "context": {
                        "input": self.context.input_data,
                        "state": self.context.state
                    },
                    "created_at": self.context.created_at
                }
            )
            await self.db.commit()
        
        async def _get_or_create_definition(self) -> str:
            """Get or create workflow definition."""
            
            sql = """
            INSERT INTO workflows.workflow_definitions (
                name, description, steps, is_active
            ) VALUES (
                :name, :description, :steps, true
            )
            ON CONFLICT (name) DO UPDATE
            SET updated_at = NOW()
            RETURNING id
            """
            
            result = await self.db.execute(
                sql,
                {
                    "name": self.name,
                    "description": f"DBOS workflow: {self.name}",
                    "steps": {"steps": []}  # Placeholder
                }
            )
            
            row = result.fetchone()
            return row["id"]
    
    def dbos_workflow(name: str):
        """Decorator for DBOS workflows."""
        def decorator(func: Callable) -> Callable:
            @workflow
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                # Initialize workflow context
                workflow_id = DBOS.workflow_id()
                await self.initialize_context(
                    workflow_id,
                    {"args": args, "kwargs": kwargs}
                )
                
                try:
                    # Execute workflow
                    result = await func(self, *args, **kwargs)
                    
                    # Mark as completed
                    await self._complete_workflow(result)
                    
                    return result
                    
                except Exception as e:
                    # Mark as failed
                    await self._fail_workflow(str(e))
                    raise
            
            return wrapper
        return decorator
    
    def dbos_step(name: str, retries: int = 3):
        """Decorator for DBOS workflow steps."""
        def decorator(func: Callable) -> Callable:
            @step
            @wraps(func)
            async def wrapper(self, *args, **kwargs):
                await self.log_step(name, f"Starting step: {name}")
                
                attempt = 0
                last_error = None
                
                while attempt < retries:
                    try:
                        result = await func(self, *args, **kwargs)
                        
                        # Log successful completion
                        await self._complete_step(name, result)
                        
                        return result
                        
                    except Exception as e:
                        attempt += 1
                        last_error = e
                        
                        if attempt < retries:
                            await self.log_step(
                                name,
                                f"Step failed, retrying ({attempt}/{retries})",
                                {"error": str(e)}
                            )
                            await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        else:
                            await self._fail_step(name, str(e))
                
                raise last_error
            
            return wrapper
        return decorator

### Memory Consolidation Workflow

**`src/workflows/memory_consolidation.py`**

python

    from typing import Dict, Any, List
    from datetime import datetime, timedelta
    
    from src.workflows.base import DBOSWorkflow, dbos_workflow, dbos_step
    from src.memory import MemoryType
    from src.memory.episodic import EpisodicMemoryManager
    from src.memory.semantic import SemanticMemoryManager
    
    class MemoryConsolidationWorkflow(DBOSWorkflow[Dict[str, Any]]):
        """Workflow for consolidating agent memories."""
        
        @dbos_workflow("memory_consolidation")
        async def run(
            self,
            memory_types: List[MemoryType] = None,
            min_importance: float = 0.3,
            time_window: timedelta = timedelta(days=7)
        ) -> Dict[str, Any]:
            """Run memory consolidation workflow."""
            
            # Store parameters
            await self.update_state("memory_types", memory_types)
            await self.update_state("min_importance", min_importance)
            await self.update_state("time_window", time_window.total_seconds())
            
            # Fetch memories
            memories = await self.fetch_recent_memories()
            await self.update_state("total_memories", len(memories))
            
            # Calculate importance scores
            scored_memories = await self.calculate_importance_scores(memories)
            
            # Apply decay
            decayed_memories = await self.apply_decay_function(scored_memories)
            
            # Find similar memories
            similarity_groups = await self.find_similar_memories(decayed_memories)
            
            # Consolidate similar memories
            consolidation_result = await self.consolidate_similar(similarity_groups)
            
            # Update relationship graph
            graph_result = await self.update_relationship_graph(
                consolidation_result["kept_memories"]
            )
            
            # Generate summary
            summary = {
                "total_processed": len(memories),
                "consolidated": consolidation_result["consolidated_count"],
                "removed": consolidation_result["removed_count"],
                "strengthened": consolidation_result["strengthened_count"],
                "new_relationships": graph_result["new_relationships"],
                "execution_time": (
                    datetime.utcnow() - self.context.created_at
                ).total_seconds()
            }
            
            return summary
        
        @dbos_step("fetch_recent_memories")
        async def fetch_recent_memories(self) -> List[Dict[str, Any]]:
            """Fetch recent memories for consolidation."""
            
            memory_types = await self.get_state("memory_types")
            time_window = timedelta(
                seconds=await self.get_state("time_window")
            )
            
            cutoff = datetime.utcnow() - time_window
            
            sql = """
            SELECT id, type, content, embedding, importance,
                   decayed_importance, access_count, created_at,
                   last_accessed_at, metadata, type_data
            FROM memory.memories
            WHERE agent_id = :agent_id
              AND created_at > :cutoff
            """
            
            params = {
                "agent_id": self.agent_id,
                "cutoff": cutoff
            }
            
            if memory_types:
                sql += " AND type = ANY(:types)"
                params["types"] = memory_types
            
            sql += " ORDER BY created_at DESC"
            
            result = await self.db.execute(sql, params)
            memories = [dict(row) for row in result.fetchall()]
            
            await self.log_step(
                "fetch_recent_memories",
                f"Fetched {len(memories)} memories",
                {"count": len(memories)}
            )
            
            return memories
        
        @dbos_step("calculate_importance_scores")
        async def calculate_importance_scores(
            self,
            memories: List[Dict[str, Any]]
        ) -> List[Dict[str, Any]]:
            """Calculate updated importance scores."""
            
            scored_memories = []
            
            for memory in memories:
                # Base importance
                base_importance = memory["importance"]
                
                # Access frequency factor
                access_factor = 1.0 + (memory["access_count"] * 0.1)
                
                # Recency factor
                age_days = (
                    datetime.utcnow() - memory["created_at"]
                ).days
                recency_factor = 1.0 / (1.0 + age_days * 0.1)
                
                # Type-specific factors
                type_factor = 1.0
                
                if memory["type"] == MemoryType.EPISODIC:
                    # Emotional memories are more important
                    emotional_valence = memory.get("type_data", {}).get(
                        "emotionalValence", 0
                    )
                    type_factor = 1.0 + abs(emotional_valence) * 0.5
                
                elif memory["type"] == MemoryType.PROSPECTIVE:
                    # Active goals are very important
                    status = memory.get("type_data", {}).get("status")
                    if status == "active":
                        type_factor = 2.0
                
                # Calculate final score
                final_importance = min(1.0,
                    base_importance * access_factor * 
                    recency_factor * type_factor
                )
                
                memory["calculated_importance"] = final_importance
                scored_memories.append(memory)
            
            await self.log_step(
                "calculate_importance_scores",
                "Calculated importance scores",
                {
                    "avg_importance": sum(
                        m["calculated_importance"] for m in scored_memories
                    ) / len(scored_memories)
                }
            )
            
            return scored_memories
        
        @dbos_step("apply_decay_function")
        async def apply_decay_function(
            self,
            memories: List[Dict[str, Any]]
        ) -> List[Dict[str, Any]]:
            """Apply forgetting curve decay."""
            
            min_importance = await self.get_state("min_importance")
            decayed_memories = []
            removed_count = 0
            
            for memory in memories:
                # Calculate time since last access
                time_since_access = (
                    datetime.utcnow() - memory["last_accessed_at"]
                ).total_seconds() / 86400  # Days
                
                # Apply exponential decay
                decay_rate = memory.get("decay_rate", 0.95)
                decayed_importance = (
                    memory["calculated_importance"] * 
                    (decay_rate ** time_since_access)
                )
                
                memory["decayed_importance"] = decayed_importance
                
                # Remove if below threshold
                if decayed_importance < min_importance:
                    removed_count += 1
                    # Mark for removal
                    memory["marked_for_removal"] = True
                else:
                    decayed_memories.append(memory)
            
            await self.log_step(
                "apply_decay_function",
                f"Applied decay, {removed_count} marked for removal",
                {"removed": removed_count, "kept": len(decayed_memories)}
            )
            
            return decayed_memories
        
        @dbos_step("find_similar_memories")
        async def find_similar_memories(
            self,
            memories: List[Dict[str, Any]]
        ) -> List[List[Dict[str, Any]]]:
            """Group similar memories."""
            
            import numpy as np
            from sklearn.cluster import DBSCAN
            
            # Extract embeddings
            embeddings = np.array([
                m["embedding"] for m in memories
                if m.get("embedding")
            ])
            
            if len(embeddings) < 2:
                return [[m] for m in memories]
            
            # Cluster using DBSCAN
            clustering = DBSCAN(
                eps=0.15,  # Similarity threshold
                min_samples=2,
                metric='cosine'
            ).fit(embeddings)
            
            # Group memories by cluster
            groups = {}
            for i, label in enumerate(clustering.labels_):
                if label == -1:  # Noise point
                    groups[f"single_{i}"] = [memories[i]]
                else:
                    if label not in groups:
                        groups[label] = []
                    groups[label].append(memories[i])
            
            similarity_groups = list(groups.values())
            
            await self.log_step(
                "find_similar_memories",
                f"Found {len(similarity_groups)} memory groups",
                {
                    "total_groups": len(similarity_groups),
                    "clustered_memories": sum(
                        len(g) for g in similarity_groups if len(g) > 1
                    )
                }
            )
            
            return similarity_groups
        
        @dbos_step("consolidate_similar")
        async def consolidate_similar(
            self,
            similarity_groups: List[List[Dict[str, Any]]]
        ) -> Dict[str, Any]:
            """Consolidate similar memories."""
            
            kept_memories = []
            consolidated_count = 0
            removed_count = 0
            strengthened_count = 0
            
            for group in similarity_groups:
                if len(group) == 1:
                    # Single memory, keep as is
                    kept_memories.append(group[0])
                    continue
                
                # Sort by importance
                group.sort(
                    key=lambda m: m["decayed_importance"],
                    reverse=True
                )
                
                # Keep the most important memory
                primary = group[0]
                
                # Consolidate others into primary
                for secondary in group[1:]:
                    # Check if memories are from same type and time period
                    same_type = primary["type"] == secondary["type"]
                    
                    time_diff = abs(
                        (primary["created_at"] - secondary["created_at"])
                        .total_seconds()
                    )
                    same_period = time_diff < 86400  # Within 24 hours
                    
                    if same_type and same_period:
                        # Merge memories
                        primary["content"] = (
                            f"{primary['content']}\n\n"
                            f"[Consolidated: {secondary['content'][:100]}...]"
                        )
                        
                        # Boost importance
                        primary["importance"] = min(
                            1.0,
                            primary["importance"] + 0.1
                        )
                        
                        # Update access count
                        primary["access_count"] += secondary["access_count"]
                        
                        # Mark secondary for removal
                        removed_count += 1
                        consolidated_count += 1
                    else:
                        # Different type or time, create relationship
                        await self._create_memory_relationship(
                            primary["id"],
                            secondary["id"],
                            "similar_to"
                        )
                        strengthened_count += 1
                        kept_memories.append(secondary)
                
                kept_memories.append(primary)
            
            # Update database
            await self._update_consolidated_memories(kept_memories)
            
            result = {
                "kept_memories": kept_memories,
                "consolidated_count": consolidated_count,
                "removed_count": removed_count,
                "strengthened_count": strengthened_count
            }
            
            await self.log_step(
                "consolidate_similar",
                "Completed consolidation",
                result
            )
            
            return result
        
        @dbos_step("update_relationship_graph")
        async def update_relationship_graph(
            self,
            memories: List[Dict[str, Any]]
        ) -> Dict[str, Any]:
            """Update memory relationship graph."""
            
            new_relationships = 0
            
            # Build concept co-occurrence relationships
            for i, mem1 in enumerate(memories):
                if mem1["type"] != MemoryType.SEMANTIC:
                    continue
                
                concepts1 = set(mem1.get("type_data", {}).get("concepts", []))
                
                for mem2 in memories[i+1:]:
                    if mem2["type"] != MemoryType.SEMANTIC:
                        continue
                    
                    concepts2 = set(mem2.get("type_data", {}).get("concepts", []))
                    
                    # Check for concept overlap
                    overlap = concepts1 & concepts2
                    if overlap:
                        await self._create_memory_relationship(
                            mem1["id"],
                            mem2["id"],
                            "shares_concepts",
                            metadata={"concepts": list(overlap)}
                        )
                        new_relationships += 1
            
            # Build temporal relationships for episodic memories
            episodic_memories = [
                m for m in memories
                if m["type"] == MemoryType.EPISODIC
            ]
            
            episodic_memories.sort(key=lambda m: m["created_at"])
            
            for i in range(len(episodic_memories) - 1):
                if (episodic_memories[i+1]["created_at"] - 
                    episodic_memories[i]["created_at"]).total_seconds() < 3600:
                    
                    await self._create_memory_relationship(
                        episodic_memories[i]["id"],
                        episodic_memories[i+1]["id"],
                        "followed_by"
                    )
                    new_relationships += 1
            
            result = {
                "new_relationships": new_relationships,
                "total_memories": len(memories)
            }
            
            await self.log_step(
                "update_relationship_graph",
                "Updated relationship graph",
                result
            )
            
            return result
        
        async def _create_memory_relationship(
            self,
            source_id: str,
            target_id: str,
            relationship_type: str,
            metadata: Dict[str, Any] = None
        ):
            """Create relationship between memories."""
            
            sql = """
            INSERT INTO memory.relationships (
                source_memory, target_memory,
                relationship_type, metadata
            ) VALUES (
                :source, :target, :type, :metadata
            )
            ON CONFLICT (source_memory, target_memory, relationship_type)
            DO UPDATE SET
                strength = relationships.strength + 0.1,
                metadata = relationships.metadata || :metadata
            """
            
            await self.db.execute(
                sql,
                {
                    "source": source_id,
                    "target": target_id,
                    "type": relationship_type,
                    "metadata": metadata or {}
                }
            )
        
        async def _update_consolidated_memories(
            self,
            memories: List[Dict[str, Any]]
        ):
            """Update consolidated memories in database."""
            
            for memory in memories:
                if memory.get("marked_for_removal"):
                    # Delete memory
                    sql = "DELETE FROM memory.memories WHERE id = :id"
                    await self.db.execute(sql, {"id": memory["id"]})
                else:
                    # Update memory
                    sql = """
                    UPDATE memory.memories
                    SET content = :content,
                        importance = :importance,
                        decayed_importance = :decayed_importance,
                        access_count = :access_count,
                        updated_at = NOW()
                    WHERE id = :id
                    """
                    
                    await self.db.execute(
                        sql,
                        {
                            "id": memory["id"],
                            "content": memory["content"],
                            "importance": memory.get("importance"),
                            "decayed_importance": memory.get("decayed_importance"),
                            "access_count": memory.get("access_count")
                        }
                    )
            
            await self.db.commit()
        
        async def _complete_workflow(self, result: Dict[str, Any]):
            """Mark workflow as completed."""
            
            sql = """
            UPDATE workflows.workflow_instances
            SET status = 'completed',
                output = :output,
                completed_at = NOW()
            WHERE id = :workflow_id
            """
            
            await self.db.execute(
                sql,
                {
                    "workflow_id": self.context.workflow_id,
                    "output": result
                }
            )
            await self.db.commit()
        
        async def _fail_workflow(self, error: str):
            """Mark workflow as failed."""
            
            sql = """
            UPDATE workflows.workflow_instances
            SET status = 'failed',
                error = :error,
                completed_at = NOW()
            WHERE id = :workflow_id
            """
            
            await self.db.execute(
                sql,
                {
                    "workflow_id": self.context.workflow_id,
                    "error": {"message": error}
                }
            )
            await self.db.commit()
        
        async def _complete_step(self, step_name: str, result: Any):
            """Mark step as completed."""
            
            sql = """
            UPDATE workflows.step_executions
            SET status = 'completed',
                output = :output,
                completed_at = NOW(),
                duration_ms = EXTRACT(
                    MILLISECONDS FROM NOW() - started_at
                )
            WHERE instance_id = :instance_id
              AND step_name = :step_name
              AND status = 'running'
            """
            
            await self.db.execute(
                sql,
                {
                    "instance_id": self.context.workflow_id,
                    "step_name": step_name,
                    "output": {"result": str(result)[:1000]}
                }
            )
            await self.db.commit()
        
        async def _fail_step(self, step_name: str, error: str):
            """Mark step as failed."""
            
            sql = """
            UPDATE workflows.step_executions
            SET status = 'failed',
                error = :error,
                completed_at = NOW()
            WHERE instance_id = :instance_id
              AND step_name = :step_name
              AND status = 'running'
            """
            
            await self.db.execute(
                sql,
                {
                    "instance_id": self.context.workflow_id,
                    "step_name": step_name,
                    "error": {"message": error}
                }
            )
            await self.db.commit()

### Agent Conversation Workflow

**`src/workflows/agent_conversation.py`**

python

    from typing import Dict, Any, List, Optional
    from datetime import datetime
    
    from src.workflows.base import DBOSWorkflow, dbos_workflow, dbos_step
    from src.memory import MemoryType
    from src.memory.episodic import EpisodicMemoryManager
    from src.memory.semantic import SemanticMemoryManager
    from src.memory.prospective import ProspectiveMemoryManager
    from src.agents.llm import generate_completion
    
    class AgentConversationWorkflow(DBOSWorkflow[Dict[str, Any]]):
        """Workflow for handling agent conversations with memory integration."""
        
        @dbos_workflow("agent_conversation")
        async def run(
            self,
            session_id: str,
            user_message: str,
            context: Optional[Dict[str, Any]] = None
        ) -> Dict[str, Any]:
            """Process a conversation turn."""
            
            # Store parameters
            await self.update_state("session_id", session_id)
            await self.update_state("user_message", user_message)
            await self.update_state("context", context or {})
            
            # Retrieve relevant memories
            relevant_memories = await self.retrieve_relevant_memories(user_message)
            
            # Generate response
            response = await self.generate_response(
                user_message,
                relevant_memories
            )
            
            # Extract memories from conversation
            extracted_memories = await self.extract_memories(
                user_message,
                response["content"]
            )
            
            # Store new memories
            stored_memories = await self.store_memories(extracted_memories)
            
            # Update goals if needed
            goal_updates = await self.update_goals(
                user_message,
                response["content"]
            )
            
            # Store message in session
            await self.store_message(
                session_id,
                user_message,
                response["content"]
            )
            
            return {
                "response": response["content"],
                "relevant_memories": len(relevant_memories),
                "new_memories": len(stored_memories),
                "goal_updates": goal_updates,
                "tokens_used": response.get("tokens_used", 0)
            }
        
        @dbos_step("retrieve_relevant_memories")
        async def retrieve_relevant_memories(
            self,
            query: str
        ) -> List[Dict[str, Any]]:
            """Retrieve memories relevant to the query."""
            
            # Search across all memory types
            sql = """
            SELECT * FROM memory.search_memories(
                :agent_id,
                :query,
                NULL,  -- All types
                20,    -- Limit
                0.7,   -- Threshold
                false  -- Don't include heavily decayed
            )
            """
            
            result = await self.db.execute(
                sql,
                {"agent_id": self.agent_id, "query": query}
            )
            
            memories = []
            for row in result.fetchall():
                memory = dict(row)
                
                # Enhance with type-specific data
                if memory["type"] == MemoryType.EPISODIC:
                    # Add temporal context
                    memory["temporal_distance"] = (
                        datetime.utcnow() - memory["created_at"]
                    ).days
                
                elif memory["type"] == MemoryType.SEMANTIC:
                    # Add confidence score
                    memory["confidence"] = memory.get("metadata", {}).get(
                        "confidence", 1.0
                    )
                
                elif memory["type"] == MemoryType.PROSPECTIVE:
                    # Add goal status
                    memory["goal_active"] = (
                        memory.get("metadata", {}).get("status") == "active"
                    )
                
                memories.append(memory)
            
            # Sort by relevance and importance
            memories.sort(
                key=lambda m: m["similarity"] * m["importance"],
                reverse=True
            )
            
            await self.log_step(
                "retrieve_relevant_memories",
                f"Retrieved {len(memories)} relevant memories",
                {"count": len(memories)}
            )
            
            return memories[:10]  # Top 10 most relevant
        
        @dbos_step("generate_response")
        async def generate_response(
            self,
            user_message: str,
            memories: List[Dict[str, Any]]
        ) -> Dict[str, Any]:
            """Generate LLM response with memory context."""
            
            # Get session context
            session_id = await self.get_state("session_id")
            
            # Get conversation history
            sql = """
            SELECT role, content
            FROM agents.messages
            WHERE session_id = :session_id
            ORDER BY created_at DESC
            LIMIT 10
            """
            
            result = await self.db.execute(
                sql, {"session_id": session_id}
            )
            
            history = [
                {"role": row["role"], "content": row["content"]}
                for row in reversed(result.fetchall())
            ]
            
            # Format memories for context
            memory_context = self._format_memory_context(memories)
            
            # Build system prompt with memory context
            system_prompt = f"""You are a helpful AI assistant with access to your memories.
    
    Relevant memories:
    {memory_context}
    
    Use these memories to provide more personalized and contextual responses.
    If you reference a memory, be natural about it - don't explicitly say "according to my memories".
    """
            
            # Add current message
            messages = [
                {"role": "system", "content": system_prompt}
            ] + history + [
                {"role": "user", "content": user_message}
            ]
            
            # Generate response
            response = await generate_completion(
                self.db,
                self.agent_id,
                messages
            )
            
            await self.log_step(
                "generate_response",
                "Generated response",
                {
                    "tokens_used": response.get("tokens_used", 0),
                    "model": response.get("model", "unknown")
                }
            )
            
            return response
        
        @dbos_step("extract_memories")
        async def extract_memories(
            self,
            user_message: str,
            assistant_response: str
        ) -> List[Dict[str, Any]]:
            """Extract memories from conversation."""
            
            context = await self.get_state("context")
            
            # Use LLM to extract memories
            extraction_prompt = f"""Analyze this conversation and extract important information that should be remembered.
    
    User: {user_message}
    Assistant: {assistant_response}
    
    Extract:
    1. Facts or information that should be stored as semantic memory
    2. Events or experiences that should be stored as episodic memory
    3. Goals or tasks mentioned that should be tracked
    4. Patterns of behavior or preferences
    
    Format as JSON array with objects containing:
    - type: "episodic", "semantic", or "prospective"
    - content: The memory content
    - importance: 0-1 score
    - metadata: Any relevant metadata
    """
            
            extraction_response = await generate_completion(
                self.db,
                self.agent_id,
                [
                    {"role": "system", "content": "You are a memory extraction system."},
                    {"role": "user", "content": extraction_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_array"}
            )
            
            try:
                extracted = json.loads(extraction_response["content"])
            except:
                extracted = []
            
            # Add conversation context
            for memory in extracted:
                memory["source_context"] = {
                    "conversation_id": await self.get_state("session_id"),
                    "user_message": user_message,
                    "assistant_response": assistant_response[:200],
                    **context
                }
            
            # Always create episodic memory of the conversation
            conversation_memory = {
                "type": "episodic",
                "content": f"User: {user_message}\nAssistant: {assistant_response[:200]}...",
                "importance": 0.5,
                "metadata": {
                    "conversation_turn": True,
                    "session_id": await self.get_state("session_id")
                },
                "source_context": context
            }
            
            extracted.append(conversation_memory)
            
            await self.log_step(
                "extract_memories",
                f"Extracted {len(extracted)} memories",
                {"count": len(extracted)}
            )
            
            return extracted
        
        @dbos_step("store_memories")
        async def store_memories(
            self,
            memories: List[Dict[str, Any]]
        ) -> List[str]:
            """Store extracted memories."""
            
            stored_ids = []
            
            emm = EpisodicMemoryManager(self.db)
            smm = SemanticMemoryManager(self.db)
            pmm = ProspectiveMemoryManager(self.db)
            
            for memory in memories:
                try:
                    if memory["type"] == "episodic":
                        stored = await emm.store_episode(
                            self.agent_id,
                            memory["content"],
                            memory.get("source_context", {}),
                            emotional_valence=memory.get("emotional_valence")
                        )
                        stored_ids.append(stored.id)
                    
                    elif memory["type"] == "semantic":
                        stored = await smm.store_fact(
                            self.agent_id,
                            memory["content"],
                            concepts=memory.get("concepts"),
                            confidence=memory.get("confidence", 1.0),
                            source="conversation"
                        )
                        stored_ids.append(stored.id)
                    
                    elif memory["type"] == "prospective":
                        stored = await pmm.create_goal(
                            self.agent_id,
                            memory["content"],
                            deadline=memory.get("deadline"),
                            priority=memory.get("priority", 5)
                        )
                        stored_ids.append(stored.id)
                    
                except Exception as e:
                    await self.log_step(
                        "store_memories",
                        f"Failed to store memory: {e}",
                        {"error": str(e), "memory": memory}
                    )
            
            await self.log_step(
                "store_memories",
                f"Stored {len(stored_ids)} memories",
                {"stored": stored_ids}
            )
            
            return stored_ids
        
        @dbos_step("update_goals")
        async def update_goals(
            self,
            user_message: str,
            assistant_response: str
        ) -> Dict[str, Any]:
            """Update goals based on conversation."""
            
            pmm = ProspectiveMemoryManager(self.db)
            
            updates = {
                "completed": [],
                "progressed": [],
                "new": []
            }
            
            # Check if any goals were mentioned
            active_goals = await pmm.get_active_goals(self.agent_id)
            
            for goal in active_goals:
                # Simple keyword matching - in production use NLP
                if any(keyword in user_message.lower() 
                       for keyword in ["done", "completed", "finished"]):
                    
                    if goal.content.lower() in user_message.lower():
                        await pmm.complete_goal(goal.id)
                        updates["completed"].append(goal.id)
                
                elif goal.content.lower() in user_message.lower():
                    # Goal was discussed, increment progress slightly
                    new_progress = min(1.0, goal.progress + 0.1)
                    await pmm.update_goal_progress(
                        goal.id,
                        new_progress,
                        f"Discussed in conversation"
                    )
                    updates["progressed"].append(goal.id)
            
            await self.log_step(
                "update_goals",
                "Updated goals",
                updates
            )
            
            return updates
        
        @dbos_step("store_message")
        async def store_message(
            self,
            session_id: str,
            user_message: str,
            assistant_response: str
        ):
            """Store messages in session history."""
            
            # Store user message
            sql = """
            INSERT INTO agents.messages (
                session_id, role, content, token_count
            ) VALUES (
                :session_id, 'user', :content,
                :token_count
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "session_id": session_id,
                    "content": user_message,
                    "token_count": len(user_message) // 4  # Rough estimate
                }
            )
            
            # Store assistant message
            await self.db.execute(
                sql,
                {
                    "session_id": session_id,
                    "content": assistant_response,
                    "token_count": len(assistant_response) // 4
                }
            )
            
            # Update session stats
            sql = """
            UPDATE agents.sessions
            SET message_count = message_count + 2,
                total_tokens_used = total_tokens_used + :tokens,
                updated_at = NOW()
            WHERE id = :session_id
            """
            
            response_data = await self.get_state("response_data", {})
            tokens_used = response_data.get("tokens_used", 
                (len(user_message) + len(assistant_response)) // 4
            )
            
            await self.db.execute(
                sql,
                {
                    "session_id": session_id,
                    "tokens": tokens_used
                }
            )
            
            await self.db.commit()
            
            await self.log_step(
                "store_message",
                "Stored messages in session",
                {"session_id": session_id}
            )
        
        def _format_memory_context(
            self,
            memories: List[Dict[str, Any]]
        ) -> str:
            """Format memories for LLM context."""
            
            if not memories:
                return "No relevant memories found."
            
            formatted = []
            
            for i, memory in enumerate(memories[:5]):  # Top 5 memories
                memory_str = f"{i+1}. "
                
                if memory["type"] == MemoryType.EPISODIC:
                    days_ago = memory.get("temporal_distance", 0)
                    memory_str += f"[{days_ago} days ago] "
                
                elif memory["type"] == MemoryType.SEMANTIC:
                    confidence = memory.get("confidence", 1.0)
                    memory_str += f"[Fact, confidence: {confidence:.1f}] "
                
                elif memory["type"] == MemoryType.PROSPECTIVE:
                    if memory.get("goal_active"):
                        memory_str += "[Active Goal] "
                    else:
                        memory_str += "[Completed Goal] "
                
                memory_str += memory["content"]
                
                if len(memory_str) > 200:
                    memory_str = memory_str[:197] + "..."
                
                formatted.append(memory_str)
            
            return "\n".join(formatted)

### Scheduled Workflows

**`src/workflows/scheduled.py`**

python

    from datetime import datetime, timedelta
    
    from dbos import scheduled
    from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
    from src.memory.prospective import ProspectiveMemoryManager
    
    @scheduled(cron="0 * * * *")  # Every hour
    async def consolidate_all_agent_memories():
        """Scheduled task to consolidate memories for all agents."""
        
        from src.database import get_db
        
        async with get_db() as db:
            # Get all active agents
            sql = """
            SELECT id, memory_config
            FROM agents.agents
            WHERE is_active = true
              AND (memory_config->>'consolidationInterval')::int > 0
            """
            
            result = await db.execute(sql)
            agents = result.fetchall()
            
            for agent in agents:
                try:
                    # Check if consolidation is due
                    interval = agent["memory_config"].get(
                        "consolidationInterval", 3600
                    )
                    
                    # Get last consolidation time
                    check_sql = """
                    SELECT MAX(completed_at) as last_run
                    FROM memory.consolidation_log
                    WHERE agent_id = :agent_id
                      AND error IS NULL
                    """
                    
                    check_result = await db.execute(
                        check_sql, {"agent_id": agent["id"]}
                    )
                    last_run = check_result.fetchone()["last_run"]
                    
                    if last_run and (
                        datetime.utcnow() - last_run
                    ).total_seconds() < interval:
                        continue
                    
                    # Run consolidation workflow
                    workflow = MemoryConsolidationWorkflow(
                        "scheduled_consolidation",
                        agent["id"],
                        db
                    )
                    
                    await workflow.run(
                        min_importance=agent["memory_config"].get(
                            "importanceThreshold", 0.3
                        )
                    )
                    
                except Exception as e:
                    print(f"Consolidation failed for agent {agent['id']}: {e}")
    
    @scheduled(cron="*/15 * * * *")  # Every 15 minutes
    async def check_prospective_memory_deadlines():
        """Check for approaching goal deadlines."""
        
        from src.database import get_db
        
        async with get_db() as db:
            pmm = ProspectiveMemoryManager(db)
            
            # Find goals with approaching deadlines
            sql = """
            SELECT DISTINCT m.agent_id
            FROM memory.memories m
            WHERE m.type = 'prospective'
              AND (m.type_data->>'status') = 'active'
              AND (m.type_data->>'deadline') IS NOT NULL
              AND (m.type_data->>'deadline')::timestamp < :threshold
              AND (m.type_data->>'deadline')::timestamp > NOW()
            """
            
            threshold = datetime.utcnow() + timedelta(hours=24)
            
            result = await db.execute(sql, {"threshold": threshold})
            agents = result.fetchall()
            
            for agent_row in agents:
                agent_id = agent_row["agent_id"]
                
                # Get goals approaching deadline
                goals = await pmm.get_active_goals(agent_id)
                
                for goal in goals:
                    if not goal.deadline:
                        continue
                    
                    time_until = goal.deadline - datetime.utcnow()
                    
                    if timedelta(0) < time_until < timedelta(hours=24):
                        # Create reminder
                        reminder_content = (
                            f"Reminder: Goal '{goal.content}' "
                            f"is due in {time_until.total_seconds() // 3600} hours"
                        )
                        
                        # Store as high-importance episodic memory
                        sql = """
                        INSERT INTO memory.memories (
                            agent_id, type, content, importance,
                            type_data, metadata
                        ) VALUES (
                            :agent_id, 'episodic', :content, 0.9,
                            jsonb_build_object(
                                'emotionalValence', -0.3,
                                'temporalContext', jsonb_build_object(
                                    'timestamp', :now,
                                    'context', 'deadline_reminder'
                                )
                            ),
                            jsonb_build_object(
                                'goal_id', :goal_id,
                                'is_reminder', true
                            )
                        )
                        """
                        
                        await db.execute(
                            sql,
                            {
                                "agent_id": agent_id,
                                "content": reminder_content,
                                "now": datetime.utcnow().isoformat(),
                                "goal_id": goal.id
                            }
                        )
                
                await db.commit()
    
    @scheduled(cron="0 0 * * 0")  # Weekly on Sunday
    async def weekly_agent_review():
        """Weekly review of agent performance and goals."""
        
        from src.database import get_db
        
        async with get_db() as db:
            sql = """
            SELECT id
            FROM agents.agents
            WHERE is_active = true
            """
            
            result = await db.execute(sql)
            agents = result.fetchall()
            
            for agent in agents:
                try:
                    pmm = ProspectiveMemoryManager(db)
                    
                    # Review goals
                    review = await pmm.review_goals(
                        agent["id"],
                        review_period=timedelta(days=7)
                    )
                    
                    # Store review as semantic memory
                    review_content = f"""Weekly Review:
    - Completed: {review['statistics']['completed_count']} goals
    - Active: {review['statistics']['active_count']} goals
    - Failed: {review['statistics']['failed_count']} goals
    - Average progress: {review['statistics'].get('avg_progress', 0):.1%}
    """
                    
                    if review['recommendations']:
                        review_content += "\nRecommendations:\n"
                        for rec in review['recommendations'][:3]:
                            review_content += f"- {rec['message']}\n"
                    
                    sql = """
                    INSERT INTO memory.memories (
                        agent_id, type, content, importance,
                        type_data, metadata
                    ) VALUES (
                        :agent_id, 'semantic', :content, 0.7,
                        jsonb_build_object(
                            'concepts', ARRAY['review', 'goals', 'performance'],
                            'confidence', 1.0
                        ),
                        jsonb_build_object(
                            'review_type', 'weekly',
                            'statistics', :stats
                        )
                    )
                    """
                    
                    await db.execute(
                        sql,
                        {
                            "agent_id": agent["id"],
                            "content": review_content,
                            "stats": review['statistics']
                        }
                    )
                    
                    await db.commit()
                    
                except Exception as e:
                    print(f"Weekly review failed for agent {agent['id']}: {e}")

* * *

## 10\. FastAPI Application Layer {#fastapi-layer}

### Application Configuration

**`src/config.py`**

python

    from typing import Optional, Dict, Any
    from pydantic_settings import BaseSettings, SettingsConfigDict
    from functools import lru_cache
    
    class Settings(BaseSettings):
        # Database
        database_url: str = "postgresql://postgres:postgres@localhost:5432/julep_v2"
        database_pool_size: int = 20
        database_max_overflow: int = 40
        
        # Redis (for pgmq)
        redis_url: Optional[str] = "redis://localhost:6379"
        
        # API Keys
        openai_api_key: Optional[str] = None
        anthropic_api_key: Optional[str] = None
        
        # Hasura
        hasura_graphql_endpoint: str = "http://localhost:8080/v1/graphql"
        hasura_admin_secret: str = "myadminsecret"
        
        # Application
        secret_key: str = "your-secret-key-here"
        environment: str = "development"
        log_level: str = "INFO"
        
        # DBOS
        dbos_database_url: Optional[str] = None
        dbos_namespace: str = "julep_v2"
        
        # Vector dimensions
        embedding_dimensions: int = 1536
        
        # API Settings
        api_title: str = "Julep V2 API"
        api_version: str = "0.1.0"
        api_prefix: str = "/api/v1"
        
        # CORS
        cors_origins: list[str] = ["*"]
        cors_credentials: bool = True
        cors_methods: list[str] = ["*"]
        cors_headers: list[str] = ["*"]
        
        # Rate Limiting
        rate_limit_enabled: bool = True
        rate_limit_default: str = "100/minute"
        rate_limit_burst: int = 20
        
        # Memory Settings
        memory_consolidation_interval: int = 3600  # seconds
        memory_decay_rate: float = 0.95
        memory_importance_threshold: float = 0.3
        
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False
        )
        
        @property
        def dbos_database_url_computed(self) -> str:
            return self.dbos_database_url or self.database_url
    
    @lru_cache()
    def get_settings() -> Settings:
        return Settings()
    
    # Export for convenience
    settings = get_settings()

### Database Connection Management

**`src/database.py`**

python

    from typing import AsyncGenerator, Optional
    from contextlib import asynccontextmanager
    from sqlalchemy.ext.asyncio import (
        AsyncSession, 
        AsyncEngine,
        create_async_engine,
        async_sessionmaker
    )
    from sqlalchemy.pool import NullPool, QueuePool
    from sqlalchemy.orm import declarative_base
    
    from src.config import settings
    
    # Create base class for SQLAlchemy models
    Base = declarative_base()
    
    # Global engine instance
    _engine: Optional[AsyncEngine] = None
    _session_factory: Optional[async_sessionmaker] = None
    
    def get_engine() -> AsyncEngine:
        """Get or create the database engine."""
        global _engine
        
        if _engine is None:
            # Use asyncpg for better performance
            database_url = settings.database_url.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
            
            _engine = create_async_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=settings.database_pool_size,
                max_overflow=settings.database_max_overflow,
                pool_pre_ping=True,  # Verify connections
                echo=settings.environment == "development",
                future=True
            )
        
        return _engine
    
    def get_session_factory() -> async_sessionmaker:
        """Get or create the session factory."""
        global _session_factory
        
        if _session_factory is None:
            _session_factory = async_sessionmaker(
                bind=get_engine(),
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False
            )
        
        return _session_factory
    
    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        """Dependency to get database session."""
        async with get_session_factory()() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    @asynccontextmanager
    async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
        """Context manager for database session."""
        async with get_session_factory()() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def init_db():
        """Initialize database (create tables, etc)."""
        engine = get_engine()
        
        async with engine.begin() as conn:
            # In production, use Alembic migrations instead
            # await conn.run_sync(Base.metadata.create_all)
            
            # Verify extensions are installed
            result = await conn.execute(
                "SELECT extname FROM pg_extension WHERE extname IN ('vector', 'pgmq', 'pg_jsonschema')"
            )
            installed = {row[0] for row in result}
            required = {'vector', 'pgmq', 'pg_jsonschema'}
            
            missing = required - installed
            if missing:
                raise RuntimeError(f"Missing required PostgreSQL extensions: {missing}")
    
    async def close_db():
        """Close database connections."""
        global _engine, _session_factory
        
        if _engine:
            await _engine.dispose()
            _engine = None
        
        _session_factory = None
    
    # Health check query
    async def check_db_health() -> bool:
        """Check if database is accessible."""
        try:
            async with get_db_context() as db:
                result = await db.execute("SELECT 1")
                return result.scalar() == 1
        except Exception:
            return False

### Main Application

**`src/api/main.py`**

python

    from contextlib import asynccontextmanager
    from typing import Dict, Any
    
    from fastapi import FastAPI, Request, status
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    from fastapi.responses import JSONResponse
    import uvicorn
    
    from src.config import settings
    from src.database import init_db, close_db, check_db_health
    from src.api.routers import (
        agents, memory, protocols, workflows, health
    )
    from src.api.middleware import (
        RateLimitMiddleware,
        RequestLoggingMiddleware,
        ErrorHandlingMiddleware
    )
    from src.utils.logging import setup_logging
    
    # Setup logging
    logger = setup_logging()
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Application lifespan events."""
        # Startup
        logger.info("Starting Julep V2 API")
        
        try:
            # Initialize database
            await init_db()
            logger.info("Database initialized")
            
            # Initialize DBOS
            if settings.environment == "production":
                from dbos import init_dbos
                init_dbos(settings.dbos_database_url_computed)
                logger.info("DBOS initialized")
            
            yield
            
        finally:
            # Shutdown
            logger.info("Shutting down Julep V2 API")
            await close_db()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        lifespan=lifespan
    )
    
    # Add middleware
    app.add_middleware(ErrorHandlingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    
    if settings.rate_limit_enabled:
        app.add_middleware(RateLimitMiddleware)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure in production
    )
    
    # Include routers
    app.include_router(
        agents.router,
        prefix=f"{settings.api_prefix}/agents",
        tags=["agents"]
    )
    
    app.include_router(
        memory.router,
        prefix=f"{settings.api_prefix}/memory",
        tags=["memory"]
    )
    
    app.include_router(
        protocols.router,
        prefix=f"{settings.api_prefix}/protocols",
        tags=["protocols"]
    )
    
    app.include_router(
        workflows.router,
        prefix=f"{settings.api_prefix}/workflows",
        tags=["workflows"]
    )
    
    app.include_router(
        health.router,
        prefix=f"{settings.api_prefix}/health",
        tags=["health"]
    )
    
    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "name": settings.api_title,
            "version": settings.api_version,
            "status": "running",
            "docs": f"{settings.api_prefix}/docs"
        }
    
    # Exception handlers
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Not Found",
                "message": f"Path {request.url.path} not found"
            }
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        logger.error(f"Internal server error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred"
            }
        )
    
    if __name__ == "__main__":
        uvicorn.run(
            "src.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.environment == "development",
            log_level=settings.log_level.lower()
        )

### API Middleware

**`src/api/middleware.py`**

python

    import time
    import uuid
    from typing import Callable, Dict, Any
    from datetime import datetime
    
    from fastapi import Request, Response, status
    from fastapi.responses import JSONResponse
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.types import ASGIApp
    
    from src.utils.logging import get_logger
    from src.utils.rate_limit import RateLimiter
    
    logger = get_logger(__name__)
    
    class RequestLoggingMiddleware(BaseHTTPMiddleware):
        """Log all requests with timing information."""
        
        async def dispatch(self, request: Request, call_next: Callable) -> Response:
            request_id = str(uuid.uuid4())
            
            # Add request ID to request state
            request.state.request_id = request_id
            
            # Log request
            logger.info(
                f"Request started",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "client": request.client.host if request.client else None
                }
            )
            
            # Time the request
            start_time = time.time()
            
            try:
                response = await call_next(request)
                
                # Calculate duration
                duration = time.time() - start_time
                
                # Add headers
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Response-Time"] = f"{duration:.3f}"
                
                # Log response
                logger.info(
                    f"Request completed",
                    extra={
                        "request_id": request_id,
                        "status_code": response.status_code,
                        "duration": duration
                    }
                )
                
                return response
                
            except Exception as e:
                duration = time.time() - start_time
                
                logger.error(
                    f"Request failed",
                    extra={
                        "request_id": request_id,
                        "duration": duration,
                        "error": str(e)
                    },
                    exc_info=True
                )
                
                raise
    
    class ErrorHandlingMiddleware(BaseHTTPMiddleware):
        """Handle exceptions and return consistent error responses."""
        
        async def dispatch(self, request: Request, call_next: Callable) -> Response:
            try:
                return await call_next(request)
                
            except ValueError as e:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={
                        "error": "Bad Request",
                        "message": str(e),
                        "request_id": getattr(request.state, "request_id", None)
                    }
                )
                
            except PermissionError as e:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "error": "Forbidden",
                        "message": str(e),
                        "request_id": getattr(request.state, "request_id", None)
                    }
                )
                
            except Exception as e:
                logger.error(
                    f"Unhandled exception",
                    extra={
                        "request_id": getattr(request.state, "request_id", None),
                        "error": str(e)
                    },
                    exc_info=True
                )
                
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred",
                        "request_id": getattr(request.state, "request_id", None)
                    }
                )
    
    class RateLimitMiddleware(BaseHTTPMiddleware):
        """Rate limiting middleware."""
        
        def __init__(self, app: ASGIApp):
            super().__init__(app)
            self.limiter = RateLimiter()
        
        async def dispatch(self, request: Request, call_next: Callable) -> Response:
            # Get client identifier
            client_id = self._get_client_id(request)
            
            # Check rate limit
            allowed, retry_after = await self.limiter.check_rate_limit(
                client_id,
                request.url.path
            )
            
            if not allowed:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "Too Many Requests",
                        "message": "Rate limit exceeded",
                        "retry_after": retry_after
                    },
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(self.limiter.default_limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(time.time()) + retry_after)
                    }
                )
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            limit_info = await self.limiter.get_limit_info(client_id)
            response.headers["X-RateLimit-Limit"] = str(limit_info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(limit_info["remaining"])
            response.headers["X-RateLimit-Reset"] = str(limit_info["reset"])
            
            return response
        
        def _get_client_id(self, request: Request) -> str:
            """Get client identifier for rate limiting."""
            
            # Try to get authenticated user ID
            if hasattr(request.state, "user_id"):
                return f"user:{request.state.user_id}"
            
            # Try to get API key
            api_key = request.headers.get("X-API-Key")
            if api_key:
                return f"api_key:{api_key[:8]}"
            
            # Fall back to IP address
            if request.client:
                return f"ip:{request.client.host}"
            
            return "anonymous"
    
    class MetricsMiddleware(BaseHTTPMiddleware):
        """Collect metrics for monitoring."""
        
        def __init__(self, app: ASGIApp):
            super().__init__(app)
            self.metrics: Dict[str, Any] = {
                "requests_total": 0,
                "requests_by_status": {},
                "requests_by_path": {},
                "response_times": []
            }
        
        async def dispatch(self, request: Request, call_next: Callable) -> Response:
            start_time = time.time()
            
            # Increment total requests
            self.metrics["requests_total"] += 1
            
            # Track by path
            path = request.url.path
            if path not in self.metrics["requests_by_path"]:
                self.metrics["requests_by_path"][path] = 0
            self.metrics["requests_by_path"][path] += 1
            
            try:
                response = await call_next(request)
                
                # Track by status code
                status = response.status_code
                if status not in self.metrics["requests_by_status"]:
                    self.metrics["requests_by_status"][status] = 0
                self.metrics["requests_by_status"][status] += 1
                
                # Track response time
                duration = time.time() - start_time
                self.metrics["response_times"].append({
                    "path": path,
                    "duration": duration,
                    "timestamp": datetime.utcnow()
                })
                
                # Keep only last 1000 response times
                if len(self.metrics["response_times"]) > 1000:
                    self.metrics["response_times"] = self.metrics["response_times"][-1000:]
                
                return response
                
            except Exception as e:
                # Track errors
                if "errors" not in self.metrics:
                    self.metrics["errors"] = 0
                self.metrics["errors"] += 1

I

Continue

Mapped out comprehensive implementation roadmap for complex system.

7s

The user wants me to continue the comprehensive implementor's guide. I've already covered:

1.  Prerequisites and Environment Setup
2.  Project Structure and Initial Configuration
3.  PostgreSQL Database Setup
4.  TypeSpec Schema Definition
5.  Database Schema Implementation
6.  Memory System Implementation (all 4 types)
7.  MCP Protocol Implementation (server, client, and manager)
8.  A2A Protocol Implementation
9.  DBOS Workflow Integration
10.  FastAPI Application Layer (partially - main app, config, database, and middleware)

I need to continue with:

-   Completing the FastAPI routers
-   Agent API implementation
-   Memory API implementation
-   Protocol API implementation
-   Workflow API implementation
-   Health/monitoring endpoints
-   Hasura configuration
-   Testing strategy
-   Deployment and operations
-   Troubleshooting guide
-   Performance optimization

Let me continue with the API routers and the remaining sections.

### Agent API Router

**`src/api/routers/agents.py`**

python

    from typing import List, Optional, Dict, Any
    from datetime import datetime
    from uuid import UUID
    
    from fastapi import APIRouter, Depends, HTTPException, status, Query
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select, update, delete
    
    from src.database import get_db
    from src.api.schemas.agents import (
        AgentCreate, AgentUpdate, AgentResponse,
        SessionCreate, SessionResponse, MessageCreate
    )
    from src.agents.crud import AgentCRUD
    from src.protocols.mcp.manager import MCPManager
    from src.protocols.a2a.agent import A2AAgent
    from src.workflows.agent_conversation import AgentConversationWorkflow
    
    router = APIRouter()
    
    @router.get("/", response_model=List[AgentResponse])
    async def list_agents(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        agent_type: Optional[str] = None,
        is_active: Optional[bool] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """List all agents with optional filtering."""
        
        query = select(AgentCRUD.model)
        
        if agent_type:
            query = query.filter(AgentCRUD.model.type == agent_type)
        
        if is_active is not None:
            query = query.filter(AgentCRUD.model.is_active == is_active)
        
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        agents = result.scalars().all()
        
        return [AgentResponse.from_orm(agent) for agent in agents]
    
    @router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
    async def create_agent(
        agent: AgentCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Create a new agent."""
        
        try:
            # Create agent
            new_agent = await AgentCRUD.create(db, agent)
            
            # Initialize MCP if configured
            if agent.mcp_servers:
                mcp_manager = MCPManager(str(new_agent.id), db)
                await mcp_manager.initialize()
            
            # Initialize A2A if configured
            if agent.a2a_capabilities:
                a2a_agent = A2AAgent(str(new_agent.id), db)
                await a2a_agent.initialize()
            
            return AgentResponse.from_orm(new_agent)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create agent: {str(e)}"
            )
    
    @router.get("/{agent_id}", response_model=AgentResponse)
    async def get_agent(
        agent_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get agent by ID."""
        
        agent = await AgentCRUD.get(db, agent_id)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        return AgentResponse.from_orm(agent)
    
    @router.put("/{agent_id}", response_model=AgentResponse)
    async def update_agent(
        agent_id: UUID,
        agent_update: AgentUpdate,
        db: AsyncSession = Depends(get_db)
    ):
        """Update agent configuration."""
        
        agent = await AgentCRUD.get(db, agent_id)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        # Update agent
        updated_agent = await AgentCRUD.update(db, agent_id, agent_update)
        
        return AgentResponse.from_orm(updated_agent)
    
    @router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_agent(
        agent_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Delete an agent."""
        
        agent = await AgentCRUD.get(db, agent_id)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        # Deactivate instead of hard delete
        await AgentCRUD.deactivate(db, agent_id)
    
    @router.post("/{agent_id}/sessions", response_model=SessionResponse)
    async def create_session(
        agent_id: UUID,
        session: SessionCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Create a new conversation session."""
        
        agent = await AgentCRUD.get(db, agent_id)
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent {agent_id} not found"
            )
        
        if not agent.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent is not active"
            )
        
        # Create session
        sql = """
        INSERT INTO agents.sessions (
            agent_id, user_id, context_window, max_messages, metadata
        ) VALUES (
            :agent_id, :user_id, :context_window, :max_messages, :metadata
        ) RETURNING *
        """
        
        result = await db.execute(
            sql,
            {
                "agent_id": agent_id,
                "user_id": session.user_id,
                "context_window": session.context_window or 4096,
                "max_messages": session.max_messages or 100,
                "metadata": session.metadata or {}
            }
        )
        
        new_session = result.fetchone()
        await db.commit()
        
        return SessionResponse(**new_session)
    
    @router.post("/{agent_id}/sessions/{session_id}/messages")
    async def send_message(
        agent_id: UUID,
        session_id: UUID,
        message: MessageCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Send a message in a conversation session."""
        
        # Verify session exists and is active
        sql = """
        SELECT s.*, a.name as agent_name, a.model
        FROM agents.sessions s
        JOIN agents.agents a ON s.agent_id = a.id
        WHERE s.id = :session_id 
          AND s.agent_id = :agent_id
          AND s.is_active = true
        """
        
        result = await db.execute(
            sql,
            {"session_id": session_id, "agent_id": agent_id}
        )
        
        session = result.fetchone()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found or inactive"
            )
        
        # Run conversation workflow
        workflow = AgentConversationWorkflow(
            "conversation",
            str(agent_id),
            db
        )
        
        try:
            result = await workflow.run(
                str(session_id),
                message.content,
                message.context
            )
            
            return {
                "response": result["response"],
                "session_id": str(session_id),
                "metadata": {
                    "relevant_memories": result["relevant_memories"],
                    "new_memories": result["new_memories"],
                    "tokens_used": result["tokens_used"]
                }
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Conversation failed: {str(e)}"
            )
    
    @router.get("/{agent_id}/sessions/{session_id}/messages")
    async def get_messages(
        agent_id: UUID,
        session_id: UUID,
        limit: int = Query(20, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
    ):
        """Get conversation history."""
        
        sql = """
        SELECT role, content, created_at, token_count
        FROM agents.messages
        WHERE session_id = :session_id
        ORDER BY created_at DESC
        LIMIT :limit
        """
        
        result = await db.execute(
            sql,
            {"session_id": session_id, "limit": limit}
        )
        
        messages = [
            {
                "role": row["role"],
                "content": row["content"],
                "created_at": row["created_at"].isoformat(),
                "tokens": row["token_count"]
            }
            for row in reversed(result.fetchall())
        ]
        
        return {
            "session_id": str(session_id),
            "messages": messages,
            "count": len(messages)
        }
    
    @router.post("/{agent_id}/tools/{tool_name}/execute")
    async def execute_tool(
        agent_id: UUID,
        tool_name: str,
        tool_input: Dict[str, Any],
        db: AsyncSession = Depends(get_db)
    ):
        """Execute an MCP tool."""
        
        mcp_manager = MCPManager(str(agent_id), db)
        await mcp_manager.initialize()
        
        try:
            result = await mcp_manager.execute_tool(tool_name, tool_input)
            
            return {
                "tool": tool_name,
                "result": result,
                "success": True
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tool execution failed: {str(e)}"
            )
    
    @router.get("/{agent_id}/stats")
    async def get_agent_stats(
        agent_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get agent statistics."""
        
        sql = """
        WITH session_stats AS (
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(*) FILTER (WHERE is_active) as active_sessions,
                SUM(message_count) as total_messages,
                SUM(total_tokens_used) as total_tokens
            FROM agents.sessions
            WHERE agent_id = :agent_id
        ),
        memory_stats AS (
            SELECT 
                type,
                COUNT(*) as count,
                AVG(importance) as avg_importance
            FROM memory.memories
            WHERE agent_id = :agent_id
            GROUP BY type
        ),
        recent_activity AS (
            SELECT 
                COUNT(*) as messages_24h
            FROM agents.messages m
            JOIN agents.sessions s ON m.session_id = s.id
            WHERE s.agent_id = :agent_id
              AND m.created_at > NOW() - INTERVAL '24 hours'
        )
        SELECT 
            s.*,
            r.messages_24h,
            json_agg(json_build_object(
                'type', m.type,
                'count', m.count,
                'avg_importance', m.avg_importance
            )) as memory_breakdown
        FROM session_stats s
        CROSS JOIN recent_activity r
        LEFT JOIN memory_stats m ON true
        GROUP BY s.total_sessions, s.active_sessions, 
                 s.total_messages, s.total_tokens, r.messages_24h
        """
        
        result = await db.execute(sql, {"agent_id": agent_id})
        stats = result.fetchone()
        
        return {
            "agent_id": str(agent_id),
            "sessions": {
                "total": stats["total_sessions"],
                "active": stats["active_sessions"]
            },
            "messages": {
                "total": stats["total_messages"],
                "last_24h": stats["messages_24h"]
            },
            "tokens_used": stats["total_tokens"],
            "memory": stats["memory_breakdown"]
        }

### Memory API Router

**`src/api/routers/memory.py`**

python

    from typing import List, Optional, Dict, Any
    from datetime import datetime, timedelta
    from uuid import UUID
    
    from fastapi import APIRouter, Depends, HTTPException, status, Query
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.api.schemas.memory import (
        MemoryCreate, MemorySearch, MemoryResponse,
        ConsolidationRequest, ConsolidationResponse
    )
    from src.memory import MemoryType, search_memories
    from src.memory.episodic import EpisodicMemoryManager
    from src.memory.semantic import SemanticMemoryManager
    from src.memory.implicit import ImplicitMemoryManager
    from src.memory.prospective import ProspectiveMemoryManager
    from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
    
    router = APIRouter()
    
    @router.post("/store", response_model=MemoryResponse)
    async def store_memory(
        memory: MemoryCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Store a new memory."""
        
        try:
            if memory.type == MemoryType.EPISODIC:
                manager = EpisodicMemoryManager(db)
                stored = await manager.store_episode(
                    memory.agent_id,
                    memory.content,
                    memory.metadata or {},
                    emotional_valence=memory.type_data.get("emotional_valence")
                )
            
            elif memory.type == MemoryType.SEMANTIC:
                manager = SemanticMemoryManager(db)
                stored = await manager.store_fact(
                    memory.agent_id,
                    memory.content,
                    concepts=memory.type_data.get("concepts"),
                    confidence=memory.type_data.get("confidence", 1.0)
                )
            
            elif memory.type == MemoryType.IMPLICIT:
                manager = ImplicitMemoryManager(db)
                stored = await manager.record_behavior(
                    memory.agent_id,
                    memory.content,
                    memory.metadata or {},
                    outcome=memory.type_data.get("outcome")
                )
            
            elif memory.type == MemoryType.PROSPECTIVE:
                manager = ProspectiveMemoryManager(db)
                stored = await manager.create_goal(
                    memory.agent_id,
                    memory.content,
                    deadline=memory.type_data.get("deadline"),
                    priority=memory.type_data.get("priority", 5)
                )
            
            else:
                raise ValueError(f"Unknown memory type: {memory.type}")
            
            return MemoryResponse.from_orm(stored)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to store memory: {str(e)}"
            )
    
    @router.post("/search", response_model=List[MemoryResponse])
    async def search_agent_memories(
        search: MemorySearch,
        db: AsyncSession = Depends(get_db)
    ):
        """Search memories using vector similarity."""
        
        try:
            memories = await search_memories(
                db,
                search.agent_id,
                search.query,
                memory_types=search.types,
                limit=search.limit,
                threshold=search.threshold,
                include_decayed=search.include_decayed
            )
            
            return [MemoryResponse.from_orm(m) for m in memories]
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Search failed: {str(e)}"
            )
    
    @router.get("/{memory_id}", response_model=MemoryResponse)
    async def get_memory(
        memory_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get a specific memory by ID."""
        
        sql = """
        SELECT m.*, 
               array_agg(r.target_memory) as related_memories
        FROM memory.memories m
        LEFT JOIN memory.relationships r ON m.id = r.source_memory
        WHERE m.id = :memory_id
        GROUP BY m.id
        """
        
        result = await db.execute(sql, {"memory_id": memory_id})
        memory = result.fetchone()
        
        if not memory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Memory {memory_id} not found"
            )
        
        # Update access count
        await db.execute(
            """
            UPDATE memory.memories 
            SET access_count = access_count + 1,
                last_accessed_at = NOW()
            WHERE id = :memory_id
            """,
            {"memory_id": memory_id}
        )
        await db.commit()
        
        return MemoryResponse(**memory)
    
    @router.post("/consolidate", response_model=ConsolidationResponse)
    async def consolidate_memories(
        request: ConsolidationRequest,
        db: AsyncSession = Depends(get_db)
    ):
        """Run memory consolidation for an agent."""
        
        workflow = MemoryConsolidationWorkflow(
            "manual_consolidation",
            request.agent_id,
            db
        )
        
        try:
            result = await workflow.run(
                memory_types=request.memory_types,
                min_importance=request.min_importance,
                time_window=timedelta(days=request.days)
            )
            
            return ConsolidationResponse(**result)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Consolidation failed: {str(e)}"
            )
    
    @router.get("/agent/{agent_id}/episodic")
    async def get_episodic_memories(
        agent_id: UUID,
        time_range: Optional[int] = Query(None, description="Days to look back"),
        emotional_filter: Optional[str] = Query(None, enum=["positive", "negative", "neutral"]),
        limit: int = Query(20, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
    ):
        """Get episodic memories with filtering."""
        
        manager = EpisodicMemoryManager(db)
        
        memories = await manager.retrieve_episodes(
            str(agent_id),
            "",  # Empty query for browsing
            limit=limit,
            time_range=timedelta(days=time_range) if time_range else None,
            emotional_filter=emotional_filter
        )
        
        return [
            {
                "id": m.id,
                "content": m.content,
                "emotional_valence": m.emotional_valence,
                "importance": m.importance,
                "created_at": m.created_at.isoformat(),
                "temporal_context": m.temporal_context
            }
            for m in memories
        ]
    
    @router.get("/agent/{agent_id}/semantic/graph")
    async def get_knowledge_graph(
        agent_id: UUID,
        max_depth: int = Query(3, ge=1, le=5),
        db: AsyncSession = Depends(get_db)
    ):
        """Get agent's knowledge graph."""
        
        manager = SemanticMemoryManager(db)
        
        graph = await manager.build_knowledge_graph(
            str(agent_id),
            max_depth=max_depth
        )
        
        # Convert NetworkX graph to JSON-serializable format
        nodes = [
            {
                "id": node,
                "type": graph.nodes[node].get("type", "concept"),
                "memories": graph.nodes[node].get("memories", [])
            }
            for node in graph.nodes()
        ]
        
        edges = [
            {
                "source": edge[0],
                "target": edge[1],
                "relation": graph.edges[edge].get("relation", "related_to"),
                "weight": graph.edges[edge].get("weight", 1.0)
            }
            for edge in graph.edges()
        ]
        
        return {
            "agent_id": str(agent_id),
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "max_depth": max_depth
            }
        }
    
    @router.get("/agent/{agent_id}/prospective/goals")
    async def get_agent_goals(
        agent_id: UUID,
        status: Optional[str] = Query(None, enum=["active", "completed", "failed", "deferred"]),
        include_subgoals: bool = Query(True),
        db: AsyncSession = Depends(get_db)
    ):
        """Get agent's goals."""
        
        manager = ProspectiveMemoryManager(db)
        
        goals = await manager.get_active_goals(
            str(agent_id),
            include_subgoals=include_subgoals
        )
        
        # Filter by status if provided
        if status:
            goals = [g for g in goals if g.status == status]
        
        return [
            {
                "id": g.id,
                "content": g.content,
                "status": g.status,
                "priority": g.priority,
                "progress": g.progress,
                "deadline": g.deadline.isoformat() if g.deadline else None,
                "dependencies": g.dependencies
            }
            for g in goals
        ]
    
    @router.post("/agent/{agent_id}/prospective/goals/{goal_id}/progress")
    async def update_goal_progress(
        agent_id: UUID,
        goal_id: UUID,
        progress: float = Query(..., ge=0, le=1),
        checkpoint: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """Update goal progress."""
        
        manager = ProspectiveMemoryManager(db)
        
        try:
            await manager.update_goal_progress(
                str(goal_id),
                progress,
                checkpoint
            )
            
            return {"status": "updated", "progress": progress}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update goal: {str(e)}"
            )
    
    @router.get("/agent/{agent_id}/implicit/habits")
    async def get_agent_habits(
        agent_id: UUID,
        days: int = Query(30, ge=7, le=365),
        min_frequency: int = Query(10, ge=1),
        db: AsyncSession = Depends(get_db)
    ):
        """Extract agent's habitual patterns."""
        
        manager = ImplicitMemoryManager(db)
        
        habits = await manager.extract_habits(
            str(agent_id),
            time_window=timedelta(days=days),
            min_frequency=min_frequency
        )
        
        return {
            "agent_id": str(agent_id),
            "time_window_days": days,
            "habits": habits,
            "count": len(habits)
        }
    
    @router.post("/relationships")
    async def create_memory_relationship(
        source_id: UUID,
        target_id: UUID,
        relationship_type: str,
        strength: float = Query(1.0, ge=0, le=1),
        metadata: Optional[Dict[str, Any]] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """Create relationship between memories."""
        
        sql = """
        INSERT INTO memory.relationships (
            source_memory, target_memory, relationship_type, strength, metadata
        ) VALUES (
            :source, :target, :type, :strength, :metadata
        )
        ON CONFLICT (source_memory, target_memory, relationship_type)
        DO UPDATE SET 
            strength = GREATEST(relationships.strength, :strength),
            metadata = relationships.metadata || :metadata
        RETURNING *
        """
        
        try:
            result = await db.execute(
                sql,
                {
                    "source": source_id,
                    "target": target_id,
                    "type": relationship_type,
                    "strength": strength,
                    "metadata": metadata or {}
                }
            )
            
            relationship = result.fetchone()
            await db.commit()
            
            return {
                "id": relationship["id"],
                "source": str(relationship["source_memory"]),
                "target": str(relationship["target_memory"]),
                "type": relationship["relationship_type"],
                "strength": relationship["strength"]
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create relationship: {str(e)}"
            )

### Protocol API Router

**`src/api/routers/protocols.py`**

python

    from typing import List, Optional, Dict, Any
    from uuid import UUID
    
    from fastapi import APIRouter, Depends, HTTPException, status, Query
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.api.schemas.protocols import (
        MCPServerCreate, MCPToolResponse, MCPResourceResponse,
        A2ATaskCreate, A2ATaskResponse, A2AAgentCardResponse
    )
    from src.protocols.mcp.manager import MCPManager
    from src.protocols.a2a.agent import A2AAgent
    
    router = APIRouter()
    
    # MCP Endpoints
    
    @router.post("/mcp/servers")
    async def create_mcp_server(
        server: MCPServerCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Create and start an MCP server."""
        
        manager = MCPManager(server.agent_id, db)
        
        try:
            mcp_server = await manager.start_server(
                server.name,
                server.transport
            )
            
            return {
                "server_id": mcp_server.server_id,
                "name": mcp_server.name,
                "transport": mcp_server.transport,
                "status": "running"
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to start MCP server: {str(e)}"
            )
    
    @router.get("/mcp/tools", response_model=List[MCPToolResponse])
    async def list_mcp_tools(
        agent_id: UUID,
        server_name: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """List available MCP tools."""
        
        manager = MCPManager(str(agent_id), db)
        await manager.initialize()
        
        tools = await manager.list_all_tools()
        
        if server_name:
            tools = [t for t in tools if t.get("server") == server_name]
        
        return tools
    
    @router.post("/mcp/tools/{tool_name}/execute")
    async def execute_mcp_tool(
        agent_id: UUID,
        tool_name: str,
        tool_input: Dict[str, Any],
        db: AsyncSession = Depends(get_db)
    ):
        """Execute an MCP tool."""
        
        manager = MCPManager(str(agent_id), db)
        await manager.initialize()
        
        try:
            result = await manager.execute_tool(tool_name, tool_input)
            
            return {
                "tool": tool_name,
                "output": result,
                "success": True
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tool execution failed: {str(e)}"
            )
    
    @router.get("/mcp/resources", response_model=List[MCPResourceResponse])
    async def list_mcp_resources(
        agent_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """List available MCP resources."""
        
        manager = MCPManager(str(agent_id), db)
        await manager.initialize()
        
        # Get resources from all servers
        sql = """
        SELECT r.*, s.name as server_name
        FROM protocols.mcp_resources r
        JOIN protocols.mcp_servers s ON r.server_id = s.id
        WHERE s.agent_id = :agent_id
          AND s.is_active = true
        """
        
        result = await db.execute(sql, {"agent_id": agent_id})
        resources = result.fetchall()
        
        return [
            MCPResourceResponse(
                uri=r["uri"],
                name=r["name"],
                description=r["description"],
                mime_type=r["mime_type"],
                server_name=r["server_name"]
            )
            for r in resources
        ]
    
    @router.get("/mcp/resources/{uri}")
    async def get_mcp_resource(
        agent_id: UUID,
        uri: str,
        db: AsyncSession = Depends(get_db)
    ):
        """Get MCP resource content."""
        
        manager = MCPManager(str(agent_id), db)
        await manager.initialize()
        
        try:
            resource = await manager.get_resource(uri)
            
            return {
                "uri": uri,
                "content": resource["content"],
                "mime_type": resource["mimeType"]
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resource not found: {str(e)}"
            )
    
    # A2A Endpoints
    
    @router.post("/a2a/tasks", response_model=A2ATaskResponse)
    async def create_a2a_task(
        task: A2ATaskCreate,
        db: AsyncSession = Depends(get_db)
    ):
        """Create a new A2A task."""
        
        a2a_agent = A2AAgent(task.client_agent, db)
        await a2a_agent.initialize()
        
        try:
            created_task = await a2a_agent.create_task(
                task.remote_agent,
                task.name,
                task.input,
                task.description
            )
            
            return A2ATaskResponse.from_orm(created_task)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create task: {str(e)}"
            )
    
    @router.get("/a2a/tasks/{task_id}", response_model=A2ATaskResponse)
    async def get_a2a_task(
        task_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get A2A task status."""
        
        sql = """
        SELECT t.*,
               json_agg(DISTINCT a.*) as artifacts,
               json_agg(DISTINCT m.* ORDER BY m.created_at) as messages
        FROM protocols.a2a_tasks t
        LEFT JOIN protocols.a2a_artifacts a ON t.id = a.task_id
        LEFT JOIN protocols.a2a_messages m ON t.id = m.task_id
        WHERE t.id = :task_id
        GROUP BY t.id
        """
        
        result = await db.execute(sql, {"task_id": task_id})
        task = result.fetchone()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        return A2ATaskResponse(**task)
    
    @router.put("/a2a/tasks/{task_id}/progress")
    async def update_task_progress(
        task_id: UUID,
        agent_id: UUID,
        progress: float = Query(..., ge=0, le=1),
        message: Optional[str] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """Update task progress (for remote agent)."""
        
        # Verify agent is the remote agent for this task
        sql = """
        SELECT remote_agent FROM protocols.a2a_tasks WHERE id = :task_id
        """
        
        result = await db.execute(sql, {"task_id": task_id})
        task = result.fetchone()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found"
            )
        
        if task["remote_agent"] != agent_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the remote agent can update progress"
            )
        
        a2a_agent = A2AAgent(str(agent_id), db)
        await a2a_agent.update_task_progress(str(task_id), progress, message)
        
        return {"status": "updated", "progress": progress}
    
    @router.post("/a2a/tasks/{task_id}/complete")
    async def complete_a2a_task(
        task_id: UUID,
        agent_id: UUID,
        output: Dict[str, Any],
        artifacts: Optional[List[Dict[str, Any]]] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """Complete an A2A task."""
        
        a2a_agent = A2AAgent(str(agent_id), db)
        
        try:
            await a2a_agent.complete_task(str(task_id), output, artifacts)
            
            return {"status": "completed"}
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to complete task: {str(e)}"
            )
    
    @router.post("/a2a/tasks/{task_id}/messages")
    async def send_task_message(
        task_id: UUID,
        agent_id: UUID,
        content: str,
        parts: Optional[List[Dict[str, Any]]] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """Send a message about a task."""
        
        a2a_agent = A2AAgent(str(agent_id), db)
        
        await a2a_agent.send_task_message(str(task_id), content, parts)
        
        return {"status": "sent"}
    
    @router.get("/a2a/agents", response_model=List[A2AAgentCardResponse])
    async def discover_a2a_agents(
        capabilities: Optional[List[str]] = Query(None),
        db: AsyncSession = Depends(get_db)
    ):
        """Discover available A2A agents."""
        
        # Use any agent for discovery
        a2a_agent = A2AAgent("system", db)
        
        agents = await a2a_agent.discover_agents(capabilities)
        
        return [A2AAgentCardResponse.from_orm(a) for a in agents]
    
    @router.get("/a2a/agents/{agent_id}/card")
    async def get_agent_card(
        agent_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get an agent's A2A card."""
        
        sql = """
        SELECT a.*, ag.name
        FROM protocols.a2a_agents a
        JOIN agents.agents ag ON a.agent_id = ag.id
        WHERE a.agent_id = :agent_id
        """
        
        result = await db.execute(sql, {"agent_id": agent_id})
        card = result.fetchone()
        
        if not card:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent card not found for {agent_id}"
            )
        
        return {
            "agent_id": str(card["agent_id"]),
            "name": card["name"],
            "capabilities": card["capabilities"],
            "protocols": card["protocols"],
            "endpoints": card["endpoints"],
            "is_public": card["is_public"]
        }
    
    @router.post("/a2a/agents/{agent_id}/capabilities")
    async def add_agent_capability(
        agent_id: UUID,
        capability: str,
        db: AsyncSession = Depends(get_db)
    ):
        """Add a capability to an agent."""
        
        sql = """
        UPDATE protocols.a2a_agents
        SET capabilities = array_append(capabilities, :capability),
            last_seen = NOW()
        WHERE agent_id = :agent_id
          AND NOT (:capability = ANY(capabilities))
        """
        
        result = await db.execute(
            sql,
            {"agent_id": agent_id, "capability": capability}
        )
        
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Capability already exists or agent not found"
            )
        
        await db.commit()
        
        return {"status": "added", "capability": capability}

### Workflow API Router

**`src/api/routers/workflows.py`**

python

    from typing import List, Optional, Dict, Any
    from datetime import datetime, timedelta
    from uuid import UUID
    
    from fastapi import APIRouter, Depends, HTTPException, status, Query
    from sqlalchemy.ext.asyncio import AsyncSession
    
    from src.database import get_db
    from src.api.schemas.workflows import (
        WorkflowDefinitionCreate, WorkflowInstanceResponse,
        WorkflowExecutionRequest
    )
    from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
    from src.workflows.agent_conversation import AgentConversationWorkflow
    
    router = APIRouter()
    
    @router.get("/definitions")
    async def list_workflow_definitions(
        is_active: Optional[bool] = None,
        db: AsyncSession = Depends(get_db)
    ):
        """List available workflow definitions."""
        
        sql = """
        SELECT id, name, description, version, tags, is_active, created_at
        FROM workflows.workflow_definitions
        """
        
        params = {}
        
        if is_active is not None:
            sql += " WHERE is_active = :is_active"
            params["is_active"] = is_active
        
        sql += " ORDER BY name"
        
        result = await db.execute(sql, params)
        definitions = result.fetchall()
        
        return [
            {
                "id": str(d["id"]),
                "name": d["name"],
                "description": d["description"],
                "version": d["version"],
                "tags": d["tags"],
                "is_active": d["is_active"],
                "created_at": d["created_at"].isoformat()
            }
            for d in definitions
        ]
    
    @router.post("/execute/{workflow_name}")
    async def execute_workflow(
        workflow_name: str,
        execution: WorkflowExecutionRequest,
        db: AsyncSession = Depends(get_db)
    ):
        """Execute a workflow."""
        
        try:
            if workflow_name == "memory_consolidation":
                workflow = MemoryConsolidationWorkflow(
                    workflow_name,
                    execution.agent_id,
                    db
                )
                
                result = await workflow.run(
                    memory_types=execution.parameters.get("memory_types"),
                    min_importance=execution.parameters.get("min_importance", 0.3),
                    time_window=timedelta(
                        days=execution.parameters.get("days", 7)
                    )
                )
            
            elif workflow_name == "agent_conversation":
                workflow = AgentConversationWorkflow(
                    workflow_name,
                    execution.agent_id,
                    db
                )
                
                result = await workflow.run(
                    session_id=execution.parameters["session_id"],
                    user_message=execution.parameters["message"],
                    context=execution.parameters.get("context", {})
                )
            
            else:
                raise ValueError(f"Unknown workflow: {workflow_name}")
            
            return {
                "workflow_id": workflow.context.workflow_id,
                "status": "completed",
                "result": result
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Workflow execution failed: {str(e)}"
            )
    
    @router.get("/instances/{instance_id}", response_model=WorkflowInstanceResponse)
    async def get_workflow_instance(
        instance_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Get workflow instance details."""
        
        sql = """
        SELECT wi.*, wd.name as workflow_name
        FROM workflows.workflow_instances wi
        JOIN workflows.workflow_definitions wd ON wi.definition_id = wd.id
        WHERE wi.id = :instance_id
        """
        
        result = await db.execute(sql, {"instance_id": instance_id})
        instance = result.fetchone()
        
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workflow instance {instance_id} not found"
            )
        
        # Get step executions
        steps_sql = """
        SELECT step_name, status, started_at, completed_at, 
               duration_ms, error
        FROM workflows.step_executions
        WHERE instance_id = :instance_id
        ORDER BY started_at
        """
        
        steps_result = await db.execute(steps_sql, {"instance_id": instance_id})
        steps = steps_result.fetchall()
        
        return WorkflowInstanceResponse(
            id=str(instance["id"]),
            workflow_name=instance["workflow_name"],
            agent_id=str(instance["agent_id"]),
            status=instance["status"],
            context=instance["context"],
            output=instance["output"],
            error=instance["error"],
            created_at=instance["created_at"],
            started_at=instance["started_at"],
            completed_at=instance["completed_at"],
            steps=[
                {
                    "name": s["step_name"],
                    "status": s["status"],
                    "started_at": s["started_at"],
                    "completed_at": s["completed_at"],
                    "duration_ms": s["duration_ms"],
                    "error": s["error"]
                }
                for s in steps
            ]
        )
    
    @router.get("/agent/{agent_id}/history")
    async def get_workflow_history(
        agent_id: UUID,
        workflow_name: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = Query(20, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
    ):
        """Get workflow execution history for an agent."""
        
        sql = """
        SELECT wi.*, wd.name as workflow_name
        FROM workflows.workflow_instances wi
        JOIN workflows.workflow_definitions wd ON wi.definition_id = wd.id
        WHERE wi.agent_id = :agent_id
        """
        
        params = {"agent_id": agent_id}
        
        if workflow_name:
            sql += " AND wd.name = :workflow_name"
            params["workflow_name"] = workflow_name
        
        if status:
            sql += " AND wi.status = :status"
            params["status"] = status
        
        sql += " ORDER BY wi.created_at DESC LIMIT :limit"
        params["limit"] = limit
        
        result = await db.execute(sql, params)
        instances = result.fetchall()
        
        return [
            {
                "id": str(i["id"]),
                "workflow_name": i["workflow_name"],
                "status": i["status"],
                "created_at": i["created_at"].isoformat(),
                "completed_at": i["completed_at"].isoformat() if i["completed_at"] else None,
                "duration_seconds": (
                    (i["completed_at"] - i["created_at"]).total_seconds()
                    if i["completed_at"] else None
                )
            }
            for i in instances
        ]
    
    @router.post("/instances/{instance_id}/cancel")
    async def cancel_workflow(
        instance_id: UUID,
        db: AsyncSession = Depends(get_db)
    ):
        """Cancel a running workflow."""
        
        sql = """
        UPDATE workflows.workflow_instances
        SET status = 'cancelled',
            completed_at = NOW(),
            error = jsonb_build_object('message', 'Cancelled by user')
        WHERE id = :instance_id
          AND status IN ('pending', 'running')
        RETURNING id
        """
        
        result = await db.execute(sql, {"instance_id": instance_id})
        updated = result.fetchone()
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workflow not found or not in cancellable state"
            )
        
        await db.commit()
        
        return {"status": "cancelled", "instance_id": str(instance_id)}
    
    @router.get("/stats")
    async def get_workflow_stats(
        days: int = Query(7, ge=1, le=365),
        db: AsyncSession = Depends(get_db)
    ):
        """Get workflow execution statistics."""
        
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        sql = """
        WITH workflow_stats AS (
            SELECT 
                wd.name as workflow_name,
                COUNT(*) as total_executions,
                COUNT(*) FILTER (WHERE wi.status = 'completed') as successful,
                COUNT(*) FILTER (WHERE wi.status = 'failed') as failed,
                COUNT(*) FILTER (WHERE wi.status = 'cancelled') as cancelled,
                AVG(EXTRACT(EPOCH FROM (wi.completed_at - wi.created_at)))
                    FILTER (WHERE wi.status = 'completed') as avg_duration_seconds,
                MIN(wi.created_at) as first_execution,
                MAX(wi.created_at) as last_execution
            FROM workflows.workflow_instances wi
            JOIN workflows.workflow_definitions wd ON wi.definition_id = wd.id
            WHERE wi.created_at > :cutoff
            GROUP BY wd.name
        )
        SELECT 
            workflow_name,
            total_executions,
            successful,
            failed,
            cancelled,
            avg_duration_seconds,
            first_execution,
            last_execution,
            CASE 
                WHEN total_executions > 0 
                THEN (successful::float / total_executions * 100)
                ELSE 0 
            END as success_rate
        FROM workflow_stats
        ORDER BY total_executions DESC
        """
        
        result = await db.execute(sql, {"cutoff": cutoff})
        stats = result.fetchall()
        
        return {
            "period_days": days,
            "workflows": [
                {
                    "name": s["workflow_name"],
                    "executions": {
                        "total": s["total_executions"],
                        "successful": s["successful"],
                        "failed": s["failed"],
                        "cancelled": s["cancelled"]
                    },
                    "success_rate": round(s["success_rate"], 2),
                    "avg_duration_seconds": round(s["avg_duration_seconds"], 2) if s["avg_duration_seconds"] else None,
                    "first_execution": s["first_execution"].isoformat(),
                    "last_execution": s["last_execution"].isoformat()
                }
                for s in stats
            ]
        }

### Health and Monitoring Router

**`src/api/routers/health.py`**

python

    from typing import Dict, Any
    from datetime import datetime
    
    from fastapi import APIRouter, Depends, status
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import text
    
    from src.database import get_db, check_db_health
    from src.config import settings
    
    router = APIRouter()
    
    @router.get("/", status_code=status.HTTP_200_OK)
    async def health_check():
        """Basic health check endpoint."""
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.api_version
        }
    
    @router.get("/live", status_code=status.HTTP_200_OK)
    async def liveness_probe():
        """Kubernetes liveness probe."""
        return {"status": "alive"}
    
    @router.get("/ready")
    async def readiness_probe(db: AsyncSession = Depends(get_db)):
        """Kubernetes readiness probe."""
        
        checks = {
            "database": False,
            "extensions": False,
            "queues": False
        }
        
        try:
            # Check database connectivity
            result = await db.execute(text("SELECT 1"))
            checks["database"] = result.scalar() == 1
            
            # Check required extensions
            ext_result = await db.execute(
                text("""
                SELECT COUNT(*) = 3 as all_present
                FROM pg_extension 
                WHERE extname IN ('vector', 'pgmq', 'pg_jsonschema')
                """)
            )
            checks["extensions"] = ext_result.scalar()
            
            # Check message queues
            queue_result = await db.execute(
                text("""
                SELECT COUNT(*) >= 4 as queues_exist
                FROM pgmq.meta
                WHERE queue_name IN ('mcp_messages', 'a2a_tasks', 
                                    'memory_consolidation', 'workflow_events')
                """)
            )
            checks["queues"] = queue_result.scalar()
            
        except Exception as e:
            return {
                "status": "not ready",
                "checks": checks,
                "error": str(e)
            }, status.HTTP_503_SERVICE_UNAVAILABLE
        
        if all(checks.values()):
            return {
                "status": "ready",
                "checks": checks
            }
        else:
            return {
                "status": "not ready",
                "checks": checks
            }, status.HTTP_503_SERVICE_UNAVAILABLE
    
    @router.get("/metrics")
    async def get_metrics(db: AsyncSession = Depends(get_db)):
        """Get application metrics."""
        
        metrics = {}
        
        try:
            # Database metrics
            db_metrics = await db.execute(
                text("""
                SELECT 
                    (SELECT COUNT(*) FROM agents.agents WHERE is_active) as active_agents,
                    (SELECT COUNT(*) FROM agents.sessions WHERE is_active) as active_sessions,
                    (SELECT COUNT(*) FROM memory.memories) as total_memories,
                    (SELECT COUNT(*) FROM protocols.a2a_tasks WHERE status = 'running') as running_tasks,
                    (SELECT pg_database_size(current_database())) as database_size_bytes
                """)
            )
            
            db_data = db_metrics.fetchone()
            metrics["database"] = {
                "active_agents": db_data[0],
                "active_sessions": db_data[1],
                "total_memories": db_data[2],
                "running_tasks": db_data[3],
                "size_mb": round(db_data[4] / (1024 * 1024), 2)
            }
            
            # Queue metrics
            queue_metrics = await db.execute(
                text("""
                SELECT queue_name, queue_length, total_messages
                FROM pgmq.metrics
                WHERE queue_name IN ('mcp_messages', 'a2a_tasks', 
                                    'memory_consolidation', 'workflow_events')
                """)
            )
            
            metrics["queues"] = {
                row[0]: {
                    "length": row[1],
                    "total_processed": row[2]
                }
                for row in queue_metrics.fetchall()
            }
            
            # Memory type distribution
            memory_dist = await db.execute(
                text("""
                SELECT type, COUNT(*) as count, 
                       AVG(importance) as avg_importance
                FROM memory.memories
                GROUP BY type
                """)
            )
            
            metrics["memory_distribution"] = {
                row[0]: {
                    "count": row[1],
                    "avg_importance": round(row[2], 3)
                }
                for row in memory_dist.fetchall()
            }
            
            # Recent activity
            activity = await db.execute(
                text("""
                SELECT 
                    (SELECT COUNT(*) FROM agents.messages 
                     WHERE created_at > NOW() - INTERVAL '1 hour') as messages_last_hour,
                    (SELECT COUNT(*) FROM memory.memories 
                     WHERE created_at > NOW() - INTERVAL '1 hour') as memories_last_hour,
                    (SELECT COUNT(*) FROM workflows.workflow_instances 
                     WHERE created_at > NOW() - INTERVAL '1 hour') as workflows_last_hour
                """)
            )
            
            activity_data = activity.fetchone()
            metrics["recent_activity"] = {
                "messages_last_hour": activity_data[0],
                "memories_last_hour": activity_data[1],
                "workflows_last_hour": activity_data[2]
            }
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": metrics
            }
            
        except Exception as e:
            return {
                "error": "Failed to collect metrics",
                "details": str(e)
            }, status.HTTP_500_INTERNAL_SERVER_ERROR
    
    @router.get("/dependencies")
    async def check_dependencies():
        """Check external dependencies."""
        
        dependencies = {
            "openai": {
                "configured": bool(settings.openai_api_key),
                "status": "unknown"
            },
            "anthropic": {
                "configured": bool(settings.anthropic_api_key),
                "status": "unknown"
            },
            "hasura": {
                "configured": bool(settings.hasura_graphql_endpoint),
                "status": "unknown"
            }
        }
        
        # Test OpenAI
        if dependencies["openai"]["configured"]:
            try:
                import openai
                client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
                models = await client.models.list()
                dependencies["openai"]["status"] = "connected"
                dependencies["openai"]["models"] = len(models.data)
            except:
                dependencies["openai"]["status"] = "error"
        
        # Test Hasura
        if dependencies["hasura"]["configured"]:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        f"{settings.hasura_graphql_endpoint}/health",
                        headers={"X-Hasura-Admin-Secret": settings.hasura_admin_secret}
                    )
                    if response.status_code == 200:
                        dependencies["hasura"]["status"] = "connected"
                    else:
                        dependencies["hasura"]["status"] = "error"
            except:
                dependencies["hasura"]["status"] = "error"
        
        return dependencies

* * *

## 11\. Hasura Configuration {#hasura-setup}

### Hasura Metadata Configuration

**`hasura/metadata/databases.yaml`**

yaml

    - name: default
      kind: postgres
      configuration:
        connection_info:
          database_url:
            from_env: HASURA_GRAPHQL_DATABASE_URL
          isolation_level: read-committed
          pool_settings:
            connection_lifetime: 600
            idle_timeout: 180
            max_connections: 50
            retries: 1
      tables:
        - table:
            schema: agents
            name: agents
          configuration:
            custom_name: agents
            custom_root_fields:
              select: agents
              select_by_pk: agent
              insert: createAgent
              update: updateAgent
              delete: deleteAgent
          object_relationships:
            - name: sessions
              using:
                foreign_key_constraint_on:
                  column: agent_id
                  table:
                    schema: agents
                    name: sessions
            - name: memories
              using:
                foreign_key_constraint_on:
                  column: agent_id
                  table:
                    schema: memory
                    name: memories
          select_permissions:
            - role: user
              permission:
                columns:
                  - id
                  - name
                  - type
                  - model
                  - is_active
                  - created_at
                  - updated_at
                filter: {}
                allow_aggregations: true
        
        - table:
            schema: agents
            name: sessions
          configuration:
            custom_name: sessions
          object_relationships:
            - name: agent
              using:
                foreign_key_constraint_on: agent_id
          array_relationships:
            - name: messages
              using:
                foreign_key_constraint_on:
                  column: session_id
                  table:
                    schema: agents
                    name: messages
        
        - table:
            schema: memory
            name: memories
          configuration:
            custom_name: memories
          object_relationships:
            - name: agent
              using:
                foreign_key_constraint_on: agent_id
          array_relationships:
            - name: relationships_from
              using:
                foreign_key_constraint_on:
                  column: source_memory
                  table:
                    schema: memory
                    name: relationships
            - name: relationships_to
              using:
                foreign_key_constraint_on:
                  column: target_memory
                  table:
                    schema: memory
                    name: relationships
        
        - table:
            schema: protocols
            name: a2a_tasks
          configuration:
            custom_name: a2a_tasks
          object_relationships:
            - name: client_agent
              using:
                foreign_key_constraint_on: client_agent
            - name: remote_agent
              using:
                foreign_key_constraint_on: remote_agent
          array_relationships:
            - name: artifacts
              using:
                foreign_key_constraint_on:
                  column: task_id
                  table:
                    schema: protocols
                    name: a2a_artifacts
            - name: messages
              using:
                foreign_key_constraint_on:
                  column: task_id
                  table:
                    schema: protocols
                    name: a2a_messages
      
      functions:
        - function:
            schema: memory
            name: search_memories
          configuration:
            exposed_as: query
            custom_name: searchMemories
        
        - function:
            schema: memory
            name: consolidate_memories
          configuration:
            exposed_as: mutation
            custom_name: consolidateMemories
        
        - function:
            schema: protocols
            name: execute_mcp_tool
          configuration:
            exposed_as: mutation
            custom_name: executeMCPTool
        
        - function:
            schema: protocols
            name: discover_a2a_agents
          configuration:
            exposed_as: query
            custom_name: discoverA2AAgents

### Hasura Actions Configuration

**`hasura/metadata/actions.yaml`**

yaml

    actions:
      - name: createConversation
        definition:
          kind: synchronous
          handler: http://app:8000/api/v1/agents/{{$body.input.agentId}}/sessions
          headers:
            - name: Content-Type
              value: application/json
          request_transform:
            method: POST
            body:
              action: transform
              template: |
                {
                  "user_id": {{$body.input.userId}},
                  "metadata": {{$body.input.metadata}}
                }
        permissions:
          - role: user
      
      - name: sendMessage
        definition:
          kind: synchronous
          handler: http://app:8000/api/v1/agents/{{$body.input.agentId}}/sessions/{{$body.input.sessionId}}/messages
          headers:
            - name: Content-Type
              value: application/json
          request_transform:
            method: POST
            body:
              action: transform
              template: |
                {
                  "content": {{$body.input.content}},
                  "context": {{$body.input.context}}
                }
        permissions:
          - role: user
      
      - name: executeWorkflow
        definition:
          kind: asynchronous
          handler: http://app:8000/api/v1/workflows/execute/{{$body.input.workflowName}}
          headers:
            - name: Content-Type
              value: application/json
          request_transform:
            method: POST
            body:
              action: transform
              template: |
                {
                  "agent_id": {{$body.input.agentId}},
                  "parameters": {{$body.input.parameters}}
                }
        permissions:
          - role: user
    
    custom_types:
      enums:
        - name: AgentType
          values:
            - value: conversational
            - value: task_oriented
            - value: research
            - value: coordinator
        
        - name: MemoryType
          values:
            - value: episodic
            - value: semantic
            - value: implicit
            - value: prospective
        
        - name: TaskStatus
          values:
            - value: pending
            - value: running
            - value: completed
            - value: failed
            - value: cancelled
      
      input_objects:
        - name: MemorySearchInput
          fields:
            - name: query
              type: String!
            - name: types
              type: "[MemoryType!]"
            - name: limit
              type: Int
            - name: threshold
              type: Float
      
      objects:
        - name: ConversationResponse
          fields:
            - name: response
              type: String!
            - name: sessionId
              type: uuid!
            - name: metadata
              type: jsonb

### Hasura Remote Schemas

**`hasura/metadata/remote_schemas.yaml`**

yaml

    - name: typespec_api
      definition:
        url: http://app:8000/api/v1/graphql
        headers:
          - name: X-Hasura-Role
            value: service
        forward_client_headers: true
      comment: TypeSpec generated GraphQL API

### Hasura Event Triggers

**`hasura/metadata/event_triggers.yaml`**

yaml

    - table:
        schema: agents
        name: messages
      event_triggers:
        - name: message_created
          definition:
            enable_manual: true
            insert:
              columns: "*"
          retry_conf:
            num_retries: 3
            interval_sec: 10
            timeout_sec: 60
          webhook: http://app:8000/api/v1/webhooks/message-created
          headers:
            - name: X-Hasura-Event-Secret
              value_from_env: HASURA_EVENT_SECRET
    
    - table:
        schema: memory
        name: memories
      event_triggers:
        - name: memory_importance_decay
          definition:
            enable_manual: true
            update:
              columns:
                - importance
                - decayed_importance
          retry_conf:
            num_retries: 3
            interval_sec: 10
            timeout_sec: 60
          webhook: http://app:8000/api/v1/webhooks/memory-decay
    
    - table:
        schema: protocols
        name: a2a_tasks
      event_triggers:
        - name: task_status_changed
          definition:
            enable_manual: true
            update:
              columns:
                - status
          retry_conf:
            num_retries: 3
            interval_sec: 10
            timeout_sec: 60
          webhook: http://app:8000/api/v1/webhooks/task-status-changed

### Hasura Permissions

**`hasura/metadata/permissions.yaml`**

yaml

    # Agent permissions
    - table:
        schema: agents
        name: agents
      insert_permissions:
        - role: user
          permission:
            check:
              _or:
                - created_by:
                    _eq: X-Hasura-User-Id
                - is_public:
                    _eq: true
            columns:
              - name
              - description
              - type
              - model
              - metadata
      
      select_permissions:
        - role: user
          permission:
            columns: "*"
            filter:
              _or:
                - created_by:
                    _eq: X-Hasura-User-Id
                - is_public:
                    _eq: true
      
      update_permissions:
        - role: user
          permission:
            columns:
              - name
              - description
              - model
              - metadata
              - is_active
            filter:
              created_by:
                _eq: X-Hasura-User-Id
    
    # Memory permissions
    - table:
        schema: memory
        name: memories
      select_permissions:
        - role: user
          permission:
            columns:
              - id
              - type
              - content
              - importance
              - created_at
            filter:
              agent:
                created_by:
                  _eq: X-Hasura-User-Id
      
      insert_permissions:
        - role: service
          permission:
            columns: "*"
            check: {}
    
    # Protocol permissions
    - table:
        schema: protocols
        name: a2a_agents
      select_permissions:
        - role: user
          permission:
            columns: "*"
            filter:
              is_public:
                _eq: true

* * *

## 12\. Testing Strategy {#testing}

### Unit Tests

**`tests/test_memory_managers.py`**

python

    import pytest
    from datetime import datetime, timedelta
    from uuid import uuid4
    
    from src.memory.episodic import EpisodicMemoryManager
    from src.memory.semantic import SemanticMemoryManager
    from src.memory.prospective import ProspectiveMemoryManager
    from src.memory import MemoryType
    
    @pytest.fixture
    async def db_session():
        """Provide test database session."""
        from src.database import get_session_factory
        
        async with get_session_factory()() as session:
            yield session
            await session.rollback()
    
    @pytest.fixture
    def agent_id():
        """Provide test agent ID."""
        return str(uuid4())
    
    class TestEpisodicMemoryManager:
        async def test_store_episode(self, db_session, agent_id):
            """Test storing episodic memory."""
            manager = EpisodicMemoryManager(db_session)
            
            memory = await manager.store_episode(
                agent_id,
                "I had a great conversation about AI safety",
                {"topic": "AI safety", "mood": "engaged"},
                emotional_valence=0.8
            )
            
            assert memory.id is not None
            assert memory.type == MemoryType.EPISODIC
            assert memory.emotional_valence == 0.8
            assert memory.importance > 0
        
        async def test_retrieve_episodes(self, db_session, agent_id):
            """Test retrieving episodic memories."""
            manager = EpisodicMemoryManager(db_session)
            
            # Store test memories
            memories_data = [
                ("Happy birthday party", 0.9),
                ("Difficult meeting", -0.6),
                ("Neutral observation", 0.0)
            ]
            
            for content, valence in memories_data:
                await manager.store_episode(
                    agent_id, content, {}, 
                    emotional_valence=valence
                )
            
            # Retrieve positive memories
            positive = await manager.retrieve_episodes(
                agent_id,
                "memories",
                emotional_filter="positive"
            )
            
            assert len(positive) == 1
            assert positive[0].emotional_valence > 0
        
        async def test_consolidate_episodes(self, db_session, agent_id):
            """Test episodic memory consolidation."""
            manager = EpisodicMemoryManager(db_session)
            
            # Store similar memories
            for i in range(3):
                await manager.store_episode(
                    agent_id,
                    f"Meeting with John about project #{i}",
                    {"person": "John", "topic": "project"}
                )
            
            # Consolidate
            result = await manager.consolidate_episodes(agent_id)
            
            assert result["consolidated"] > 0
    
    class TestSemanticMemoryManager:
        async def test_store_fact(self, db_session, agent_id):
            """Test storing semantic memory."""
            manager = SemanticMemoryManager(db_session)
            
            memory = await manager.store_fact(
                agent_id,
                "Paris is the capital of France",
                concepts=["Paris", "France", "capital"],
                confidence=1.0
            )
            
            assert memory.id is not None
            assert memory.type == MemoryType.SEMANTIC
            assert memory.confidence == 1.0
            assert len(memory.concepts) == 3
        
        async def test_query_knowledge(self, db_session, agent_id):
            """Test querying semantic knowledge."""
            manager = SemanticMemoryManager(db_session)
            
            # Store test facts
            facts = [
                ("Dogs are mammals", ["dog", "mammal"]),
                ("Cats are mammals", ["cat", "mammal"]),
                ("Mammals are animals", ["mammal", "animal"])
            ]
            
            for content, concepts in facts:
                await manager.store_fact(
                    agent_id, content, concepts
                )
            
            # Query about mammals
            results = await manager.query_knowledge(
                agent_id,
                "What are mammals?",
                concept_filter=["mammal"]
            )
            
            assert len(results) >= 2
        
        async def test_build_knowledge_graph(self, db_session, agent_id):
            """Test building knowledge graph."""
            manager = SemanticMemoryManager(db_session)
            
            # Store related facts
            await manager.store_fact(
                agent_id,
                "Python is a programming language",
                ["Python", "programming language"]
            )
            
            await manager.store_fact(
                agent_id,
                "Programming languages are used to write software",
                ["programming language", "software"]
            )
            
            # Build graph
            graph = await manager.build_knowledge_graph(agent_id)
            
            assert len(graph.nodes()) >= 3
            assert len(graph.edges()) >= 1
    
    class TestProspectiveMemoryManager:
        async def test_create_goal(self, db_session, agent_id):
            """Test creating a goal."""
            manager = ProspectiveMemoryManager(db_session)
            
            goal = await manager.create_goal(
                agent_id,
                "Complete the project documentation",
                deadline=datetime.utcnow() + timedelta(days=7),
                priority=8
            )
            
            assert goal.id is not None
            assert goal.type == MemoryType.PROSPECTIVE
            assert goal.priority == 8
            assert goal.status == "active"
        
        async def test_update_goal_progress(self, db_session, agent_id):
            """Test updating goal progress."""
            manager = ProspectiveMemoryManager(db_session)
            
            # Create goal
            goal = await manager.create_goal(
                agent_id,
                "Read 10 research papers"
            )
            
            # Update progress
            await manager.update_goal_progress(
                goal.id,
                0.3,
                "Read 3 papers"
            )
            
            # Verify update
            updated = await manager.get_active_goals(agent_id)
            goal_updated = next(g for g in updated if g.id == goal.id)
            
            assert goal_updated.progress == 0.3
        
        async def test_goal_dependencies(self, db_session, agent_id):
            """Test goal dependencies."""
            manager = ProspectiveMemoryManager(db_session)
            
            # Create parent goal
            parent = await manager.create_goal(
                agent_id,
                "Launch new product"
            )
            
            # Create dependent goals
            design = await manager.create_goal(
                agent_id,
                "Complete product design",
                parent_goal_id=parent.id
            )
            
            development = await manager.create_goal(
                agent_id,
                "Develop product features",
                parent_goal_id=parent.id
            )
            
            # Add dependency
            await manager.add_dependency(development.id, design.id)
            
            # Verify parent has subgoals
            goals = await manager.get_active_goals(agent_id)
            parent_goal = next(g for g in goals if g.id == parent.id)
            
            assert len(parent_goal.subgoals) == 2

### Integration Tests

**`tests/test_workflows.py`**

python

    import pytest
    from datetime import timedelta
    from uuid import uuid4
    
    from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
    from src.workflows.agent_conversation import AgentConversationWorkflow
    from src.memory import MemoryType
    
    @pytest.fixture
    async def populated_agent(db_session):
        """Create agent with test data."""
        from src.agents.crud import AgentCRUD
        from src.api.schemas.agents import AgentCreate
        
        agent = await AgentCRUD.create(
            db_session,
            AgentCreate(
                name="Test Agent",
                type="conversational",
                model="gpt-4"
            )
        )
        
        # Add memories
        from src.memory.episodic import EpisodicMemoryManager
        
        emm = EpisodicMemoryManager(db_session)
        
        for i in range(10):
            await emm.store_episode(
                str(agent.id),
                f"Test memory {i}",
                {"index": i}
            )
        
        await db_session.commit()
        return agent
    
    class TestMemoryConsolidationWorkflow:
        async def test_consolidation_workflow(self, db_session, populated_agent):
            """Test memory consolidation workflow."""
            workflow = MemoryConsolidationWorkflow(
                "test_consolidation",
                str(populated_agent.id),
                db_session
            )
            
            result = await workflow.run(
                min_importance=0.2,
                time_window=timedelta(days=1)
            )
            
            assert result["total_processed"] >= 10
            assert "execution_time" in result
        
        async def test_consolidation_with_decay(self, db_session, populated_agent):
            """Test consolidation with memory decay."""
            # Age some memories
            await db_session.execute(
                """
                UPDATE memory.memories
                SET last_accessed_at = NOW() - INTERVAL '7 days'
                WHERE agent_id = :agent_id
                LIMIT 5
                """,
                {"agent_id": populated_agent.id}
            )
            
            workflow = MemoryConsolidationWorkflow(
                "test_decay",
                str(populated_agent.id),
                db_session
            )
            
            result = await workflow.run(
                min_importance=0.5
            )
            
            assert result["removed"] > 0
    
    class TestAgentConversationWorkflow:
        async def test_conversation_workflow(self, db_session, populated_agent):
            """Test agent conversation workflow."""
            # Create session
            from src.api.schemas.agents import SessionCreate
            
            session_sql = """
            INSERT INTO agents.sessions (agent_id, user_id)
            VALUES (:agent_id, :user_id)
            RETURNING id
            """
            
            session_result = await db_session.execute(
                session_sql,
                {"agent_id": populated_agent.id, "user_id": uuid4()}
            )
            
            session_id = session_result.scalar()
            await db_session.commit()
            
            # Run conversation
            workflow = AgentConversationWorkflow(
                "test_conversation",
                str(populated_agent.id),
                db_session
            )
            
            # Mock LLM response
            with pytest.mock.patch(
                "src.agents.llm.generate_completion",
                return_value={
                    "content": "Hello! How can I help you?",
                    "tokens_used": 20
                }
            ):
                result = await workflow.run(
                    str(session_id),
                    "Hello, AI assistant!",
                    {}
                )
            
            assert "response" in result
            assert result["new_memories"] > 0

### API Tests

**`tests/test_api_agents.py`**

python

    import pytest
    from httpx import AsyncClient
    from uuid import uuid4
    
    from src.api.main import app
    
    @pytest.fixture
    async def client():
        """Provide test client."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    
    class TestAgentAPI:
        async def test_create_agent(self, client):
            """Test agent creation endpoint."""
            response = await client.post(
                "/api/v1/agents/",
                json={
                    "name": "Test Agent",
                    "type": "conversational",
                    "model": "gpt-4",
                    "description": "A test agent"
                }
            )
            
            assert response.status_code == 201
            data = response.json()
            assert data["name"] == "Test Agent"
            assert "id" in data
        
        async def test_list_agents(self, client):
            """Test listing agents."""
            # Create test agents
            for i in range(3):
                await client.post(
                    "/api/v1/agents/",
                    json={
                        "name": f"Agent {i}",
                        "type": "conversational"
                    }
                )
            
            response = await client.get("/api/v1/agents/")
            assert response.status_code == 200
            
            data = response.json()
            assert len(data) >= 3
        
        async def test_agent_conversation(self, client):
            """Test agent conversation flow."""
            # Create agent
            agent_response = await client.post(
                "/api/v1/agents/",
                json={
                    "name": "Chat Agent",
                    "type": "conversational"
                }
            )
            
            agent_id = agent_response.json()["id"]
            
            # Create session
            session_response = await client.post(
                f"/api/v1/agents/{agent_id}/sessions",
                json={"user_id": str(uuid4())}
            )
            
            session_id = session_response.json()["id"]
            
            # Send message
            with pytest.mock.patch(
                "src.workflows.agent_conversation.generate_completion",
                return_value={
                    "content": "Hello! I'm here to help.",
                    "tokens_used": 15
                }
            ):
                message_response = await client.post(
                    f"/api/v1/agents/{agent_id}/sessions/{session_id}/messages",
                    json={"content": "Hello!"}
                )
            
            assert message_response.status_code == 200
            data = message_response.json()
            assert "response" in data

### Performance Tests

**`tests/test_performance.py`**

python

    import pytest
    import asyncio
    import time
    from concurrent.futures import ThreadPoolExecutor
    
    from src.memory import search_memories
    from src.memory.episodic import EpisodicMemoryManager
    
    class TestPerformance:
        async def test_memory_search_performance(self, db_session, agent_id):
            """Test memory search performance."""
            manager = EpisodicMemoryManager(db_session)
            
            # Create 1000 test memories
            for i in range(1000):
                await manager.store_episode(
                    agent_id,
                    f"Memory number {i} with some content",
                    {"index": i}
                )
            
            await db_session.commit()
            
            # Test search performance
            start_time = time.time()
            
            results = await search_memories(
                db_session,
                agent_id,
                "content",
                limit=20
            )
            
            search_time = time.time() - start_time
            
            assert len(results) == 20
            assert search_time < 0.1  # Should complete in under 100ms
        
        async def test_concurrent_operations(self, db_session):
            """Test concurrent agent operations."""
            from src.agents.crud import AgentCRUD
            from src.api.schemas.agents import AgentCreate
            
            async def create_agent(index):
                agent = await AgentCRUD.create(
                    db_session,
                    AgentCreate(
                        name=f"Concurrent Agent {index}",
                        type="conversational"
                    )
                )
                return agent
            
            # Create 10 agents concurrently
            start_time = time.time()
            
            tasks = [create_agent(i) for i in range(10)]
            agents = await asyncio.gather(*tasks)
            
            creation_time = time.time() - start_time
            
            assert len(agents) == 10
            assert creation_time < 2.0  # Should complete in under 2 seconds
        
        async def test_workflow_performance(self, db_session, populated_agent):
            """Test workflow execution performance."""
            from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
            
            workflow = MemoryConsolidationWorkflow(
                "perf_test",
                str(populated_agent.id),
                db_session
            )
            
            start_time = time.time()
            
            result = await workflow.run()
            
            execution_time = time.time() - start_time
            
            assert result["total_processed"] > 0
            assert execution_time < 5.0  # Should complete in under 5 seconds

* * *

## 13\. Deployment and Operations {#deployment}

### Docker Configuration

**`docker/app/Dockerfile`**

dockerfile

    FROM python:3.11-slim
    
    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        build-essential \
        postgresql-client \
        curl \
        && rm -rf /var/lib/apt/lists/*
    
    # Set working directory
    WORKDIR /app
    
    # Install Python dependencies
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy application code
    COPY src/ ./src/
    COPY schemas/ ./schemas/
    COPY scripts/ ./scripts/
    
    # Set environment variables
    ENV PYTHONPATH=/app
    ENV PYTHONUNBUFFERED=1
    
    # Create non-root user
    RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
    USER appuser
    
    # Health check
    HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
      CMD curl -f http://localhost:8000/api/v1/health || exit 1
    
    # Run application
    CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

### Docker Compose Production

**`docker-compose.prod.yml`**

yaml

    version: '3.8'
    
    services:
      postgres:
        image: pgvector/pgvector:pg15
        restart: always
        environment:
          POSTGRES_DB: julep_v2
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
          POSTGRES_INITDB_ARGS: "-c shared_preload_libraries='pg_stat_statements,pgmq,vector'"
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./docker/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
        networks:
          - julep_network
        deploy:
          resources:
            limits:
              cpus: '2'
              memory: 4G
            reservations:
              cpus: '1'
              memory: 2G
    
      app:
        build:
          context: .
          dockerfile: docker/app/Dockerfile
        restart: always
        environment:
          DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/julep_v2
          OPENAI_API_KEY: ${OPENAI_API_KEY}
          ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
          SECRET_KEY: ${SECRET_KEY}
          ENVIRONMENT: production
        depends_on:
          postgres:
            condition: service_healthy
        networks:
          - julep_network
        deploy:
          replicas: 3
          resources:
            limits:
              cpus: '1'
              memory: 2G
          update_config:
            parallelism: 1
            delay: 10s
          restart_policy:
            condition: on-failure
    
      hasura:
        image: hasura/graphql-engine:v2.36.0
        restart: always
        ports:
          - "8080:8080"
        environment:
          HASURA_GRAPHQL_DATABASE_URL: postgres://postgres:${POSTGRES_PASSWORD}@postgres:5432/julep_v2
          HASURA_GRAPHQL_ENABLE_CONSOLE: "false"
          HASURA_GRAPHQL_ADMIN_SECRET: ${HASURA_ADMIN_SECRET}
          HASURA_GRAPHQL_JWT_SECRET: |
            {
              "type": "HS256",
              "key": "${JWT_SECRET}"
            }
        depends_on:
          postgres:
            condition: service_healthy
        networks:
          - julep_network
        volumes:
          - ./hasura/metadata:/hasura-metadata
    
      nginx:
        image: nginx:alpine
        restart: always
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
          - ./docker/nginx/ssl:/etc/nginx/ssl
        depends_on:
          - app
          - hasura
        networks:
          - julep_network
    
      prometheus:
        image: prom/prometheus
        restart: always
        volumes:
          - ./docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
          - prometheus_data:/prometheus
        ports:
          - "9090:9090"
        networks:
          - julep_network
    
      grafana:
        image: grafana/grafana
        restart: always
        environment:
          GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
        volumes:
          - grafana_data:/var/lib/grafana
          - ./docker/grafana/dashboards:/etc/grafana/provisioning/dashboards
        ports:
          - "3000:3000"
        networks:
          - julep_network
    
    networks:
      julep_network:
        driver: bridge
    
    volumes:
      postgres_data:
      prometheus_data:
      grafana_data:

### Kubernetes Deployment

**`k8s/deployment.yaml`**

yaml

    apiVersion: v1
    kind: Namespace
    metadata:
      name: julep-v2
    
    ---
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: julep-config
      namespace: julep-v2
    data:
      DATABASE_POOL_SIZE: "20"
      DATABASE_MAX_OVERFLOW: "40"
      ENVIRONMENT: "production"
      LOG_LEVEL: "INFO"
      EMBEDDING_DIMENSIONS: "1536"
    
    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: julep-secrets
      namespace: julep-v2
    type: Opaque
    stringData:
      database-url: postgresql://postgres:password@postgres-service:5432/julep_v2
      openai-api-key: ${OPENAI_API_KEY}
      anthropic-api-key: ${ANTHROPIC_API_KEY}
      secret-key: ${SECRET_KEY}
      hasura-admin-secret: ${HASURA_ADMIN_SECRET}
    
    ---
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: julep-app
      namespace: julep-v2
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: julep-app
      template:
        metadata:
          labels:
            app: julep-app
        spec:
          containers:
          - name: app
            image: julep-v2:latest
            ports:
            - containerPort: 8000
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: julep-secrets
                  key: database-url
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: julep-secrets
                  key: openai-api-key
            envFrom:
            - configMapRef:
                name: julep-config
            resources:
              requests:
                memory: "1Gi"
                cpu: "500m"
              limits:
                memory: "2Gi"
                cpu: "1000m"
            livenessProbe:
              httpGet:
                path: /api/v1/health/live
                port: 8000
              initialDelaySeconds: 30
              periodSeconds: 10
            readinessProbe:
              httpGet:
                path: /api/v1/health/ready
                port: 8000
              initialDelaySeconds: 10
              periodSeconds: 5
    
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: julep-service
      namespace: julep-v2
    spec:
      selector:
        app: julep-app
      ports:
      - port: 80
        targetPort: 8000
      type: LoadBalancer
    
    ---
    apiVersion: apps/v1
    kind: StatefulSet
    metadata:
      name: postgres
      namespace: julep-v2
    spec:
      serviceName: postgres-service
      replicas: 1
      selector:
        matchLabels:
          app: postgres
      template:
        metadata:
          labels:
            app: postgres
        spec:
          containers:
          - name: postgres
            image: pgvector/pgvector:pg15
            ports:
            - containerPort: 5432
            env:
            - name: POSTGRES_DB
              value: julep_v2
            - name: POSTGRES_USER
              value: postgres
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            volumeMounts:
            - name: postgres-storage
              mountPath: /var/lib/postgresql/data
            resources:
              requests:
                memory: "2Gi"
                cpu: "1000m"
              limits:
                memory: "4Gi"
                cpu: "2000m"
      volumeClaimTemplates:
      - metadata:
          name: postgres-storage
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 100Gi
    
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: postgres-service
      namespace: julep-v2
    spec:
      selector:
        app: postgres
      ports:
      - port: 5432
        targetPort: 5432
      clusterIP: None
    
    ---
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: julep-hpa
      namespace: julep-v2
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: julep-app
      minReplicas: 3
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      - type: Resource
        resource:
          name: memory
          target:
            type: Utilization
            averageUtilization: 80

### Monitoring Configuration

**`docker/prometheus/prometheus.yml`**

yaml

    global:
      scrape_interval: 15s
      evaluation_interval: 15s
    
    scrape_configs:
      - job_name: 'julep-app'
        static_configs:
          - targets: ['app:8000']
        metrics_path: '/api/v1/health/metrics'
    
      - job_name: 'postgres'
        static_configs:
          - targets: ['postgres:9187']
    
      - job_name: 'hasura'
        static_configs:
          - targets: ['hasura:8080']
        metrics_path: '/v1/metrics'
    
      - job_name: 'node-exporter'
        static_configs:
          - targets: ['node-exporter:9100']
    
    alerting:
      alertmanagers:
        - static_configs:
            - targets: ['alertmanager:9093']
    
    rule_files:
      - 'alerts.yml'

**`docker/prometheus/alerts.yml`**

yaml

    groups:
      - name: julep_alerts
        interval: 30s
        rules:
          - alert: HighErrorRate
            expr: rate(julep_errors_total[5m]) > 0.05
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: High error rate detected
              description: "Error rate is {{ $value }} errors per second"
    
          - alert: HighMemoryUsage
            expr: julep_memory_usage_bytes / julep_memory_limit_bytes > 0.9
            for: 5m
            labels:
              severity: critical
            annotations:
              summary: High memory usage
              description: "Memory usage is above 90%"
    
          - alert: DatabaseConnectionPoolExhausted
            expr: julep_db_connections_active / julep_db_connections_max > 0.9
            for: 2m
            labels:
              severity: critical
            annotations:
              summary: Database connection pool near exhaustion
              description: "{{ $value }}% of connections in use"
    
          - alert: SlowWorkflowExecution
            expr: histogram_quantile(0.95, julep_workflow_duration_seconds) > 30
            for: 10m
            labels:
              severity: warning
            annotations:
              summary: Workflow execution time degraded
              description: "95th percentile execution time is {{ $value }}s"

* * *

## 14\. Troubleshooting Guide {#troubleshooting}

### Common Issues and Solutions

#### Database Connection Issues

**Problem:** Application fails to connect to PostgreSQL

    sqlalchemy.exc.OperationalError: could not connect to server

**Solutions:**

1.  Check PostgreSQL is running:
    
    bash
    
        docker-compose ps postgres
        docker-compose logs postgres
    
2.  Verify connection string:
    
    bash
    
        echo $DATABASE_URL
        # Should be: postgresql://user:password@host:5432/database
    
3.  Test connection directly:
    
    bash
    
        docker-compose exec postgres psql -U postgres -d julep_v2
    

#### Extension Installation Issues

**Problem:** Required PostgreSQL extensions not found

    RuntimeError: Missing required PostgreSQL extensions: {'vector', 'pgmq'}

**Solutions:**

1.  Install extensions manually:
    
    sql
    
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE EXTENSION IF NOT EXISTS pgmq;
        CREATE EXTENSION IF NOT EXISTS pg_jsonschema;
    
2.  Rebuild PostgreSQL image with extensions:
    
    bash
    
        docker-compose build --no-cache postgres
    

#### Memory Search Performance Issues

**Problem:** Memory searches taking too long

    Memory search exceeded 100ms threshold

**Solutions:**

1.  Check and create indexes:
    
    sql
    
        -- Check existing indexes
        SELECT indexname, indexdef 
        FROM pg_indexes 
        WHERE tablename = 'memories';
        
        -- Create HNSW index if missing
        CREATE INDEX CONCURRENTLY memories_embedding_hnsw_idx 
        ON memory.memories 
        USING hnsw (embedding vector_cosine_ops);
    
2.  Analyze query performance:
    
    sql
    
        EXPLAIN (ANALYZE, BUFFERS) 
        SELECT * FROM memory.search_memories(...);
    
3.  Vacuum and analyze tables:
    
    sql
    
        VACUUM ANALYZE memory.memories;
    

#### Workflow Execution Failures

**Problem:** DBOS workflows failing or hanging

    Workflow instance stuck in 'running' state

**Solutions:**

1.  Check workflow logs:
    
    sql
    
        SELECT * FROM workflows.workflow_instances 
        WHERE status = 'running' 
        AND created_at < NOW() - INTERVAL '1 hour';
    
2.  View step execution details:
    
    sql
    
        SELECT * FROM workflows.step_executions 
        WHERE instance_id = 'stuck-workflow-id'
        ORDER BY started_at;
    
3.  Force workflow cancellation:
    
    bash
    
        curl -X POST http://localhost:8000/api/v1/workflows/instances/{id}/cancel
    

#### MCP Protocol Connection Issues

**Problem:** MCP servers not responding

    MCP server connection timeout

**Solutions:**

1.  Check server status:
    
    sql
    
        SELECT * FROM protocols.mcp_servers 
        WHERE is_active = true 
        AND last_heartbeat < NOW() - INTERVAL '5 minutes';
    
2.  Restart MCP servers:
    
    python
    
        # In Python console
        from src.protocols.mcp.manager import MCPManager
        manager = MCPManager(agent_id, db)
        await manager.initialize()
    
3.  Debug STDIO connections:
    
    bash
    
        # Test MCP server directly
        echo '{"jsonrpc":"2.0","method":"initialize","params":{},"id":1}' | \
        your-mcp-server-command
    

### Performance Optimization Checklist

1.  **Database Tuning:**
    
    sql
    
        -- Update PostgreSQL configuration
        ALTER SYSTEM SET shared_buffers = '4GB';
        ALTER SYSTEM SET effective_cache_size = '12GB';
        ALTER SYSTEM SET work_mem = '256MB';
        ALTER SYSTEM SET maintenance_work_mem = '2GB';
        
        -- Reload configuration
        SELECT pg_reload_conf();
    
2.  **Connection Pooling:**
    
    python
    
        # Adjust pool settings in config.py
        DATABASE_POOL_SIZE = 50  # Increase for high load
        DATABASE_MAX_OVERFLOW = 100
    
3.  **Query Optimization:**
    
    sql
    
        -- Find slow queries
        SELECT query, mean_exec_time, calls
        FROM pg_stat_statements
        WHERE mean_exec_time > 100
        ORDER BY mean_exec_time DESC
        LIMIT 10;
    
4.  **Memory Consolidation Tuning:**
    
    python
    
        # Adjust consolidation parameters
        MEMORY_CONSOLIDATION_INTERVAL = 7200  # Run less frequently
        MEMORY_DECAY_RATE = 0.98  # Slower decay
    

### Debugging Tools

**Database Query Logger:**

python

    # Enable query logging for debugging
    import logging
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

**Memory Profiling:**

python

    from memory_profiler import profile
    
    @profile
    def memory_intensive_function():
        # Your code here
        pass

**Async Debugging:**

python

    import asyncio
    
    # Enable async debug mode
    asyncio.get_event_loop().set_debug(True)

**Request Tracing:**

python

    # Add to request headers
    headers = {
        "X-Request-ID": str(uuid.uuid4()),
        "X-Debug-Mode": "true"
    }

* * *

## 15\. Performance Optimization {#performance}

### Database Optimizations

#### Index Strategy

sql

    -- Essential indexes for performance
    
    -- Memory search optimization
    CREATE INDEX CONCURRENTLY idx_memories_agent_type_importance 
    ON memory.memories(agent_id, type, decayed_importance DESC)
    WHERE decayed_importance > 0.3;
    
    -- Session message retrieval
    CREATE INDEX CONCURRENTLY idx_messages_session_created 
    ON agents.messages(session_id, created_at DESC);
    
    -- Goal deadline tracking
    CREATE INDEX CONCURRENTLY idx_memories_prospective_deadline 
    ON memory.memories((type_data->>'deadline')::timestamp)
    WHERE type = 'prospective' 
      AND type_data->>'status' = 'active'
      AND type_data->>'deadline' IS NOT NULL;
    
    -- Partial indexes for common queries
    CREATE INDEX CONCURRENTLY idx_active_agents 
    ON agents.agents(created_at DESC) 
    WHERE is_active = true;
    
    -- BRIN index for time-series data
    CREATE INDEX idx_messages_created_brin 
    ON agents.messages USING BRIN(created_at);

#### Query Optimization Patterns

python

    # Bad: N+1 query problem
    for agent in agents:
        memories = await get_memories(agent.id)
        
    # Good: Batch loading
    agent_ids = [agent.id for agent in agents]
    memories = await get_memories_batch(agent_ids)
    
    # Bad: Loading unnecessary columns
    SELECT * FROM memory.memories WHERE agent_id = :id
    
    # Good: Select only needed columns
    SELECT id, content, importance 
    FROM memory.memories 
    WHERE agent_id = :id

#### Connection Pool Tuning

python

    # Optimized connection pool settings
    from sqlalchemy.pool import NullPool, QueuePool
    
    # For high-concurrency scenarios
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=50,
        max_overflow=100,
        pool_timeout=30,
        pool_recycle=3600,
        pool_pre_ping=True,
        echo_pool=True  # Debug pool usage
    )
    
    # For serverless/lambda
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=NullPool  # No pooling
    )

### Memory System Optimizations

#### Embedding Caching

python

    from functools import lru_cache
    import hashlib
    
    class EmbeddingCache:
        def __init__(self, max_size=10000):
            self.cache = {}
            self.max_size = max_size
        
        def get_key(self, text: str, model: str) -> str:
            return hashlib.md5(f"{model}:{text}".encode()).hexdigest()
        
        async def get_embedding(self, text: str, model: str) -> Optional[List[float]]:
            key = self.get_key(text, model)
            
            # Check cache
            if key in self.cache:
                return self.cache[key]
            
            # Check database cache
            sql = """
            SELECT embedding 
            FROM embedding_cache 
            WHERE cache_key = :key
            """
            result = await db.execute(sql, {"key": key})
            
            if result:
                embedding = result.scalar()
                self.cache[key] = embedding
                return embedding
            
            # Generate new embedding
            embedding = await generate_embedding(text, model)
            
            # Store in cache
            await self.store_embedding(key, embedding)
            
            return embedding

#### Batch Processing

python

    async def batch_store_memories(
        memories: List[MemoryCreate],
        batch_size: int = 100
    ) -> List[Memory]:
        """Batch insert memories for better performance."""
        
        stored = []
        
        for i in range(0, len(memories), batch_size):
            batch = memories[i:i + batch_size]
            
            # Generate embeddings in parallel
            embeddings = await asyncio.gather(*[
                generate_embedding(m.content) for m in batch
            ])
            
            # Batch insert
            values = [
                {
                    "agent_id": m.agent_id,
                    "type": m.type,
                    "content": m.content,
                    "embedding": emb,
                    "importance": m.importance
                }
                for m, emb in zip(batch, embeddings)
            ]
            
            result = await db.execute(
                """
                INSERT INTO memory.memories 
                (agent_id, type, content, embedding, importance)
                VALUES (:agent_id, :type, :content, :embedding, :importance)
                RETURNING *
                """,
                values
            )
            
            stored.extend(result.fetchall())
        
        return stored

### API Response Optimization

#### Response Caching

python

    from fastapi_cache import FastAPICache
    from fastapi_cache.decorator import cache
    from fastapi_cache.backends.redis import RedisBackend
    
    # Initialize cache
    @app.on_event("startup")
    async def startup():
        redis = aioredis.from_url("redis://localhost")
        FastAPICache.init(RedisBackend(redis), prefix="julep-cache")
    
    # Cache responses
    @router.get("/agents/{agent_id}/stats")
    @cache(expire=300)  # Cache for 5 minutes
    async def get_agent_stats(agent_id: UUID):
        # Expensive computation
        return stats

#### Pagination and Cursors

python

    from fastapi import Query
    from typing import Optional
    
    @router.get("/memories")
    async def list_memories(
        agent_id: UUID,
        cursor: Optional[str] = None,
        limit: int = Query(20, le=100)
    ):
        """Cursor-based pagination for large datasets."""
        
        query = """
        SELECT id, content, created_at
        FROM memory.memories
        WHERE agent_id = :agent_id
        """
        
        if cursor:
            # Decode cursor (timestamp + id)
            decoded = base64.b64decode(cursor).decode()
            timestamp, last_id = decoded.split(":")
            
            query += """
            AND (created_at, id) < (:timestamp, :last_id)
            """
        
        query += """
        ORDER BY created_at DESC, id DESC
        LIMIT :limit
        """
        
        results = await db.execute(query, params)
        
        # Generate next cursor
        if results:
            last = results[-1]
            next_cursor = base64.b64encode(
                f"{last.created_at}:{last.id}".encode()
            ).decode()
        else:
            next_cursor = None
        
        return {
            "items": results,
            "next_cursor": next_cursor
        }

### Async Optimization

#### Concurrent Operations

python

    async def process_agent_request(agent_id: str, message: str):
        """Process request with concurrent operations."""
        
        # Run independent operations concurrently
        results = await asyncio.gather(
            search_memories(agent_id, message),
            get_active_goals(agent_id),
            check_rate_limits(agent_id),
            return_exceptions=True
        )
        
        memories, goals, rate_limit = results
        
        # Handle any exceptions
        if isinstance(memories, Exception):
            logger.error(f"Memory search failed: {memories}")
            memories = []

#### Background Tasks

python

    from fastapi import BackgroundTasks
    
    @router.post("/agents/{agent_id}/consolidate")
    async def trigger_consolidation(
        agent_id: UUID,
        background_tasks: BackgroundTasks
    ):
        """Trigger memory consolidation in background."""
        
        # Quick response
        background_tasks.add_task(
            run_consolidation_workflow,
            agent_id
        )
        
        return {"status": "consolidation_started"}
    
    async def run_consolidation_workflow(agent_id: str):
        """Run consolidation without blocking."""
        
        workflow = MemoryConsolidationWorkflow(
            "background_consolidation",
            agent_id,
            db
        )
        
        try:
            await workflow.run()
        except Exception as e:
            logger.error(f"Consolidation failed: {e}")

### Monitoring and Profiling

#### Custom Metrics

python

    from prometheus_client import Counter, Histogram, Gauge
    
    # Define metrics
    memory_searches = Counter(
        'julep_memory_searches_total',
        'Total number of memory searches',
        ['agent_type', 'memory_type']
    )
    
    search_duration = Histogram(
        'julep_memory_search_duration_seconds',
        'Memory search duration',
        ['memory_type']
    )
    
    active_sessions = Gauge(
        'julep_active_sessions',
        'Number of active sessions'
    )
    
    # Use metrics
    @search_duration.time()
    async def search_memories_with_metrics(...):
        memory_searches.labels(
            agent_type=agent.type,
            memory_type=memory_type
        ).inc()
        
        # Actual search logic
        return results

#### Performance Profiling

python

    import cProfile
    import pstats
    from line_profiler import LineProfiler
    
    # Profile specific functions
    def profile_memory_consolidation():
        profiler = cProfile.Profile()
        profiler.enable()
        
        # Run consolidation
        asyncio.run(consolidate_memories(agent_id))
        
        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(20)
    
    # Line-by-line profiling
    lp = LineProfiler()
    lp_wrapper = lp(search_memories)
    
    # Run and show results
    lp_wrapper(agent_id, query)
    lp.print_stats()

This comprehensive implementor's guide provides everything needed to build the Julep V2 prototype. The modular architecture allows for incremental development while the PostgreSQL-centric approach simplifies operations and improves performance. The combination of TypeSpec for schema management, DBOS for workflow orchestration, and native protocol support creates a powerful platform for building sophisticated AI agents.







