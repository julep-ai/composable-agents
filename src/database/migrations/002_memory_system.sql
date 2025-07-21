-- Memory System Tables Migration
-- AIDEV-NOTE: memory-schema; comprehensive memory system for agent cognition

-- Enum type for memory types
CREATE TYPE memory_type AS ENUM ('episodic', 'semantic', 'implicit', 'prospective');

-- Base memory table
CREATE TABLE memory.memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
    type memory_type NOT NULL,
    
    -- Core content
    content TEXT NOT NULL,
    embedding vector(1536),
    
    -- Importance and decay
    importance FLOAT DEFAULT 0.5 CHECK (importance >= 0 AND importance <= 1),
    decayed_importance FLOAT,
    decay_rate FLOAT DEFAULT 0.95,
    
    -- Access patterns
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    source_context JSONB,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Relationships
    related_memories UUID[] DEFAULT '{}',
    
    -- Type-specific data stored in JSONB
    type_data JSONB DEFAULT '{}'
);

-- Indexes for memory
CREATE INDEX idx_memories_agent_type ON memory.memories(agent_id, type);
CREATE INDEX idx_memories_importance ON memory.memories(agent_id, decayed_importance DESC)
    WHERE decayed_importance > 0.3;
CREATE INDEX idx_memories_embedding ON memory.memories 
    USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_memories_created ON memory.memories(created_at DESC);
CREATE INDEX idx_memories_metadata ON memory.memories USING GIN(metadata);

-- Episodic memory specific view
CREATE VIEW memory.episodic_memories AS
SELECT 
    m.*,
    (type_data->>'emotionalValence')::FLOAT as emotional_valence,
    type_data->'sensoryDetails' as sensory_details,
    type_data->'temporalContext' as temporal_context
FROM memory.memories m
WHERE m.type = 'episodic';

-- Semantic memory specific view
CREATE VIEW memory.semantic_memories AS
SELECT 
    m.*,
    (type_data->>'confidence')::FLOAT as confidence,
    type_data->'concepts' as concepts,
    type_data->'relationships' as relationships
FROM memory.memories m
WHERE m.type = 'semantic';

-- Implicit memory specific view
CREATE VIEW memory.implicit_memories AS
SELECT 
    m.*,
    type_data->>'pattern' as pattern,
    (type_data->>'frequency')::INTEGER as frequency,
    (type_data->>'lastTriggered')::TIMESTAMPTZ as last_triggered
FROM memory.memories m
WHERE m.type = 'implicit';

-- Prospective memory specific view
CREATE VIEW memory.prospective_memories AS
SELECT 
    m.*,
    (type_data->>'goalId')::UUID as goal_id,
    (type_data->>'deadline')::TIMESTAMPTZ as deadline,
    (type_data->>'priority')::INTEGER as priority,
    type_data->>'status' as status,
    (type_data->'dependencies')::UUID[] as dependencies
FROM memory.memories m
WHERE m.type = 'prospective';

-- Memory relationships table
CREATE TABLE memory.relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_memory UUID NOT NULL REFERENCES memory.memories(id) ON DELETE CASCADE,
    target_memory UUID NOT NULL REFERENCES memory.memories(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,
    strength FLOAT DEFAULT 1.0 CHECK (strength >= 0 AND strength <= 1),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT unique_relationship UNIQUE(source_memory, target_memory, relationship_type)
);

CREATE INDEX idx_relationships_source ON memory.relationships(source_memory);
CREATE INDEX idx_relationships_target ON memory.relationships(target_memory);
CREATE INDEX idx_relationships_type ON memory.relationships(relationship_type);

-- ConceptNet integration table
CREATE TABLE memory.concepts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    concept VARCHAR(255) NOT NULL UNIQUE,
    embedding vector(1536),
    conceptnet_uri VARCHAR(500),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concepts_embedding ON memory.concepts 
    USING hnsw (embedding vector_cosine_ops);

