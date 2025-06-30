# MCP Integration Directory Guide

<!-- AIDEV-NOTE: mcp-overview; Model Context Protocol server/client implementations -->
This directory contains MCP (Model Context Protocol) integrations for Julep V2, enabling agents to connect with external tools and resources.

## Directory Structure

- **servers/**: MCP server implementations for exposing Julep capabilities
- **clients/**: MCP client implementations for connecting to external servers
- **registry/**: Tool and resource registry management
- **examples/**: Example MCP configurations and usage patterns

## MCP Protocol Overview

<!-- AIDEV-NOTE: mcp-protocol; standardized tool/resource access for LLMs -->
MCP provides a standardized way for LLMs to access:
- **Tools**: Executable functions with defined inputs/outputs
- **Resources**: Data sources like files, databases, APIs
- **Prompts**: Reusable prompt templates

## Implementation Guidelines

<!-- AIDEV-NOTE: mcp-patterns; best practices for MCP integration -->
1. **Database-backed Registry**: Store tool/resource definitions in PostgreSQL
2. **Message Queue**: Use pgmq for reliable message delivery
3. **Async Communication**: All MCP operations should be async
4. **Error Handling**: Implement proper error codes per MCP spec
5. **Security**: Validate all tool inputs and sandbox execution

## Performance Considerations

- Tool discovery should complete in <10ms
- Tool execution timeout: 30s default, configurable
- Resource streaming for large data transfers
- Connection pooling for external MCP servers

<!-- AIDEV-TODO: mcp-server-example; add example MCP server implementation -->
<!-- AIDEV-TODO: mcp-client-example; add example MCP client usage -->