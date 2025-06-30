/**
 * Memory API contracts
 * Cognitive memory system endpoints
 */

import "@typespec/rest";
import "@typespec/http";
import "../models/memory.tsp";

using TypeSpec.Rest;
using TypeSpec.Http;

namespace JulepV2;

/**
 * Memory management interface
 * 
 * AIDEV-NOTE: memory-api; cognitive memory operations
 * - Vector similarity search with pgvector
 * - Memory consolidation triggers
 * - Bulk operations for efficiency
 */
@route("/agents/{agentId}/memories")
interface Memories {
  @doc("Search memories using vector similarity")
  @post
  @route("search")
  search(
    @path agentId: uuid,
    @body request: {
      query: string;
      memoryTypes?: MemoryType[];
      limit?: int32 = 10;
      minImportance?: float32 = 0.0;
    }
  ): {
    @body memories: Memory[];
    @header("X-Search-Time-Ms") searchTime: int32;
  };
  
  @doc("Store a new memory")
  @post
  store(
    @path agentId: uuid,
    @body memory: {
      type: MemoryType;
      content: unknown;
      importance?: float32;
    }
  ): {
    @statusCode statusCode: 201;
    @body memory: Memory;
  };
  
  @doc("Retrieve memory by ID")
  @get
  @route("{memoryId}")
  retrieve(
    @path agentId: uuid,
    @path memoryId: uuid
  ): Memory;
  
  @doc("Trigger memory consolidation")
  @post
  @route("consolidate")
  consolidate(
    @path agentId: uuid,
    @body options?: {
      decayFactor?: float32;
      strengthenThreshold?: float32;
    }
  ): {
    @statusCode statusCode: 202;
    @body workflow: {
      workflowId: uuid;
      status: string;
    };
  };
}

// AIDEV-TODO: memory-bulk; batch operations for efficiency
// AIDEV-TODO: memory-export; memory backup and restore
// AIDEV-TODO: memory-analytics; memory usage patterns