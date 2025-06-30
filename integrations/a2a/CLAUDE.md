# A2A Integration Directory Guide

<!-- AIDEV-NOTE: a2a-overview; Agent-to-Agent protocol for multi-agent collaboration -->
This directory contains A2A (Agent-to-Agent) protocol implementations, enabling agents to discover, communicate, and collaborate with each other.

## Directory Structure

- **protocol/**: Core A2A protocol implementation
- **discovery/**: Agent discovery and capability matching
- **tasks/**: Task lifecycle management
- **cards/**: AgentCard definitions and management

## A2A Protocol Overview

<!-- AIDEV-NOTE: a2a-features; extends MCP with agent-specific capabilities -->
A2A builds on MCP by adding:
- **Agent Discovery**: Find agents with specific capabilities
- **Task Management**: Create, assign, monitor multi-step tasks
- **Capability Matching**: Match task requirements to agent skills
- **State Synchronization**: Coordinate state across agents

## Implementation Guidelines

<!-- AIDEV-NOTE: a2a-patterns; best practices for agent collaboration -->
1. **AgentCards in PostgreSQL**: Store agent capabilities as JSONB
2. **Task State Machine**: Use DBOS for durable task orchestration
3. **Capability Queries**: Use pgvector for semantic capability matching
4. **Message Routing**: pgmq for reliable inter-agent messaging
5. **Protocol Bridge**: Enable MCP<->A2A communication

## Task Lifecycle

1. **Task Creation**: Define requirements and constraints
2. **Agent Matching**: Find capable agents via similarity search
3. **Task Assignment**: Assign to best-match agent(s)
4. **Execution Monitoring**: Track progress with DBOS workflows
5. **Result Aggregation**: Combine outputs from multiple agents

<!-- AIDEV-TODO: agent-card-schema; define AgentCard TypeSpec model -->
<!-- AIDEV-TODO: task-state-machine; implement task lifecycle with DBOS -->