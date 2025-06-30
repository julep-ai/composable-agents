/**
 * Protocol definitions for MCP and A2A
 * Enabling agent tool use and inter-agent communication
 */

import "@typespec/rest";

using TypeSpec.Rest;

namespace JulepV2;

/**
 * MCP (Model Context Protocol) tool definition
 * 
 * AIDEV-NOTE: mcp-tool; standardized tool interface
 * - Input/output schemas for validation
 * - Server registration for discovery
 * - Execution timeout configuration
 */
@resource("tools")
model MCPTool {
  @key
  @visibility("read")
  id: uuid;
  
  @doc("Unique tool name within the server")
  name: string;
  
  @doc("Human-readable description")
  description: string;
  
  @doc("JSON Schema for tool input validation")
  inputSchema: unknown;
  
  @doc("JSON Schema for tool output")
  outputSchema?: unknown;
  
  @doc("MCP server that provides this tool")
  serverId: uuid;
  
  @doc("Whether the tool is currently available")
  enabled: boolean = true;
  
  @doc("Maximum execution time in milliseconds")
  @minValue(1000)
  @maxValue(300000)
  timeoutMs: int32 = 30000;
}

/**
 * A2A AgentCard for capability advertisement
 * 
 * AIDEV-NOTE: agent-card; enables agent discovery
 * - Semantic descriptions for capability matching
 * - Protocol version compatibility
 * - Resource requirements and constraints
 */
model A2AAgentCard {
  @doc("Human-readable agent description")
  description: string;
  
  @doc("List of capabilities this agent provides")
  capabilities: string[];
  
  @doc("Supported A2A protocol version")
  protocolVersion: string = "1.0";
  
  @doc("Resource requirements")
  requirements?: AgentRequirements;
  
  @doc("Additional metadata")
  metadata?: Record<unknown>;
}

model AgentRequirements {
  @doc("Minimum memory in MB")
  minMemoryMB?: int32;
  
  @doc("Required tools")
  requiredTools?: string[];
  
  @doc("Maximum concurrent tasks")
  maxConcurrentTasks?: int32;
}

// AIDEV-TODO: mcp-messages; define MCP message types
// AIDEV-TODO: a2a-messages; define A2A protocol messages
// AIDEV-TODO: protocol-bridge; MCP<->A2A translation models