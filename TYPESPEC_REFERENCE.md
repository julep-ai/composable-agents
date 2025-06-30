# TypeSpec Reference for Julep v2

<!-- AIDEV-NOTE: typespec-reference; comprehensive guide for schema-first API development in Julep v2 -->

## Overview

TypeSpec is a language for describing APIs and automatically generating various outputs including OpenAPI specifications, client SDKs, and database schemas. In Julep v2, TypeSpec serves as the **single source of truth** for our API contracts, enabling us to generate PostgreSQL schemas, FastAPI code, Python clients, and Hasura GraphQL schemas from unified type definitions.

### Why TypeSpec for Julep v2?

<!-- AIDEV-NOTE: typespec-benefits; key advantages for postgresql-centric architecture -->
- **Schema-first development**: Define APIs before implementation
- **Multi-target generation**: One definition → multiple outputs (OpenAPI, Python SDK, DB schema)
- **Type safety**: Strong typing across the entire stack
- **PostgreSQL integration**: Can generate SQL schemas that work with pgvector, pgai, pgmq
- **Protocol support**: Easy definition of MCP and A2A protocol structures

## Installation & Setup

### Prerequisites
- Node.js 18+
- npm or pnpm

### Installation
```bash
# Install TypeSpec CLI globally
npm install -g @typespec/compiler

# Install required libraries
npm install @typespec/http @typespec/openapi3 @typespec/rest
```

### Project Initialization
```bash
# Create new TypeSpec project
tsp init

# Choose "Generic REST API" template
# Select @typespec/http and @typespec/openapi3 libraries
```

## Project Structure

<!-- AIDEV-NOTE: project-structure; recommended layout for julep v2 typespec definitions -->
```
schemas/
├── typespec/
│   ├── main.tsp              # Main entry point
│   ├── agents.tsp            # Agent models and operations
│   ├── memory.tsp            # Memory system models
│   ├── protocols.tsp         # MCP and A2A protocol definitions
│   ├── sessions.tsp          # Session and conversation models
│   └── common.tsp            # Shared types and utilities
├── generated/
│   ├── openapi/             # Generated OpenAPI specs
│   ├── python/              # Generated Python SDK
│   └── sql/                 # Generated SQL schemas
├── tspconfig.yaml           # TypeSpec configuration
└── package.json            # Dependencies
```

## Configuration (tspconfig.yaml)

<!-- AIDEV-NOTE: tspconfig-example; multi-emitter setup for complete code generation -->
```yaml
emit:
  - "@typespec/openapi3"
  - "@typespec/http-client-python"

options:
  "@typespec/openapi3":
    emitter-output-dir: "{project-root}/generated/openapi"
    version: "3.1.0"
    
  "@typespec/http-client-python":
    emitter-output-dir: "{project-root}/generated/python"
    packageDetails:
      name: "julep-client"
      version: "2.0.0"

output-dir: "{project-root}/generated"
```

## Core Language Concepts

### Models (Data Structures)

<!-- AIDEV-NOTE: typespec-models; defining data structures for julep entities -->
```typescript
// Basic model definition
model Agent {
  id: string;
  name: string;
  description?: string;
  created_at: utcDateTime;
  updated_at: utcDateTime;
}

// Model with validation constraints
model CreateAgentRequest {
  @minLength(1)
  @maxLength(100)
  name: string;
  
  @maxLength(500)
  description?: string;
  
  @doc("Initial memory configuration")
  memory_config?: MemoryConfig;
}

// Model inheritance
model BaseEntity {
  id: string;
  created_at: utcDateTime;
  updated_at: utcDateTime;
}

model Agent extends BaseEntity {
  name: string;
  description?: string;
}
```

### Enums and Unions

```typescript
// String enum
enum MemoryType {
  episodic: "episodic",
  semantic: "semantic", 
  implicit: "implicit",
  prospective: "prospective"
}

// Union types for flexible responses
union AgentResponse {
  success: Agent,
  error: ErrorResponse
}

// Discriminated union
@discriminator("type")
union MemoryEntry {
  episodic: EpisodicMemory,
  semantic: SemanticMemory,
  implicit: ImplicitMemory,
  prospective: ProspectiveMemory
}
```

### Operations (API Endpoints)

