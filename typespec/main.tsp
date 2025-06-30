/**
 * Julep V2 API TypeSpec Definition
 * Main entry point for TypeSpec compilation
 * 
 * AIDEV-NOTE: main-entry; TypeSpec 1.1.0 project structure
 * - Import all model definitions
 * - Configure service metadata
 * - Define API versioning strategy
 */

import "@typespec/rest";
import "@typespec/openapi";
import "@typespec/openapi3";
import "@typespec/versioning";

// Import all model definitions
import "./models/agent.tsp";
import "./models/memory.tsp";
import "./models/protocol.tsp";
import "./models/workflow.tsp";

// Import API contracts
import "./contracts/agents.tsp";
import "./contracts/memory.tsp";
import "./contracts/protocols.tsp";

using TypeSpec.Http;
using TypeSpec.Rest;
using TypeSpec.OpenAPI;
using TypeSpec.Versioning;

@service({
  title: "Julep V2 API",
  description: "Protocol-native co-agents with cognitive memory architecture"
})
@server("https://api.julep.ai", "Production API server")
@server("http://localhost:8000", "Local development server")
@versioned(Versions)
namespace JulepV2;

/**
 * API version definitions
 * AIDEV-NOTE: versioning; support multiple API versions
 */
enum Versions {
  @doc("Initial alpha release")
  v2_0_alpha: "2.0.0-alpha",
  
  @doc("Beta release with stable API")
  v2_0_beta: "2.0.0-beta",
  
  @doc("Production release")
  v2_0: "2.0.0"
}

// AIDEV-TODO: auth-definition; add OAuth2/JWT authentication specs
// AIDEV-TODO: rate-limiting; define rate limit headers and responses
// AIDEV-TODO: error-models; standardized error response models