-- Memory consolidation log
CREATE TABLE memory.consolidation_log (
    id SERIAL PRIMARY KEY,
    agent_id UUID NOT NULL REFERENCES agents.agents(id) ON DELETE CASCADE,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    memories_processed INTEGER DEFAULT 0,
    memories_consolidated INTEGER DEFAULT 0,
    memories_strengthened INTEGER DEFAULT 0,
    memories_decayed INTEGER DEFAULT 0,
    memories_removed INTEGER DEFAULT 0,
    error TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_consolidation_agent ON memory.consolidation_log(agent_id, started_at DESC);

-- Memory search function
CREATE OR REPLACE FUNCTION memory.search_memories(
    p_agent_id UUID,
    p_query TEXT,
    p_types memory_type[] DEFAULT NULL,
    p_limit INTEGER DEFAULT 10,
    p_threshold FLOAT DEFAULT 0.7,
    p_include_decayed BOOLEAN DEFAULT false
) RETURNS TABLE(
    memory_id UUID,
    content TEXT,
    type memory_type,
    similarity FLOAT,
    importance FLOAT,
    metadata JSONB
) AS $$
DECLARE
    query_embedding vector(1536);
BEGIN
    -- Generate embedding for query
    query_embedding := ai_generate_embedding('text-embedding-3-small', p_query);
    
    RETURN QUERY
    SELECT 
        m.id,
        m.content,
        m.type,
        1 - (m.embedding <=> query_embedding) as similarity,
        COALESCE(m.decayed_importance, m.importance) as importance,
        m.metadata
    FROM memory.memories m
    WHERE m.agent_id = p_agent_id
        AND (p_types IS NULL OR m.type = ANY(p_types))
        AND m.embedding IS NOT NULL
        AND (p_include_decayed OR COALESCE(m.decayed_importance, m.importance) > 0.1)
        AND (1 - (m.embedding <=> query_embedding)) > p_threshold
    ORDER BY similarity DESC, importance DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Memory consolidation function
CREATE OR REPLACE FUNCTION memory.consolidate_memories(
    p_agent_id UUID,
    p_types memory_type[] DEFAULT NULL,
    p_min_importance FLOAT DEFAULT 0.3
) RETURNS JSONB AS $$
DECLARE
    v_log_id INTEGER;
    v_processed INTEGER := 0;
    v_consolidated INTEGER := 0;
    v_strengthened INTEGER := 0;
    v_decayed INTEGER := 0;
    v_removed INTEGER := 0;
    v_memory RECORD;
    v_related RECORD;
    v_similarity FLOAT;
BEGIN
    -- Create consolidation log entry
    INSERT INTO memory.consolidation_log (agent_id)
    VALUES (p_agent_id)
    RETURNING id INTO v_log_id;
    
    -- Process each memory
    FOR v_memory IN
        SELECT * FROM memory.memories
        WHERE agent_id = p_agent_id
            AND (p_types IS NULL OR type = ANY(p_types))
        ORDER BY created_at DESC
    LOOP
        v_processed := v_processed + 1;
        
        -- Apply decay
        UPDATE memory.memories
        SET decayed_importance = importance * POWER(decay_rate, 
            EXTRACT(EPOCH FROM (NOW() - last_accessed_at)) / 86400)
        WHERE id = v_memory.id;
        
        -- Check if memory should be removed
        IF v_memory.decayed_importance < p_min_importance THEN
            DELETE FROM memory.memories WHERE id = v_memory.id;
            v_removed := v_removed + 1;
            CONTINUE;
        END IF;
        
        -- Find similar memories to consolidate
        FOR v_related IN
            SELECT m2.*, 
                   1 - (v_memory.embedding <=> m2.embedding) as similarity
            FROM memory.memories m2
            WHERE m2.agent_id = p_agent_id
                AND m2.id != v_memory.id
                AND m2.type = v_memory.type
                AND 1 - (v_memory.embedding <=> m2.embedding) > 0.9
            ORDER BY similarity DESC
            LIMIT 5
        LOOP
            -- Merge highly similar memories
            IF v_related.similarity > 0.95 THEN
                -- Strengthen the more important memory
                IF v_memory.importance > v_related.importance THEN
                    UPDATE memory.memories
                    SET importance = LEAST(1.0, importance + 0.1),
                        access_count = access_count + v_related.access_count
                    WHERE id = v_memory.id;
                    
                    DELETE FROM memory.memories WHERE id = v_related.id;
                    v_consolidated := v_consolidated + 1;
                END IF;
            ELSE
                -- Create relationship for related memories
                INSERT INTO memory.relationships (
                    source_memory, target_memory, 
                    relationship_type, strength
                ) VALUES (
                    v_memory.id, v_related.id,
                    'similar_to', v_related.similarity
                ) ON CONFLICT DO NOTHING;
            END IF;
        END LOOP;
    END LOOP;
    
    -- Update consolidation log
    UPDATE memory.consolidation_log
    SET completed_at = NOW(),
        memories_processed = v_processed,
        memories_consolidated = v_consolidated,
        memories_strengthened = v_strengthened,
        memories_decayed = v_decayed,
        memories_removed = v_removed
    WHERE id = v_log_id;
    
    RETURN jsonb_build_object(
        'processed', v_processed,
        'consolidated', v_consolidated,
        'strengthened', v_strengthened,
        'decayed', v_decayed,
        'removed', v_removed
    );
END;
$$ LANGUAGE plpgsql;

-- AIDEV-NOTE: memory-tables-complete; comprehensive memory system with search and consolidation