<!-- AIDEV-NOTE: typespec-operations; rest api endpoint definitions -->
```typescript
@route("/agents")
interface Agents {
  // GET /agents
  @get
  list(@query limit?: int32, @query offset?: int32): Agent[];
  
  // POST /agents
  @post
  create(@body request: CreateAgentRequest): Agent | ErrorResponse;
  
  // GET /agents/{id}
  @route("{id}")
  @get
  get(@path id: string): Agent | NotFoundResponse;
  
  // PUT /agents/{id}
  @route("{id}")
  @put
  update(@path id: string, @body request: UpdateAgentRequest): Agent | ErrorResponse;
  
  // DELETE /agents/{id}
  @route("{id}")
  @delete
  delete(@path id: string): NoContentResponse | ErrorResponse;
}
```

## Memory System Models

<!-- AIDEV-NOTE: memory-models; cognitive memory system type definitions -->
```typescript
// Base memory entry
model BaseMemoryEntry {
  id: string;
  agent_id: string;
  content: string;
  embedding?: float32[];
  created_at: utcDateTime;
  importance_score?: float32;
}

// Episodic memory (experiences and events)
model EpisodicMemory extends BaseMemoryEntry {
  type: "episodic";
  session_id: string;
  sequence_number: int32;
  context: Record<unknown>;
}

// Semantic memory (facts and knowledge)
model SemanticMemory extends BaseMemoryEntry {
  type: "semantic";
  category: string;
  confidence_score: float32;
  related_concepts?: string[];
}

// Implicit memory (patterns and beliefs)  
model ImplicitMemory extends BaseMemoryEntry {
  type: "implicit";
  pattern_type: string;
  activation_strength: float32;
}

// Prospective memory (goals and intentions)
model ProspectiveMemory extends BaseMemoryEntry {
  type: "prospective";
  goal_state: string;
  trigger_conditions: string[];
  deadline?: utcDateTime;
  priority: "low" | "medium" | "high";
}
```

## Protocol Definitions

### MCP (Model Context Protocol)

<!-- AIDEV-NOTE: mcp-protocol; model context protocol type definitions -->
```typescript
// MCP Message structure
model MCPMessage {
  jsonrpc: "2.0";
  id?: string | int32;
  method?: string;
  params?: Record<unknown>;
  result?: unknown;
  error?: MCPError;
}

model MCPError {
  code: int32;
  message: string;
  data?: unknown;
}

// MCP Tool definition
model MCPTool {
  name: string;
  description: string;
  input_schema: Record<unknown>;
}

// MCP operations
@route("/mcp")
interface MCP {
  @post
  @route("call")
  call(@body request: MCPMessage): MCPMessage;
  
  @get
  @route("tools")
  listTools(): MCPTool[];
}
```

### A2A (Agent-to-Agent) Protocol

<!-- AIDEV-NOTE: a2a-protocol; agent-to-agent communication definitions -->
```typescript
// A2A Task structure
model A2ATask {
  id: string;
  context_id: string;
  status: A2ATaskStatus;
  artifacts?: A2AArtifact[];
  metadata?: Record<unknown>;
}

enum A2ATaskState {
  submitted: "submitted",
  working: "working", 
  input_required: "input_required",
  completed: "completed",
  failed: "failed",
  canceled: "canceled"
}

model A2ATaskStatus {
  state: A2ATaskState;
  message?: string;
  timestamp: utcDateTime;
}

model A2AArtifact {
  artifact_id: string;
  name?: string;
  description?: string;
  parts: A2APart[];
  metadata?: Record<unknown>;
}

@discriminator("type")
union A2APart {
  text: A2ATextPart,
  file: A2AFilePart,
  data: A2ADataPart
}
```

## Compilation & Generation

### Basic Commands

```bash
# Compile TypeSpec to generate outputs
tsp compile .

# Watch mode for development
tsp compile . --watch

# Compile with specific emitters
tsp compile . --emit @typespec/openapi3

# Dry run (no file output)
tsp compile . --dry-run
```

### Integration with Build Process

