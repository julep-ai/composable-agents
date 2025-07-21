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

-- AIDEV-NOTE: schema-creation; create schemas for logical separation
CREATE SCHEMA IF NOT EXISTS agents;
CREATE SCHEMA IF NOT EXISTS memory;
CREATE SCHEMA IF NOT EXISTS protocols;
CREATE SCHEMA IF NOT EXISTS workflows;

-- AIDEV-NOTE: run-migrations; execute all migration files
-- Migrations are now located in src/database/migrations/
\i /app/src/database/migrations/001_initial_schema.sql
\i /app/src/database/migrations/002_memory_system.sql
\i /app/src/database/migrations/003_protocols.sql
\i /app/src/database/migrations/004_workflows.sql
\i /app/src/database/migrations/005_functions.sql

-- AIDEV-NOTE: database-initialized; Julep V2 database schema complete