# Julep-PG Documentation

<!-- AIDEV-NOTE: open-source-guide; community contribution and project documentation -->
## Table of Contents

1.  [Introduction](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#introduction)
    -   [What is Julep-PG?](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#what-is-julep-pg)
    -   [Why PostgreSQL-Native?](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#why-postgresql-native)
    -   [Architecture Overview](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#architecture-overview)
    -   [Key Features](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#key-features)
2.  [Getting Started](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#getting-started)
    -   [Prerequisites](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#prerequisites)
    -   [Quick Start](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#quick-start)
    -   [Installation](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#installation)
    -   [First Agent](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#first-agent)
3.  [Core Concepts](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#core-concepts)
    -   [Agents](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#agents)
    -   [Memory System](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#memory-system)
    -   [Sessions & Conversations](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#sessions-conversations)
    -   [Protocols (MCP & A2A)](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#protocols)
    -   [Workflows](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#workflows)
4.  [Architecture Deep Dive](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#architecture-deep-dive)
    -   [Database-Centric Design](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#database-centric-design)
    -   [PostgreSQL Extensions](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#postgresql-extensions)
    -   [Schema Design](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#schema-design)
    -   [Performance Architecture](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#performance-architecture)
5.  [API Reference](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#api-reference)
    -   [REST API](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#rest-api)
    -   [GraphQL API](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#graphql-api)
    -   [WebSocket API](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#websocket-api)
    -   [Database Functions](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#database-functions)
6.  [Memory System](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#memory-system-detailed)
    -   [Episodic Memory](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#episodic-memory)
    -   [Semantic Memory](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#semantic-memory)
    -   [Implicit Memory](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#implicit-memory)
    -   [Prospective Memory](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#prospective-memory)
    -   [Memory Consolidation](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#memory-consolidation)
7.  [Protocol Implementation](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#protocol-implementation)
    -   [MCP (Model Context Protocol)](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#mcp-protocol)
    -   [A2A (Agent-to-Agent)](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#a2a-protocol)
    -   [Protocol Integration](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#protocol-integration)
8.  [Workflow System](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#workflow-system)
    -   [DBOS Integration](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#dbos-integration)
    -   [Built-in Workflows](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#built-in-workflows)
    -   [Custom Workflows](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#custom-workflows)
    -   [Scheduled Tasks](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#scheduled-tasks)
9.  [Configuration Guide](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#configuration-guide)
    -   [Environment Variables](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#environment-variables)
    -   [Database Configuration](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#database-configuration)
    -   [Extension Configuration](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#extension-configuration)
    -   [Performance Tuning](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#performance-tuning)
10.  [Operations Guide](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#operations-guide)
    -   [Deployment](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#deployment)
    -   [Monitoring](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#monitoring)
    -   [Backup & Recovery](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#backup-recovery)
    -   [Scaling](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#scaling)
11.  [Development Guide](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#development-guide)
    -   [Setting Up Development](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#development-setup)
    -   [Code Structure](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#code-structure)
    -   [Testing](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#testing)
    -   [Contributing](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#contributing)
12.  [Troubleshooting](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#troubleshooting)
    -   [Common Issues](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#common-issues)
    -   [Performance Issues](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#performance-issues)
    -   [Debugging Tools](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#debugging-tools)
13.  [Examples & Tutorials](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#examples-tutorials)
    -   [Building a Conversational Agent](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#tutorial-conversational-agent)
    -   [Multi-Agent Collaboration](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#tutorial-multi-agent)
    -   [RAG Implementation](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#tutorial-rag)
    -   [Custom Tools](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#tutorial-custom-tools)
14.  [Migration Guide](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#migration-guide)
    -   [From Julep v1](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#from-julep-v1)
    -   [From Other Platforms](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#from-other-platforms)
15.  [Reference](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#reference)
    -   [Glossary](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#glossary)
    -   [FAQ](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#faq)
    -   [Resources](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#resources)

* * *

## 1\. Introduction {#introduction}

### What is Julep-PG? {#what-is-julep-pg}

Julep-PG is a revolutionary approach to building AI agent platforms that leverages PostgreSQL's extensibility to implement sophisticated agent capabilities directly within the database. Instead of complex microservice architectures, Julep-PG uses PostgreSQL extensions like pgai, pgvector, pgmq, and pgrag to create a unified, high-performance platform for stateful AI agents.

**Key Innovation**: By moving agent logic, memory management, and workflow orchestration into PostgreSQL, we achieve:

-   **8-40x faster inference** for local models
-   **25x faster workflow transitions** compared to external orchestrators
-   **Dramatically reduced operational complexity**
-   **Native ACID compliance** for all agent operations

### Why PostgreSQL-Native? {#why-postgresql-native}

Traditional AI agent platforms suffer from several architectural challenges:

1.  **Network Overhead**: Every operation requires multiple network hops between services
2.  **Consistency Challenges**: Distributed state management is complex and error-prone
3.  **Operational Complexity**: Multiple systems to monitor, secure, and scale
4.  **Cost Inefficiency**: Redundant infrastructure and over-provisioning

Julep-PG solves these by leveraging PostgreSQL's maturity and extensibility:

sql

    -- Everything is a simple SQL query
    SELECT * FROM agents.have_conversation(
        agent_id := '123e4567-e89b-12d3-a456-426614174000',
        message := 'What should I work on today?',
        context := jsonb_build_object('time_of_day', 'morning')
    );

### Architecture Overview {#architecture-overview}

mermaid

    graph TB
        subgraph "Client Layer"
            REST[REST API]
            GQL[GraphQL API]
            WS[WebSocket]
        end
        
        subgraph "Application Layer"
            FA[FastAPI Server]
            HA[Hasura GraphQL]
            DBOS[DBOS Workflows]
        end
        
        subgraph "PostgreSQL Core"
            subgraph "Extensions"
                PGAI[pgai - LLM Integration]
                PGV[pgvector - Embeddings]
                PGMQ[pgmq - Message Queue]
                PGRAG[pgrag - RAG Pipeline]
                PGJS[pg_jsonschema - Validation]
            end
            
            subgraph "Core Tables"
                AGT[Agents]
                MEM[Memories]
                SES[Sessions]
                WF[Workflows]
            end
            
            subgraph "Functions"
                CONV[Conversation Logic]
                SRCH[Memory Search]
                CONS[Consolidation]
            end
        end
        
        REST --> FA
        GQL --> HA
        WS --> FA
        FA --> PGAI
        FA --> PGV
        HA --> AGT
        DBOS --> PGMQ

### Key Features {#key-features}

#### 🧠 **Cognitive Memory System**

-   **Episodic Memory**: Temporal sequences with emotional context
-   **Semantic Memory**: Factual knowledge with concept graphs
-   **Implicit Memory**: Behavioral patterns and preferences
-   **Prospective Memory**: Goals, plans, and future intentions

#### 🔧 **Native Tool Integration**

-   100+ built-in integrations
-   PostgreSQL functions as tools
-   MCP protocol support
-   Custom tool creation

#### 🤝 **Multi-Agent Collaboration**

-   A2A (Agent-to-Agent) protocol
-   Task delegation and coordination
-   Shared memory spaces
-   Agent discovery

#### ⚡ **High-Performance Architecture**

-   Vector search with HNSW indexing
-   Parallel query execution
-   Connection pooling
-   Caching strategies

#### 🔒 **Enterprise-Ready**

-   ACID compliance
-   Row-level security
-   Audit logging
-   Backup/recovery

* * *

## 2\. Getting Started {#getting-started}

### Prerequisites {#prerequisites}

Before installing Julep-PG, ensure you have:

-   **PostgreSQL 15+** with development headers
-   **Docker & Docker Compose** (recommended)
-   **Python 3.11+** (for API server)
-   **Node.js 18+** (for TypeSpec)
-   **4GB+ RAM** for development
-   **16GB+ RAM** for production

### Quick Start {#quick-start}

The fastest way to get started is using Docker Compose:

bash

    # Clone the repository
    git clone https://github.com/julep-ai/julep-pg.git
    cd julep-pg
    
    # Copy environment variables
    cp .env.example .env
    
    # Edit .env with your API keys
    # Required: OPENAI_API_KEY or ANTHROPIC_API_KEY
    
    # Start all services
    docker-compose up -d
    
    # Wait for services to be ready
    docker-compose exec app python -m scripts.wait_for_db
    
    # Run initial setup
    docker-compose exec app python -m scripts.setup_database
    
    # Verify installation
    curl http://localhost:8000/api/v1/health

### Installation {#installation}

#### Option 1: Docker Installation (Recommended)

bash

    # Production deployment
    docker-compose -f docker-compose.prod.yml up -d
    
    # Development with hot reload
    docker-compose -f docker-compose.dev.yml up

#### Option 2: Manual Installation

1.  **Install PostgreSQL Extensions**:

bash

    # Install pgvector
    git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
    cd pgvector
    make
    sudo make install
    
    # Install pgmq
    git clone https://github.com/pgmq/pgmq.git
    cd pgmq
    make
    sudo make install
    
    # Install pg_jsonschema
    git clone https://github.com/supabase/pg_jsonschema.git
    cd pg_jsonschema
    make
    sudo make install

2.  **Setup Database**:

sql

    -- Connect to PostgreSQL
    psql -U postgres
    
    -- Create database
    CREATE DATABASE julep_pg;
    
    -- Connect to database
    \c julep_pg
    
    -- Enable extensions
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE EXTENSION IF NOT EXISTS pgmq;
    CREATE EXTENSION IF NOT EXISTS pg_jsonschema;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Run schema creation
    \i schemas/001_core_schema.sql
    \i schemas/002_memory_schema.sql
    \i schemas/003_protocol_schema.sql
    \i schemas/004_workflow_schema.sql

3.  **Install Python Application**:

bash

    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # Install dependencies
    pip install -r requirements.txt
    
    # Run migrations
    alembic upgrade head
    
    # Start server
    uvicorn src.api.main:app --reload

### First Agent {#first-agent}

Let's create your first AI agent:

python

    import httpx
    import asyncio
    
    async def create_first_agent():
        async with httpx.AsyncClient() as client:
            # Create an agent
            agent_response = await client.post(
                "http://localhost:8000/api/v1/agents",
                json={
                    "name": "Assistant",
                    "type": "conversational",
                    "model": "gpt-4",
                    "system_prompt": "You are a helpful AI assistant.",
                    "memory_config": {
                        "enable_episodic": True,
                        "enable_semantic": True
                    }
                }
            )
            agent = agent_response.json()
            
            # Create a conversation session
            session_response = await client.post(
                f"http://localhost:8000/api/v1/agents/{agent['id']}/sessions",
                json={"user_id": "test-user"}
            )
            session = session_response.json()
            
            # Send a message
            message_response = await client.post(
                f"http://localhost:8000/api/v1/agents/{agent['id']}/sessions/{session['id']}/messages",
                json={"content": "Hello! What's your name?"}
            )
            
            print(f"Agent response: {message_response.json()['response']}")
    
    # Run the example
    asyncio.run(create_first_agent())

Or using SQL directly:

sql

    -- Create an agent
    INSERT INTO agents.agents (name, type, model, system_prompt)
    VALUES ('SQL Assistant', 'conversational', 'gpt-4', 'You are a helpful assistant.')
    RETURNING id;
    
    -- Create a session
    INSERT INTO agents.sessions (agent_id, user_id)
    VALUES ('your-agent-id', 'user-123')
    RETURNING id;
    
    -- Have a conversation
    SELECT * FROM agents.send_message(
        session_id := 'your-session-id',
        content := 'Hello! How can you help me?'
    );

* * *

## 3\. Core Concepts {#core-concepts}

### Agents {#agents}

Agents are the fundamental building blocks of Julep-PG. Each agent represents an AI entity with its own personality, capabilities, and memory.

#### Agent Types

1.  **Conversational Agents**: Optimized for dialogue and chat interactions
2.  **Task-Oriented Agents**: Focused on completing specific objectives
3.  **Research Agents**: Specialized in information gathering and analysis
4.  **Coordinator Agents**: Orchestrate multi-agent collaborations

#### Agent Configuration

python

    {
        "name": "Research Assistant",
        "type": "research",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 4096,
        "system_prompt": "You are an expert research assistant...",
        
        # Memory configuration
        "memory_config": {
            "enable_episodic": True,      # Remember conversations
            "enable_semantic": True,      # Store facts and knowledge
            "enable_implicit": True,      # Learn behavioral patterns
            "enable_prospective": True,   # Track goals and plans
            "consolidation_interval": 3600,  # Consolidate every hour
            "decay_rate": 0.95,          # Memory decay factor
            "importance_threshold": 0.3   # Minimum importance to retain
        },
        
        # Protocol configurations
        "mcp_servers": [
            {
                "name": "calculator",
                "transport": "stdio",
                "command": "mcp-calculator"
            }
        ],
        
        "a2a_capabilities": {
            "capabilities": ["research", "summarization", "fact_checking"],
            "protocols": ["a2a/v1"],
            "is_public": True
        }
    }

### Memory System {#memory-system}

The memory system is inspired by human cognitive architecture, providing agents with sophisticated memory capabilities:

#### Memory Types Comparison

Type

Purpose

Example

Decay

Consolidation

**Episodic**

Personal experiences

"User asked about Python yesterday"

Yes

Merges similar events

**Semantic**

Facts and knowledge

"Python is a programming language"

Slow

Links concepts

**Implicit**

Behavioral patterns

"User prefers concise answers"

No

Strengthens with repetition

**Prospective**

Future intentions

"Remind user about meeting tomorrow"

No

Updates on completion

#### Memory Lifecycle

mermaid

    graph LR
        A[Experience] --> B[Encoding]
        B --> C[Storage]
        C --> D[Consolidation]
        D --> E[Retrieval]
        E --> F[Decay/Strengthening]
        F --> C

### Sessions & Conversations {#sessions-conversations}

Sessions maintain conversation context and manage token windows:

python

    # Session configuration
    {
        "agent_id": "agent-uuid",
        "user_id": "user-123",
        "context_window": 4096,      # Max tokens to maintain
        "max_messages": 100,         # Max messages to store
        "metadata": {
            "channel": "web",
            "user_timezone": "America/New_York"
        }
    }

#### Context Management

The system automatically manages context windows:

1.  **Token Counting**: Accurate token counts using tiktoken
2.  **Smart Truncation**: Preserves important messages
3.  **Summary Generation**: Compresses old conversations
4.  **Memory Integration**: Pulls relevant memories

### Protocols {#protocols}

#### MCP (Model Context Protocol)

MCP enables agents to use external tools and resources:

python

    # Tool definition
    {
        "name": "web_search",
        "description": "Search the web for information",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "max_results": {"type": "integer", "default": 5}
            },
            "required": ["query"]
        }
    }

#### A2A (Agent-to-Agent) Protocol

Enables agents to collaborate on complex tasks:

python

    # Task delegation
    {
        "client_agent": "coordinator-uuid",
        "remote_agent": "researcher-uuid",
        "task": {
            "name": "research_topic",
            "input": {
                "topic": "quantum computing",
                "depth": "comprehensive"
            }
        }
    }

### Workflows {#workflows}

Workflows orchestrate multi-step processes using DBOS:

python

    @dbos_workflow("document_analysis")
    async def analyze_document(self, document_url: str):
        # Step 1: Download document
        content = await self.download_document(document_url)
        
        # Step 2: Extract text
        text = await self.extract_text(content)
        
        # Step 3: Generate summary
        summary = await self.generate_summary(text)
        
        # Step 4: Extract key points
        key_points = await self.extract_key_points(text)
        
        # Step 5: Store in memory
        await self.store_analysis(summary, key_points)
        
        return {
            "summary": summary,
            "key_points": key_points
        }

* * *

## 4\. Architecture Deep Dive {#architecture-deep-dive}

### Database-Centric Design {#database-centric-design}

Julep-PG's architecture centers around PostgreSQL as the single source of truth for all operations. This design eliminates the complexity of distributed systems while leveraging PostgreSQL's battle-tested reliability.

#### Architectural Principles

1.  **Data Locality**: Keep compute close to data
2.  **ACID Compliance**: Every operation is transactional
3.  **Extensibility**: Leverage PostgreSQL's extension ecosystem
4.  **Simplicity**: One system to learn, deploy, and operate

#### Component Architecture

mermaid

    graph TB
        subgraph "External Clients"
            WEB[Web Apps]
            MOB[Mobile Apps]
            API[API Clients]
            CLI[CLI Tools]
        end
        
        subgraph "API Gateway Layer"
            NGINX[Nginx]
            CDN[CDN]
        end
        
        subgraph "Application Tier"
            subgraph "FastAPI Services"
                AUTH[Auth Service]
                AGENT[Agent Service]
                MEM[Memory Service]
                PROTO[Protocol Service]
            end
            
            subgraph "GraphQL Layer"
                HASURA[Hasura Engine]
                SUB[Subscriptions]
            end
            
            subgraph "Background Workers"
                CONSOLIDATION[Memory Consolidation]
                SCHEDULER[Task Scheduler]
                CLEANUP[Cleanup Worker]
            end
        end
        
        subgraph "PostgreSQL Database"
            subgraph "Extensions Layer"
                PGAI[pgai]
                VECTOR[pgvector]
                QUEUE[pgmq]
                RAG[pgrag]
                SCHEMA[pg_jsonschema]
            end
            
            subgraph "Schema Layer"
                subgraph "Core Schemas"
                    AGENTS_SCHEMA[agents.*]
                    MEMORY_SCHEMA[memory.*]
                    PROTOCOLS_SCHEMA[protocols.*]
                    WORKFLOWS_SCHEMA[workflows.*]
                end
            end
            
            subgraph "Function Layer"
                STORED_PROCS[Stored Procedures]
                TRIGGERS[Triggers]
                VIEWS[Materialized Views]
            end
        end
        
        WEB --> NGINX
        MOB --> NGINX
        API --> NGINX
        CLI --> NGINX
        
        NGINX --> AUTH
        NGINX --> AGENT
        NGINX --> MEM
        NGINX --> PROTO
        NGINX --> HASURA
        
        AUTH --> AGENTS_SCHEMA
        AGENT --> AGENTS_SCHEMA
        AGENT --> PGAI
        MEM --> MEMORY_SCHEMA
        MEM --> VECTOR
        PROTO --> PROTOCOLS_SCHEMA
        PROTO --> QUEUE
        
        HASURA --> AGENTS_SCHEMA
        HASURA --> MEMORY_SCHEMA
        
        CONSOLIDATION --> MEMORY_SCHEMA
        SCHEDULER --> WORKFLOWS_SCHEMA
        CLEANUP --> AGENTS_SCHEMA

### PostgreSQL Extensions {#postgresql-extensions}

#### pgai - LLM Integration

pgai provides native PostgreSQL functions for LLM operations:

sql

    -- Direct LLM calls from SQL
    SELECT ai_chat_completion(
        'gpt-4',
        jsonb_build_array(
            jsonb_build_object('role', 'system', 'content', 'You are helpful'),
            jsonb_build_object('role', 'user', 'content', 'Hello!')
        )
    );
    
    -- Embedding generation
    SELECT ai_generate_embedding('text-embedding-3-small', 'Some text to embed');

#### pgvector - Vector Operations

Enables efficient similarity search:

sql

    -- Create vector column
    ALTER TABLE memories ADD COLUMN embedding vector(1536);
    
    -- Create HNSW index for fast search
    CREATE INDEX memories_embedding_idx ON memories 
    USING hnsw (embedding vector_cosine_ops);
    
    -- Similarity search
    SELECT content, 1 - (embedding <=> query_embedding) as similarity
    FROM memories
    ORDER BY embedding <=> query_embedding
    LIMIT 10;

#### pgmq - Message Queue

Built-in message queue for async operations:

sql

    -- Create queue
    SELECT pgmq.create_queue('task_queue');
    
    -- Send message
    SELECT pgmq.send('task_queue', '{"task": "process_document", "id": 123}');
    
    -- Read messages
    SELECT * FROM pgmq.read('task_queue', 10, 1);
    
    -- Archive processed messages
    SELECT pgmq.archive('task_queue', msg_id);

#### pgrag - RAG Pipeline

Complete RAG implementation in PostgreSQL:

sql

    -- Document chunking
    SELECT pgrag.chunk_document(
        content := 'Long document text...',
        chunk_size := 512,
        overlap := 50
    );
    
    -- RAG retrieval
    SELECT pgrag.retrieve_context(
        query := 'What is the main topic?',
        collection := 'documents',
        top_k := 5
    );

### Schema Design {#schema-design}

#### Design Principles

1.  **Normalization**: Proper 3NF where appropriate
2.  **Denormalization**: Strategic denormalization for performance
3.  **JSONB Usage**: Flexible schema for metadata
4.  **Partitioning**: Time-based partitioning for large tables

#### Core Tables Structure

sql

    -- Agents table with full configuration
    CREATE TABLE agents.agents (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        description TEXT,
        type agent_type NOT NULL DEFAULT 'conversational',
        
        -- Model configuration
        model VARCHAR(100) NOT NULL DEFAULT 'gpt-4',
        temperature FLOAT DEFAULT 0.7,
        max_tokens INTEGER DEFAULT 4096,
        system_prompt TEXT,
        
        -- Configuration as JSONB for flexibility
        metadata JSONB DEFAULT '{}',
        mcp_servers JSONB DEFAULT '[]',
        a2a_capabilities JSONB,
        memory_config JSONB DEFAULT '{
            "enable_episodic": true,
            "enable_semantic": true,
            "consolidation_interval": 3600
        }',
        
        -- State tracking
        is_active BOOLEAN DEFAULT true,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Indexes for common queries
        CONSTRAINT valid_temperature CHECK (temperature >= 0 AND temperature <= 2),
        CONSTRAINT valid_max_tokens CHECK (max_tokens > 0 AND max_tokens <= 128000)
    );
    
    -- Indexes for performance
    CREATE INDEX idx_agents_active ON agents.agents(is_active) WHERE is_active = true;
    CREATE INDEX idx_agents_type ON agents.agents(type);
    CREATE INDEX idx_agents_metadata ON agents.agents USING GIN(metadata);

#### Memory Table with Vector Support

sql

    CREATE TABLE memory.memories (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
        type memory_type NOT NULL,
        
        -- Content and embedding
        content TEXT NOT NULL,
        embedding vector(1536),
        
        -- Importance and decay
        importance FLOAT DEFAULT 0.5,
        decayed_importance FLOAT,
        decay_rate FLOAT DEFAULT 0.95,
        
        -- Access patterns
        access_count INTEGER DEFAULT 0,
        last_accessed_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Flexible metadata
        metadata JSONB DEFAULT '{}',
        source_context JSONB,
        
        -- Type-specific data
        type_data JSONB DEFAULT '{}',
        
        -- Relationships
        related_memories UUID[] DEFAULT '{}',
        
        -- Timestamps
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );
    
    -- Optimized indexes
    CREATE INDEX idx_memories_agent_type ON memory.memories(agent_id, type);
    CREATE INDEX idx_memories_embedding ON memory.memories 
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    CREATE INDEX idx_memories_importance ON memory.memories(agent_id, decayed_importance DESC)
        WHERE decayed_importance > 0.3;

### Performance Architecture {#performance-architecture}

#### Query Optimization Strategy

1.  **Index Design**:
    -   B-tree for exact matches
    -   GiST/GIN for JSONB queries
    -   HNSW for vector similarity
    -   BRIN for time-series data
2.  **Partitioning Strategy**:
    
    sql
    
        -- Partition messages by month
        CREATE TABLE agents.messages (
            id SERIAL,
            session_id UUID,
            created_at TIMESTAMPTZ,
            content TEXT
        ) PARTITION BY RANGE (created_at);
        
        -- Create monthly partitions
        CREATE TABLE agents.messages_2024_01 
        PARTITION OF agents.messages
        FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
    
3.  **Materialized Views**:
    
    sql
    
        CREATE MATERIALIZED VIEW memory.agent_stats AS
        SELECT 
            agent_id,
            type,
            COUNT(*) as memory_count,
            AVG(importance) as avg_importance,
            MAX(created_at) as latest_memory
        FROM memory.memories
        GROUP BY agent_id, type;
        
        -- Refresh periodically
        REFRESH MATERIALIZED VIEW CONCURRENTLY memory.agent_stats;
    

#### Connection Pooling

python

    # Optimized connection pool configuration
    DATABASE_POOL_CONFIG = {
        "pool_size": 50,           # Base connections
        "max_overflow": 100,       # Additional connections under load
        "pool_timeout": 30,        # Wait time for connection
        "pool_recycle": 3600,      # Recycle connections hourly
        "pool_pre_ping": True,     # Verify connections before use
        "echo_pool": False         # Set True for debugging
    }

#### Caching Strategy

1.  **Query Result Cache**:
    
    python
    
        from functools import lru_cache
        import hashlib
        
        @lru_cache(maxsize=1000)
        async def get_agent_cached(agent_id: str):
            return await db.get_agent(agent_id)
    
2.  **Embedding Cache**:
    
    sql
    
        CREATE TABLE cache.embeddings (
            text_hash VARCHAR(64) PRIMARY KEY,
            model VARCHAR(50),
            embedding vector(1536),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
        
        -- Clean old cache entries
        DELETE FROM cache.embeddings 
        WHERE created_at < NOW() - INTERVAL '7 days';
    

* * *

## 5\. API Reference {#api-reference}

### REST API {#rest-api}

The REST API provides comprehensive access to all Julep-PG functionality. All endpoints follow RESTful conventions and return JSON responses.

#### Authentication

http

    Authorization: Bearer <api_key>
    X-API-Key: <api_key>

#### Base URL

    https://api.julep-pg.ai/v1
    # or for self-hosted
    http://localhost:8000/api/v1

#### Common Headers

http

    Content-Type: application/json
    Accept: application/json
    X-Request-ID: <uuid>  # Optional request tracking

#### Agents Endpoints

##### Create Agent

http

    POST /agents
    Content-Type: application/json
    
    {
        "name": "Research Assistant",
        "type": "research",
        "model": "gpt-4",
        "temperature": 0.7,
        "system_prompt": "You are a helpful research assistant.",
        "memory_config": {
            "enable_episodic": true,
            "enable_semantic": true,
            "consolidation_interval": 3600
        },
        "metadata": {
            "department": "R&D",
            "clearance_level": "standard"
        }
    }
    
    Response: 201 Created
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Research Assistant",
        "type": "research",
        "created_at": "2024-01-15T09:30:00Z",
        ...
    }

##### List Agents

http

    GET /agents?type=research&is_active=true&limit=20&offset=0
    
    Response: 200 OK
    {
        "items": [...],
        "total": 45,
        "limit": 20,
        "offset": 0
    }

##### Update Agent

http

    PUT /agents/{agent_id}
    Content-Type: application/json
    
    {
        "name": "Updated Assistant",
        "temperature": 0.8,
        "metadata": {
            "department": "R&D",
            "clearance_level": "elevated"
        }
    }

##### Delete Agent

http

    DELETE /agents/{agent_id}
    
    Response: 204 No Content

#### Sessions Endpoints

##### Create Session

http

    POST /agents/{agent_id}/sessions
    Content-Type: application/json
    
    {
        "user_id": "user-123",
        "context_window": 4096,
        "metadata": {
            "channel": "web",
            "session_type": "support"
        }
    }
    
    Response: 201 Created
    {
        "id": "session-uuid",
        "agent_id": "agent-uuid",
        "user_id": "user-123",
        "is_active": true,
        "created_at": "2024-01-15T09:30:00Z"
    }

##### Send Message

http

    POST /agents/{agent_id}/sessions/{session_id}/messages
    Content-Type: application/json
    
    {
        "content": "What is quantum computing?",
        "context": {
            "previous_topic": "physics",
            "user_expertise": "beginner"
        }
    }
    
    Response: 200 OK
    {
        "response": "Quantum computing is a revolutionary approach...",
        "session_id": "session-uuid",
        "metadata": {
            "tokens_used": 156,
            "relevant_memories": 3,
            "processing_time_ms": 423
        }
    }

#### Memory Endpoints

##### Store Memory

http

    POST /memory/store
    Content-Type: application/json
    
    {
        "agent_id": "agent-uuid",
        "type": "semantic",
        "content": "The Earth orbits the Sun",
        "importance": 0.9,
        "metadata": {
            "source": "science_textbook",
            "confidence": 1.0
        }
    }

##### Search Memories

http

    POST /memory/search
    Content-Type: application/json
    
    {
        "agent_id": "agent-uuid",
        "query": "solar system facts",
        "types": ["semantic", "episodic"],
        "limit": 10,
        "threshold": 0.7
    }
    
    Response: 200 OK
    [
        {
            "id": "memory-uuid",
            "content": "The Earth orbits the Sun",
            "type": "semantic",
            "similarity": 0.89,
            "importance": 0.9
        },
        ...
    ]

##### Consolidate Memories

http

    POST /memory/consolidate
    Content-Type: application/json
    
    {
        "agent_id": "agent-uuid",
        "memory_types": ["episodic"],
        "min_importance": 0.3,
        "days": 7
    }
    
    Response: 200 OK
    {
        "total_processed": 150,
        "consolidated": 23,
        "removed": 45,
        "strengthened": 12,
        "execution_time": 2.34
    }

#### Protocol Endpoints

##### MCP Tool Execution

http

    POST /mcp/tools/{tool_name}/execute
    Content-Type: application/json
    
    {
        "agent_id": "agent-uuid",
        "input": {
            "query": "weather in New York",
            "units": "celsius"
        }
    }
    
    Response: 200 OK
    {
        "tool": "weather_search",
        "output": {
            "temperature": 5,
            "conditions": "cloudy",
            "humidity": 78
        },
        "execution_time_ms": 234
    }

##### A2A Task Creation

http

    POST /a2a/tasks
    Content-Type: application/json
    
    {
        "client_agent": "coordinator-uuid",
        "remote_agent": "researcher-uuid",
        "name": "research_quantum_computing",
        "input": {
            "topic": "quantum computing applications",
            "depth": "comprehensive",
            "max_sources": 10
        },
        "description": "Research practical applications of quantum computing"
    }
    
    Response: 201 Created
    {
        "id": "task-uuid",
        "status": "pending",
        "created_at": "2024-01-15T09:30:00Z"
    }

### GraphQL API {#graphql-api}

The GraphQL API (powered by Hasura) provides flexible querying capabilities:

#### Schema Overview

graphql

    type Agent {
        id: UUID!
        name: String!
        type: AgentType!
        model: String!
        memories(
            where: MemoryFilter
            order_by: [MemoryOrderBy!]
            limit: Int
            offset: Int
        ): [Memory!]!
        sessions(
            where: SessionFilter
            order_by: [SessionOrderBy!]
        ): [Session!]!
        created_at: Timestamp!
    }
    
    type Memory {
        id: UUID!
        agent: Agent!
        type: MemoryType!
        content: String!
        importance: Float!
        embedding: [Float!]
        relationships_from: [MemoryRelationship!]!
        relationships_to: [MemoryRelationship!]!
    }
    
    type Session {
        id: UUID!
        agent: Agent!
        user_id: String
        messages(
            order_by: [MessageOrderBy!]
            limit: Int
        ): [Message!]!
        is_active: Boolean!
    }

#### Query Examples

##### Get Agent with Recent Memories

graphql

    query GetAgentWithMemories($agentId: UUID!) {
        agent(id: $agentId) {
            id
            name
            type
            memories(
                where: {
                    created_at: { _gte: "2024-01-01" }
                    importance: { _gte: 0.5 }
                }
                order_by: { created_at: desc }
                limit: 10
            ) {
                id
                type
                content
                importance
                created_at
            }
        }
    }

##### Search Across Agents

graphql

    query SearchAgents($searchTerm: String!) {
        agents(
            where: {
                _or: [
                    { name: { _ilike: $searchTerm } }
                    { description: { _ilike: $searchTerm } }
                    { metadata: { _contains: { tags: [$searchTerm] } } }
                ]
            }
        ) {
            id
            name
            type
            created_at
        }
    }

#### Mutations

##### Create Agent with Subscription

graphql

    mutation CreateAgent($input: AgentInput!) {
        insert_agents_one(object: $input) {
            id
            name
            type
            created_at
        }
    }
    
    subscription WatchAgent($agentId: UUID!) {
        agents(where: { id: { _eq: $agentId } }) {
            id
            name
            updated_at
            sessions_aggregate {
                aggregate {
                    count
                }
            }
        }
    }

### WebSocket API {#websocket-api}

Real-time communication for live conversations:

javascript

    // Connect to WebSocket
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    // Authenticate
    ws.send(JSON.stringify({
        type: 'auth',
        token: 'your-api-key'
    }));
    
    // Start conversation
    ws.send(JSON.stringify({
        type: 'conversation.start',
        agent_id: 'agent-uuid',
        session_id: 'session-uuid'
    }));
    
    // Send message
    ws.send(JSON.stringify({
        type: 'message.send',
        content: 'Hello, assistant!'
    }));
    
    // Receive response
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        switch(data.type) {
            case 'message.response':
                console.log('Assistant:', data.content);
                break;
            case 'message.thinking':
                console.log('Assistant is thinking...');
                break;
            case 'memory.recalled':
                console.log('Recalled:', data.memories);
                break;
        }
    };

### Database Functions {#database-functions}

Direct SQL function calls for advanced users:

#### Memory Search Function

sql

    -- Search memories with vector similarity
    CREATE OR REPLACE FUNCTION memory.search_memories(
        p_agent_id UUID,
        p_query TEXT,
        p_types memory_type[] DEFAULT NULL,
        p_limit INTEGER DEFAULT 10,
        p_threshold FLOAT DEFAULT 0.7
    ) RETURNS TABLE(
        memory_id UUID,
        content TEXT,
        type memory_type,
        similarity FLOAT,
        importance FLOAT
    ) AS $$
    BEGIN
        -- Implementation details...
    END;
    $$ LANGUAGE plpgsql;
    
    -- Usage
    SELECT * FROM memory.search_memories(
        'agent-uuid',
        'quantum computing',
        ARRAY['semantic', 'episodic'],
        10,
        0.8
    );

#### Conversation Function

sql

    -- Complete conversation handling in one function
    CREATE OR REPLACE FUNCTION agents.have_conversation(
        p_session_id UUID,
        p_message TEXT,
        p_context JSONB DEFAULT '{}'
    ) RETURNS TABLE(
        response TEXT,
        tokens_used INTEGER,
        memories_recalled INTEGER
    ) AS $$
    BEGIN
        -- Implementation details...
    END;
    $$ LANGUAGE plpgsql;

* * *

## 6\. Memory System (Detailed) {#memory-system-detailed}

### Episodic Memory {#episodic-memory}

Episodic memory captures temporal sequences of experiences with rich contextual information, similar to human autobiographical memory.

#### Storage Structure

python

    {
        "id": "memory-uuid",
        "agent_id": "agent-uuid",
        "type": "episodic",
        "content": "User asked about their previous project status",
        "embedding": [0.023, -0.445, ...],  # 1536-dimensional vector
        "importance": 0.75,
        "emotional_valence": 0.2,  # Slightly positive
        "sensory_details": {
            "time_of_day": "morning",
            "conversation_tone": "professional",
            "urgency": "moderate"
        },
        "temporal_context": {
            "timestamp": "2024-01-15T09:30:00Z",
            "day_of_week": "Monday",
            "duration_seconds": 180,
            "preceded_by": "Greeting",
            "followed_by": "Task assignment"
        },
        "source_context": {
            "session_id": "session-uuid",
            "user_id": "user-123",
            "channel": "web",
            "location": "dashboard"
        }
    }

#### Retrieval Patterns

python

    # Time-based retrieval
    memories = await episodic_manager.retrieve_episodes(
        agent_id="agent-uuid",
        time_range=timedelta(days=7),
        emotional_filter="positive"
    )
    
    # Context-aware retrieval
    memories = await episodic_manager.retrieve_by_context(
        agent_id="agent-uuid",
        context={
            "user_id": "user-123",
            "topic": "project status"
        }
    )
    
    # Sequence retrieval
    memory_sequence = await episodic_manager.get_temporal_sequence(
        agent_id="agent-uuid",
        anchor_memory_id="memory-uuid",
        window_minutes=30
    )

#### Consolidation Process

Episodic memories undergo consolidation to merge similar experiences:

python

    async def consolidate_episodes(self, agent_id: str):
        # Group similar episodes within 24-hour windows
        similar_groups = await self.find_similar_episodes(
            agent_id=agent_id,
            similarity_threshold=0.85,
            time_window=timedelta(hours=24)
        )
        
        for group in similar_groups:
            if len(group) > 1:
                # Create consolidated memory
                consolidated = self.merge_episodes(group)
                
                # Preserve unique details in metadata
                consolidated.metadata["consolidated_from"] = [
                    m.id for m in group
                ]
                
                # Increase importance for repeated experiences
                consolidated.importance = min(
                    1.0, 
                    max(m.importance for m in group) + 0.1 * len(group)
                )

### Semantic Memory {#semantic-memory}

Semantic memory stores factual knowledge and conceptual understanding, building a knowledge graph over time.

#### Knowledge Representation

python

    {
        "id": "memory-uuid",
        "type": "semantic",
        "content": "Python is a high-level programming language",
        "concepts": ["Python", "programming language", "high-level"],
        "relationships": [
            {
                "type": "is_a",
                "source": "Python",
                "target": "programming language",
                "strength": 1.0
            },
            {
                "type": "has_property",
                "source": "Python",
                "target": "high-level",
                "strength": 1.0
            }
        ],
        "confidence": 1.0,
        "source": "direct_knowledge",
        "verification_status": "verified",
        "last_updated": "2024-01-15T09:30:00Z"
    }

#### Knowledge Graph Operations

python

    # Build knowledge graph
    graph = await semantic_manager.build_knowledge_graph(
        agent_id="agent-uuid",
        max_depth=3
    )
    
    # Query with inference
    results = await semantic_manager.query_with_inference(
        agent_id="agent-uuid",
        query="What programming languages are similar to Python?",
        inference_rules=["transitive", "similarity"]
    )
    
    # Add new fact with validation
    await semantic_manager.add_fact(
        agent_id="agent-uuid",
        fact="Django is a Python web framework",
        confidence=0.95,
        validate_consistency=True
    )

#### Concept Learning

sql

    -- Track concept evolution
    CREATE TABLE memory.concept_evolution (
        concept_id UUID REFERENCES memory.concepts(id),
        version INTEGER,
        definition TEXT,
        confidence FLOAT,
        learned_from JSONB,
        timestamp TIMESTAMPTZ DEFAULT NOW()
    );
    
    -- Concept relationship strength update
    UPDATE memory.relationships
    SET strength = strength * 0.9 + new_evidence * 0.1
    WHERE source_concept = 'Python' 
      AND target_concept = 'web development';

### Implicit Memory {#implicit-memory}

Implicit memory captures unconscious patterns, preferences, and behavioral tendencies.

#### Pattern Recognition

python

    {
        "id": "memory-uuid",
        "type": "implicit",
        "pattern": "user_prefers_concise_answers",
        "evidence": [
            {
                "timestamp": "2024-01-15T09:00:00Z",
                "context": "technical_question",
                "feedback": "positive"
            },
            {
                "timestamp": "2024-01-15T10:00:00Z",
                "context": "explanation_request",
                "feedback": "requested_shorter"
            }
        ],
        "confidence": 0.85,
        "frequency": 15,
        "last_triggered": "2024-01-15T11:00:00Z"
    }

#### Behavioral Learning

python

    # Record behavior
    await implicit_manager.record_behavior(
        agent_id="agent-uuid",
        action="provided_code_example",
        context={
            "user_type": "developer",
            "question_type": "implementation",
            "time_of_day": "morning"
        },
        outcome="positive_feedback"
    )
    
    # Get behavioral tendencies
    tendencies = await implicit_manager.get_tendencies(
        agent_id="agent-uuid",
        context={
            "user_type": "developer",
            "time_of_day": "morning"
        }
    )
    # Returns: ["provide_code_examples", "use_technical_language", "be_concise"]

#### Habit Formation

python

    # Extract habits
    habits = await implicit_manager.extract_habits(
        agent_id="agent-uuid",
        time_window=timedelta(days=30),
        min_frequency=10
    )
    
    # Result:
    [
        {
            "pattern": "morning_greeting_style",
            "description": "Uses informal greetings in morning conversations",
            "strength": 0.9,
            "consistency": 0.95,
            "contexts": ["time_of_day:morning", "conversation_start"]
        }
    ]

### Prospective Memory {#prospective-memory}

Prospective memory manages future-oriented cognition: goals, plans, and intentions.

#### Goal Hierarchies

python

    {
        "id": "goal-uuid",
        "type": "prospective",
        "content": "Complete user's project documentation",
        "goal_type": "task",
        "priority": 8,
        "deadline": "2024-01-20T17:00:00Z",
        "status": "active",
        "progress": 0.35,
        "subgoals": [
            {
                "id": "subgoal-1",
                "content": "Gather requirements",
                "status": "completed",
                "completed_at": "2024-01-15T10:00:00Z"
            },
            {
                "id": "subgoal-2",
                "content": "Write technical specifications",
                "status": "active",
                "progress": 0.6,
                "dependencies": ["subgoal-1"]
            }
        ],
        "reminders": [
            {
                "trigger_time": "2024-01-18T09:00:00Z",
                "message": "Documentation deadline in 2 days"
            }
        ]
    }

#### Goal Management

python

    # Create complex goal
    goal = await prospective_manager.create_goal(
        agent_id="agent-uuid",
        goal="Help user launch their product",
        breakdown_strategy="automatic",
        deadline=datetime.utcnow() + timedelta(days=30)
    )
    
    # Update progress with milestone
    await prospective_manager.update_progress(
        goal_id="goal-uuid",
        progress=0.4,
        milestone="Completed market research phase",
        artifacts=["research_report.pdf", "competitor_analysis.xlsx"]
    )
    
    # Get next actions
    next_actions = await prospective_manager.suggest_next_actions(
        agent_id="agent-uuid",
        context={
            "available_time": 120,  # minutes
            "energy_level": "high",
            "user_availability": True
        }
    )

#### Intention Monitoring

sql

    -- Monitor approaching deadlines
    CREATE OR REPLACE FUNCTION memory.check_approaching_deadlines()
    RETURNS TABLE(
        goal_id UUID,
        content TEXT,
        deadline TIMESTAMPTZ,
        hours_remaining FLOAT,
        priority INTEGER
    ) AS $$
    BEGIN
        RETURN QUERY
        SELECT 
            m.id,
            m.content,
            (m.type_data->>'deadline')::TIMESTAMPTZ,
            EXTRACT(EPOCH FROM (
                (m.type_data->>'deadline')::TIMESTAMPTZ - NOW()
            )) / 3600,
            (m.type_data->>'priority')::INTEGER
        FROM memory.memories m
        WHERE m.type = 'prospective'
            AND m.type_data->>'status' = 'active'
            AND (m.type_data->>'deadline')::TIMESTAMPTZ < NOW() + INTERVAL '48 hours'
            AND (m.type_data->>'deadline')::TIMESTAMPTZ > NOW()
        ORDER BY hours_remaining ASC, priority DESC;
    END;
    $$ LANGUAGE plpgsql;

### Memory Consolidation {#memory-consolidation}

Memory consolidation is a critical process that maintains memory system health and improves retrieval efficiency.

#### Consolidation Algorithm

python

    @dbos_workflow("memory_consolidation")
    async def consolidate_memories(self, agent_id: str):
        """Complete memory consolidation workflow."""
        
        # Step 1: Identify candidate memories
        candidates = await self.get_consolidation_candidates(
            agent_id=agent_id,
            min_age_days=1,
            max_importance=0.7
        )
        
        # Step 2: Apply forgetting curve
        for memory in candidates:
            decayed_importance = self.calculate_decay(
                original_importance=memory.importance,
                age_days=(datetime.utcnow() - memory.created_at).days,
                access_count=memory.access_count,
                decay_rate=memory.decay_rate
            )
            
            if decayed_importance < REMOVAL_THRESHOLD:
                await self.mark_for_removal(memory.id)
            else:
                memory.decayed_importance = decayed_importance
        
        # Step 3: Merge similar memories
        similarity_groups = await self.find_similar_groups(
            candidates,
            similarity_threshold=0.9
        )
        
        for group in similarity_groups:
            merged = await self.merge_memory_group(group)
            await self.create_consolidation_record(group, merged)
        
        # Step 4: Strengthen important connections
        await self.strengthen_memory_connections(agent_id)
        
        # Step 5: Update memory graph
        await self.rebuild_memory_graph(agent_id)

#### Forgetting Curve Implementation

python

    def calculate_decay(
        original_importance: float,
        age_days: float,
        access_count: int,
        decay_rate: float = 0.95
    ) -> float:
        """Ebbinghaus forgetting curve with modifications."""
        
        # Base decay
        base_decay = decay_rate ** age_days
        
        # Access bonus (logarithmic)
        access_bonus = 1 + (math.log(access_count + 1) * 0.1)
        
        # Importance factor (important memories decay slower)
        importance_factor = 0.5 + (original_importance * 0.5)
        
        # Calculate final importance
        decayed = original_importance * base_decay * access_bonus * importance_factor
        
        return min(1.0, max(0.0, decayed))

#### Memory Graph Optimization

sql

    -- Rebuild memory relationship graph
    CREATE OR REPLACE FUNCTION memory.rebuild_memory_graph(p_agent_id UUID)
    RETURNS VOID AS $$
    DECLARE
        v_memory RECORD;
        v_related RECORD;
        v_similarity FLOAT;
    BEGIN
        -- Clear weak relationships
        DELETE FROM memory.relationships
        WHERE source_memory IN (
            SELECT id FROM memory.memories WHERE agent_id = p_agent_id
        )
        AND strength < 0.3;
        
        -- Rebuild strong connections
        FOR v_memory IN
            SELECT id, embedding, type, content
            FROM memory.memories
            WHERE agent_id = p_agent_id
                AND decayed_importance > 0.5
        LOOP
            -- Find strongly related memories
            FOR v_related IN
                SELECT id, embedding, type
                FROM memory.memories
                WHERE agent_id = p_agent_id
                    AND id != v_memory.id
                    AND embedding IS NOT NULL
                    AND 1 - (embedding <=> v_memory.embedding) > 0.8
                LIMIT 10
            LOOP
                v_similarity := 1 - (v_memory.embedding <=> v_related.embedding);
                
                -- Create or update relationship
                INSERT INTO memory.relationships (
                    source_memory, target_memory,
                    relationship_type, strength
                ) VALUES (
                    v_memory.id, v_related.id,
                    CASE
                        WHEN v_memory.type = v_related.type THEN 'similar'
                        ELSE 'cross_type_association'
                    END,
                    v_similarity
                )
                ON CONFLICT (source_memory, target_memory, relationship_type)
                DO UPDATE SET strength = GREATEST(
                    relationships.strength,
                    EXCLUDED.strength
                );
            END LOOP;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;

* * *

## 7\. Protocol Implementation {#protocol-implementation}

### MCP (Model Context Protocol) {#mcp-protocol}

The Model Context Protocol enables agents to interact with external tools and resources through a standardized interface.

#### MCP Architecture

mermaid

    graph LR
        subgraph "Agent"
            CLIENT[MCP Client]
            TOOL_REG[Tool Registry]
            RESOURCE_CACHE[Resource Cache]
        end
        
        subgraph "MCP Servers"
            CALC[Calculator Server]
            WEB[Web Search Server]
            DB[Database Server]
            FILE[File System Server]
        end
        
        subgraph "Protocol Layer"
            STDIO[STDIO Transport]
            HTTP[HTTP Transport]
            MSGPACK[Message Pack]
        end
        
        CLIENT --> STDIO --> CALC
        CLIENT --> HTTP --> WEB
        CLIENT --> STDIO --> DB
        CLIENT --> HTTP --> FILE

#### Tool Definition Schema

typescript

    interface MCPTool {
        name: string;
        description: string;
        inputSchema: {
            type: "object";
            properties: Record<string, any>;
            required?: string[];
        };
        outputSchema?: {
            type: "object";
            properties: Record<string, any>;
        };
        examples?: Example[];
        rateLimit?: {
            requests: number;
            window: number;  // seconds
        };
    }
    
    // Example tool definition
    const webSearchTool: MCPTool = {
        name: "web_search",
        description: "Search the web for current information",
        inputSchema: {
            type: "object",
            properties: {
                query: {
                    type: "string",
                    description: "Search query"
                },
                max_results: {
                    type: "integer",
                    default: 5,
                    minimum: 1,
                    maximum: 20
                },
                search_type: {
                    type: "string",
                    enum: ["web", "news", "images", "videos"],
                    default: "web"
                }
            },
            required: ["query"]
        },
        examples: [
            {
                input: { query: "latest AI developments", max_results: 3 },
                output: { results: [...] }
            }
        ]
    };

#### MCP Server Implementation

python

    class MCPServer:
        """Base class for MCP server implementation."""
        
        def __init__(self, name: str, transport: str = "stdio"):
            self.name = name
            self.transport = transport
            self.tools: Dict[str, MCPTool] = {}
            self.resources: Dict[str, MCPResource] = {}
            self.prompts: Dict[str, MCPPrompt] = {}
            
        def register_tool(
            self,
            name: str,
            handler: Callable,
            description: str,
            input_schema: Dict[str, Any]
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
            
            # Validate schema
            jsonschema.validate(
                instance={},
                schema=input_schema
            )
        
        async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
            """Handle incoming MCP request."""
            
            method = request.get("method")
            params = request.get("params", {})
            
            handlers = {
                "initialize": self._handle_initialize,
                "tools/list": self._handle_list_tools,
                "tools/execute": self._handle_execute_tool,
                "resources/list": self._handle_list_resources,
                "resources/get": self._handle_get_resource,
                "prompts/list": self._handle_list_prompts,
                "prompts/get": self._handle_get_prompt
            }
            
            handler = handlers.get(method)
            if not handler:
                raise ValueError(f"Unknown method: {method}")
            
            return await handler(params)

#### Tool Execution Flow

python

    async def execute_tool(
        agent_id: str,
        tool_name: str,
        tool_input: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an MCP tool with full lifecycle management."""
        
        # 1. Find tool in registry
        tool = await find_tool(agent_id, tool_name)
        if not tool:
            raise ToolNotFoundError(f"Tool {tool_name} not found")
        
        # 2. Validate input
        validate_tool_input(tool.input_schema, tool_input)
        
        # 3. Check rate limits
        if not await check_rate_limit(agent_id, tool_name):
            raise RateLimitExceededError()
        
        # 4. Log execution start
        execution_id = await log_tool_execution_start(
            agent_id, tool_name, tool_input
        )
        
        try:
            # 5. Execute tool
            if tool.server.transport == "stdio":
                result = await execute_stdio_tool(tool, tool_input)
            else:
                result = await execute_http_tool(tool, tool_input)
            
            # 6. Validate output
            if tool.output_schema:
                validate_tool_output(tool.output_schema, result)
            
            # 7. Log success
            await log_tool_execution_success(execution_id, result)
            
            # 8. Update usage statistics
            await update_tool_usage_stats(tool_name, execution_id)
            
            return result
            
        except Exception as e:
            # 9. Log failure
            await log_tool_execution_failure(execution_id, str(e))
            raise

#### Resource Management

python

    class MCPResourceManager:
        """Manages MCP resources with caching."""
        
        def __init__(self, cache_ttl: int = 3600):
            self.cache_ttl = cache_ttl
            self.cache: Dict[str, CachedResource] = {}
        
        async def get_resource(
            self,
            uri: str,
            force_refresh: bool = False
        ) -> Dict[str, Any]:
            """Get resource with intelligent caching."""
            
            # Check cache
            if not force_refresh and uri in self.cache:
                cached = self.cache[uri]
                if cached.is_valid():
                    return cached.data
            
            # Fetch from server
            resource_data = await self.fetch_from_server(uri)
            
            # Update cache
            self.cache[uri] = CachedResource(
                data=resource_data,
                timestamp=datetime.utcnow(),
                ttl=self.cache_ttl
            )
            
            return resource_data
        
        async def subscribe_to_resource(
            self,
            uri: str,
            callback: Callable
        ):
            """Subscribe to resource changes."""
            
            subscription = ResourceSubscription(
                uri=uri,
                callback=callback,
                websocket=await self.create_websocket_connection()
            )
            
            await subscription.start()

### A2A (Agent-to-Agent) Protocol {#a2a-protocol}

The A2A protocol enables agents to discover, communicate, and collaborate with each other.

#### Protocol Specification

yaml

    # A2A Protocol v1 Specification
    version: "1.0"
    namespace: "ai.julep.a2a"
    
    message_types:
      - discovery_request
      - discovery_response
      - capability_query
      - task_request
      - task_accept
      - task_reject
      - task_update
      - task_complete
      - task_failed
      - message
      - artifact_transfer
    
    capabilities:
      - research
      - analysis
      - summarization
      - translation
      - code_generation
      - data_processing
      - planning
      - coordination

#### Agent Discovery

python

    class A2ADiscovery:
        """Agent discovery and capability matching."""
        
        async def discover_agents(
            self,
            capabilities: List[str],
            requirements: Optional[Dict[str, Any]] = None
        ) -> List[A2AAgentCard]:
            """Discover agents with specific capabilities."""
            
            # Query local registry
            local_agents = await self.query_local_registry(
                capabilities, requirements
            )
            
            # Query federated registries
            if self.federation_enabled:
                remote_agents = await self.query_federated_registries(
                    capabilities, requirements
                )
                local_agents.extend(remote_agents)
            
            # Rank by capability match
            ranked_agents = self.rank_agents(
                local_agents,
                capabilities,
                requirements
            )
            
            return ranked_agents
        
        def rank_agents(
            self,
            agents: List[A2AAgentCard],
            required_capabilities: List[str],
            requirements: Dict[str, Any]
        ) -> List[A2AAgentCard]:
            """Rank agents by suitability."""
            
            scored_agents = []
            
            for agent in agents:
                score = 0.0
                
                # Capability match score
                capability_overlap = len(
                    set(required_capabilities) & 
                    set(agent.capabilities)
                )
                score += capability_overlap / len(required_capabilities)
                
                # Performance history
                if agent.performance_metrics:
                    score += agent.performance_metrics.success_rate * 0.3
                    score += (1 - agent.performance_metrics.avg_response_time / 1000) * 0.2
                
                # Availability
                if agent.availability:
                    score += agent.availability.current_load < 0.8 ? 0.2 : 0
                
                scored_agents.append((score, agent))
            
            return [agent for _, agent in sorted(
                scored_agents, 
                key=lambda x: x[0], 
                reverse=True
            )]

#### Task Delegation

python

    class A2ATaskManager:
        """Manages task delegation between agents."""
        
        async def delegate_task(
            self,
            task: TaskDefinition,
            target_agent: str,
            timeout: Optional[int] = None
        ) -> TaskResult:
            """Delegate a task to another agent."""
            
            # 1. Create task record
            task_record = await self.create_task_record(
                task=task,
                client_agent=self.agent_id,
                remote_agent=target_agent,
                timeout=timeout
            )
            
            # 2. Send task request
            request = TaskRequest(
                task_id=task_record.id,
                task=task,
                client_agent=self.agent_id,
                deadline=datetime.utcnow() + timedelta(seconds=timeout or 3600)
            )
            
            await self.send_message(target_agent, request)
            
            # 3. Wait for acceptance
            response = await self.wait_for_response(
                task_record.id,
                timeout=30  # 30 seconds to accept/reject
            )
            
            if isinstance(response, TaskReject):
                raise TaskRejectedError(response.reason)
            
            # 4. Monitor task progress
            return await self.monitor_task(task_record.id, timeout)
        
        async def monitor_task(
            self,
            task_id: str,
            timeout: Optional[int]
        ) -> TaskResult:
            """Monitor task execution with updates."""
            
            start_time = datetime.utcnow()
            
            while True:
                # Check for updates
                update = await self.check_task_update(task_id)
                
                if update:
                    if update.status == "completed":
                        return TaskResult(
                            success=True,
                            output=update.output,
                            artifacts=update.artifacts
                        )
                    elif update.status == "failed":
                        raise TaskFailedError(update.error)
                    else:
                        # Progress update
                        await self.handle_progress_update(task_id, update)
                
                # Check timeout
                if timeout:
                    elapsed = (datetime.utcnow() - start_time).total_seconds()
                    if elapsed > timeout:
                        raise TaskTimeoutError()
                
                await asyncio.sleep(1)

#### Multi-Agent Collaboration Patterns

python

    # 1. Pipeline Pattern
    async def pipeline_collaboration(agents: List[str], initial_input: Any):
        """Agents process data in sequence."""
        
        result = initial_input
        
        for agent in agents:
            task = TaskDefinition(
                name="pipeline_step",
                input=result
            )
            
            task_result = await delegate_task(task, agent)
            result = task_result.output
        
        return result
    
    # 2. Parallel Pattern
    async def parallel_collaboration(agents: List[str], task: TaskDefinition):
        """Multiple agents work on the same task."""
        
        tasks = []
        
        for agent in agents:
            tasks.append(delegate_task(task, agent))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Aggregate results
        return aggregate_results(results)
    
    # 3. Hierarchical Pattern
    async def hierarchical_collaboration(
        coordinator: str,
        workers: List[str],
        task: TaskDefinition
    ):
        """Coordinator delegates subtasks to workers."""
        
        # Coordinator plans subtasks
        plan_task = TaskDefinition(
            name="plan_subtasks",
            input=task
        )
        
        plan = await delegate_task(plan_task, coordinator)
        
        # Execute subtasks in parallel
        subtask_results = []
        
        for subtask, worker in zip(plan.subtasks, workers):
            result = await delegate_task(subtask, worker)
            subtask_results.append(result)
        
        # Coordinator aggregates results
        aggregate_task = TaskDefinition(
            name="aggregate_results",
            input=subtask_results
        )
        
        return await delegate_task(aggregate_task, coordinator)

### Protocol Integration {#protocol-integration}

#### Unified Protocol Handler

python

    class ProtocolManager:
        """Manages both MCP and A2A protocols."""
        
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.mcp_manager = MCPManager(agent_id)
            self.a2a_agent = A2AAgent(agent_id)
            
        async def handle_tool_request(
            self,
            tool_name: str,
            input_data: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Route tool requests to appropriate handler."""
            
            # Check local MCP tools first
            if await self.mcp_manager.has_tool(tool_name):
                return await self.mcp_manager.execute_tool(
                    tool_name, input_data
                )
            
            # Check if another agent provides this tool
            agents_with_tool = await self.a2a_agent.discover_agents(
                capabilities=[f"tool:{tool_name}"]
            )
            
            if agents_with_tool:
                # Delegate to capable agent
                task = TaskDefinition(
                    name=f"execute_tool_{tool_name}",
                    input=input_data
                )
                
                result = await self.a2a_agent.delegate_task(
                    task, agents_with_tool[0].agent_id
                )
                
                return result.output
            
            raise ToolNotFoundError(f"Tool {tool_name} not available")

* * *

## 8\. Workflow System {#workflow-system}

### DBOS Integration {#dbos-integration}

DBOS (Database-Oriented Operating System) provides durable, fault-tolerant workflow execution directly in PostgreSQL.

#### Workflow Architecture

mermaid

    graph TB
        subgraph "Workflow Definition"
            DEF[Workflow Schema]
            STEPS[Step Definitions]
            RETRY[Retry Policies]
        end
        
        subgraph "DBOS Runtime"
            EXEC[Workflow Executor]
            STATE[State Management]
            QUEUE[Task Queue - pgmq]
        end
        
        subgraph "Execution"
            INST[Workflow Instance]
            STEP1[Step 1]
            STEP2[Step 2]
            STEP3[Step 3]
        end
        
        DEF --> EXEC
        EXEC --> INST
        INST --> STEP1 --> STEP2 --> STEP3
        STATE --> INST
        QUEUE --> STEP1

#### Workflow Definition

python

    from dbos import workflow, step, scheduled
    from typing import Dict, Any, List
    
    class DocumentProcessingWorkflow(DBOSWorkflow):
        """Example workflow for document processing."""
        
        @workflow(name="process_document")
        async def process_document(
            self,
            document_url: str,
            processing_options: Dict[str, Any]
        ) -> Dict[str, Any]:
            """Main workflow function."""
            
            # Initialize workflow context
            await self.initialize_context({
                "document_url": document_url,
                "options": processing_options,
                "start_time": datetime.utcnow()
            })
            
            # Step 1: Download document
            document_content = await self.download_document(document_url)
            
            # Step 2: Extract text
            extracted_text = await self.extract_text(
                document_content,
                processing_options.get("ocr_enabled", False)
            )
            
            # Step 3: Analyze content
            analysis = await self.analyze_content(
                extracted_text,
                processing_options.get("analysis_depth", "standard")
            )
            
            # Step 4: Generate summary
            summary = await self.generate_summary(
                extracted_text,
                analysis,
                processing_options.get("summary_length", 500)
            )
            
            # Step 5: Store results
            await self.store_results(analysis, summary)
            
            return {
                "summary": summary,
                "analysis": analysis,
                "processing_time": (
                    datetime.utcnow() - self.context.start_time
                ).total_seconds()
            }
        
        @step(name="download_document", retries=3)
        async def download_document(self, url: str) -> bytes:
            """Download document with retry logic."""
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30)
                response.raise_for_status()
                
                # Store in context for recovery
                await self.update_state("document_size", len(response.content))
                
                return response.content
        
        @step(name="extract_text", timeout=300)
        async def extract_text(
            self,
            content: bytes,
            ocr_enabled: bool
        ) -> str:
            """Extract text from document."""
            
            # Detect document type
            doc_type = detect_document_type(content)
            
            if doc_type == "pdf":
                text = await extract_pdf_text(content, ocr_enabled)
            elif doc_type == "docx":
                text = await extract_docx_text(content)
            elif doc_type == "html":
                text = await extract_html_text(content)
            else:
                text = content.decode("utf-8", errors="ignore")
            
            # Update progress
            await self.update_state("text_length", len(text))
            
            return text
        
        @step(name="analyze_content")
        async def analyze_content(
            self,
            text: str,
            depth: str
        ) -> Dict[str, Any]:
            """Analyze document content."""
            
            analysis = {
                "word_count": len(text.split()),
                "language": detect_language(text),
                "readability_score": calculate_readability(text)
            }
            
            if depth == "deep":
                # Additional analysis
                analysis.update({
                    "entities": await extract_entities(text),
                    "key_phrases": await extract_key_phrases(text),
                    "sentiment": await analyze_sentiment(text),
                    "topics": await extract_topics(text)
                })
            
            return analysis

#### State Management

python

    class WorkflowStateManager:
        """Manages workflow state in PostgreSQL."""
        
        async def save_checkpoint(
            self,
            workflow_id: str,
            step_name: str,
            state_data: Dict[str, Any]
        ):
            """Save workflow checkpoint for recovery."""
            
            sql = """
            INSERT INTO workflows.checkpoints (
                workflow_id, step_name, state_data, created_at
            ) VALUES (
                :workflow_id, :step_name, :state_data, NOW()
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "workflow_id": workflow_id,
                    "step_name": step_name,
                    "state_data": state_data
                }
            )
        
        async def recover_from_checkpoint(
            self,
            workflow_id: str
        ) -> Optional[Dict[str, Any]]:
            """Recover workflow from last checkpoint."""
            
            sql = """
            SELECT step_name, state_data
            FROM workflows.checkpoints
            WHERE workflow_id = :workflow_id
            ORDER BY created_at DESC
            LIMIT 1
            """
            
            result = await self.db.execute(
                sql, {"workflow_id": workflow_id}
            )
            
            checkpoint = result.fetchone()
            
            if checkpoint:
                return {
                    "step_name": checkpoint["step_name"],
                    "state": checkpoint["state_data"]
                }
            
            return None

### Built-in Workflows {#built-in-workflows}

#### Memory Consolidation Workflow

python

    @workflow(name="memory_consolidation")
    async def consolidate_memories(
        self,
        agent_id: str,
        options: ConsolidationOptions
    ) -> ConsolidationResult:
        """Consolidate agent memories for optimal performance."""
        
        # Step 1: Analyze memory distribution
        distribution = await self.analyze_memory_distribution(agent_id)
        
        # Step 2: Identify consolidation candidates
        candidates = await self.identify_candidates(
            agent_id,
            distribution,
            options.min_importance,
            options.time_window
        )
        
        # Step 3: Apply decay function
        decayed = await self.apply_decay(candidates, options.decay_rate)
        
        # Step 4: Find similar memories
        clusters = await self.cluster_similar_memories(
            decayed,
            options.similarity_threshold
        )
        
        # Step 5: Merge clusters
        merged = await self.merge_memory_clusters(clusters)
        
        # Step 6: Update relationships
        await self.update_memory_graph(agent_id, merged)
        
        # Step 7: Clean up
        removed = await self.remove_weak_memories(
            agent_id,
            options.removal_threshold
        )
        
        return ConsolidationResult(
            analyzed=len(candidates),
            merged=len(merged),
            removed=len(removed),
            duration=(datetime.utcnow() - self.start_time).total_seconds()
        )

#### Agent Training Workflow

python

    @workflow(name="agent_training")
    async def train_agent(
        self,
        agent_id: str,
        training_data: List[TrainingExample],
        parameters: TrainingParameters
    ) -> TrainingResult:
        """Train agent on specific behaviors or knowledge."""
        
        # Step 1: Validate training data
        validated_data = await self.validate_training_data(training_data)
        
        # Step 2: Create training memories
        for example in validated_data:
            # Store as semantic memory for facts
            if example.type == "fact":
                await self.store_semantic_memory(
                    agent_id,
                    example.content,
                    example.metadata
                )
            
            # Store as implicit memory for behaviors
            elif example.type == "behavior":
                await self.store_implicit_pattern(
                    agent_id,
                    example.pattern,
                    example.context
                )
        
        # Step 3: Test understanding
        test_results = await self.test_agent_learning(
            agent_id,
            validated_data,
            parameters.test_samples
        )
        
        # Step 4: Reinforce successful patterns
        await self.reinforce_patterns(
            agent_id,
            test_results.successful_patterns
        )
        
        return TrainingResult(
            examples_processed=len(validated_data),
            success_rate=test_results.success_rate,
            knowledge_gained=test_results.new_concepts
        )

### Custom Workflows {#custom-workflows}

#### Creating Custom Workflows

python

    # 1. Define workflow class
    class CustomAnalysisWorkflow(DBOSWorkflow):
        """Custom workflow for specialized analysis."""
        
        def __init__(self, name: str, agent_id: str, db_session: AsyncSession):
            super().__init__(name, agent_id, db_session)
            self.analyzer = CustomAnalyzer()
        
        @workflow(name="custom_analysis")
        async def run_analysis(
            self,
            data_source: str,
            analysis_type: str,
            parameters: Dict[str, Any]
        ) -> AnalysisResult:
            """Main workflow entry point."""
            
            # Workflow implementation
            pass
        
        @step(name="prepare_data", retries=2)
        async def prepare_data(self, source: str) -> pd.DataFrame:
            """Prepare data for analysis."""
            
            # Step implementation
            pass
    
    # 2. Register workflow
    async def register_custom_workflow():
        workflow_definition = {
            "name": "custom_analysis",
            "description": "Performs custom data analysis",
            "steps": [
                {
                    "name": "prepare_data",
                    "type": "function",
                    "retries": 2
                },
                {
                    "name": "analyze",
                    "type": "function",
                    "timeout": 600
                }
            ],
            "parameters_schema": {
                "type": "object",
                "properties": {
                    "data_source": {"type": "string"},
                    "analysis_type": {"type": "string"}
                }
            }
        }
        
        await workflow_registry.register(workflow_definition)
    
    # 3. Execute workflow
    async def execute_custom_workflow(agent_id: str):
        workflow = CustomAnalysisWorkflow(
            "custom_analysis_instance",
            agent_id,
            db_session
        )
        
        result = await workflow.run_analysis(
            data_source="s3://bucket/data.csv",
            analysis_type="statistical",
            parameters={"confidence_level": 0.95}
        )
        
        return result

#### Workflow Composition

python

    class CompositeWorkflow(DBOSWorkflow):
        """Compose multiple workflows into a larger workflow."""
        
        @workflow(name="composite_research")
        async def research_and_report(
            self,
            topic: str,
            depth: str = "comprehensive"
        ) -> ResearchReport:
            """Research a topic and generate a report."""
            
            # Sub-workflow 1: Information gathering
            raw_data = await self.run_subworkflow(
                InformationGatheringWorkflow,
                topic=topic,
                sources=["web", "academic", "news"],
                max_results=50
            )
            
            # Sub-workflow 2: Fact checking
            verified_data = await self.run_subworkflow(
                FactCheckingWorkflow,
                data=raw_data,
                verification_level=depth
            )
            
            # Sub-workflow 3: Analysis
            analysis = await self.run_subworkflow(
                AnalysisWorkflow,
                data=verified_data,
                analysis_types=["statistical", "thematic", "temporal"]
            )
            
            # Sub-workflow 4: Report generation
            report = await self.run_subworkflow(
                ReportGenerationWorkflow,
                analysis=analysis,
                format="markdown",
                sections=["executive_summary", "findings", "conclusions"]
            )
            
            return report

### Scheduled Tasks {#scheduled-tasks}

#### Scheduled Workflow Configuration

python

    # Define scheduled workflows
    @scheduled(cron="0 */6 * * *")  # Every 6 hours
    async def scheduled_memory_maintenance():
        """Perform regular memory maintenance for all agents."""
        
        agents = await get_active_agents()
        
        for agent in agents:
            try:
                workflow = MemoryMaintenanceWorkflow(
                    f"maintenance_{agent.id}",
                    agent.id,
                    get_db_session()
                )
                
                await workflow.run(
                    tasks=[
                        "consolidate_memories",
                        "update_importance_scores",
                        "clean_expired_goals",
                        "optimize_indexes"
                    ]
                )
                
            except Exception as e:
                logger.error(f"Maintenance failed for agent {agent.id}: {e}")
    
    @scheduled(cron="0 9 * * 1")  # Weekly on Monday at 9 AM
    async def weekly_agent_performance_review():
        """Generate weekly performance reports."""
        
        workflow = PerformanceReviewWorkflow(
            "weekly_review",
            "system",
            get_db_session()
        )
        
        report = await workflow.generate_weekly_report(
            metrics=[
                "conversation_quality",
                "response_time",
                "memory_utilization",
                "goal_completion_rate"
            ]
        )
        
        # Send report to administrators
        await notify_admins(report)
    
    @scheduled(interval=300)  # Every 5 minutes
    async def process_pending_tasks():
        """Process pending A2A tasks."""
        
        pending_tasks = await get_pending_tasks(limit=10)
        
        for task in pending_tasks:
            asyncio.create_task(process_single_task(task))

#### Dynamic Scheduling

python

    class DynamicScheduler:
        """Dynamically schedule workflows based on conditions."""
        
        async def schedule_workflow(
            self,
            workflow_class: Type[DBOSWorkflow],
            trigger_condition: str,
            parameters: Dict[str, Any],
            schedule_options: ScheduleOptions
        ) -> str:
            """Schedule a workflow with dynamic triggers."""
            
            schedule_id = str(uuid.uuid4())
            
            # Create schedule record
            sql = """
            INSERT INTO workflows.dynamic_schedules (
                id, workflow_name, trigger_condition,
                parameters, options, is_active
            ) VALUES (
                :id, :workflow_name, :trigger_condition,
                :parameters, :options, true
            )
            """
            
            await self.db.execute(
                sql,
                {
                    "id": schedule_id,
                    "workflow_name": workflow_class.__name__,
                    "trigger_condition": trigger_condition,
                    "parameters": parameters,
                    "options": schedule_options.dict()
                }
            )
            
            # Start monitoring for trigger
            asyncio.create_task(
                self.monitor_trigger(schedule_id, trigger_condition)
            )
            
            return schedule_id
        
        async def monitor_trigger(
            self,
            schedule_id: str,
            condition: str
        ):
            """Monitor for trigger conditions."""
            
            while True:
                if await self.evaluate_condition(condition):
                    # Trigger workflow
                    await self.execute_scheduled_workflow(schedule_id)
                    
                    # Check if one-time or recurring
                    schedule = await self.get_schedule(schedule_id)
                    if schedule.options.one_time:
                        await self.deactivate_schedule(schedule_id)
                        break
                
                await asyncio.sleep(60)  # Check every minute

* * *

## 9\. Configuration Guide {#configuration-guide}

### Environment Variables {#environment-variables}

#### Required Environment Variables

bash

    # Database Configuration
    DATABASE_URL=postgresql://user:password@localhost:5432/julep_pg
    DATABASE_POOL_SIZE=50
    DATABASE_MAX_OVERFLOW=100
    
    # API Keys (at least one required)
    OPENAI_API_KEY=sk-...
    ANTHROPIC_API_KEY=sk-ant-...
    
    # Security
    SECRET_KEY=your-secret-key-here-minimum-32-chars
    JWT_SECRET=your-jwt-secret-minimum-32-chars
    
    # Application
    ENVIRONMENT=production  # development, staging, production
    LOG_LEVEL=INFO         # DEBUG, INFO, WARNING, ERROR

#### Optional Environment Variables

bash

    # Performance Tuning
    EMBEDDING_CACHE_SIZE=10000
    QUERY_CACHE_TTL=300
    CONNECTION_POOL_RECYCLE=3600
    
    # Memory System
    MEMORY_CONSOLIDATION_INTERVAL=3600
    MEMORY_DECAY_RATE=0.95
    MEMORY_IMPORTANCE_THRESHOLD=0.3
    
    # Monitoring
    PROMETHEUS_ENABLED=true
    PROMETHEUS_PORT=9090
    GRAFANA_ENABLED=true
    
    # External Services
    HASURA_GRAPHQL_ENDPOINT=http://localhost:8080/v1/graphql
    HASURA_ADMIN_SECRET=your-hasura-secret
    REDIS_URL=redis://localhost:6379
    
    # Feature Flags
    ENABLE_A2A_FEDERATION=true
    ENABLE_MEMORY_OPTIMIZATION=true
    ENABLE_QUERY_CACHING=true

### Database Configuration {#database-configuration}

#### PostgreSQL Configuration

ini

    # postgresql.conf optimizations for Julep-PG
    
    # Memory Settings
    shared_buffers = 4GB              # 25% of RAM
    effective_cache_size = 12GB       # 75% of RAM
    work_mem = 256MB                  # For complex queries
    maintenance_work_mem = 2GB        # For VACUUM, indexes
    
    # Checkpoint Settings
    checkpoint_completion_target = 0.9
    wal_buffers = 16MB
    min_wal_size = 2GB
    max_wal_size = 8GB
    
    # Query Planner
    random_page_cost = 1.1            # For SSD storage
    effective_io_concurrency = 200    # For SSD storage
    default_statistics_target = 500    # Better query plans
    
    # Parallel Query
    max_parallel_workers_per_gather = 4
    max_parallel_workers = 8
    max_parallel_maintenance_workers = 4
    
    # Connection Settings
    max_connections = 200
    superuser_reserved_connections = 3
    
    # Logging
    log_min_duration_statement = 100  # Log slow queries
    log_checkpoints = on
    log_connections = on
    log_disconnections = on
    log_lock_waits = on
    log_temp_files = 0
    
    # Extensions
    shared_preload_libraries = 'pg_stat_statements,pgmq,vector'
    
    # Vector Extension Settings
    vector.max_vector_size = 2048
    vector.enable_parallel = on

#### Connection Pool Configuration

python

    # config/database.py
    from sqlalchemy.pool import QueuePool, NullPool
    import os
    
    def get_pool_config():
        """Get connection pool configuration based on environment."""
        
        env = os.getenv("ENVIRONMENT", "development")
        
        if env == "production":
            return {
                "poolclass": QueuePool,
                "pool_size": int(os.getenv("DATABASE_POOL_SIZE", 50)),
                "max_overflow": int(os.getenv("DATABASE_MAX_OVERFLOW", 100)),
                "pool_timeout": 30,
                "pool_recycle": 3600,
                "pool_pre_ping": True,
                "echo_pool": False
            }
        elif env == "development":
            return {
                "poolclass": QueuePool,
                "pool_size": 5,
                "max_overflow": 10,
                "pool_timeout": 30,
                "pool_recycle": 1800,
                "pool_pre_ping": True,
                "echo_pool": True
            }
        else:  # serverless
            return {
                "poolclass": NullPool,
                "pool_pre_ping": True
            }

### Extension Configuration {#extension-configuration}

#### pgvector Configuration

sql

    -- Configure pgvector indexes
    CREATE INDEX CONCURRENTLY memories_embedding_hnsw 
    ON memory.memories 
    USING hnsw (embedding vector_cosine_ops)
    WITH (
        m = 16,                    -- Number of connections
        ef_construction = 64,      -- Size of dynamic candidate list
        ef = 40                    -- Size of the search candidate list
    );
    
    -- Optimize for different query patterns
    CREATE INDEX CONCURRENTLY memories_embedding_ivfflat
    ON memory.memories 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 1000)           -- Number of inverted lists
    WHERE importance > 0.5;        -- Partial index for important memories

#### pgmq Configuration

sql

    -- Create queues with specific configurations
    SELECT pgmq.create_queue(
        queue_name := 'high_priority_tasks',
        max_age := 3600,           -- Messages expire after 1 hour
        fill_factor := 90,         -- Table fill factor
        autovacuum_enabled := true
    );
    
    SELECT pgmq.create_queue(
        queue_name := 'memory_consolidation',
        max_age := 86400,          -- Messages expire after 24 hours
        partition_size := 10000    -- Partition after 10k messages
    );
    
    -- Set queue policies
    SELECT pgmq.set_queue_policy(
        'high_priority_tasks',
        max_retries := 3,
        retry_delay := 60,         -- Retry after 60 seconds
        dead_letter_queue := 'failed_tasks'
    );

#### pgai Configuration

python

    # config/ai_models.py
    AI_MODEL_CONFIG = {
        "openai": {
            "default_model": "gpt-4",
            "embedding_model": "text-embedding-3-small",
            "temperature": 0.7,
            "max_tokens": 4096,
            "timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 1
        },
        "anthropic": {
            "default_model": "claude-3-sonnet",
            "temperature": 0.7,
            "max_tokens": 4096,
            "timeout": 30
        },
        "local": {
            "enabled": False,
            "model_path": "/models/llama2-7b",
            "device": "cuda",
            "quantization": "int8"
        }
    }
    
    # Rate limiting per model
    RATE_LIMITS = {
        "gpt-4": {
            "requests_per_minute": 500,
            "tokens_per_minute": 40000
        },
        "gpt-3.5-turbo": {
            "requests_per_minute": 3500,
            "tokens_per_minute": 90000
        }
    }

### Performance Tuning {#performance-tuning}

#### Query Optimization Settings

python

    # config/performance.py
    PERFORMANCE_CONFIG = {
        "query_optimization": {
            "enable_parallel_queries": True,
            "parallel_workers": 4,
            "enable_jit": True,
            "statement_timeout": 30000,  # 30 seconds
            "lock_timeout": 10000        # 10 seconds
        },
        
        "caching": {
            "query_cache_enabled": True,
            "query_cache_size": "1GB",
            "query_cache_ttl": 300,
            "embedding_cache_size": 10000,
            "embedding_cache_ttl": 3600
        },
        
        "memory_management": {
            "consolidation_batch_size": 100,
            "consolidation_parallel_jobs": 4,
            "importance_update_interval": 3600,
            "decay_calculation_interval": 86400
        },
        
        "indexing": {
            "autovacuum_scale_factor": 0.1,
            "autovacuum_analyze_scale_factor": 0.05,
            "maintenance_work_mem": "2GB",
            "max_parallel_maintenance_workers": 4
        }
    }

#### Memory System Tuning

yaml

    # config/memory_tuning.yaml
    memory_system:
      episodic:
        max_memories_per_agent: 10000
        consolidation_threshold: 0.85
        clustering_algorithm: "dbscan"
        clustering_params:
          eps: 0.15
          min_samples: 2
        
      semantic:
        max_concepts_per_agent: 5000
        concept_embedding_model: "text-embedding-3-small"
        relationship_strength_threshold: 0.3
        inference_rules:
          - transitive_closure
          - concept_similarity
          - hierarchical_inheritance
        
      implicit:
        pattern_detection_window: 30  # days
        min_pattern_frequency: 5
        confidence_threshold: 0.7
        
      prospective:
        max_active_goals: 100
        reminder_advance_time: 86400  # 24 hours
        goal_review_interval: 604800  # 1 week

#### Application Performance

python

    # config/app_performance.py
    import os
    from typing import Dict, Any
    
    class PerformanceOptimizer:
        """Dynamic performance optimization based on load."""
        
        @staticmethod
        def get_optimized_settings() -> Dict[str, Any]:
            cpu_count = os.cpu_count() or 4
            
            return {
                # Uvicorn settings
                "workers": min(cpu_count * 2, 8),
                "worker_connections": 1000,
                "keepalive": 5,
                "limit_concurrency": 1000,
                
                # Async settings
                "asyncio_loop": "uvloop",
                "max_concurrent_requests": 500,
                "request_timeout": 30,
                
                # Database settings
                "db_connection_pool": {
                    "size": cpu_count * 10,
                    "max_overflow": cpu_count * 20,
                    "timeout": 30,
                    "recycle": 3600
                },
                
                # Cache settings
                "cache_backend": "redis" if cpu_count > 4 else "memory",
                "cache_size": "2GB" if cpu_count > 4 else "512MB"
            }

* * *

## 10\. Operations Guide {#operations-guide}

### Deployment {#deployment}

#### Production Deployment Checklist

markdown

    # Pre-Deployment Checklist
    
    ## Infrastructure
    - [ ] PostgreSQL 15+ installed with required extensions
    - [ ] Minimum 16GB RAM for production
    - [ ] SSD storage with >100GB free space
    - [ ] Network connectivity verified
    - [ ] SSL certificates configured
    
    ## Database Setup
    - [ ] Extensions installed: pgvector, pgmq, pg_jsonschema
    - [ ] Initial schema deployed
    - [ ] Indexes created and analyzed
    - [ ] Backup strategy configured
    - [ ] Monitoring queries enabled
    
    ## Application
    - [ ] Environment variables configured
    - [ ] API keys validated
    - [ ] Connection pools sized appropriately
    - [ ] Health checks passing
    - [ ] Logging configured
    
    ## Security
    - [ ] Database credentials rotated
    - [ ] API keys secured in vault
    - [ ] Network policies configured
    - [ ] Rate limiting enabled
    - [ ] Audit logging active
    
    ## Monitoring
    - [ ] Prometheus exporters running
    - [ ] Grafana dashboards imported
    - [ ] Alerts configured
    - [ ] Log aggregation working

#### Docker Deployment

yaml

    # docker-compose.production.yml
    version: '3.8'
    
    services:
      postgres:
        image: pgvector/pgvector:pg15
        restart: unless-stopped
        environment:
          POSTGRES_PASSWORD_FILE: /run/secrets/db_password
          POSTGRES_DB: julep_pg
        secrets:
          - db_password
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
        deploy:
          resources:
            limits:
              cpus: '4'
              memory: 8G
            reservations:
              cpus: '2'
              memory: 4G
        healthcheck:
          test: ["CMD", "pg_isready", "-U", "postgres"]
          interval: 10s
          timeout: 5s
          retries: 5
    
      app:
        image: julep-pg:latest
        restart: unless-stopped
        environment:
          DATABASE_URL_FILE: /run/secrets/database_url
          OPENAI_API_KEY_FILE: /run/secrets/openai_key
          SECRET_KEY_FILE: /run/secrets/secret_key
        secrets:
          - database_url
          - openai_key
          - secret_key
        depends_on:
          postgres:
            condition: service_healthy
        deploy:
          replicas: 3
          update_config:
            parallelism: 1
            delay: 10s
            failure_action: rollback
          restart_policy:
            condition: on-failure
            delay: 5s
            max_attempts: 3
    
      nginx:
        image: nginx:alpine
        restart: unless-stopped
        ports:
          - "80:80"
          - "443:443"
        volumes:
          - ./nginx.conf:/etc/nginx/nginx.conf:ro
          - ./ssl:/etc/nginx/ssl:ro
        depends_on:
          - app
    
    secrets:
      db_password:
        external: true
      database_url:
        external: true
      openai_key:
        external: true
      secret_key:
        external: true
    
    volumes:
      postgres_data:
        driver: local

#### Kubernetes Deployment

yaml

    # k8s/julep-pg-deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: julep-pg
      namespace: julep
    spec:
      replicas: 3
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 0
      selector:
        matchLabels:
          app: julep-pg
      template:
        metadata:
          labels:
            app: julep-pg
        spec:
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 100
                podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: app
                      operator: In
                      values:
                      - julep-pg
                  topologyKey: kubernetes.io/hostname
          
          containers:
          - name: app
            image: julep-pg:latest
            ports:
            - containerPort: 8000
              name: http
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
            
            resources:
              requests:
                cpu: 500m
                memory: 1Gi
              limits:
                cpu: 2000m
                memory: 4Gi
            
            livenessProbe:
              httpGet:
                path: /api/v1/health/live
                port: 8000
              initialDelaySeconds: 30
              periodSeconds: 10
              timeoutSeconds: 5
              failureThreshold: 3
            
            readinessProbe:
              httpGet:
                path: /api/v1/health/ready
                port: 8000
              initialDelaySeconds: 10
              periodSeconds: 5
              timeoutSeconds: 3
              failureThreshold: 3
            
            startupProbe:
              httpGet:
                path: /api/v1/health/ready
                port: 8000
              initialDelaySeconds: 0
              periodSeconds: 10
              timeoutSeconds: 3
              failureThreshold: 30

### Monitoring {#monitoring}

#### Metrics Collection

python

    # monitoring/metrics.py
    from prometheus_client import Counter, Histogram, Gauge, Info
    import time
    from functools import wraps
    
    # Define metrics
    request_count = Counter(
        'julep_http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status']
    )
    
    request_duration = Histogram(
        'julep_http_request_duration_seconds',
        'HTTP request duration',
        ['method', 'endpoint']
    )
    
    active_agents = Gauge(
        'julep_active_agents',
        'Number of active agents'
    )
    
    memory_count = Gauge(
        'julep_memory_count',
        'Number of memories by type',
        ['agent_id', 'memory_type']
    )
    
    db_connections = Gauge(
        'julep_db_connections_active',
        'Active database connections'
    )
    
    llm_tokens_used = Counter(
        'julep_llm_tokens_total',
        'Total LLM tokens used',
        ['model', 'operation']
    )
    
    workflow_duration = Histogram(
        'julep_workflow_duration_seconds',
        'Workflow execution duration',
        ['workflow_name', 'status']
    )
    
    # Decorator for timing functions
    def track_time(metric: Histogram):
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start
                    metric.observe(duration)
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start
                    metric.observe(duration)
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

#### Grafana Dashboard Configuration

json

    {
      "dashboard": {
        "title": "Julep-PG Monitoring",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(julep_http_requests_total[5m])",
                "legendFormat": "{{method}} {{endpoint}}"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Response Time (95th percentile)",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(julep_http_request_duration_seconds_bucket[5m]))",
                "legendFormat": "{{endpoint}}"
              }
            ],
            "type": "graph"
          },
          {
            "title": "Active Agents",
            "targets": [
              {
                "expr": "julep_active_agents"
              }
            ],
            "type": "stat"
          },
          {
            "title": "Memory Distribution",
            "targets": [
              {
                "expr": "sum by (memory_type) (julep_memory_count)",
                "legendFormat": "{{memory_type}}"
              }
            ],
            "type": "piechart"
          },
          {
            "title": "Database Connections",
            "targets": [
              {
                "expr": "julep_db_connections_active"
              }
            ],
            "type": "gauge",
            "options": {
              "max": 200
            }
          },
          {
            "title": "LLM Token Usage",
            "targets": [
              {
                "expr": "rate(julep_llm_tokens_total[1h])",
                "legendFormat": "{{model}}"
              }
            ],
            "type": "graph"
          }
        ]
      }
    }

#### Health Checks

python

    # monitoring/health.py
    from typing import Dict, Any
    import asyncio
    from datetime import datetime
    
    class HealthChecker:
        """Comprehensive health checking system."""
        
        async def check_all(self) -> Dict[str, Any]:
            """Run all health checks."""
            
            checks = await asyncio.gather(
                self.check_database(),
                self.check_extensions(),
                self.check_message_queues(),
                self.check_llm_apis(),
                self.check_memory_system(),
                return_exceptions=True
            )
            
            results = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": "healthy",
                "checks": {}
            }
            
            check_names = [
                "database", "extensions", "message_queues",
                "llm_apis", "memory_system"
            ]
            
            for name, result in zip(check_names, checks):
                if isinstance(result, Exception):
                    results["checks"][name] = {
                        "status": "unhealthy",
                        "error": str(result)
                    }
                    results["status"] = "unhealthy"
                else:
                    results["checks"][name] = result
                    if result["status"] != "healthy":
                        results["status"] = "degraded"
            
            return results
        
        async def check_database(self) -> Dict[str, Any]:
            """Check database connectivity and performance."""
            
            try:
                start = time.time()
                
                # Test basic connectivity
                result = await db.execute("SELECT 1")
                
                # Check connection pool
                pool_stats = db.pool.status()
                
                # Check replication lag if applicable
                lag_result = await db.execute("""
                    SELECT EXTRACT(EPOCH FROM (NOW() - pg_last_xact_replay_timestamp()))
                    AS replication_lag
                """)
                
                lag = lag_result.scalar() or 0
                
                return {
                    "status": "healthy" if lag < 10 else "degraded",
                    "latency_ms": (time.time() - start) * 1000,
                    "pool_size": pool_stats.size,
                    "pool_available": pool_stats.available,
                    "replication_lag_seconds": lag
                }
                
            except Exception as e:
                return {
                    "status": "unhealthy",
                    "error": str(e)
                }

### Backup & Recovery {#backup-recovery}

#### Backup Strategy

bash

    #!/bin/bash
    # backup/backup.sh
    
    # Configuration
    BACKUP_DIR="/backups/julep-pg"
    RETENTION_DAYS=30
    S3_BUCKET="s3://backups/julep-pg"
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR/$(date +%Y%m%d)"
    
    # Backup database with custom format for parallelism
    pg_dump \
      -h localhost \
      -U postgres \
      -d julep_pg \
      -Fc \
      -j 4 \
      -f "$BACKUP_DIR/$(date +%Y%m%d)/julep_pg_$(date +%H%M%S).dump"
    
    # Backup vector indexes separately (they can be large)
    psql -U postgres -d julep_pg -c "
    SELECT pg_dump_vector_indexes('$BACKUP_DIR/$(date +%Y%m%d)/vector_indexes.sql')
    "
    
    # Backup application configuration
    tar -czf "$BACKUP_DIR/$(date +%Y%m%d)/config_$(date +%H%M%S).tar.gz" \
      /app/config \
      /app/.env
    
    # Upload to S3
    aws s3 sync "$BACKUP_DIR/$(date +%Y%m%d)" "$S3_BUCKET/$(date +%Y%m%d)"
    
    # Clean old backups
    find "$BACKUP_DIR" -type d -mtime +$RETENTION_DAYS -exec rm -rf {} \;
    
    # Verify backup
    pg_restore --list "$BACKUP_DIR/$(date +%Y%m%d)/julep_pg_*.dump" > /dev/null
    if [ $? -eq 0 ]; then
        echo "Backup successful"
        # Send success notification
    else
        echo "Backup verification failed"
        # Send alert
        exit 1
    fi

#### Recovery Procedures

bash

    #!/bin/bash
    # backup/restore.sh
    
    # Point-in-time recovery
    restore_to_timestamp() {
        local TIMESTAMP=$1
        local BACKUP_FILE=$2
        
        # Stop application
        systemctl stop julep-pg
        
        # Restore base backup
        pg_restore \
            -h localhost \
            -U postgres \
            -d julep_pg_restore \
            -j 4 \
            --clean \
            --if-exists \
            "$BACKUP_FILE"
        
        # Apply WAL logs to timestamp
        psql -U postgres -c "
        SELECT pg_create_restore_point('before_restore');
        SELECT pg_switch_wal();
        "
        
        # Restore to specific time
        recovery_conf="
        restore_command = 'cp /archive/%f %p'
        recovery_target_time = '$TIMESTAMP'
        recovery_target_action = 'promote'
        "
        
        echo "$recovery_conf" > /var/lib/postgresql/data/recovery.conf
        
        # Start PostgreSQL in recovery mode
        pg_ctl start -D /var/lib/postgresql/data
        
        # Wait for recovery
        while ! pg_isready; do
            sleep 1
        done
        
        # Verify recovery
        psql -U postgres -d julep_pg_restore -c "
        SELECT COUNT(*) FROM agents.agents;
        SELECT COUNT(*) FROM memory.memories;
        "
        
        # Swap databases
        psql -U postgres <<EOF
        ALTER DATABASE julep_pg RENAME TO julep_pg_old;
        ALTER DATABASE julep_pg_restore RENAME TO julep_pg;
    EOF
        
        # Rebuild vector indexes
        psql -U postgres -d julep_pg -f /backups/vector_indexes.sql
        
        # Start application
        systemctl start julep-pg
    }

#### Disaster Recovery Plan

markdown

    # Disaster Recovery Runbook
    
    ## Scenario 1: Database Corruption
    1. Stop all application instances
    2. Identify last known good backup
    3. Restore from backup using `restore.sh`
    4. Replay WAL logs to minimize data loss
    5. Verify data integrity
    6. Rebuild indexes if necessary
    7. Start application instances
    8. Run verification tests
    
    ## Scenario 2: Complete System Failure
    1. Provision new infrastructure
    2. Install PostgreSQL and extensions
    3. Restore latest backup from S3
    4. Configure replication if applicable
    5. Deploy application
    6. Update DNS/load balancer
    7. Verify functionality
    
    ## Scenario 3: Data Loss Prevention
    1. Enable continuous archiving:
       ```sql
       ALTER SYSTEM SET archive_mode = on;
       ALTER SYSTEM SET archive_command = 'cp %p /archive/%f';

2.  Set up streaming replication:
    
    sql
    
        -- On primary
        CREATE ROLE replicator REPLICATION LOGIN PASSWORD 'secure_password';
        
        -- On replica
        pg_basebackup -h primary_host -D /var/lib/postgresql/data -U replicator -Fp -Xs -P
    
3.  Configure automated failover with Patroni or repmgr

## Recovery Time Objectives

-   Database restoration: < 30 minutes
-   Application deployment: < 15 minutes
-   Full system recovery: < 1 hour
-   Data loss: < 5 minutes (with WAL archiving)

    
    ### Scaling {#scaling}
    
    #### Horizontal Scaling Strategies
    
    ```python
    # scaling/horizontal.py
    from typing import List, Dict, Any
    import hashlib
    
    class ShardManager:
        """Manage horizontal sharding for large deployments."""
        
        def __init__(self, shard_configs: List[Dict[str, Any]]):
            self.shards = shard_configs
            self.shard_count = len(shard_configs)
        
        def get_shard(self, agent_id: str) -> Dict[str, Any]:
            """Determine which shard an agent belongs to."""
            
            # Consistent hashing
            hash_value = int(hashlib.md5(agent_id.encode()).hexdigest(), 16)
            shard_index = hash_value % self.shard_count
            
            return self.shards[shard_index]
        
        async def migrate_agent(
            self,
            agent_id: str,
            from_shard: int,
            to_shard: int
        ):
            """Migrate agent between shards."""
            
            # 1. Start transaction on both shards
            from_conn = self.shards[from_shard]["connection"]
            to_conn = self.shards[to_shard]["connection"]
            
            async with from_conn.transaction():
                async with to_conn.transaction():
                    # 2. Copy agent data
                    agent_data = await from_conn.fetch("""
                        SELECT * FROM agents.agents WHERE id = $1
                    """, agent_id)
                    
                    await to_conn.execute("""
                        INSERT INTO agents.agents 
                        SELECT * FROM unnest($1::agents.agents[])
                    """, agent_data)
                    
                    # 3. Copy memories
                    memories = await from_conn.fetch("""
                        SELECT * FROM memory.memories WHERE agent_id = $1
                    """, agent_id)
                    
                    await to_conn.execute("""
                        INSERT INTO memory.memories 
                        SELECT * FROM unnest($1::memory.memories[])
                    """, memories)
                    
                    # 4. Copy sessions and messages
                    # ... similar pattern
                    
                    # 5. Delete from source
                    await from_conn.execute("""
                        DELETE FROM agents.agents WHERE id = $1
                    """, agent_id)

#### Vertical Scaling Guidelines

yaml

    # scaling/vertical_scaling.yaml
    
    scaling_tiers:
      small:
        description: "Development and small deployments"
        agents: 100
        memory_size: 100000
        specifications:
          cpu: 4
          ram: 16GB
          storage: 500GB SSD
          postgres:
            shared_buffers: 4GB
            effective_cache_size: 12GB
            max_connections: 100
      
      medium:
        description: "Standard production deployment"
        agents: 1000
        memory_size: 10000000
        specifications:
          cpu: 16
          ram: 64GB
          storage: 2TB NVMe
          postgres:
            shared_buffers: 16GB
            effective_cache_size: 48GB
            max_connections: 500
      
      large:
        description: "High-traffic production"
        agents: 10000
        memory_size: 100000000
        specifications:
          cpu: 32
          ram: 256GB
          storage: 10TB NVMe RAID
          postgres:
            shared_buffers: 64GB
            effective_cache_size: 192GB
            max_connections: 1000
      
      xlarge:
        description: "Enterprise deployment"
        agents: 100000
        memory_size: 1000000000
        specifications:
          cpu: 64
          ram: 512GB
          storage: 50TB NVMe RAID
          postgres:
            shared_buffers: 128GB
            effective_cache_size: 384GB
            max_connections: 2000

#### Read Replica Configuration

sql

    -- Configure read replicas for scaling read operations
    -- On primary
    CREATE PUBLICATION julep_replica FOR ALL TABLES;
    
    -- On replica
    CREATE SUBSCRIPTION julep_replica
    CONNECTION 'host=primary dbname=julep_pg user=replicator'
    PUBLICATION julep_replica;
    
    -- Route read queries to replicas
    -- In application configuration
    READ_REPLICA_URLS = [
        "postgresql://replica1.example.com/julep_pg",
        "postgresql://replica2.example.com/julep_pg",
        "postgresql://replica3.example.com/julep_pg"
    ]
    
    -- Load balancing for read queries
    class ReadReplicaRouter:
        def __init__(self, replicas: List[str]):
            self.replicas = replicas
            self.current = 0
        
        def get_connection(self) -> str:
            """Round-robin load balancing."""
            conn = self.replicas[self.current]
            self.current = (self.current + 1) % len(self.replicas)
            return conn

* * *

## 11\. Development Guide {#development-guide}

### Setting Up Development {#development-setup}

#### Development Environment Setup

bash

    # 1. Clone repository
    git clone https://github.com/julep-ai/julep-pg.git
    cd julep-pg
    
    # 2. Create Python virtual environment
    python3.11 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    
    # 3. Install development dependencies
    pip install -e ".[dev]"
    
    # 4. Install pre-commit hooks
    pre-commit install
    
    # 5. Set up development database
    docker-compose -f docker-compose.dev.yml up -d
    
    # 6. Run database migrations
    alembic upgrade head
    
    # 7. Seed development data
    python scripts/seed_dev_data.py
    
    # 8. Start development server
    uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

#### Development Tools Configuration

yaml

    # .pre-commit-config.yaml
    repos:
      - repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v4.4.0
        hooks:
          - id: trailing-whitespace
          - id: end-of-file-fixer
          - id: check-yaml
          - id: check-added-large-files
    
      - repo: https://github.com/psf/black
        rev: 23.12.1
        hooks:
          - id: black
            language_version: python3.11
    
      - repo: https://github.com/pycqa/isort
        rev: 5.13.2
        hooks:
          - id: isort
            args: ["--profile", "black"]
    
      - repo: https://github.com/pycqa/flake8
        rev: 7.0.0
        hooks:
          - id: flake8
            args: ["--max-line-length=88", "--extend-ignore=E203"]
    
      - repo: https://github.com/pre-commit/mirrors-mypy
        rev: v1.8.0
        hooks:
          - id: mypy
            additional_dependencies: [types-all]

### Code Structure {#code-structure}

#### Project Organization

    julep-pg/
    ├── src/
    │   ├── api/                    # FastAPI application
    │   │   ├── __init__.py
    │   │   ├── main.py            # Application entry point
    │   │   ├── dependencies.py    # Dependency injection
    │   │   ├── middleware/        # Custom middleware
    │   │   ├── routers/           # API endpoints
    │   │   └── schemas/           # Pydantic models
    │   │
    │   ├── agents/                # Agent management
    │   │   ├── __init__.py
    │   │   ├── models.py         # SQLAlchemy models
    │   │   ├── crud.py           # CRUD operations
    │   │   ├── llm.py            # LLM integrations
    │   │   └── sessions.py       # Session management
    │   │
    │   ├── memory/                # Memory system
    │   │   ├── __init__.py
    │   │   ├── base.py           # Base memory classes
    │   │   ├── episodic.py       # Episodic memory
    │   │   ├── semantic.py       # Semantic memory
    │   │   ├── implicit.py       # Implicit memory
    │   │   ├── prospective.py    # Prospective memory
    │   │   └── consolidation.py  # Consolidation logic
    │   │
    │   ├── protocols/             # Protocol implementations
    │   │   ├── __init__.py
    │   │   ├── mcp/              # Model Context Protocol
    │   │   │   ├── server.py
    │   │   │   ├── client.py
    │   │   │   └── registry.py
    │   │   └── a2a/              # Agent-to-Agent
    │   │       ├── agent.py
    │   │       ├── discovery.py
    │   │       └── tasks.py
    │   │
    │   ├── workflows/             # DBOS workflows
    │   │   ├── __init__.py
    │   │   ├── base.py           # Base workflow class
    │   │   ├── memory_consolidation.py
    │   │   ├── agent_conversation.py
    │   │   └── scheduled.py
    │   │
    │   ├── database/              # Database utilities
    │   │   ├── __init__.py
    │   │   ├── connection.py     # Connection management
    │   │   ├── migrations/       # Alembic migrations
    │   │   └── functions/        # SQL functions
    │   │
    │   └── utils/                 # Utility modules
    │       ├── __init__.py
    │       ├── embeddings.py     # Embedding generation
    │       ├── logging.py        # Logging configuration
    │       ├── monitoring.py     # Metrics collection
    │       └── validation.py     # Input validation
    │
    ├── tests/                     # Test suite
    │   ├── __init__.py
    │   ├── conftest.py           # Pytest configuration
    │   ├── unit/                 # Unit tests
    │   ├── integration/          # Integration tests
    │   └── e2e/                  # End-to-end tests
    │
    ├── scripts/                   # Utility scripts
    │   ├── setup_database.py
    │   ├── seed_dev_data.py
    │   └── performance_test.py
    │
    ├── schemas/                   # Database schemas
    │   ├── typespec/             # TypeSpec definitions
    │   └── sql/                  # SQL schemas
    │
    ├── config/                    # Configuration files
    │   ├── default.yaml
    │   ├── development.yaml
    │   └── production.yaml
    │
    ├── docker/                    # Docker configurations
    │   ├── app/
    │   ├── postgres/
    │   └── nginx/
    │
    ├── docs/                      # Documentation
    │   ├── api/                  # API documentation
    │   ├── architecture/         # Architecture

Claude does not have internet access enabled. Enable web search for up to date and accurate links.

I

Continue

Mapped out remaining documentation sections to complete.

4s

The user wants me to continue the documentation from where it left off. Looking at the last section, I was in the middle of the Development Guide section, specifically showing the project structure. I need to continue from there and complete the remaining sections of the documentation.

Looking at the table of contents, I still need to complete:

-   The rest of Development Guide (Code Structure, Testing, Contributing)
-   Troubleshooting (Common Issues, Performance Issues, Debugging Tools)
-   Examples & Tutorials
-   Migration Guide
-   Reference (Glossary, FAQ, Resources)

Let me continue from where I left off in the Code Structure section.

    │   ├── guides/               # User guides
    │   └── diagrams/             # Architecture diagrams
    │
    ├── .env.example              # Environment variables template
    ├── .gitignore               # Git ignore rules
    ├── docker-compose.yml       # Development compose
    ├── docker-compose.prod.yml  # Production compose
    ├── pyproject.toml           # Python project configuration
    ├── requirements.txt         # Python dependencies
    ├── requirements-dev.txt     # Development dependencies
    ├── Makefile                 # Build automation
    └── README.md               # Project documentation

#### Code Style Guidelines

python

    # src/style_guide.py
    """
    Julep-PG Code Style Guidelines
    
    1. Use type hints for all functions
    2. Docstrings for all public functions/classes
    3. Async-first design
    4. Dependency injection over globals
    5. Explicit error handling
    """
    
    from typing import Optional, List, Dict, Any
    from datetime import datetime
    import asyncio
    
    # GOOD: Type hints and docstring
    async def process_message(
        agent_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a message from a user.
        
        Args:
            agent_id: The ID of the agent processing the message
            message: The user's message content
            context: Optional context for the conversation
            
        Returns:
            Dict containing the response and metadata
            
        Raises:
            AgentNotFoundError: If the agent doesn't exist
            ProcessingError: If message processing fails
        """
        # Implementation...
        pass
    
    # BAD: No type hints, no docstring
    def process_message(agent_id, message, context=None):
        # Implementation...
        pass
    
    # GOOD: Dependency injection
    class MemoryManager:
        def __init__(self, db_session: AsyncSession, cache: Cache):
            self.db = db_session
            self.cache = cache
    
    # BAD: Global dependencies
    db = get_database()
    cache = get_cache()
    
    class MemoryManager:
        def __init__(self):
            # Uses globals
            pass
    
    # GOOD: Explicit error handling
    async def get_agent(agent_id: str) -> Agent:
        try:
            agent = await db.get_agent(agent_id)
            if not agent:
                raise AgentNotFoundError(f"Agent {agent_id} not found")
            return agent
        except DatabaseError as e:
            logger.error(f"Database error retrieving agent: {e}")
            raise ServiceUnavailableError("Unable to retrieve agent")
    
    # GOOD: Structured logging
    import structlog
    logger = structlog.get_logger()
    
    async def process_request(request_id: str):
        logger.info(
            "processing_request",
            request_id=request_id,
            timestamp=datetime.utcnow()
        )

### Testing {#testing}

#### Test Structure

python

    # tests/conftest.py
    import pytest
    import asyncio
    from typing import AsyncGenerator
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from testcontainers.postgres import PostgresContainer
    
    @pytest.fixture(scope="session")
    def event_loop():
        """Create an instance of the default event loop for the test session."""
        loop = asyncio.get_event_loop_policy().new_event_loop()
        yield loop
        loop.close()
    
    @pytest.fixture(scope="session")
    async def postgres_container():
        """Start PostgreSQL container for testing."""
        with PostgresContainer(image="pgvector/pgvector:pg15") as postgres:
            yield postgres
    
    @pytest.fixture(scope="function")
    async def db_session(postgres_container) -> AsyncGenerator[AsyncSession, None]:
        """Provide a transactional database session for tests."""
        # Create engine
        engine = create_async_engine(
            postgres_container.get_connection_url(),
            echo=True
        )
        
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create session
        async with AsyncSession(engine) as session:
            async with session.begin():
                yield session
                # Rollback transaction after test
                await session.rollback()
        
        # Cleanup
        await engine.dispose()
    
    @pytest.fixture
    async def test_agent(db_session: AsyncSession) -> Agent:
        """Create a test agent."""
        agent = Agent(
            name="Test Agent",
            type="conversational",
            model="gpt-4",
            system_prompt="You are a test agent."
        )
        db_session.add(agent)
        await db_session.commit()
        return agent
    
    @pytest.fixture
    def mock_llm(monkeypatch):
        """Mock LLM calls for testing."""
        async def mock_completion(*args, **kwargs):
            return {
                "content": "Mocked response",
                "tokens_used": 10
            }
        
        monkeypatch.setattr(
            "src.agents.llm.generate_completion",
            mock_completion
        )

#### Unit Tests

python

    # tests/unit/test_memory_managers.py
    import pytest
    from datetime import datetime, timedelta
    from src.memory.episodic import EpisodicMemoryManager
    from src.memory.semantic import SemanticMemoryManager
    
    class TestEpisodicMemoryManager:
        """Test episodic memory operations."""
        
        async def test_store_episode(self, db_session, test_agent):
            """Test storing an episodic memory."""
            manager = EpisodicMemoryManager(db_session)
            
            memory = await manager.store_episode(
                agent_id=str(test_agent.id),
                content="Had a conversation about AI ethics",
                context={"topic": "ethics", "user_mood": "curious"},
                emotional_valence=0.3
            )
            
            assert memory.id is not None
            assert memory.type == "episodic"
            assert memory.emotional_valence == 0.3
            assert memory.importance > 0
            assert "topic" in memory.source_context
        
        async def test_retrieve_by_emotion(self, db_session, test_agent):
            """Test retrieving memories by emotional valence."""
            manager = EpisodicMemoryManager(db_session)
            
            # Store memories with different emotions
            memories = [
                ("Happy moment", 0.8),
                ("Sad event", -0.6),
                ("Neutral observation", 0.0),
                ("Exciting discovery", 0.9)
            ]
            
            for content, valence in memories:
                await manager.store_episode(
                    agent_id=str(test_agent.id),
                    content=content,
                    context={},
                    emotional_valence=valence
                )
            
            # Retrieve positive memories
            positive_memories = await manager.retrieve_episodes(
                agent_id=str(test_agent.id),
                query="memories",
                emotional_filter="positive"
            )
            
            assert len(positive_memories) == 2
            assert all(m.emotional_valence > 0 for m in positive_memories)
        
        async def test_temporal_sequence(self, db_session, test_agent):
            """Test retrieving temporal sequences."""
            manager = EpisodicMemoryManager(db_session)
            
            # Create a sequence of events
            base_time = datetime.utcnow()
            
            for i in range(5):
                await manager.store_episode(
                    agent_id=str(test_agent.id),
                    content=f"Event {i} in sequence",
                    context={"sequence_id": "test", "order": i}
                )
                # Small delay to ensure ordering
                await asyncio.sleep(0.1)
            
            # Retrieve sequence
            sequence = await manager.get_temporal_sequence(
                agent_id=str(test_agent.id),
                start_time=base_time,
                end_time=datetime.utcnow()
            )
            
            assert len(sequence) == 5
            # Verify temporal ordering
            for i in range(len(sequence) - 1):
                assert sequence[i].created_at < sequence[i + 1].created_at
    
    class TestSemanticMemoryManager:
        """Test semantic memory operations."""
        
        async def test_store_fact(self, db_session, test_agent):
            """Test storing semantic facts."""
            manager = SemanticMemoryManager(db_session)
            
            fact = await manager.store_fact(
                agent_id=str(test_agent.id),
                content="Python is a programming language",
                concepts=["Python", "programming language"],
                confidence=1.0
            )
            
            assert fact.type == "semantic"
            assert fact.confidence == 1.0
            assert "Python" in fact.concepts
            assert len(fact.relationships) > 0
        
        async def test_knowledge_inference(self, db_session, test_agent):
            """Test knowledge inference from facts."""
            manager = SemanticMemoryManager(db_session)
            
            # Store related facts
            await manager.store_fact(
                str(test_agent.id),
                "Python is a programming language",
                ["Python", "programming language"]
            )
            
            await manager.store_fact(
                str(test_agent.id),
                "Programming languages are used to write software",
                ["programming language", "software"]
            )
            
            await manager.store_fact(
                str(test_agent.id),
                "Django is a Python framework",
                ["Django", "Python", "framework"]
            )
            
            # Test inference
            inferences = await manager.infer_new_facts(
                str(test_agent.id),
                max_inferences=5
            )
            
            # Should infer that Python is used to write software
            assert any(
                "Python" in inf["content"] and "software" in inf["content"]
                for inf in inferences
            )
        
        @pytest.mark.parametrize("query,expected_concepts", [
            ("What is Python?", ["Python"]),
            ("programming languages", ["programming language"]),
            ("web frameworks", ["framework", "web"])
        ])
        async def test_knowledge_query(
            self, db_session, test_agent, query, expected_concepts
        ):
            """Test querying knowledge base."""
            manager = SemanticMemoryManager(db_session)
            
            # Store test knowledge
            facts = [
                ("Python is a high-level programming language", 
                 ["Python", "programming language", "high-level"]),
                ("Django is a web framework for Python",
                 ["Django", "web", "framework", "Python"]),
                ("Flask is another Python web framework",
                 ["Flask", "Python", "web", "framework"])
            ]
            
            for content, concepts in facts:
                await manager.store_fact(
                    str(test_agent.id), content, concepts
                )
            
            # Query knowledge
            results = await manager.query_knowledge(
                str(test_agent.id),
                query
            )
            
            assert len(results) > 0
            # Check if expected concepts appear in results
            result_concepts = set()
            for r in results:
                result_concepts.update(r.concepts)
            
            assert any(c in result_concepts for c in expected_concepts)

#### Integration Tests

python

    # tests/integration/test_agent_conversation.py
    import pytest
    from src.workflows.agent_conversation import AgentConversationWorkflow
    from src.api.routers.agents import create_session, send_message
    
    class TestAgentConversation:
        """Test complete agent conversation flow."""
        
        async def test_conversation_with_memory(
            self, db_session, test_agent, mock_llm
        ):
            """Test conversation with memory integration."""
            # Create session
            session = await create_session(
                db_session,
                agent_id=test_agent.id,
                user_id="test-user"
            )
            
            # First message - establish context
            response1 = await send_message(
                db_session,
                agent_id=test_agent.id,
                session_id=session.id,
                message="My name is Alice and I love quantum physics"
            )
            
            assert response1["response"] == "Mocked response"
            
            # Check if memory was created
            memories = await db_session.execute("""
                SELECT * FROM memory.memories 
                WHERE agent_id = :agent_id 
                AND content LIKE '%Alice%quantum physics%'
            """, {"agent_id": test_agent.id})
            
            assert memories.rowcount > 0
            
            # Second message - test memory recall
            response2 = await send_message(
                db_session,
                agent_id=test_agent.id,
                session_id=session.id,
                message="What's my name and what do I like?"
            )
            
            # In real scenario, would check if "Alice" and "quantum physics"
            # appear in the context provided to LLM
        
        async def test_multi_turn_conversation(
            self, db_session, test_agent, mock_llm
        ):
            """Test multi-turn conversation management."""
            session = await create_session(
                db_session,
                agent_id=test_agent.id,
                user_id="test-user"
            )
            
            messages = [
                "Hello, I need help with a project",
                "It's about building a recommendation system",
                "I want to use collaborative filtering",
                "Can you explain how it works?",
                "What are the alternatives?"
            ]
            
            for i, message in enumerate(messages):
                response = await send_message(
                    db_session,
                    agent_id=test_agent.id,
                    session_id=session.id,
                    message=message
                )
                
                assert response["response"] is not None
                
                # Verify message order is preserved
                stored_messages = await db_session.execute("""
                    SELECT * FROM agents.messages 
                    WHERE session_id = :session_id 
                    ORDER BY created_at
                """, {"session_id": session.id})
                
                assert stored_messages.rowcount == (i + 1) * 2  # User + assistant
    
    class TestMemoryConsolidation:
        """Test memory consolidation workflow."""
        
        async def test_consolidation_process(
            self, db_session, test_agent
        ):
            """Test full consolidation workflow."""
            from src.workflows.memory_consolidation import MemoryConsolidationWorkflow
            from src.memory.episodic import EpisodicMemoryManager
            
            manager = EpisodicMemoryManager(db_session)
            
            # Create similar memories over time
            base_content = "Meeting with John about project"
            
            for i in range(10):
                await manager.store_episode(
                    str(test_agent.id),
                    f"{base_content} - session {i}",
                    {"person": "John", "topic": "project"},
                    emotional_valence=0.1 * (i % 3)
                )
            
            # Run consolidation
            workflow = MemoryConsolidationWorkflow(
                "test_consolidation",
                str(test_agent.id),
                db_session
            )
            
            result = await workflow.run(
                memory_types=["episodic"],
                min_importance=0.2,
                time_window=timedelta(days=1)
            )
            
            assert result["total_processed"] >= 10
            assert result["consolidated"] > 0
            
            # Verify consolidated memories exist
            memories = await db_session.execute("""
                SELECT * FROM memory.memories 
                WHERE agent_id = :agent_id 
                AND type = 'episodic'
                AND content LIKE '%Consolidated%'
            """, {"agent_id": test_agent.id})
            
            assert memories.rowcount > 0

#### End-to-End Tests

python

    # tests/e2e/test_complete_scenarios.py
    import pytest
    import httpx
    from datetime import datetime, timedelta
    
    class TestCompleteScenarios:
        """End-to-end tests for complete user scenarios."""
        
        @pytest.mark.e2e
        async def test_research_assistant_scenario(self, api_client: httpx.AsyncClient):
            """Test complete research assistant workflow."""
            
            # 1. Create research assistant agent
            agent_response = await api_client.post("/api/v1/agents", json={
                "name": "Research Assistant",
                "type": "research",
                "model": "gpt-4",
                "system_prompt": "You are an expert research assistant.",
                "memory_config": {
                    "enable_episodic": True,
                    "enable_semantic": True,
                    "enable_prospective": True
                }
            })
            
            assert agent_response.status_code == 201
            agent = agent_response.json()
            
            # 2. Create session
            session_response = await api_client.post(
                f"/api/v1/agents/{agent['id']}/sessions",
                json={"user_id": "researcher-001"}
            )
            
            session = session_response.json()
            
            # 3. Assign research task
            task_response = await api_client.post(
                f"/api/v1/agents/{agent['id']}/sessions/{session['id']}/messages",
                json={
                    "content": "I need you to research quantum computing applications in healthcare. Focus on recent developments from 2023-2024."
                }
            )
            
            assert "quantum computing" in task_response.json()["response"].lower()
            
            # 4. Check if goal was created
            goals_response = await api_client.get(
                f"/api/v1/memory/agent/{agent['id']}/prospective/goals"
            )
            
            goals = goals_response.json()
            assert any("quantum computing" in g["content"].lower() for g in goals)
            
            # 5. Simulate research progress
            await api_client.post(
                f"/api/v1/agents/{agent['id']}/sessions/{session['id']}/messages",
                json={
                    "content": "I found 3 interesting applications: quantum imaging for MRI, drug discovery simulations, and protein folding predictions."
                }
            )
            
            # 6. Verify semantic memories were created
            search_response = await api_client.post("/api/v1/memory/search", json={
                "agent_id": agent['id'],
                "query": "quantum healthcare applications",
                "types": ["semantic"]
            })
            
            memories = search_response.json()
            assert len(memories) > 0
            assert any("quantum imaging" in m["content"].lower() for m in memories)
            
            # 7. Test knowledge graph
            graph_response = await api_client.get(
                f"/api/v1/memory/agent/{agent['id']}/semantic/graph"
            )
            
            graph = graph_response.json()
            assert "quantum computing" in [n["id"] for n in graph["nodes"]]
        
        @pytest.mark.e2e
        async def test_multi_agent_collaboration(self, api_client: httpx.AsyncClient):
            """Test multi-agent collaboration scenario."""
            
            # 1. Create coordinator agent
            coordinator = await api_client.post("/api/v1/agents", json={
                "name": "Project Coordinator",
                "type": "coordinator",
                "a2a_capabilities": {
                    "capabilities": ["coordination", "planning"],
                    "is_public": True
                }
            }).json()
            
            # 2. Create specialist agents
            researcher = await api_client.post("/api/v1/agents", json={
                "name": "Researcher",
                "type": "research",
                "a2a_capabilities": {
                    "capabilities": ["research", "analysis"],
                    "is_public": True
                }
            }).json()
            
            writer = await api_client.post("/api/v1/agents", json={
                "name": "Writer",
                "type": "task_oriented",
                "a2a_capabilities": {
                    "capabilities": ["writing", "summarization"],
                    "is_public": True
                }
            }).json()
            
            # 3. Coordinator discovers available agents
            discovery_response = await api_client.get(
                "/api/v1/protocols/a2a/agents?capabilities=research"
            )
            
            available_agents = discovery_response.json()
            assert any(a["name"] == "Researcher" for a in available_agents)
            
            # 4. Create collaborative task
            task_response = await api_client.post("/api/v1/protocols/a2a/tasks", json={
                "client_agent": coordinator["id"],
                "remote_agent": researcher["id"],
                "name": "research_ai_trends",
                "input": {
                    "topic": "AI trends in 2024",
                    "depth": "comprehensive"
                }
            })
            
            task = task_response.json()
            
            # 5. Monitor task progress
            import asyncio
            for _ in range(10):  # Poll for 10 seconds
                status_response = await api_client.get(
                    f"/api/v1/protocols/a2a/tasks/{task['id']}"
                )
                
                task_status = status_response.json()
                
                if task_status["status"] == "completed":
                    break
                
                await asyncio.sleep(1)
            
            assert task_status["status"] == "completed"
            assert task_status["output"] is not None

### Contributing {#contributing}

#### Contribution Guidelines

markdown

    # Contributing to Julep-PG
    
    We welcome contributions! Here's how to get started:
    
    ## Code of Conduct
    
    - Be respectful and inclusive
    - Welcome newcomers and help them get started
    - Focus on constructive criticism
    - Respect differing viewpoints
    
    ## How to Contribute
    
    1. **Fork the repository**
       ```bash
       git clone https://github.com/julep-ai/julep-pg.git
       cd julep-pg
       git remote add upstream https://github.com/julep-ai/julep-pg.git

2.  **Create a feature branch**
    
    bash
    
        git checkout -b feature/your-feature-name
    
3.  **Make your changes**
    -   Follow code style guidelines
    -   Add tests for new functionality
    -   Update documentation
4.  **Run tests**
    
    bash
    
        make test
        make lint
    
5.  **Commit your changes**
    
    bash
    
        git commit -m "feat: add new memory consolidation algorithm"
    
    Follow conventional commits:
    -   `feat:` New feature
    -   `fix:` Bug fix
    -   `docs:` Documentation
    -   `test:` Tests
    -   `refactor:` Code refactoring
    -   `perf:` Performance improvements
6.  **Push and create PR**
    
    bash
    
        git push origin feature/your-feature-name
    

## Development Workflow

### Setting Up Development Environment

See [Development Setup](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#development-setup)

### Running Tests

bash

    # Run all tests
    pytest
    
    # Run specific test file
    pytest tests/unit/test_memory_managers.py
    
    # Run with coverage
    pytest --cov=src --cov-report=html
    
    # Run only unit tests
    pytest tests/unit/
    
    # Run only integration tests
    pytest tests/integration/
    
    # Run e2e tests (requires running services)
    pytest tests/e2e/ -m e2e

### Code Quality Checks

bash

    # Format code
    black src/ tests/
    
    # Sort imports
    isort src/ tests/
    
    # Type checking
    mypy src/
    
    # Linting
    flake8 src/ tests/
    
    # Security scanning
    bandit -r src/
    
    # All checks
    make quality

## Pull Request Process

1.  **Ensure tests pass**
2.  **Update documentation**
3.  **Add changelog entry**
4.  **Request review**
5.  **Address feedback**
6.  **Merge after approval**

## Areas for Contribution

### Good First Issues

-   Add new MCP tool integrations
-   Improve error messages
-   Add more examples
-   Enhance documentation

### Feature Requests

-   New memory types
-   Protocol enhancements
-   Performance optimizations
-   UI improvements

### Bug Fixes

Check our issue tracker for reported bugs.

## Release Process

1.  Update version in `pyproject.toml`
2.  Update CHANGELOG.md
3.  Create release PR
4.  Tag release after merge
5.  Deploy to PyPI

    
    #### Development Makefile
    
    ```makefile
    # Makefile
    .PHONY: help install test lint format clean docs
    
    help:
    	@echo "Available commands:"
    	@echo "  install    Install dependencies"
    	@echo "  test       Run tests"
    	@echo "  lint       Run linters"
    	@echo "  format     Format code"
    	@echo "  clean      Clean build artifacts"
    	@echo "  docs       Build documentation"
    	@echo "  dev        Start development environment"
    	@echo "  build      Build Docker images"
    
    install:
    	pip install -e ".[dev]"
    	pre-commit install
    
    test:
    	pytest -v
    
    test-cov:
    	pytest --cov=src --cov-report=html --cov-report=term
    
    lint:
    	flake8 src/ tests/
    	mypy src/
    	bandit -r src/
    
    format:
    	black src/ tests/
    	isort src/ tests/
    
    clean:
    	rm -rf build/ dist/ *.egg-info
    	find . -type d -name __pycache__ -exec rm -rf {} +
    	find . -type f -name "*.pyc" -delete
    
    docs:
    	cd docs && make html
    
    dev:
    	docker-compose up -d postgres
    	uvicorn src.api.main:app --reload
    
    build:
    	docker build -t julep-pg:latest -f docker/app/Dockerfile .
    
    quality: format lint test
    
    migrate:
    	alembic upgrade head
    
    migrate-create:
    	alembic revision --autogenerate -m "$(message)"
    
    seed:
    	python scripts/seed_dev_data.py

* * *

## 12\. Troubleshooting {#troubleshooting}

### Common Issues {#common-issues}

#### Installation Issues

**Problem: PostgreSQL extensions fail to install**

bash

    ERROR: could not open extension control file "/usr/share/postgresql/15/extension/vector.control"

**Solution:**

bash

    # Install from source
    git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
    cd pgvector
    make
    sudo make install
    
    # Or use pre-built packages
    sudo apt install postgresql-15-pgvector  # Debian/Ubuntu
    sudo yum install pgvector_15            # RHEL/CentOS

**Problem: Python dependencies conflict**

bash

    ERROR: pip's dependency resolver does not currently take into account all the packages

**Solution:**

bash

    # Use a fresh virtual environment
    python -m venv venv_fresh
    source venv_fresh/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

#### Database Connection Issues

**Problem: "Too many connections" error**

python

    sqlalchemy.exc.OperationalError: FATAL: sorry, too many clients already

**Solution:**

sql

    -- Check current connections
    SELECT count(*) FROM pg_stat_activity;
    
    -- Increase max connections
    ALTER SYSTEM SET max_connections = 300;
    -- Restart PostgreSQL
    
    -- Or kill idle connections
    SELECT pg_terminate_backend(pid) 
    FROM pg_stat_activity 
    WHERE state = 'idle' 
    AND state_change < current_timestamp - INTERVAL '10 minutes';

**Problem: Connection pool exhausted**

python

    TimeoutError: QueuePool limit of size 50 overflow 100 reached

**Solution:**

python

    # Increase pool size in configuration
    DATABASE_POOL_SIZE = 100
    DATABASE_MAX_OVERFLOW = 200
    
    # Or use NullPool for serverless
    from sqlalchemy.pool import NullPool
    
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=NullPool
    )

#### Memory System Issues

**Problem: Vector similarity search returns no results**

python

    # No results even though memories exist
    results = await search_memories(agent_id, "quantum physics")
    # results = []

**Solution:**

python

    # 1. Check if embeddings were generated
    SELECT COUNT(*) FROM memory.memories 
    WHERE agent_id = 'your-agent-id' 
    AND embedding IS NULL;
    
    # 2. Regenerate missing embeddings
    async def regenerate_embeddings():
        memories = await db.execute("""
            SELECT id, content FROM memory.memories 
            WHERE embedding IS NULL
        """)
        
        for memory in memories:
            embedding = await generate_embedding(memory.content)
            await db.execute("""
                UPDATE memory.memories 
                SET embedding = :embedding 
                WHERE id = :id
            """, {"embedding": embedding, "id": memory.id})
    
    # 3. Check index
    REINDEX INDEX CONCURRENTLY memories_embedding_idx;

**Problem: Memory consolidation taking too long**

python

    # Consolidation workflow times out
    WorkflowTimeoutError: Workflow exceeded 300 second timeout

**Solution:**

python

    # 1. Batch consolidation
    async def batch_consolidate(agent_id: str, batch_size: int = 100):
        total_memories = await get_memory_count(agent_id)
        
        for offset in range(0, total_memories, batch_size):
            await consolidate_batch(
                agent_id, 
                offset=offset, 
                limit=batch_size
            )
    
    # 2. Optimize queries
    CREATE INDEX CONCURRENTLY idx_memories_consolidation 
    ON memory.memories(agent_id, type, created_at DESC) 
    WHERE decayed_importance > 0.3;
    
    # 3. Increase timeout
    @workflow(timeout=3600)  # 1 hour
    async def consolidate_memories(self, agent_id: str):
        # ...

### Performance Issues {#performance-issues}

#### Slow Query Diagnosis

sql

    -- Enable query timing
    \timing on
    
    -- Find slow queries
    SELECT query, mean_exec_time, calls
    FROM pg_stat_statements
    WHERE mean_exec_time > 100
    ORDER BY mean_exec_time DESC
    LIMIT 20;
    
    -- Analyze specific query
    EXPLAIN (ANALYZE, BUFFERS) 
    SELECT * FROM memory.search_memories('agent-id', 'search term');
    
    -- Check missing indexes
    SELECT schemaname, tablename, attname, n_distinct, correlation
    FROM pg_stats
    WHERE schemaname = 'memory'
    AND n_distinct > 100
    AND correlation < 0.1
    ORDER BY n_distinct DESC;

#### Memory Usage Optimization

python

    # Monitor memory usage
    import psutil
    import gc
    
    def check_memory_usage():
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss / 1024 / 1024,  # MB
            "vms": memory_info.vms / 1024 / 1024,  # MB
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available / 1024 / 1024
        }
    
    # Optimize large result sets
    async def stream_large_results():
        # Use server-side cursor
        async with db.stream(
            "SELECT * FROM memory.memories WHERE agent_id = :agent_id",
            {"agent_id": agent_id}
        ) as result:
            async for partition in result.partitions(100):
                for row in partition:
                    yield process_row(row)
                
                # Force garbage collection periodically
                gc.collect()

#### Connection Pool Tuning

python

    # Monitor pool usage
    from sqlalchemy.pool import QueuePool
    
    def get_pool_stats(engine):
        pool = engine.pool
        
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "total": pool.size() + pool.overflow()
        }
    
    # Dynamic pool sizing
    class DynamicPool:
        def __init__(self, min_size=5, max_size=100):
            self.min_size = min_size
            self.max_size = max_size
            self.current_size = min_size
            
        def adjust_pool_size(self, usage_percent):
            if usage_percent > 80 and self.current_size < self.max_size:
                self.current_size = min(
                    self.current_size * 1.5, 
                    self.max_size
                )
            elif usage_percent < 20 and self.current_size > self.min_size:
                self.current_size = max(
                    self.current_size * 0.7,
                    self.min_size
                )

### Debugging Tools {#debugging-tools}

#### SQL Query Logging

python

    # Enable SQL logging
    import logging
    
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
    
    # Custom query logger
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    import time
    
    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())
        logger.debug("Start Query: %s", statement)
    
    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logger.debug("Query Complete in %fs", total)
        
        if total > 1.0:  # Log slow queries
            logger.warning("Slow query (%fs): %s", total, statement)

#### Memory Profiling

python

    # Memory profiler decorator
    from memory_profiler import profile
    import tracemalloc
    
    @profile
    def memory_intensive_function():
        # Function implementation
        pass
    
    # Trace memory allocations
    tracemalloc.start()
    
    # Your code here
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 10**6:.1f} MB")
    print(f"Peak memory usage: {peak / 10**6:.1f} MB")
    
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("[ Top 10 memory allocations ]")
    for stat in top_stats[:10]:
        print(stat)

#### Request Tracing

python

    # Distributed tracing with OpenTelemetry
    from opentelemetry import trace
    from opentelemetry.exporter.jaeger import JaegerExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    
    # Setup tracing
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Trace operations
    async def process_with_tracing(request_id: str):
        with tracer.start_as_current_span(
            "process_request",
            attributes={"request.id": request_id}
        ) as span:
            
            # Trace database query
            with tracer.start_as_current_span("db_query"):
                result = await db.query("SELECT ...")
            
            # Trace LLM call
            with tracer.start_as_current_span("llm_generation"):
                response = await generate_completion(...)
            
            span.set_attribute("response.tokens", response["tokens"])
            
            return response

#### Interactive Debugging

python

    # IPython embed for debugging
    from IPython import embed
    
    async def debug_function():
        data = await fetch_data()
        
        # Drop into IPython shell
        embed()  # You can inspect 'data' and other variables
        
        processed = process_data(data)
        return processed
    
    # Remote debugging with debugpy
    import debugpy
    
    # Enable debugging on port 5678
    debugpy.listen(("0.0.0.0", 5678))
    
    # Pause and wait for debugger to attach
    debugpy.wait_for_client()

* * *

## 13\. Examples & Tutorials {#examples-tutorials}

### Building a Conversational Agent {#tutorial-conversational-agent}

#### Step 1: Create the Agent

python

    import httpx
    import asyncio
    from typing import Dict, Any
    
    async def create_conversational_agent():
        """Create a conversational agent with memory capabilities."""
        
        async with httpx.AsyncClient() as client:
            # Create agent with specific configuration
            agent_config = {
                "name": "Sophie",
                "type": "conversational",
                "model": "gpt-4",
                "temperature": 0.8,
                "system_prompt": """You are Sophie, a helpful and empathetic AI assistant. 
                You remember conversations and learn from interactions. 
                You can help with various tasks while maintaining a friendly personality.""",
                "memory_config": {
                    "enable_episodic": True,
                    "enable_semantic": True,
                    "enable_implicit": True,
                    "enable_prospective": True,
                    "consolidation_interval": 3600,
                    "decay_rate": 0.95
                },
                "metadata": {
                    "personality_traits": ["helpful", "curious", "empathetic"],
                    "expertise_areas": ["general_knowledge", "emotional_support", "task_assistance"]
                }
            }
            
            response = await client.post(
                "http://localhost:8000/api/v1/agents",
                json=agent_config
            )
            
            agent = response.json()
            print(f"Created agent: {agent['name']} (ID: {agent['id']})")
            
            return agent
    
    # Run the creation
    agent = asyncio.run(create_conversational_agent())

#### Step 2: Implement Conversation Logic

python

    class ConversationManager:
        """Manage conversations with memory integration."""
        
        def __init__(self, agent_id: str, base_url: str = "http://localhost:8000"):
            self.agent_id = agent_id
            self.base_url = base_url
            self.session_id = None
            self.client = httpx.AsyncClient()
        
        async def start_session(self, user_id: str) -> str:
            """Start a new conversation session."""
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/agents/{self.agent_id}/sessions",
                json={
                    "user_id": user_id,
                    "metadata": {
                        "platform": "tutorial",
                        "start_time": datetime.utcnow().isoformat()
                    }
                }
            )
            
            session = response.json()
            self.session_id = session["id"]
            return self.session_id
        
        async def send_message(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
            """Send a message and get response."""
            
            if not self.session_id:
                raise ValueError("No active session. Call start_session first.")
            
            response = await self.client.post(
                f"{self.base_url}/api/v1/agents/{self.agent_id}/sessions/{self.session_id}/messages",
                json={
                    "content": message,
                    "context": context or {}
                }
            )
            
            return response.json()
        
        async def get_conversation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
            """Retrieve conversation history."""
            
            response = await self.client.get(
                f"{self.base_url}/api/v1/agents/{self.agent_id}/sessions/{self.session_id}/messages",
                params={"limit": limit}
            )
            
            return response.json()["messages"]
        
        async def close(self):
            """Close the HTTP client."""
            await self.client.aclose()

#### Step 3: Create Interactive Chat

python

    async def interactive_chat():
        """Run an interactive chat session."""
        
        # Create agent if needed
        agent = await create_conversational_agent()
        
        # Initialize conversation manager
        manager = ConversationManager(agent["id"])
        
        # Start session
        user_id = input("Enter your name: ")
        await manager.start_session(user_id)
        
        print(f"\n🤖 {agent['name']}: Hello! I'm {agent['name']}. How can I help you today?\n")
        
        try:
            while True:
                # Get user input
                user_input = input(f"💬 {user_id}: ")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n🤖 {agent['name']}: Goodbye! It was nice talking with you.")
                    break
                
                # Send message
                response = await manager.send_message(user_input)
                
                # Display response
                print(f"\n🤖 {agent['name']}: {response['response']}\n")
                
                # Show metadata (optional)
                if response.get("metadata"):
                    print(f"📊 Metadata: {response['metadata']}\n")
        
        finally:
            await manager.close()
    
    # Run the chat
    asyncio.run(interactive_chat())

#### Step 4: Add Memory-Aware Features

python

    class MemoryAwareAgent:
        """Agent that actively uses its memory system."""
        
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.client = httpx.AsyncClient()
        
        async def remember_user_preference(self, preference: str, category: str):
            """Store user preference as implicit memory."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/memory/store",
                json={
                    "agent_id": self.agent_id,
                    "type": "implicit",
                    "content": preference,
                    "metadata": {
                        "category": category,
                        "confidence": 0.9
                    }
                }
            )
            
            return response.json()
        
        async def set_reminder(self, task: str, deadline: str):
            """Create a prospective memory (reminder)."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/memory/store",
                json={
                    "agent_id": self.agent_id,
                    "type": "prospective",
                    "content": task,
                    "type_data": {
                        "deadline": deadline,
                        "priority": 7,
                        "status": "active"
                    }
                }
            )
            
            return response.json()
        
        async def learn_fact(self, fact: str, concepts: List[str]):
            """Store new knowledge as semantic memory."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/memory/store",
                json={
                    "agent_id": self.agent_id,
                    "type": "semantic",
                    "content": fact,
                    "type_data": {
                        "concepts": concepts,
                        "confidence": 0.95,
                        "source": "user_provided"
                    }
                }
            )
            
            return response.json()
        
        async def recall_about_topic(self, topic: str) -> List[Dict[str, Any]]:
            """Search memories about a specific topic."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/memory/search",
                json={
                    "agent_id": self.agent_id,
                    "query": topic,
                    "limit": 10,
                    "threshold": 0.7
                }
            )
            
            return response.json()

### Multi-Agent Collaboration {#tutorial-multi-agent}

#### Step 1: Create Specialized Agents

python

    async def create_agent_team():
        """Create a team of specialized agents."""
        
        agents = {}
        
        # Research Agent
        agents["researcher"] = await create_agent({
            "name": "Dr. Research",
            "type": "research",
            "system_prompt": "You are an expert researcher. You find and analyze information thoroughly.",
            "a2a_capabilities": {
                "capabilities": ["research", "fact_checking", "data_analysis"],
                "is_public": True
            }
        })
        
        # Writer Agent
        agents["writer"] = await create_agent({
            "name": "Creative Writer",
            "type": "task_oriented",
            "system_prompt": "You are a skilled writer who creates engaging content.",
            "a2a_capabilities": {
                "capabilities": ["writing", "editing", "content_creation"],
                "is_public": True
            }
        })
        
        # Coordinator Agent
        agents["coordinator"] = await create_agent({
            "name": "Project Manager",
            "type": "coordinator",
            "system_prompt": "You coordinate tasks between agents and ensure project success.",
            "a2a_capabilities": {
                "capabilities": ["coordination", "planning", "task_delegation"],
                "is_public": True
            }
        })
        
        return agents

#### Step 2: Implement Task Delegation

python

    class AgentCoordinator:
        """Coordinate tasks between multiple agents."""
        
        def __init__(self, coordinator_id: str):
            self.coordinator_id = coordinator_id
            self.client = httpx.AsyncClient()
        
        async def delegate_research_task(
            self,
            researcher_id: str,
            topic: str,
            requirements: Dict[str, Any]
        ) -> str:
            """Delegate a research task to researcher agent."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/protocols/a2a/tasks",
                json={
                    "client_agent": self.coordinator_id,
                    "remote_agent": researcher_id,
                    "name": "research_topic",
                    "description": f"Research about {topic}",
                    "input": {
                        "topic": topic,
                        "depth": requirements.get("depth", "comprehensive"),
                        "sources": requirements.get("sources", ["academic", "web", "news"]),
                        "max_age_days": requirements.get("max_age_days", 365)
                    }
                }
            )
            
            task = response.json()
            return task["id"]
        
        async def delegate_writing_task(
            self,
            writer_id: str,
            content_type: str,
            research_data: Dict[str, Any]
        ) -> str:
            """Delegate writing task based on research."""
            
            response = await self.client.post(
                "http://localhost:8000/api/v1/protocols/a2a/tasks",
                json={
                    "client_agent": self.coordinator_id,
                    "remote_agent": writer_id,
                    "name": "create_content",
                    "description": f"Create {content_type} based on research",
                    "input": {
                        "content_type": content_type,
                        "research_data": research_data,
                        "tone": "professional",
                        "length": "medium"
                    }
                }
            )
            
            task = response.json()
            return task["id"]
        
        async def monitor_task(self, task_id: str) -> Dict[str, Any]:
            """Monitor task progress and get results."""
            
            while True:
                response = await self.client.get(
                    f"http://localhost:8000/api/v1/protocols/a2a/tasks/{task_id}"
                )
                
                task = response.json()
                
                if task["status"] in ["completed", "failed"]:
                    return task
                
                # Log progress
                if task.get("progress"):
                    print(f"Task {task_id}: {task['progress']*100:.0f}% complete")
                
                await asyncio.sleep(2)

#### Step 3: Create Collaborative Workflow

python

    async def collaborative_blog_post(topic: str):
        """Create a blog post through agent collaboration."""
        
        print(f"📝 Creating blog post about: {topic}\n")
        
        # Create agent team
        agents = await create_agent_team()
        
        # Initialize coordinator
        coordinator = AgentCoordinator(agents["coordinator"]["id"])
        
        try:
            # Step 1: Research Phase
            print("🔍 Phase 1: Researching topic...")
            research_task_id = await coordinator.delegate_research_task(
                agents["researcher"]["id"],
                topic,
                {
                    "depth": "comprehensive",
                    "sources": ["academic", "web", "news"],
                    "max_age_days": 90
                }
            )
            
            research_result = await coordinator.monitor_task(research_task_id)
            
            if research_result["status"] != "completed":
                raise Exception("Research failed")
            
            print("✅ Research completed\n")
            
            # Step 2: Writing Phase
            print("✍️ Phase 2: Writing blog post...")
            writing_task_id = await coordinator.delegate_writing_task(
                agents["writer"]["id"],
                "blog_post",
                research_result["output"]
            )
            
            writing_result = await coordinator.monitor_task(writing_task_id)
            
            if writing_result["status"] != "completed":
                raise Exception("Writing failed")
            
            print("✅ Blog post completed\n")
            
            # Step 3: Store results
            blog_post = writing_result["output"]["content"]
            
            # Create artifact
            artifact = {
                "type": "blog_post",
                "topic": topic,
                "content": blog_post,
                "metadata": {
                    "research_task": research_task_id,
                    "writing_task": writing_task_id,
                    "created_at": datetime.utcnow().isoformat()
                }
            }
            
            return artifact
            
        finally:
            await coordinator.client.aclose()
    
    # Run the collaborative workflow
    blog_post = asyncio.run(collaborative_blog_post("The Future of Quantum Computing"))
    print(f"\n📄 Blog Post:\n{blog_post['content']}")

### RAG Implementation {#tutorial-rag}

#### Step 1: Document Processing Pipeline

python

    class DocumentProcessor:
        """Process documents for RAG system."""
        
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.client = httpx.AsyncClient()
        
        async def ingest_document(
            self,
            content: str,
            metadata: Dict[str, Any]
        ) -> List[str]:
            """Ingest document and create chunks."""
            
            # Chunk document
            chunks = self.chunk_text(content, chunk_size=512, overlap=50)
            
            stored_ids = []
            
            for i, chunk in enumerate(chunks):
                # Store as semantic memory
                response = await self.client.post(
                    "http://localhost:8000/api/v1/memory/store",
                    json={
                        "agent_id": self.agent_id,
                        "type": "semantic",
                        "content": chunk,
                        "metadata": {
                            **metadata,
                            "chunk_index": i,
                            "total_chunks": len(chunks),
                            "document_type": "reference"
                        },
                        "importance": 0.7
                    }
                )
                
                stored_ids.append(response.json()["id"])
            
            return stored_ids
        
        def chunk_text(
            self,
            text: str,
            chunk_size: int,
            overlap: int
        ) -> List[str]:
            """Split text into overlapping chunks."""
            
            words = text.split()
            chunks = []
            
            for i in range(0, len(words), chunk_size - overlap):
                chunk = " ".join(words[i:i + chunk_size])
                chunks.append(chunk)
            
            return chunks
        
        async def ingest_multiple_documents(
            self,
            documents: List[Dict[str, Any]]
        ):
            """Ingest multiple documents in parallel."""
            
            tasks = []
            
            for doc in documents:
                task = self.ingest_document(
                    doc["content"],
                    doc["metadata"]
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks)
            
            total_chunks = sum(len(r) for r in results)
            print(f"✅ Ingested {len(documents)} documents as {total_chunks} chunks")

#### Step 2: RAG-Enhanced Agent

python

    class RAGAgent:
        """Agent with RAG capabilities."""
        
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.client = httpx.AsyncClient()
        
        async def answer_with_sources(
            self,
            question: str,
            session_id: str
        ) -> Dict[str, Any]:
            """Answer question using RAG."""
            
            # 1. Search relevant chunks
            search_response = await self.client.post(
                "http://localhost:8000/api/v1/memory/search",
                json={
                    "agent_id": self.agent_id,
                    "query": question,
                    "types": ["semantic"],
                    "limit": 5,
                    "threshold": 0.7
                }
            )
            
            relevant_chunks = search_response.json()
            
            # 2. Build context from chunks
            context_parts = []
            sources = []
            
            for chunk in relevant_chunks:
                context_parts.append(chunk["content"])
                sources.append({
                    "id": chunk["id"],
                    "metadata": chunk.get("metadata", {}),
                    "similarity": chunk.get("similarity", 0)
                })
            
            augmented_context = "\n\n".join(context_parts)
            
            # 3. Generate answer with context
            response = await self.client.post(
                f"http://localhost:8000/api/v1/agents/{self.agent_id}/sessions/{session_id}/messages",
                json={
                    "content": question,
                    "context": {
                        "rag_context": augmented_context,
                        "instruction": "Answer based on the provided context. If the context doesn't contain the answer, say so."
                    }
                }
            )
            
            answer = response.json()
            
            # 4. Add sources to response
            answer["sources"] = sources
            answer["context_used"] = len(relevant_chunks) > 0
            
            return answer

#### Step 3: Complete RAG Example

python

    async def rag_example():
        """Complete RAG implementation example."""
        
        # 1. Create RAG-enabled agent
        agent = await create_agent({
            "name": "RAG Assistant",
            "type": "research",
            "system_prompt": """You are a knowledgeable assistant with access to a document database.
            Always base your answers on the provided context and cite your sources.""",
            "memory_config": {
                "enable_semantic": True,
                "enable_episodic": True
            }
        })
        
        # 2. Initialize processors
        processor = DocumentProcessor(agent["id"])
        rag_agent = RAGAgent(agent["id"])
        
        # 3. Ingest documents
        documents = [
            {
                "content": """Quantum computing uses quantum bits or qubits. Unlike classical bits 
                that are either 0 or 1, qubits can exist in superposition, being both 0 and 1 
                simultaneously. This property enables quantum computers to perform certain 
                calculations exponentially faster than classical computers.""",
                "metadata": {
                    "source": "Quantum Computing Basics",
                    "author": "Dr. Smith",
                    "date": "2024-01-15"
                }
            },
            {
                "content": """Quantum entanglement is a phenomenon where two or more qubits become 
                correlated in such a way that the quantum state of each qubit cannot be described 
                independently. Einstein famously called it 'spooky action at a distance'. This 
                property is crucial for quantum communication and quantum cryptography.""",
                "metadata": {
                    "source": "Quantum Phenomena",
                    "author": "Dr. Johnson",
                    "date": "2024-02-01"
                }
            }
        ]
        
        await processor.ingest_multiple_documents(documents)
        
        # 4. Create session
        session_response = await rag_agent.client.post(
            f"http://localhost:8000/api/v1/agents/{agent['id']}/sessions",
            json={"user_id": "rag-demo-user"}
        )
        session_id = session_response.json()["id"]
        
        # 5. Ask questions
        questions = [
            "What is quantum superposition?",
            "Who called quantum entanglement 'spooky action at a distance'?",
            "How do qubits differ from classical bits?",
            "What is quantum tunneling?"  # Not in documents
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            
            answer = await rag_agent.answer_with_sources(question, session_id)
            
            print(f"💡 Answer: {answer['response']}")
            
            if answer["sources"]:
                print("📚 Sources:")
                for source in answer["sources"]:
                    print(f"  - {source['metadata'].get('source', 'Unknown')} "
                          f"(similarity: {source['similarity']:.2f})")
            else:
                print("📚 No relevant sources found")
    
    # Run the RAG example
    asyncio.run(rag_example())

### Custom Tools {#tutorial-custom-tools}

#### Step 1: Create Custom MCP Tool

python

    class WeatherTool:
        """Custom weather tool for MCP."""
        
        def __init__(self):
            self.api_key = os.getenv("WEATHER_API_KEY")
            self.base_url = "https://api.openweathermap.org/data/2.5"
        
        async def get_weather(self, location: str, units: str = "metric") -> Dict[str, Any]:
            """Get current weather for a location."""
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "q": location,
                        "units": units,
                        "appid": self.api_key
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"Weather API error: {response.text}")
                
                data = response.json()
                
                return {
                    "location": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"]
                }
        
        def get_tool_definition(self) -> Dict[str, Any]:
            """Get MCP tool definition."""
            
            return {
                "name": "get_weather",
                "description": "Get current weather information for any location",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name or location"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["metric", "imperial"],
                            "default": "metric",
                            "description": "Temperature units"
                        }
                    },
                    "required": ["location"]
                }
            }

#### Step 2: Register Tool with Agent

python

    async def register_custom_tool(agent_id: str):
        """Register custom tool with agent's MCP server."""
        
        # Initialize tool
        weather_tool = WeatherTool()
        
        # Create MCP server for agent
        async with httpx.AsyncClient() as client:
            # Register tool
            response = await client.post(
                "http://localhost:8000/api/v1/protocols/mcp/tools",
                json={
                    "agent_id": agent_id,
                    **weather_tool.get_tool_definition()
                }
            )
            
            print(f"✅ Registered tool: {response.json()}")
        
        # Tool handler (runs on server side)
        async def weather_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
            return await weather_tool.get_weather(
                params["location"],
                params.get("units", "metric")
            )
        
        return weather_tool_handler

#### Step 3: Create Tool-Using Agent

python

    class ToolAgent:
        """Agent that can use custom tools."""
        
        def __init__(self, agent_id: str):
            self.agent_id = agent_id
            self.client = httpx.AsyncClient()
            self.available_tools = {}
        
        async def discover_tools(self):
            """Discover available tools."""
            
            response = await self.client.get(
                f"http://localhost:8000/api/v1/protocols/mcp/tools",
                params={"agent_id": self.agent_id}
            )
            
            tools = response.json()
            
            for tool in tools:
                self.available_tools[tool["name"]] = tool
            
            print(f"🔧 Available tools: {list(self.available_tools.keys())}")
        
        async def use_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
            """Execute a tool."""
            
            if tool_name not in self.available_tools:
                raise ValueError(f"Tool not found: {tool_name}")
            
            response = await self.client.post(
                f"http://localhost:8000/api/v1/protocols/mcp/tools/{tool_name}/execute",
                json={
                    "agent_id": self.agent_id,
                    "input": kwargs
                }
            )
            
            return response.json()
        
        async def answer_with_tools(
            self,
            question: str,
            session_id: str
        ) -> Dict[str, Any]:
            """Answer question using available tools."""
            
            # Simplified tool selection logic
            tool_keywords = {
                "weather": "get_weather",
                "temperature": "get_weather",
                "forecast": "get_weather"
            }
            
            # Check if question needs a tool
            selected_tool = None
            for keyword, tool in tool_keywords.items():
                if keyword in question.lower():
                    selected_tool = tool
                    break
            
            context = {}
            
            if selected_tool:
                # Extract location from question (simplified)
                import re
                location_match = re.search(r"in ([A-Za-z\s]+)", question)
                
                if location_match:
                    location = location_match.group(1).strip()
                    
                    # Execute tool
                    tool_result = await self.use_tool(
                        selected_tool,
                        location=location
                    )
                    
                    context["tool_result"] = tool_result
                    context["tool_used"] = selected_tool
            
            # Send message with tool result
            response = await self.client.post(
                f"http://localhost:8000/api/v1/agents/{self.agent_id}/sessions/{session_id}/messages",
                json={
                    "content": question,
                    "context": context
                }
            )
            
            return response.json()

#### Step 4: Complete Tool Example

python

    async def custom_tool_example():
        """Example of creating and using custom tools."""
        
        # 1. Create tool-capable agent
        agent = await create_agent({
            "name": "Weather Assistant",
            "type": "conversational",
            "system_prompt": """You are a helpful weather assistant. When users ask about weather,
            use the get_weather tool to provide accurate, current information.""",
            "mcp_servers": [{
                "name": "weather_server",
                "transport": "stdio"
            }]
        })
        
        # 2. Register custom tool
        await register_custom_tool(agent["id"])
        
        # 3. Initialize tool agent
        tool_agent = ToolAgent(agent["id"])
        await tool_agent.discover_tools()
        
        # 4. Create session
        session_response = await tool_agent.client.post(
            f"http://localhost:8000/api/v1/agents/{agent['id']}/sessions",
            json={"user_id": "weather-user"}
        )
        session_id = session_response.json()["id"]
        
        # 5. Ask weather questions
        questions = [
            "What's the weather like in London?",
            "Is it hot in Tokyo right now?",
            "Tell me the temperature in New York",
            "Should I bring an umbrella in Paris?"
        ]
        
        for question in questions:
            print(f"\n❓ {question}")
            
            response = await tool_agent.answer_with_tools(question, session_id)
            
            print(f"🤖 {response['response']}")
            
            if response.get("metadata", {}).get("tool_used"):
                print(f"🔧 Used tool: {response['metadata']['tool_used']}")
    
    # Run the example
    asyncio.run(custom_tool_example())

* * *

## 14\. Migration Guide {#migration-guide}

### From Julep v1 {#from-julep-v1}

#### Migration Overview

python

    # migration/v1_to_v2.py
    """
    Julep v1 to v2 Migration Guide
    
    Key Changes:
    1. PostgreSQL-native architecture (no more separate services)
    2. New memory system with 4 types
    3. MCP and A2A protocol support
    4. DBOS workflow engine
    5. Simplified API
    """
    
    class JulepV1Migrator:
        """Migrate from Julep v1 to v2."""
        
        def __init__(self, v1_config: Dict[str, Any], v2_db_url: str):
            self.v1_config = v1_config
            self.v2_db_url = v2_db_url
            self.migration_log = []
        
        async def migrate_agents(self):
            """Migrate v1 agents to v2."""
            
            v1_agents = await self.fetch_v1_agents()
            
            for v1_agent in v1_agents:
                # Map v1 agent to v2 schema
                v2_agent = {
                    "name": v1_agent["name"],
                    "type": self.map_agent_type(v1_agent),
                    "model": v1_agent.get("model", "gpt-4"),
                    "system_prompt": v1_agent.get("instructions", ""),
                    "metadata": {
                        "v1_id": v1_agent["id"],
                        "v1_created": v1_agent["created_at"],
                        "migrated_at": datetime.utcnow().isoformat()
                    },
                    "memory_config": {
                        "enable_episodic": True,
                        "enable_semantic": True,
                        "enable_implicit": False,  # New in v2
                        "enable_prospective": False  # New in v2
                    }
                }
                
                # Create in v2
                created_agent = await self.create_v2_agent(v2_agent)
                
                # Migrate agent's data
                await self.migrate_agent_sessions(v1_agent["id"], created_agent["id"])
                await self.migrate_agent_memories(v1_agent["id"], created_agent["id"])
                
                self.migration_log.append({
                    "type": "agent",
                    "v1_id": v1_agent["id"],
                    "v2_id": created_agent["id"],
                    "status": "success"
                })
        
        def map_agent_type(self, v1_agent: Dict[str, Any]) -> str:
            """Map v1 agent roles to v2 types."""
            
            role = v1_agent.get("role", "").lower()
            
            mapping = {
                "assistant": "conversational",
                "researcher": "research",
                "analyst": "research",
                "writer": "task_oriented",
                "coder": "task_oriented",
                "manager": "coordinator"
            }
            
            return mapping.get(role, "conversational")
        
        async def migrate_agent_sessions(self, v1_agent_id: str, v2_agent_id: str):
            """Migrate conversation sessions."""
            
            v1_sessions = await self.fetch_v1_sessions(v1_agent_id)
            
            for v1_session in v1_sessions:
                # Create v2 session
                v2_session = await self.create_v2_session(
                    v2_agent_id,
                    v1_session.get("user_id", "migrated-user")
                )
                
                # Migrate messages
                v1_messages = await self.fetch_v1_messages(v1_session["id"])
                
                for msg in v1_messages:
                    await self.create_v2_message(
                        v2_session["id"],
                        msg["role"],
                        msg["content"],
                        msg["created_at"]
                    )
        
        async def migrate_agent_memories(self, v1_agent_id: str, v2_agent_id: str):
            """Migrate v1 memories to v2 memory system."""
            
            v1_memories = await self.fetch_v1_memories(v1_agent_id)
            
            for v1_memory in v1_memories:
                # Determine v2 memory type
                memory_type = self.classify_memory_type(v1_memory)
                
                # Create appropriate v2 memory
                if memory_type == "episodic":
                    await self.create_episodic_memory(v2_agent_id, v1_memory)
                elif memory_type == "semantic":
                    await self.create_semantic_memory(v2_agent_id, v1_memory)
                elif memory_type == "prospective":
                    await self.create_prospective_memory(v2_agent_id, v1_memory)
        
        def classify_memory_type(self, v1_memory: Dict[str, Any]) -> str:
            """Classify v1 memory into v2 types."""
            
            content = v1_memory["content"].lower()
            metadata = v1_memory.get("metadata", {})
            
            # Check for temporal markers
            if any(word in content for word in ["yesterday", "last week", "remember when"]):
                return "episodic"
            
            # Check for factual content
            if any(word in content for word in ["is", "are", "means", "defined as"]):
                return "semantic"
            
            # Check for future-oriented content
            if any(word in content for word in ["will", "plan to", "reminder", "deadline"]):
                return "prospective"
            
            # Default to episodic for conversations
            return "episodic"

#### Migration Script

bash

    #!/bin/bash
    # scripts/migrate_v1_to_v2.sh
    
    echo "Julep v1 to v2 Migration"
    echo "========================"
    
    # 1. Backup v1 data
    echo "Step 1: Backing up v1 data..."
    docker exec julep-v1-postgres pg_dump -U postgres julep_v1 > backup_v1_$(date +%Y%m%d).sql
    
    # 2. Setup v2 database
    echo "Step 2: Setting up v2 database..."
    docker-compose -f docker-compose.v2.yml up -d postgres
    sleep 10
    
    # 3. Run schema creation
    echo "Step 3: Creating v2 schema..."
    docker-compose exec postgres psql -U postgres -d julep_v2 -f /schemas/complete_schema.sql
    
    # 4. Run Python migration
    echo "Step 4: Migrating data..."
    python -m migration.run_migration \
        --v1-db "$V1_DATABASE_URL" \
        --v2-db "$V2_DATABASE_URL" \
        --batch-size 100
    
    # 5. Verify migration
    echo "Step 5: Verifying migration..."
    python -m migration.verify_migration
    
    echo "Migration complete!"

### From Other Platforms {#from-other-platforms}

#### LangChain Migration

python

    class LangChainMigrator:
        """Migrate from LangChain to Julep-PG."""
        
        def migrate_chain_to_workflow(self, langchain_code: str) -> str:
            """Convert LangChain chain to Julep workflow."""
            
            # Example conversion
            julep_workflow = """
    from src.workflows.base import DBOSWorkflow, dbos_workflow, dbos_step
    
    class ConvertedWorkflow(DBOSWorkflow):
        @dbos_workflow("langchain_migration")
        async def run(self, input_data: str):
            # Step 1: Process input (replaces LangChain prompt template)
            processed = await self.process_input(input_data)
            
            # Step 2: LLM call (replaces LangChain LLM)
            response = await self.generate_response(processed)
            
            # Step 3: Parse output (replaces LangChain output parser)
            parsed = await self.parse_output(response)
            
            return parsed
        
        @dbos_step("process_input")
        async def process_input(self, data: str):
            # Your prompt template logic here
            return formatted_prompt
        
        @dbos_step("generate_response")
        async def generate_response(self, prompt: str):
            # Direct LLM call
            return await generate_completion(prompt)
        
        @dbos_step("parse_output")
        async def parse_output(self, response: str):
            # Your output parsing logic
            return parsed_data
    """
            return julep_workflow
        
        def migrate_vector_store(self, vectorstore):
            """Migrate LangChain vector store to Julep memories."""
            
            # Extract documents from vector store
            documents = vectorstore.get_all_documents()
            
            migrated_memories = []
            
            for doc in documents:
                memory = {
                    "type": "semantic",
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "embedding": doc.embedding if hasattr(doc, 'embedding') else None
                }
                migrated_memories.append(memory)
            
            return migrated_memories
        
        def migrate_conversation_chain(self, chain):
            """Migrate ConversationChain to Julep agent."""
            
            agent_config = {
                "name": "Migrated from LangChain",
                "type": "conversational",
                "system_prompt": chain.prompt.template if hasattr(chain, 'prompt') else "",
                "memory_config": {
                    "enable_episodic": True,
                    "enable_semantic": True
                }
            }
            
            # Extract conversation history
            if hasattr(chain, 'memory'):
                messages = chain.memory.chat_memory.messages
                conversation_history = [
                    {
                        "role": "user" if msg.type == "human" else "assistant",
                        "content": msg.content
                    }
                    for msg in messages
                ]
            else:
                conversation_history = []
            
            return agent_config, conversation_history

#### AutoGPT/AutoGen Migration

python

    class AutoGPTMigrator:
        """Migrate from AutoGPT/AutoGen to Julep-PG."""
        
        def migrate_autogpt_agent(self, autogpt_config: Dict[str, Any]):
            """Convert AutoGPT agent to Julep agent."""
            
            # Map AutoGPT capabilities to Julep
            julep_agent = {
                "name": autogpt_config.get("ai_name", "Migrated AutoGPT Agent"),
                "type": "task_oriented",
                "model": autogpt_config.get("model", "gpt-4"),
                "system_prompt": self.build_system_prompt(autogpt_config),
                "memory_config": {
                    "enable_episodic": True,
                    "enable_semantic": True,
                    "enable_prospective": True,  # For goal tracking
                    "enable_implicit": True      # For learned behaviors
                },
                "mcp_servers": self.map_autogpt_commands_to_tools(autogpt_config)
            }
            
            return julep_agent
        
        def build_system_prompt(self, config: Dict[str, Any]) -> str:
            """Build Julep system prompt from AutoGPT config."""
            
            role = config.get("ai_role", "a helpful assistant")
            goals = config.get("ai_goals", [])
            
            prompt = f"""You are {role}.
            
    Your primary goals are:
    {chr(10).join(f'{i+1}. {goal}' for i, goal in enumerate(goals))}
    
    You have access to various tools and can break down complex tasks into steps.
    You maintain memory of past interactions and learn from experience.
    """
            
            return prompt
        
        def map_autogpt_commands_to_tools(
            self,
            config: Dict[str, Any]
        ) -> List[Dict[str, Any]]:
            """Map AutoGPT commands to MCP tools."""
            
            command_mapping = {
                "google": "web_search",
                "browse_website": "web_fetch",
                "write_to_file": "file_write",
                "read_file": "file_read",
                "execute_python": "code_interpreter",
                "send_tweet": "social_media_post"
            }
            
            mcp_servers = []
            
            for command in config.get("commands", []):
                if command in command_mapping:
                    mcp_servers.append({
                        "name": f"{command_mapping[command]}_server",
                        "transport": "stdio",
                        "command": f"mcp-{command_mapping[command]}"
                    })
            
            return mcp_servers
        
        def migrate_autogen_workflow(self, autogen_agents: List[Dict[str, Any]]):
            """Convert AutoGen multi-agent setup to Julep."""
            
            julep_agents = []
            
            for autogen_agent in autogen_agents:
                agent_type = self.classify_autogen_agent(autogen_agent)
                
                julep_agent = {
                    "name": autogen_agent["name"],
                    "type": agent_type,
                    "system_prompt": autogen_agent.get("system_message", ""),
                    "a2a_capabilities": {
                        "capabilities": self.extract_capabilities(autogen_agent),
                        "is_public": True
                    }
                }
                
                julep_agents.append(julep_agent)
            
            # Create coordinator for orchestration
            coordinator = {
                "name": "AutoGen Coordinator",
                "type": "coordinator",
                "system_prompt": "You coordinate tasks between specialized agents.",
                "a2a_capabilities": {
                    "capabilities": ["coordination", "planning"],
                    "is_public": True
                }
            }
            
            julep_agents.append(coordinator)
            
            return julep_agents
        
        def classify_autogen_agent(self, agent: Dict[str, Any]) -> str:
            """Classify AutoGen agent to Julep type."""
            
            name_lower = agent["name"].lower()
            
            if "user" in name_lower or "proxy" in name_lower:
                return "conversational"
            elif "assistant" in name_lower:
                return "task_oriented"
            elif "critic" in name_lower or "review" in name_lower:
                return "research"
            else:
                return "task_oriented"

* * *

## 15\. Reference {#reference}

### Glossary {#glossary}

**Agent**: An AI entity with its own personality, capabilities, and memory system. Agents can be conversational, task-oriented, research-focused, or coordinators.

**A2A (Agent-to-Agent) Protocol**: A protocol enabling agents to discover, communicate, and collaborate with each other on complex tasks.

**Consolidation**: The process of merging similar memories, strengthening important ones, and removing weak memories to optimize the memory system.

**DBOS (Database-Oriented Operating System)**: A system that provides durable, fault-tolerant workflow execution directly in PostgreSQL.

**Decay Rate**: The rate at which memory importance decreases over time, following the Ebbinghaus forgetting curve.

**Embedding**: A high-dimensional vector representation of text that enables semantic similarity search.

**Episodic Memory**: Memory type that captures temporal sequences of experiences with emotional and contextual information.

**HNSW (Hierarchical Navigable Small World)**: An algorithm for approximate nearest neighbor search used in pgvector for fast similarity search.

**Implicit Memory**: Memory type that captures unconscious patterns, biases, and behavioral tendencies.

**MCP (Model Context Protocol)**: A protocol for integrating external tools and resources with AI agents.

**pgai**: PostgreSQL extension providing native LLM integration functions.

**pgmq**: PostgreSQL extension implementing a message queue system.

**pgrag**: PostgreSQL extension for RAG (Retrieval-Augmented Generation) pipelines.

**pgvector**: PostgreSQL extension for vector similarity search.

**Prospective Memory**: Memory type managing future-oriented cognition including goals, plans, and intentions.

**Semantic Memory**: Memory type storing factual knowledge and conceptual understanding in a graph structure.

**Session**: A conversation context between a user and an agent, maintaining message history and state.

**Workflow**: A multi-step process orchestrated by DBOS with durability and fault tolerance.

### FAQ {#faq}

**Q: How does Julep-PG compare to LangChain?**

A: While LangChain is a library for building LLM applications, Julep-PG is a complete platform with:

-   Built-in cognitive memory system
-   Native database integration
-   Multi-agent collaboration
-   Workflow orchestration
-   No need for separate vector stores or orchestrators

**Q: Can I use Julep-PG with models other than OpenAI?**

A: Yes! Julep-PG supports:

-   OpenAI models (GPT-4, GPT-3.5)
-   Anthropic models (Claude)
-   Local models via pgai
-   Any model with an OpenAI-compatible API

**Q: How much does it cost to run Julep-PG?**

A: Julep-PG itself is open source and free. Costs include:

-   Infrastructure (PostgreSQL hosting)
-   LLM API costs (OpenAI, Anthropic, etc.)
-   Optional cloud services (backups, monitoring)

**Q: Is Julep-PG production-ready?**

A: The current version is a prototype demonstrating the architecture. Production readiness depends on:

-   Your specific use case
-   Scale requirements
-   Available resources for hardening

**Q: Can I migrate from Julep v1?**

A: Yes, we provide migration tools and guides. The main changes are:

-   PostgreSQL-native architecture
-   New memory system
-   Protocol support (MCP, A2A)
-   Simplified API

**Q: How do I handle agent conversations at scale?**

A: Julep-PG scales through:

-   Connection pooling
-   Read replicas
-   Horizontal sharding
-   Caching strategies
-   Query optimization

**Q: Can agents learn and improve over time?**

A: Yes, through:

-   Implicit memory capturing behavioral patterns
-   Memory consolidation strengthening important information
-   Prospective memory tracking goal completion
-   Continuous memory updates

**Q: How secure is Julep-PG?**

A: Security features include:

-   Row-level security in PostgreSQL
-   API key authentication
-   JWT support
-   Audit logging
-   Encrypted connections

**Q: Can I extend Julep-PG with custom functionality?**

A: Absolutely! You can:

-   Add custom MCP tools
-   Create new workflow types
-   Implement custom memory types
-   Build new protocol handlers

**Q: Where can I get help?**

A: Support options:

-   GitHub Issues for bugs
-   Discord community for discussions
-   Documentation for guides
-   Commercial support (coming soon)

### Resources {#resources}

#### Official Resources

-   **GitHub Repository**: [https://github.com/julep-ai/julep-pg](https://github.com/julep-ai/julep-pg)
-   **Documentation**: [https://docs.julep-pg.ai](https://docs.julep-pg.ai/)
-   **API Reference**: [https://api.julep-pg.ai/docs](https://api.julep-pg.ai/docs)
-   **Discord Community**: [https://discord.gg/julep-pg](https://discord.gg/julep-pg)

#### PostgreSQL Extensions

-   **pgvector**: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
-   **pgmq**: [https://github.com/pgmq/pgmq](https://github.com/pgmq/pgmq)
-   **pg\_jsonschema**: [https://github.com/supabase/pg\_jsonschema](https://github.com/supabase/pg_jsonschema)
-   **PostgreSQL Docs**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)

#### Related Projects

-   **DBOS**: [https://github.com/dbos-inc/dbos](https://github.com/dbos-inc/dbos)
-   **Hasura**: [https://hasura.io](https://hasura.io/)
-   **TypeSpec**: [https://typespec.io](https://typespec.io/)

#### Learning Resources

-   **PostgreSQL Performance Tuning**: [https://wiki.postgresql.org/wiki/Performance\_Optimization](https://wiki.postgresql.org/wiki/Performance_Optimization)
-   **Vector Databases Explained**: [https://www.pinecone.io/learn/vector-database/](https://www.pinecone.io/learn/vector-database/)
-   **LLM Integration Patterns**: [https://www.anthropic.com/research](https://www.anthropic.com/research)

#### Research Papers

-   "Cognitive Architectures for AI Agents" (2023)
-   "Efficient Vector Search in PostgreSQL" (2024)
-   "Memory Systems in Artificial Intelligence" (2023)

#### Community Contributions

-   **Example Projects**: [https://github.com/julep-ai/julep-pg-examples](https://github.com/julep-ai/julep-pg-examples)
-   **Community Tools**: [https://github.com/julep-ai/julep-pg-tools](https://github.com/julep-ai/julep-pg-tools)
-   **Tutorials**: [https://github.com/julep-ai/julep-pg-tutorials](https://github.com/julep-ai/julep-pg-tutorials)

* * *

## Conclusion

Julep-PG represents a paradigm shift in AI agent development, proving that sophisticated agent capabilities can be implemented directly within PostgreSQL. By leveraging the database's maturity, extensibility, and performance, we've created a platform that is both powerful and operationally simple.

The journey from complex microservices to elegant database-centric architecture shows that sometimes the best solution is to use the tools we already have in new and innovative ways. PostgreSQL's extension ecosystem provides everything needed for modern AI applications: vector search, message queuing, workflow orchestration, and now, with pgai, direct LLM integration.

We invite you to join us in building the future of AI agents. Whether you're migrating from another platform, starting fresh, or contributing to the project, Julep-PG provides a solid foundation for your AI agent needs.

**Get Started Today**: [https://github.com/julep-ai/julep-pg](https://github.com/julep-ai/julep-pg)

**Join the Community**: [https://discord.gg/julep-pg](https://discord.gg/julep-pg)

**Contribute**: See our [Contributing Guide](https://claude.ai/share/539fa9fc-8d6d-46b6-a604-351f87e83f74#contributing)

Together, let's make AI agents simpler, faster, and more accessible to everyone.







