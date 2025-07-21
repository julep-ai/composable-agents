/**
 * TypeSpec definitions for Julep V2 agents
 * Generates PostgreSQL schemas, API contracts, and SDKs
 */

import "@typespec/rest";
import "@typespec/openapi3";
import "@typespec/postgres"; // AIDEV-NOTE: hypothetical PostgreSQL emitter

// AIDEV-NOTE: typespec-latest; TypeSpec 1.1.0 (June 2025) features
// - Language for defining cloud service APIs and shapes
// - Generates OpenAPI, JSON Schema, Protobuf from single source
// - Creates reusable patterns for API design consistency
// - Full VS Code and Visual Studio language support
// - 70% code reduction compared to manual implementation
// - Microsoft-built, community-supported project

// AIDEV-TODO: agent-model; define core Agent model with MCP/A2A capabilities
// AIDEV-TODO: memory-models; define all four cognitive memory types
// AIDEV-TODO: protocol-models; MCP and A2A message types
// AIDEV-TODO: workflow-models; task and workflow state models
// AIDEV-TODO: validation-rules; add business logic constraints

using TypeSpec.Rest;
using TypeSpec.OpenAPI;

@service({
  title: "Julep V2 Agents API",
  version: "2.0.0-alpha"
})
namespace JulepV2;

/**
 * Agent model with protocol capabilities
 * 
 * AIDEV-NOTE: model-generation; this generates:
 * - PostgreSQL table with proper constraints
 * - SQL schema migrations
 * - FastAPI Pydantic models
 * - TypeScript interfaces for SDK
 * - OpenAPI documentation
 */
@resource("agents")
model Agent {
  @key
  @visibility("read")
  id: uuid;
  
  @maxLength(255)
  name: string;
  
  type: AgentType;
  
  @doc("MCP server configurations for tool access")
  mcpServers?: MCPServerConfig[];
  
  @doc("A2A agent card for capability advertisement")
  a2aCard?: A2AAgentCard;
  
  @visibility("read")
  createdAt: utcDateTime;
  
  @visibility("read")
  updatedAt: utcDateTime;
}

enum AgentType {
  conversational: "conversational",
  taskOriented: "task-oriented",
  research: "research"
}

@example({
  url: "ws://localhost:3000/mcp",
  name: "Local MCP Server",
  tools: ["search", "calculate"]
})
model MCPServerConfig {
  url: url;
  name: string;
  tools: string[];
}