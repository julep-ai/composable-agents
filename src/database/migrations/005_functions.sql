-- Helper Functions and Triggers Migration
-- AIDEV-NOTE: helper-functions; utility functions for the database

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Token counting function (placeholder - use tiktoken in Python)
CREATE OR REPLACE FUNCTION count_tokens(
    p_model VARCHAR,
    p_text TEXT
) RETURNS INTEGER AS $$
BEGIN
    -- Rough approximation: 1 token per 4 characters
    -- In production, call Python tiktoken via plpython3u
    RETURN CEIL(LENGTH(p_text) / 4.0);
END;
$$ LANGUAGE plpgsql;

-- Generate embedding placeholder function
-- In production, this would call the actual embedding API
CREATE OR REPLACE FUNCTION ai_generate_embedding(
    p_model VARCHAR,
    p_content TEXT
) RETURNS vector(1536) AS $$
DECLARE
    v_embedding FLOAT[];
    i INTEGER;
BEGIN
    -- Generate a dummy embedding for development
    -- In production, this would call OpenAI/other embedding API
    v_embedding := ARRAY[]::FLOAT[];
    FOR i IN 1..1536 LOOP
        v_embedding := array_append(v_embedding, random()::FLOAT);
    END LOOP;
    
    RETURN v_embedding::vector(1536);
END;
$$ LANGUAGE plpgsql;

-- Generate embedding with caching
CREATE OR REPLACE FUNCTION generate_embedding_cached(
    p_model VARCHAR,
    p_content TEXT
) RETURNS vector(1536) AS $$
DECLARE
    v_cache_key VARCHAR;
    v_embedding vector(1536);
BEGIN
    -- Create cache key
    v_cache_key := MD5(p_model || ':' || p_content);
    
    -- Check cache (in production, use a proper cache table)
    -- For now, always generate
    v_embedding := ai_generate_embedding(p_model, p_content);
    
    RETURN v_embedding;
END;
$$ LANGUAGE plpgsql;

-- Agent activity tracking
CREATE OR REPLACE FUNCTION track_agent_activity()
RETURNS TRIGGER AS $$
BEGIN
    -- Update agent last activity
    UPDATE agents.agents
    SET updated_at = NOW(),
        metadata = metadata || jsonb_build_object(
            'last_activity', NOW(),
            'total_sessions', COALESCE((metadata->>'total_sessions')::int, 0) + 1
        )
    WHERE id = NEW.agent_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER track_session_activity
    AFTER INSERT ON agents.sessions
    FOR EACH ROW
    EXECUTE FUNCTION track_agent_activity();

-- Memory importance calculation
CREATE OR REPLACE FUNCTION calculate_memory_importance(
    p_content TEXT,
    p_emotional_valence FLOAT DEFAULT NULL,
    p_access_count INTEGER DEFAULT 0,
    p_age_days FLOAT DEFAULT 0
) RETURNS FLOAT AS $$
DECLARE
    v_base_importance FLOAT;
    v_emotional_factor FLOAT;
    v_access_factor FLOAT;
    v_recency_factor FLOAT;
BEGIN
    -- Base importance from content length and complexity
    v_base_importance := LEAST(1.0, LENGTH(p_content) / 1000.0);
    
    -- Emotional factor (if provided)
    v_emotional_factor := CASE
        WHEN p_emotional_valence IS NULL THEN 1.0
        ELSE 1.0 + (ABS(p_emotional_valence) * 0.5)
    END;
    
    -- Access factor (logarithmic)
    v_access_factor := CASE
        WHEN p_access_count = 0 THEN 1.0
        ELSE 1.0 + (LN(p_access_count + 1) * 0.1)
    END;
    
    -- Recency factor (exponential decay)
    v_recency_factor := POWER(0.95, p_age_days);
    
    -- Combine factors
    RETURN LEAST(1.0, v_base_importance * v_emotional_factor * v_access_factor * v_recency_factor);
END;
$$ LANGUAGE plpgsql;

-- JSON schema validation placeholder
-- In production, use pg_jsonschema extension
CREATE OR REPLACE FUNCTION jsonb_matches_schema(
    p_schema JSONB,
    p_data JSONB
) RETURNS BOOLEAN AS $$
BEGIN
    -- Placeholder implementation
    -- In production, this would use pg_jsonschema extension:
    -- RETURN jsonb_matches_schema(p_schema::json, p_data::json);
    
    -- For now, just check that data is not null
    RETURN p_data IS NOT NULL;
END;
$$ LANGUAGE plpgsql;

-- Message queue initialization
-- Create pgmq queues for protocol messages
DO $$
BEGIN
    -- Create MCP message queue
    PERFORM pgmq.create('mcp_messages');
    
    -- Create A2A message queue
    PERFORM pgmq.create('a2a_messages');
    
    -- Create workflow event queue
    PERFORM pgmq.create('workflow_events');
EXCEPTION
    WHEN duplicate_table THEN
        -- Queues already exist
        NULL;
END $$;

-- AIDEV-NOTE: helper-functions-complete; utility functions and triggers created