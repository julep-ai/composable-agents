/**
 * Agent API contracts
 * RESTful endpoints for agent management
 */

import "@typespec/rest";
import "@typespec/http";
import "../models/agent.tsp";

using TypeSpec.Rest;
using TypeSpec.Http;

namespace JulepV2;

/**
 * Agent management interface
 * 
 * AIDEV-NOTE: agent-api; CRUD operations for agents
 * - Standard REST patterns with TypeSpec
 * - Automatic OpenAPI generation
 * - Type-safe client SDK generation
 */
@route("/agents")
interface Agents {
  @doc("List all agents with optional filtering")
  @get
  list(
    @query type?: AgentType,
    @query limit?: int32 = 50,
    @query offset?: int32 = 0
  ): {
    @body agents: Agent[];
    total: int32;
  };
  
  @doc("Create a new agent")
  @post
  create(@body agent: {
    name: string;
    type: AgentType;
    mcpServers?: MCPServerConfig[];
    a2aCard?: A2AAgentCard;
  }): {
    @statusCode statusCode: 201;
    @body agent: Agent;
  };
  
  @doc("Get agent by ID")
  @get
  read(@path id: uuid): Agent | {
    @statusCode statusCode: 404;
    @body error: {
      message: string;
    };
  };
  
  @doc("Update agent")
  @patch
  update(
    @path id: uuid,
    @body patch: {
      name?: string;
      mcpServers?: MCPServerConfig[];
      a2aCard?: A2AAgentCard;
    }
  ): Agent;
  
  @doc("Delete agent")
  @delete
  delete(@path id: uuid): {
    @statusCode statusCode: 204;
  };
}

// AIDEV-TODO: agent-search; vector similarity search for agents
// AIDEV-TODO: agent-stats; performance metrics endpoints
// AIDEV-TODO: agent-export; bulk export/import operations