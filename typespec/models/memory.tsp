/**
 * Memory system TypeSpec definitions
 * Four cognitive memory types inspired by human cognition
 */

import "@typespec/rest";

using TypeSpec.Rest;

namespace JulepV2;

/**
 * Base memory entry shared by all memory types
 * 
 * AIDEV-NOTE: memory-base; common fields for all memories
 * - Vector embeddings for similarity search
 * - Importance scores that decay over time
 * - Metadata for flexible storage
 */
@resource("memories")
model Memory {
  @key
  @visibility("read")
  id: uuid;
  
  @doc("Agent that owns this memory")
  agentId: uuid;
  
  @doc("Type of memory: episodic, semantic, implicit, or prospective")
  type: MemoryType;
  
  @doc("Vector embedding for similarity search (1536 dimensions)")
  embedding?: float32[];
  
  @doc("Importance score that decays over time")
  @minValue(0)
  @maxValue(1)
  importance: float32 = 0.5;
  
  @doc("Memory content and metadata")
  content: unknown;
  
  @visibility("read")
  createdAt: utcDateTime;
  
  @visibility("read")
  lastAccessedAt: utcDateTime;
}

enum MemoryType {
  @doc("Temporal sequences with full context")
  episodic: "episodic",
  
  @doc("Factual knowledge and concepts")
  semantic: "semantic",
  
  @doc("Unconscious patterns and biases")
  implicit: "implicit",
  
  @doc("Future goals and intentions")
  prospective: "prospective"
}

// AIDEV-TODO: episodic-model; add emotional valence and temporal context
// AIDEV-TODO: semantic-model; add knowledge graph relationships
// AIDEV-TODO: implicit-model; add behavior pattern tracking
// AIDEV-TODO: prospective-model; add goal hierarchy and dependencies