-- Protocol Tables Migration
-- AIDEV-NOTE: protocol-schema; MCP and A2A protocol support tables

-- Enum type for task status
CREATE TYPE task_status AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');

-- MCP Protocol Tables

-- MCP servers registry
CREATE TABLE protocols.mcp_servers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    transport VARCHAR(20) NOT NULL CHECK (transport IN ('stdio', 'http')),
    
    -- Connection details
    command TEXT,
    args TEXT[],
    env JSONB DEFAULT '{}',
    url TEXT,
    headers JSONB DEFAULT '{}',
    
    -- State
    is_active BOOLEAN DEFAULT true,
    last_heartbeat TIMESTAMPTZ,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_server_per_agent UNIQUE(agent_id, name),
    CONSTRAINT valid_transport_config CHECK (
        (transport = 'stdio' AND command IS NOT NULL) OR
        (transport = 'http' AND url IS NOT NULL)
    )
);

CREATE INDEX idx_mcp_servers_agent ON protocols.mcp_servers(agent_id);
CREATE INDEX idx_mcp_servers_active ON protocols.mcp_servers(is_active) WHERE is_active = true;

-- MCP tools registry
CREATE TABLE protocols.mcp_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    input_schema JSONB NOT NULL,
    enabled BOOLEAN DEFAULT true,
    
    -- Usage statistics
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    avg_duration_ms INTEGER,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_tool_per_server UNIQUE(server_id, name),
    CONSTRAINT valid_input_schema CHECK (
        jsonb_typeof(input_schema) = 'object' AND
        input_schema ? 'type' AND
        input_schema->>'type' = 'object'
    )
);

CREATE INDEX idx_mcp_tools_server ON protocols.mcp_tools(server_id);
CREATE INDEX idx_mcp_tools_enabled ON protocols.mcp_tools(enabled) WHERE enabled = true;

-- MCP resources registry
CREATE TABLE protocols.mcp_resources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
    uri TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    mime_type VARCHAR(100),
    
    -- Caching
    cached_content TEXT,
    cached_at TIMESTAMPTZ,
    cache_ttl INTEGER DEFAULT 3600, -- seconds
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_resource_per_server UNIQUE(server_id, uri)
);

CREATE INDEX idx_mcp_resources_server ON protocols.mcp_resources(server_id);

-- MCP prompts registry
CREATE TABLE protocols.mcp_prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    server_id UUID NOT NULL REFERENCES protocols.mcp_servers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    arguments JSONB DEFAULT '[]',
    template TEXT NOT NULL,
    
    -- Usage
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMPTZ,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_prompt_per_server UNIQUE(server_id, name)
);

CREATE INDEX idx_mcp_prompts_server ON protocols.mcp_prompts(server_id);

-- MCP message log (uses pgmq for actual queuing)
CREATE TABLE protocols.mcp_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(20) NOT NULL CHECK (type IN ('request', 'response', 'notification')),
    method VARCHAR(255) NOT NULL,
    params JSONB,
    result JSONB,
    error JSONB,
    
    source_agent UUID NOT NULL REFERENCES agents.agents(id),
    target_agent UUID REFERENCES agents.agents(id),
    
    -- Message tracking
    correlation_id UUID,
    queue_message_id BIGINT, -- pgmq message id
    
    -- Timing
    created_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    duration_ms INTEGER,
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (
        status IN ('pending', 'queued', 'processing', 'completed', 'failed')
    )
);

CREATE INDEX idx_mcp_messages_source ON protocols.mcp_messages(source_agent);
CREATE INDEX idx_mcp_messages_target ON protocols.mcp_messages(target_agent);
CREATE INDEX idx_mcp_messages_correlation ON protocols.mcp_messages(correlation_id);
CREATE INDEX idx_mcp_messages_created ON protocols.mcp_messages(created_at DESC);

-- A2A Protocol Tables

-- A2A agent registry (AgentCards)
CREATE TABLE protocols.a2a_agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
    
    -- AgentCard data
    capabilities TEXT[] NOT NULL,
    protocols TEXT[] DEFAULT ARRAY['a2a/v1'],
    authentication JSONB,
    endpoints JSONB DEFAULT '{}',
    
    -- Discovery
    is_public BOOLEAN DEFAULT false,
    discovery_metadata JSONB DEFAULT '{}',
    
    -- State
    is_active BOOLEAN DEFAULT true,
    last_seen TIMESTAMPTZ DEFAULT NOW(),
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_a2a_agent UNIQUE(agent_id)
);

CREATE INDEX idx_a2a_agents_public ON protocols.a2a_agents(is_public) WHERE is_public = true;
CREATE INDEX idx_a2a_agents_capabilities ON protocols.a2a_agents USING GIN(capabilities);

-- A2A tasks
CREATE TABLE protocols.a2a_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_agent UUID NOT NULL REFERENCES agents.agents(id),
    remote_agent UUID NOT NULL REFERENCES agents.agents(id),
    
    -- Task details
    name VARCHAR(255) NOT NULL,
    description TEXT,
    input JSONB,
    
    -- Status tracking
    status task_status NOT NULL DEFAULT 'pending',
    progress FLOAT DEFAULT 0 CHECK (progress >= 0 AND progress <= 1),
    
    -- Timing
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Results
    output JSONB,
    error JSONB,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_a2a_tasks_client ON protocols.a2a_tasks(client_agent);
