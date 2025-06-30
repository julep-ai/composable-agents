/**
 * Protocol API contracts
 * MCP and A2A protocol endpoints
 */

import "@typespec/rest";
import "@typespec/http";
import "../models/protocol.tsp";
import "../models/workflow.tsp";

using TypeSpec.Rest;
using TypeSpec.Http;

namespace JulepV2;

/**
 * MCP tool management interface
 * 
 * AIDEV-NOTE: mcp-api; tool discovery and execution
 * - Tool registration from MCP servers
 * - Async tool execution with timeouts
 * - Result streaming for long operations
 */
@route("/mcp")
interface MCPProtocol {
  @doc("List available MCP tools")
  @get
  @route("tools")
  listTools(
    @query serverId?: uuid,
    @query enabled?: boolean = true
  ): {
    @body tools: MCPTool[];
  };
  
  @doc("Execute an MCP tool")
  @post
  @route("tools/{toolId}/execute")
  executeTool(
    @path toolId: uuid,
    @body input: unknown
  ): {
    @statusCode statusCode: 200;
    @body result: unknown;
  } | {
    @statusCode statusCode: 202;
    @body execution: {
      executionId: uuid;
      status: "pending";
    };
  };
}

/**
 * A2A protocol interface
 * 
 * AIDEV-NOTE: a2a-api; agent discovery and task management
 * - Agent capability matching
 * - Task assignment and monitoring
 * - Multi-agent coordination
 */
@route("/a2a")
interface A2AProtocol {
  @doc("Discover agents with specific capabilities")
  @post
  @route("agents/discover")
  discoverAgents(
    @body query: {
      requiredCapabilities: string[];
      limit?: int32 = 10;
    }
  ): {
    @body agents: {
      agentId: uuid;
      name: string;
      card: A2AAgentCard;
      matchScore: float32;
    }[];
  };
  
  @doc("Create a new task for agents")
  @post
  @route("tasks")
  createTask(@body task: {
    title: string;
    description: string;
    requiredCapabilities: string[];
    priority?: TaskPriority;
    dueDate?: utcDateTime;
  }): {
    @statusCode statusCode: 201;
    @body task: Task;
  };
  
  @doc("Assign task to agents")
  @post
  @route("tasks/{taskId}/assign")
  assignTask(
    @path taskId: uuid,
    @body assignment: {
      agentIds: uuid[];
    }
  ): Task;
}

// AIDEV-TODO: protocol-events; SSE for real-time updates
// AIDEV-TODO: protocol-metrics; performance monitoring
// AIDEV-TODO: protocol-bridge; MCP<->A2A translation