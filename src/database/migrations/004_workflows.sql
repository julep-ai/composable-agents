-- Workflow Tables Migration (DBOS)
-- AIDEV-NOTE: workflow-schema; DBOS-compatible workflow state management

-- Workflow definitions
CREATE TABLE workflows.workflow_definitions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    version INTEGER NOT NULL DEFAULT 1,
    
    -- Workflow configuration
    steps JSONB NOT NULL,
    retry_policy JSONB DEFAULT '{
        "max_attempts": 3,
        "backoff_multiplier": 2,
        "initial_interval": 1000
    }',
    
    -- Metadata
    description TEXT,
    tags TEXT[] DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_workflow_defs_name ON workflows.workflow_definitions(name);
CREATE INDEX idx_workflow_defs_active ON workflows.workflow_definitions(is_active) WHERE is_active = true;

-- Workflow instances
CREATE TABLE workflows.workflow_instances (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    definition_id UUID NOT NULL REFERENCES workflows.workflow_definitions(id),
    agent_id UUID NOT NULL REFERENCES agents.agents(id),
    
    -- State
    status VARCHAR(20) DEFAULT 'pending' CHECK (
        status IN ('pending', 'running', 'completed', 'failed', 'cancelled', 'suspended')
    ),
    current_step VARCHAR(255),
    context JSONB DEFAULT '{}',
    
    -- Timing
    created_at TIMESTAMPTZ DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Error handling
    error JSONB,
    retry_count INTEGER DEFAULT 0,
    
    -- Results
    output JSONB,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_workflow_instances_agent ON workflows.workflow_instances(agent_id);
CREATE INDEX idx_workflow_instances_status ON workflows.workflow_instances(status);
CREATE INDEX idx_workflow_instances_created ON workflows.workflow_instances(created_at DESC);

-- Workflow step executions
CREATE TABLE workflows.step_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    instance_id UUID NOT NULL REFERENCES workflows.workflow_instances(id) ON DELETE CASCADE,
    step_name VARCHAR(255) NOT NULL,
    
    -- Execution details
    status VARCHAR(20) DEFAULT 'pending' CHECK (
        status IN ('pending', 'running', 'completed', 'failed', 'skipped')
    ),
    input JSONB,
    output JSONB,
    error JSONB,
    
    -- Timing
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_ms INTEGER,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_step_executions_instance ON workflows.step_executions(instance_id);
CREATE INDEX idx_step_executions_status ON workflows.step_executions(status);

-- Common workflow: Memory consolidation
INSERT INTO workflows.workflow_definitions (name, description, steps) VALUES (
    'memory_consolidation',
    'Consolidate and organize agent memories',
    '{
        "steps": [
            {
                "name": "fetch_memories",
                "type": "function",
                "function": "memory.fetch_recent_memories",
                "next": "calculate_importance"
            },
            {
                "name": "calculate_importance",
                "type": "function", 
                "function": "memory.calculate_importance_scores",
                "next": "apply_decay"
            },
            {
                "name": "apply_decay",
                "type": "function",
                "function": "memory.apply_decay_function",
                "next": "find_similar"
            },
            {
                "name": "find_similar",
                "type": "function",
                "function": "memory.find_similar_memories",
                "next": "consolidate"
            },
            {
                "name": "consolidate",
                "type": "function",
                "function": "memory.consolidate_similar",
                "next": "update_graph"
            },
            {
                "name": "update_graph",
                "type": "function",
                "function": "memory.update_relationship_graph",
                "next": null
            }
        ]
    }'::jsonb
);

-- Common workflow: Agent conversation
INSERT INTO workflows.workflow_definitions (name, description, steps) VALUES (
    'agent_conversation',
    'Handle a conversation turn with memory integration',
    '{
        "steps": [
            {
                "name": "retrieve_context",
                "type": "function",
                "function": "memory.retrieve_relevant_memories",
                "next": "generate_response"
            },
            {
                "name": "generate_response",
                "type": "function",
                "function": "agents.generate_llm_response",
                "next": "extract_memories"
            },
            {
                "name": "extract_memories",
                "type": "function",
                "function": "memory.extract_memories_from_response",
                "next": "store_memories"
            },
            {
                "name": "store_memories",
                "type": "function",
                "function": "memory.store_new_memories",
                "next": "update_goals"
            },
            {
                "name": "update_goals",
                "type": "function",
                "function": "memory.update_prospective_memories",
                "next": null
            }
        ]
    }'::jsonb
);

-- AIDEV-NOTE: workflow-tables-complete; DBOS-compatible workflow management implemented