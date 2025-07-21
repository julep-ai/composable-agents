-- Core Agent Tables Migration
-- AIDEV-NOTE: agent-schema; core tables for agent management in Julep V2

-- Enum types for agent configuration
CREATE TYPE agent_type AS ENUM ('conversational', 'task-oriented', 'research');

-- Agent main table
CREATE TABLE agents.agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type agent_type NOT NULL DEFAULT 'conversational',
    model VARCHAR(100) NOT NULL DEFAULT 'gpt-4',
    temperature FLOAT DEFAULT 0.7 CHECK (temperature >= 0 AND temperature <= 2),
    max_tokens INTEGER DEFAULT 4096 CHECK (max_tokens > 0),
    system_prompt TEXT,
    metadata JSONB DEFAULT '{}',
    
    -- Protocol configurations
    mcp_servers JSONB DEFAULT '[]',
    a2a_capabilities JSONB,
    
    -- Memory configuration
    memory_config JSONB DEFAULT '{
        "enableEpisodic": true,
        "enableSemantic": true,
        "enableImplicit": true,
        "enableProspective": true,
        "consolidationInterval": 3600,
        "decayRate": 0.95,
        "importanceThreshold": 0.3
    }',
    
    -- Metadata
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_mcp_servers CHECK (jsonb_matches_schema(
        mcp_server_array_schema(), mcp_servers
    )),
    CONSTRAINT valid_a2a_capabilities CHECK (
        a2a_capabilities IS NULL OR 
        jsonb_matches_schema(a2a_capabilities_schema(), a2a_capabilities)
    ),
    CONSTRAINT valid_memory_config CHECK (jsonb_matches_schema(
        memory_config_schema(), memory_config
    ))
);

-- Indexes for agents
CREATE INDEX idx_agents_type ON agents.agents(type);
CREATE INDEX idx_agents_active ON agents.agents(is_active) WHERE is_active = true;
CREATE INDEX idx_agents_metadata ON agents.agents USING GIN(metadata);
CREATE INDEX idx_agents_created ON agents.agents(created_at DESC);

-- Update trigger
CREATE TRIGGER update_agents_updated_at
    BEFORE UPDATE ON agents.agents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Agent sessions table
CREATE TABLE agents.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
    user_id UUID,
    
    -- Session configuration
    context_window INTEGER DEFAULT 4096,
    max_messages INTEGER DEFAULT 100,
    
    -- State
    is_active BOOLEAN DEFAULT true,
    message_count INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    
    -- Indexes
    CONSTRAINT valid_context_window CHECK (context_window > 0),
    CONSTRAINT valid_session_state CHECK (
        (is_active = true AND ended_at IS NULL) OR
        (is_active = false AND ended_at IS NOT NULL)
    )
);

CREATE INDEX idx_sessions_agent ON agents.sessions(agent_id);
CREATE INDEX idx_sessions_user ON agents.sessions(user_id);
CREATE INDEX idx_sessions_active ON agents.sessions(agent_id, is_active) WHERE is_active = true;

-- Messages table
CREATE TABLE agents.messages (
    id SERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES agents.sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'function')),
    content TEXT NOT NULL,
    
    -- Token counting
    token_count INTEGER,
    
    -- Function calls
    function_call JSONB,
    function_response JSONB,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- For memory integration
    embedding vector(1536),
    importance_score FLOAT DEFAULT 0.5
);

CREATE INDEX idx_messages_session ON agents.messages(session_id, created_at DESC);
CREATE INDEX idx_messages_embedding ON agents.messages 
    USING hnsw (embedding vector_cosine_ops) 
    WHERE embedding IS NOT NULL;

-- Helper functions for JSON schema validation
CREATE OR REPLACE FUNCTION mcp_server_array_schema() RETURNS JSONB AS $$
BEGIN
    RETURN '{
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "transport": {"enum": ["stdio", "http"]},
                "command": {"type": "string"},
                "args": {"type": "array", "items": {"type": "string"}},
                "env": {"type": "object"},
                "url": {"type": "string"},
                "headers": {"type": "object"}
            },
            "required": ["name", "transport"]
        }
    }'::jsonb;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION a2a_capabilities_schema() RETURNS JSONB AS $$
BEGIN
    RETURN '{
        "type": "object",
        "properties": {
            "capabilities": {
                "type": "array",
                "items": {"type": "string"}
            },
            "protocols": {
                "type": "array",
                "items": {"type": "string"},
                "default": ["a2a/v1"]
            },
            "authentication": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["none", "apiKey", "oauth2", "jwt"]},
                    "config": {"type": "object"}
                },
                "required": ["type"]
            },
            "endpoints": {"type": "object"}
        },
        "required": ["capabilities"]
    }'::jsonb;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION memory_config_schema() RETURNS JSONB AS $$
BEGIN
    RETURN '{
        "type": "object",
        "properties": {
            "enableEpisodic": {"type": "boolean"},
            "enableSemantic": {"type": "boolean"},
            "enableImplicit": {"type": "boolean"},
            "enableProspective": {"type": "boolean"},
            "consolidationInterval": {"type": "integer", "minimum": 60},
            "decayRate": {"type": "number", "minimum": 0, "maximum": 1},
            "importanceThreshold": {"type": "number", "minimum": 0, "maximum": 1}
        }
    }'::jsonb;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- AIDEV-NOTE: agent-tables-complete; core agent tables created with proper indexes and constraints