<!-- AIDEV-NOTE: build-integration; incorporating typespec into development workflow -->
```bash
# package.json scripts
{
  "scripts": {
    "typespec:build": "tsp compile .",
    "typespec:watch": "tsp compile . --watch",
    "typespec:check": "tsp compile . --dry-run",
    "build": "npm run typespec:build && npm run build:app"
  }
}
```

## Database Schema Generation

While TypeSpec doesn't directly generate SQL schemas, the generated OpenAPI specs can be processed to create PostgreSQL schemas:

<!-- AIDEV-NOTE: db-schema-workflow; translating typespec to postgresql schemas -->
```typescript
// TypeSpec model
model Agent {
  @doc("Unique identifier")
  id: string;
  
  @doc("Agent name")
  @minLength(1) @maxLength(100)
  name: string;
  
  @doc("Optional description") 
  @maxLength(500)
  description?: string;
  
  @doc("Creation timestamp")
  created_at: utcDateTime;
  
  @doc("Memory embeddings")
  embeddings?: float32[];
}

// Could generate SQL like:
/*
CREATE TABLE agents (
  id UUID PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(500),
  created_at TIMESTAMPTZ NOT NULL,
  embeddings vector(1536)  -- using pgvector
);
*/
```

## Best Practices for Julep v2

<!-- AIDEV-NOTE: best-practices; recommended patterns for julep v2 development -->

### 1. Model Organization
- Group related models in separate files
- Use consistent naming conventions (PascalCase for models, camelCase for properties)
- Leverage inheritance for common patterns

### 2. Validation
- Use built-in validation decorators (@minLength, @maxLength, @minValue, etc.)
- Define custom formats for domain-specific types

### 3. Documentation
- Use @doc decorators for comprehensive API documentation
- Include examples with @example decorator

### 4. Versioning
- Use namespaces to organize API versions
- Leverage TypeSpec's built-in versioning support

### 5. Error Handling
- Define consistent error response models
- Use union types for operations that can fail

## Example: Complete Agent Resource

```typescript
import "@typespec/http";
import "@typespec/rest";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
  title: "Julep Agent API",
  version: "2.0.0"
})
@server("https://api.julep.ai", "Production server")
namespace JulepAPI;

// Common models
model BaseEntity {
  id: string;
  created_at: utcDateTime;
  updated_at: utcDateTime;
}

model ErrorResponse {
  @statusCode statusCode: int32;
  error: string;
  message: string;
  details?: Record<unknown>;
}

// Agent models
model Agent extends BaseEntity {
  @minLength(1) @maxLength(100)
  name: string;
  
  @maxLength(500)
  description?: string;
  
  status: "active" | "inactive" | "suspended";
  memory_config: MemoryConfig;
}

model CreateAgentRequest {
  @minLength(1) @maxLength(100)
  name: string;
  
  @maxLength(500)
  description?: string;
  
  memory_config?: MemoryConfig;
}

model MemoryConfig {
  max_episodic_entries?: int32 = 1000;
  max_semantic_entries?: int32 = 5000;
  consolidation_enabled?: boolean = true;
}

// Agent operations
@tag("Agents")
@route("/agents")
interface Agents {
  @summary("List all agents")
  @get
  list(
    @query limit?: int32 = 20,
    @query offset?: int32 = 0
  ): {
    @body agents: Agent[];
    @header("X-Total-Count") totalCount: int32;
  };

  @summary("Create a new agent")
  @post
  create(@body request: CreateAgentRequest): Agent | ErrorResponse;

  @summary("Get agent by ID")
  @route("{id}")
  @get
  get(@path id: string): Agent | NotFoundResponse;

  @summary("Update agent")
  @route("{id}")
  @put
  update(
    @path id: string,
    @body request: CreateAgentRequest
  ): Agent | ErrorResponse;

  @summary("Delete agent")
  @route("{id}")
  @delete
  delete(@path id: string): NoContentResponse | ErrorResponse;
}
```

This TypeSpec definition would generate:
- OpenAPI 3.1 specification
- Python client SDK with proper typing
- Documentation with examples
- Foundation for PostgreSQL schema generation

## Next Steps

1. Set up TypeSpec in the `schemas/` directory
2. Define core models for agents, memory, sessions
3. Add MCP and A2A protocol definitions  
4. Configure emitters for OpenAPI and Python client generation
5. Integrate with the build process and CI/CD pipeline