CREATE INDEX idx_a2a_tasks_remote ON protocols.a2a_tasks(remote_agent);
CREATE INDEX idx_a2a_tasks_status ON protocols.a2a_tasks(status);
CREATE INDEX idx_a2a_tasks_created ON protocols.a2a_tasks(created_at DESC);

-- A2A artifacts
CREATE TABLE protocols.a2a_artifacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES protocols.a2a_tasks(id) ON DELETE CASCADE,
    
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    content TEXT,
    url TEXT,
    size_bytes BIGINT,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_a2a_artifacts_task ON protocols.a2a_artifacts(task_id);

-- A2A messages
CREATE TABLE protocols.a2a_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES protocols.a2a_tasks(id) ON DELETE CASCADE,
    sender VARCHAR(10) NOT NULL CHECK (sender IN ('client', 'remote')),
    
    content TEXT NOT NULL,
    parts JSONB DEFAULT '[]',
    
    -- Tracking
    queue_message_id BIGINT, -- pgmq message id
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    delivered_at TIMESTAMPTZ
);

CREATE INDEX idx_a2a_messages_task ON protocols.a2a_messages(task_id, created_at);

-- Protocol integration functions

-- Function to execute MCP tool
CREATE OR REPLACE FUNCTION protocols.execute_mcp_tool(
    p_tool_name VARCHAR,
    p_input JSONB,
    p_agent_id UUID
) RETURNS JSONB AS $$
DECLARE
    v_tool RECORD;
    v_message_id UUID;
    v_result JSONB;
    v_start_time TIMESTAMPTZ;
    v_duration_ms INTEGER;
BEGIN
    v_start_time := clock_timestamp();
    
    -- Find the tool
    SELECT t.*, s.transport, s.url, s.command, s.args
    INTO v_tool
    FROM protocols.mcp_tools t
    JOIN protocols.mcp_servers s ON t.server_id = s.id
    WHERE t.name = p_tool_name
        AND t.enabled = true
        AND s.is_active = true
        AND s.agent_id = p_agent_id
    LIMIT 1;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Tool % not found for agent %', p_tool_name, p_agent_id;
    END IF;
    
    -- Validate input against schema
    IF NOT jsonb_matches_schema(v_tool.input_schema, p_input) THEN
        RAISE EXCEPTION 'Invalid input for tool %', p_tool_name;
    END IF;
    
    -- Create MCP message
    INSERT INTO protocols.mcp_messages (
        type, method, params, source_agent
    ) VALUES (
        'request', 'tools/execute', 
        jsonb_build_object('tool', p_tool_name, 'input', p_input),
        p_agent_id
    ) RETURNING id INTO v_message_id;
    
    -- Queue the message
    SELECT pgmq.send(
        'mcp_messages',
        jsonb_build_object(
            'message_id', v_message_id,
            'tool_id', v_tool.id,
            'server_id', v_tool.server_id,
            'input', p_input
        )
    );
    
    -- For prototype, simulate execution
    -- In production, this would wait for actual execution
    v_result := jsonb_build_object(
        'output', jsonb_build_object('result', 'Tool executed successfully'),
        'duration_ms', 100
    );
    
    -- Update tool usage statistics
    v_duration_ms := EXTRACT(MILLISECONDS FROM clock_timestamp() - v_start_time);
    
    UPDATE protocols.mcp_tools
    SET usage_count = usage_count + 1,
        last_used_at = NOW(),
        avg_duration_ms = CASE
            WHEN avg_duration_ms IS NULL THEN v_duration_ms
            ELSE (avg_duration_ms * usage_count + v_duration_ms) / (usage_count + 1)
        END
    WHERE id = v_tool.id;
    
    -- Update message
    UPDATE protocols.mcp_messages
    SET status = 'completed',
        result = v_result,
        processed_at = NOW(),
        duration_ms = v_duration_ms
    WHERE id = v_message_id;
    
    RETURN v_result;
END;
$$ LANGUAGE plpgsql;

-- Function to discover A2A agents
CREATE OR REPLACE FUNCTION protocols.discover_a2a_agents(
    p_capabilities TEXT[] DEFAULT NULL
) RETURNS TABLE(
    agent_id UUID,
    name VARCHAR,
    capabilities TEXT[],
    protocols TEXT[],
    endpoints JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        ag.name,
        a.capabilities,
        a.protocols,
        a.endpoints
    FROM protocols.a2a_agents a
    JOIN agents.agents ag ON a.agent_id = ag.id
    WHERE a.is_public = true
        AND a.is_active = true
        AND ag.is_active = true
        AND (p_capabilities IS NULL OR 
             a.capabilities && p_capabilities) -- Array overlap
    ORDER BY a.last_seen DESC;
END;
$$ LANGUAGE plpgsql;

-- AIDEV-NOTE: protocol-tables-complete; MCP and A2A protocol support implemented