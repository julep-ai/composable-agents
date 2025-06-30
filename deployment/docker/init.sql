-- PostgreSQL initialization script for Julep V2
-- Creates required extensions and initial schema

-- AIDEV-NOTE: postgres-extensions; required for Julep V2 functionality
-- pgvector: Vector similarity search with HNSW indexing
-- pgmq: Message queue for MCP/A2A protocol messages
-- pg_stat_statements: Query performance monitoring
-- uuid-ossp: UUID generation for primary keys

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pgmq";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- AIDEV-NOTE: pgvector-config; optimal settings for HNSW performance
-- Based on pgvector 0.8.0 best practices (November 2024)
ALTER SYSTEM SET maintenance_work_mem = '2GB';
ALTER SYSTEM SET max_parallel_maintenance_workers = 4;
ALTER SYSTEM SET shared_buffers = '4GB';
ALTER SYSTEM SET effective_cache_size = '12GB';

-- Enable iterative scanning for better filtering performance
ALTER SYSTEM SET hnsw.iterative_scan = on;
ALTER SYSTEM SET ivfflat.iterative_scan = on;

-- AIDEV-TODO: schema-creation; create schemas for logical separation
CREATE SCHEMA IF NOT EXISTS agents;
CREATE SCHEMA IF NOT EXISTS memory;
CREATE SCHEMA IF NOT EXISTS protocols;
CREATE SCHEMA IF NOT EXISTS workflows;

-- AIDEV-TODO: base-tables; create core tables with proper indexes
-- Example agent table with vector embedding
CREATE TABLE IF NOT EXISTS agents.agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('conversational', 'task-oriented', 'research')),
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- AIDEV-NOTE: hnsw-index; create after data load for better performance
-- CREATE INDEX agents_embedding_idx ON agents.agents 
-- USING hnsw (embedding vector_l2_ops) 
-- WITH (m = 16, ef_construction = 64);

-- AIDEV-TODO: memory-tables; create tables for 4 memory types
-- AIDEV-TODO: protocol-tables; MCP and A2A message storage
-- AIDEV-TODO: workflow-tables; DBOS workflow state management