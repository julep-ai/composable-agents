# Julep v2 Cloud Platform - Complete User Guide

<!-- AIDEV-NOTE: comprehensive-guide; complete documentation for Julep v2 cloud platform -->
## Table of Contents

1.  [Introduction](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#introduction)
2.  [Getting Started](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#getting-started)
3.  [Authentication](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#authentication)
4.  [Creating and Managing Agents](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#creating-and-managing-agents)
5.  [Understanding the Memory System](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#understanding-the-memory-system)
6.  [Conversations and Sessions](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#conversations-and-sessions)
7.  [Tools and Integrations (MCP)](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#tools-and-integrations-mcp)
8.  [Multi-Agent Collaboration (A2A)](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#multi-agent-collaboration-a2a)
9.  [Workflows and Automation](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#workflows-and-automation)
10.  [Advanced Features](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#advanced-features)
11.  [API Reference](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#api-reference)
12.  [Best Practices](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#best-practices)
13.  [Pricing and Limits](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#pricing-and-limits)
14.  [Troubleshooting](https://claude.ai/public/artifacts/5423bc7d-8a4d-4316-8b37-39ae4e944344#troubleshooting)

* * *

## 1\. Introduction {#introduction}

<!-- AIDEV-NOTE: platform-intro; revolutionary postgres-native AI agent platform -->
Welcome to **Julep v2**, a revolutionary cloud-based AI agent platform that reimagines how intelligent agents are built and deployed. Unlike traditional AI platforms that rely on complex microservices, Julep v2 leverages a PostgreSQL-native architecture to deliver:

-   **⚡ 8-40x faster performance** compared to traditional architectures
-   **🧠 Advanced cognitive memory system** with four distinct memory types
-   **🔧 100+ built-in tool integrations** via MCP (Model Context Protocol)
-   **🤝 Multi-agent collaboration** through A2A (Agent-to-Agent) protocol
-   **🛡️ Enterprise-grade security** with ACID compliance
-   **💰 Cost-efficient operations** with transparent pricing

### What Makes Julep v2 Different?

<!-- AIDEV-NOTE: paradigm-shift; unified postgres architecture vs distributed microservices -->
Julep v2 is built on a paradigm shift: instead of distributed microservices, all agent capabilities—memory, tools, workflows, and collaboration—are implemented directly within PostgreSQL using modern extensions. This means:

1.  **No network overhead** between services
2.  **Guaranteed data consistency** for all operations
3.  **Simplified architecture** that's easier to understand and debug
4.  **Native support for complex queries** across agent data

### Who Should Use Julep v2?

-   **Developers** building conversational AI applications
-   **Enterprises** needing reliable, scalable AI agents
-   **Researchers** exploring cognitive architectures
-   **Teams** requiring multi-agent collaboration
-   **Anyone** wanting stateful, intelligent AI assistants

* * *

## 2\. Getting Started {#getting-started}

### Step 1: Create Your Account

1.  Navigate to [https://api.julep.cloud](https://api.julep.cloud/)
2.  Click "Sign Up" and provide:
    -   Email address
    -   Strong password
    -   Organization name (optional)
3.  Verify your email address
4.  Complete your profile setup

### Step 2: Access Your Dashboard

After signing in, you'll see your dashboard with:

-   **Agents Overview**: List of your AI agents
-   **Usage Metrics**: Token usage, costs, and performance stats
-   **API Keys**: Manage authentication credentials
-   **Billing**: View and manage subscription
-   **Documentation**: Quick links to guides

### Step 3: Generate Your First API Key

1.  Navigate to **Settings → API Keys**
2.  Click **"Create New API Key"**
3.  Provide a descriptive name (e.g., "Development", "Production")
4.  Set permissions:
    -   **Read**: View agents, sessions, and memories
    -   **Write**: Create and modify resources
    -   **Delete**: Remove resources
5.  Copy your API key immediately (it won't be shown again!)

bash

    # Example API key format
    julep_pk_550e8400-e29b-41d4-a716-446655440000

### Step 4: Install the SDK (Optional)

While you can use Julep v2 via direct HTTP requests, we provide SDKs for easier integration:

bash

    # Python
    pip install julep-cloud
    
    # JavaScript/TypeScript
    npm install @julep/cloud-sdk
    
    # Go
    go get github.com/julep-ai/julep-go

### Step 5: Test Your Connection

python

    # Python example
    from julep import JulepClient
    
    client = JulepClient(api_key="your_api_key_here")
    
    # Test connection
    try:
        agents = client.agents.list()
        print(f"Connected! You have {len(agents)} agents.")
    except Exception as e:
        print(f"Connection failed: {e}")

* * *

## 3\. Authentication {#authentication}

### API Key Authentication

Julep v2 uses API keys for authentication. Include your key in all requests:

http

    Authorization: Bearer julep_pk_your_api_key_here

Or using the `X-API-Key` header:

http

    X-API-Key: julep_pk_your_api_key_here

### API Key Best Practices

1.  **Never commit keys to version control**
    
    bash
    
        # .env file
        JULEP_API_KEY=julep_pk_your_api_key_here
    
2.  **Use different keys for different environments**
    -   Development: Limited permissions, rate limits
    -   Staging: Production-like but isolated
    -   Production: Full permissions, monitoring enabled
3.  **Rotate keys regularly**
    -   Set calendar reminders for key rotation
    -   Use the API to programmatically rotate keys
    -   Update all applications when rotating
4.  **Monitor key usage**
    -   Check dashboard for unusual activity
    -   Set up alerts for anomalous usage
    -   Review access logs regularly

### OAuth 2.0 (Enterprise)

Enterprise customers can configure OAuth 2.0 for SSO integration:

javascript

    // OAuth configuration example
    {
      "auth_type": "oauth2",
      "client_id": "your_client_id",
      "client_secret": "your_client_secret",
      "auth_url": "https://your-idp.com/oauth/authorize",
      "token_url": "https://your-idp.com/oauth/token",
      "scopes": ["agents:read", "agents:write", "sessions:manage"]
    }

* * *

## 4\. Creating and Managing Agents {#creating-and-managing-agents}

### Understanding Agent Types

Julep v2 supports four primary agent types:

1.  **Conversational Agents**: General-purpose chat agents
2.  **Task-Oriented Agents**: Focused on specific tasks
3.  **Research Agents**: Specialized in information gathering
4.  **Coordinator Agents**: Orchestrate other agents

### Creating Your First Agent

python

    # Python SDK example
    agent = client.agents.create(
        name="Customer Support Assistant",
        type="conversational",
        model="gpt-4",
        temperature=0.7,
        system_prompt="""You are a helpful customer support assistant for ACME Corp.
        Always be polite, professional, and try to resolve customer issues efficiently.
        You have access to customer data and can help with orders, returns, and general inquiries.""",
        memory_config={
            "enable_episodic": True,      # Remember conversations
            "enable_semantic": True,      # Store factual knowledge
            "enable_implicit": True,      # Learn behavioral patterns
            "enable_prospective": True,   # Track goals and tasks
            "consolidation_interval": 3600  # Consolidate memories hourly
        },
        metadata={
            "department": "customer_service",
            "language": "en",
            "timezone": "America/New_York"
        }
    )
    
    print(f"Created agent: {agent.id}")

### Direct API Example

bash

    curl -X POST https://api.julep.cloud/v1/agents \
      -H "Authorization: Bearer julep_pk_your_api_key" \
      -H "Content-Type: application/json" \
      -d '{
        "name": "Research Assistant",
        "type": "research",
        "model": "gpt-4",
        "temperature": 0.3,
        "system_prompt": "You are an expert research assistant...",
        "memory_config": {
          "enable_episodic": true,
          "enable_semantic": true,
          "consolidation_interval": 1800
        }
      }'

### Agent Configuration Options

#### Model Selection

python

    # Available models
    models = [
        "gpt-4",           # Most capable, higher cost
        "gpt-4-turbo",     # Faster, good balance
        "gpt-3.5-turbo",   # Fast, cost-effective
        "claude-3-opus",   # Anthropic's most capable
        "claude-3-sonnet", # Balanced performance
        "llama-3-70b",     # Open source option
    ]

#### Temperature Settings

-   `0.0 - 0.3`: Focused, deterministic (good for factual tasks)
-   `0.4 - 0.7`: Balanced creativity and consistency
-   `0.8 - 1.0`: Creative, varied responses

#### Advanced Configuration

python

    agent = client.agents.create(
        name="Advanced Assistant",
        type="task_oriented",
        model="gpt-4",
        temperature=0.5,
        max_tokens=4096,
        top_p=0.95,
        frequency_penalty=0.2,
        presence_penalty=0.1,
        
        # System prompt with variables
        system_prompt="""You are {{agent_role}} for {{company_name}}.
        Your primary objectives are:
        1. {{objective_1}}
        2. {{objective_2}}
        3. {{objective_3}}
        
        Always maintain {{tone}} tone in your responses.""",
        
        # Prompt variables (replaced at runtime)
        prompt_variables={
            "agent_role": "a senior technical advisor",
            "company_name": "TechCorp Inc.",
            "objective_1": "Provide accurate technical guidance",
            "objective_2": "Solve complex problems efficiently",
            "objective_3": "Educate users on best practices",
            "tone": "professional yet friendly"
        },
        
        # Memory configuration
        memory_config={
            "enable_episodic": True,
            "enable_semantic": True,
            "enable_implicit": True,
            "enable_prospective": True,
            "consolidation_interval": 3600,
            "decay_rate": 0.95,  # Memory importance decay
            "importance_threshold": 0.3  # Minimum importance to retain
        },
        
        # Tool access (MCP servers)
        mcp_servers=[
            {
                "name": "database_tools",
                "transport": "stdio",
                "command": "/usr/bin/database-mcp-server",
                "args": ["--read-only"],
                "env": {"DB_CONNECTION": "postgresql://..."}
            },
            {
                "name": "web_search",
                "transport": "http",
                "url": "https://search-mcp.julep.cloud",
                "headers": {"X-Search-API-Key": "..."}
            }
        ],
        
        # A2A capabilities
        a2a_capabilities={
            "capabilities": ["data_analysis", "report_generation"],
            "protocols": ["a2a/v1"],
            "authentication": {
                "type": "apiKey",
                "config": {"header": "X-A2A-Auth"}
            }
        }
    )

### Managing Agents

#### List All Agents

python

    # List with filters
    agents = client.agents.list(
        type="research",
        is_active=True,
        limit=20,
        offset=0
    )
    
    for agent in agents.items:
        print(f"{agent.name} ({agent.id}) - Created: {agent.created_at}")

#### Update Agent

python

    # Update configuration
    updated_agent = client.agents.update(
        agent_id=agent.id,
        name="Updated Research Assistant",
        temperature=0.4,
        metadata={
            "department": "R&D",
            "version": "2.0",
            "last_updated_by": "john.doe@company.com"
        }
    )

#### Activate/Deactivate Agent

python

    # Deactivate (preserve data but stop accepting requests)
    client.agents.deactivate(agent.id)
    
    # Reactivate
    client.agents.activate(agent.id)

#### Delete Agent

python

    # Soft delete (can be recovered within 30 days)
    client.agents.delete(agent.id)
    
    # Hard delete (immediate, irreversible)
    client.agents.delete(agent.id, hard_delete=True)

* * *

## 5\. Understanding the Memory System {#understanding-the-memory-system}

<!-- AIDEV-NOTE: cognitive-memory; human-inspired four-type memory system for intelligent agents -->
Julep v2's cognitive memory system is inspired by human memory, with four distinct types that work together to create truly intelligent agents.

### Episodic Memory

<!-- AIDEV-NOTE: episodic-memory; autobiographical experiences with emotional context -->
**What it is**: Autobiographical memories of specific experiences and events.

**Example**:

python

    # Episodic memory example
    {
        "type": "episodic",
        "content": "User complained about slow shipping on order #12345",
        "emotional_valence": -0.6,  # Negative emotion
        "sensory_details": {
            "channel": "chat",
            "user_tone": "frustrated",
            "resolution": "expedited_shipping"
        },
        "temporal_context": {
            "timestamp": "2024-01-15T14:30:00Z",
            "duration": 900,  # 15 minute conversation
            "preceding_event": "order_status_check",
            "following_event": "discount_offered"
        }
    }

**Use cases**:

-   Remembering past conversations
-   Learning from customer interactions
-   Personalizing responses based on history

### Semantic Memory

<!-- AIDEV-NOTE: semantic-memory; factual knowledge with relationship mapping -->
**What it is**: Factual knowledge and conceptual understanding.

**Example**:

python

    # Semantic memory example
    {
        "type": "semantic",
        "content": "ACME Corp return policy: 30 days for unopened items, 14 days for opened",
        "concepts": ["return_policy", "customer_service", "company_policy"],
        "relationships": [
            {"concept": "refund_process", "relation": "part_of"},
            {"concept": "customer_satisfaction", "relation": "impacts"}
        ],
        "confidence": 0.95
    }

**Use cases**:

-   Storing product information
-   Company policies and procedures
-   Domain-specific knowledge

### Implicit Memory

<!-- AIDEV-NOTE: implicit-memory; unconscious patterns influencing agent behavior -->
**What it is**: Unconscious patterns, skills, and behavioral tendencies.

**Example**:

python

    # Implicit memory example
    {
        "type": "implicit",
        "pattern": "users_asking_about_shipping_often_want_tracking_info",
        "frequency": 847,
        "confidence": 0.89,
        "action_tendency": "proactively_offer_tracking_link"
    }

**Use cases**:

-   Learning communication patterns
-   Developing conversational habits
-   Optimizing response strategies

### Prospective Memory

<!-- AIDEV-NOTE: prospective-memory; future-oriented goals and task planning -->
**What it is**: Remembering to perform planned actions in the future.

**Example**:

python

    # Prospective memory example
    {
        "type": "prospective",
        "content": "Follow up with customer about order satisfaction",
        "goal_id": "customer_satisfaction_check",
        "deadline": "2024-01-20T09:00:00Z",
        "priority": 7,
        "status": "active",
        "trigger_conditions": {
            "days_after_delivery": 3,
            "order_value_above": 100
        }
    }

**Use cases**:

-   Scheduling follow-ups
-   Task reminders
-   Goal tracking

### Memory Consolidation

Memories are automatically consolidated based on:

1.  **Access Frequency**: Often-accessed memories are strengthened
2.  **Importance Scores**: Critical information is preserved
3.  **Temporal Decay**: Unused memories fade over time
4.  **Cross-References**: Connected memories reinforce each other

python

    # Monitor memory statistics
    stats = client.agents.get_memory_stats(agent.id)
    print(f"""
    Memory Statistics for {agent.name}:
    - Total Memories: {stats.total_count}
    - Episodic: {stats.episodic_count}
    - Semantic: {stats.semantic_count}  
    - Implicit: {stats.implicit_count}
    - Prospective: {stats.prospective_count}
    - Avg Importance: {stats.avg_importance:.2f}
    - Last Consolidation: {stats.last_consolidation}
    """)

### Searching Memories

python

    # Search across all memory types
    memories = client.memories.search(
        agent_id=agent.id,
        query="shipping delays",
        types=["episodic", "semantic"],
        limit=10,
        threshold=0.7  # Minimum similarity score
    )
    
    for memory in memories:
        print(f"{memory.type}: {memory.content[:100]}... (score: {memory.score:.2f})")

* * *

## 6\. Conversations and Sessions {#conversations-and-sessions}

### Understanding Sessions

A **session** represents a conversation context between a user and an agent. Sessions maintain:

-   Conversation history
-   Context window management
-   User-specific state
-   Memory associations

### Creating a Session

python

    # Create a new session
    session = client.sessions.create(
        agent_id=agent.id,
        user_id="user-123",  # Your internal user ID
        context_window=4096,  # Token limit for context
        metadata={
            "channel": "web_chat",
            "user_name": "John Doe",
            "session_type": "support",
            "priority": "normal"
        }
    )
    
    print(f"Session created: {session.id}")

### Sending Messages

python

    # Send a message and get response
    response = client.messages.send(
        agent_id=agent.id,
        session_id=session.id,
        content="I need help with my recent order. It hasn't arrived yet.",
        context={
            "order_id": "ORD-789456",
            "order_date": "2024-01-10",
            "expected_delivery": "2024-01-15"
        }
    )
    
    print(f"Assistant: {response.content}")
    print(f"Tokens used: {response.tokens_used}")
    print(f"Response time: {response.duration_ms}ms")
    
    # Access metadata
    if response.metadata:
        print(f"Tool used: {response.metadata.get('tool_used')}")
        print(f"Memories accessed: {response.metadata.get('memories_accessed')}")

### Streaming Responses

For long responses, use streaming to improve user experience:

python

    # Stream response chunks
    stream = client.messages.stream(
        agent_id=agent.id,
        session_id=session.id,
        content="Explain the entire return process step by step"
    )
    
    for chunk in stream:
        print(chunk.content, end="", flush=True)
        # Update UI in real-time

### Managing Context Windows

Julep v2 automatically manages context windows, but you can customize behavior:

python

    # Configure context management
    session_config = {
        "context_window": 4096,
        "summarization_threshold": 0.8,  # Summarize when 80% full
        "message_retention": "intelligent",  # 'all', 'recent', or 'intelligent'
        "preserve_messages": [
            # Always keep specific message types
            {"role": "system"},
            {"metadata.important": True}
        ]
    }

### Conversation History

python

    # Retrieve conversation history
    messages = client.messages.list(
        agent_id=agent.id,
        session_id=session.id,
        limit=50,
        order="desc"  # Most recent first
    )
    
    # Export conversation
    export = client.sessions.export(
        session_id=session.id,
        format="json",  # or 'csv', 'txt'
        include_metadata=True
    )
    
    with open("conversation_export.json", "w") as f:
        json.dump(export, f, indent=2)

### Session Management

python

    # Get active sessions
    active_sessions = client.sessions.list(
        agent_id=agent.id,
        is_active=True,
        user_id="user-123"
    )
    
    # Resume a session
    resumed_session = client.sessions.resume(session.id)
    
    # End a session
    client.sessions.end(
        session_id=session.id,
        reason="user_inactive",
        summary="Customer inquired about order status. Issue resolved."
    )

### Multi-Turn Conversations Example

python

    # Complete conversation flow
    async def handle_conversation():
        # Start session
        session = await client.sessions.create(
            agent_id=agent.id,
            user_id="user-456"
        )
        
        # Conversation loop
        conversation = [
            "Hi, I'd like to return an item",
            "The order number is ORD-123456",
            "Yes, it's unopened and I have the receipt",
            "I'd prefer a refund to my original payment method"
        ]
        
        for user_message in conversation:
            print(f"User: {user_message}")
            
            response = await client.messages.send(
                agent_id=agent.id,
                session_id=session.id,
                content=user_message
            )
            
            print(f"Assistant: {response.content}\n")
            
            # Check if any tools were used
            if response.metadata.get("tools_used"):
                for tool in response.metadata["tools_used"]:
                    print(f"  [Used tool: {tool['name']}]")
        
        # End session with summary
        await client.sessions.end(
            session_id=session.id,
            summary="Processed return request for order ORD-123456"
        )

* * *

## 7\. Tools and Integrations (MCP) {#tools-and-integrations-mcp}

<!-- AIDEV-NOTE: mcp-protocol; usb-for-ai enabling plug-and-play tool capabilities -->
The Model Context Protocol (MCP) enables agents to use external tools and access resources. Think of it as "USB for AI" - plug in capabilities as needed.

### Understanding MCP Tools

MCP tools allow agents to:

-   Query databases
-   Call APIs
-   Process files
-   Perform calculations
-   Access external systems

### Built-in Tools

Julep v2 comes with 100+ pre-configured tools:

python

    # List available tools
    tools = client.tools.list(agent_id=agent.id)
    
    for tool in tools:
        print(f"""
    Tool: {tool.name}
    Description: {tool.description}
    Category: {tool.category}
    Input Schema: {json.dumps(tool.input_schema, indent=2)}
    ---""")

### Common Built-in Tools

#### 1\. Web Search

python

    # Enable web search for an agent
    client.agents.add_tool(
        agent_id=agent.id,
        tool_name="web_search",
        config={
            "max_results": 5,
            "safe_search": True,
            "regions": ["us", "uk", "ca"]
        }
    )
    
    # Use in conversation
    response = client.messages.send(
        agent_id=agent.id,
        session_id=session.id,
        content="What are the latest reviews for the iPhone 15?"
    )
    # Agent automatically searches and incorporates results

#### 2\. Calculator

python

    # Advanced calculations
    client.agents.add_tool(
        agent_id=agent.id,
        tool_name="calculator",
        config={
            "precision": 10,
            "timeout": 5000
        }
    )

#### 3\. Database Query

python

    # Secure database access
    client.agents.add_tool(
        agent_id=agent.id,
        tool_name="sql_query",
        config={
            "connection_string": "postgresql://...",
            "allowed_tables": ["orders", "customers", "products"],
            "read_only": True,
            "timeout": 30000
        }
    )

#### 4\. Email Integration

python

    # Email capabilities
    client.agents.add_tool(
        agent_id=agent.id,
        tool_name="email",
        config={
            "provider": "sendgrid",
            "api_key": "...",
            "from_address": "assistant@company.com",
            "templates": {
                "order_confirmation": "d-123456",
                "support_response": "d-789012"
            }
        }
    )

### Custom MCP Servers

Create your own MCP servers for custom tools:

python

    # Register custom MCP server
    custom_server = client.mcp_servers.create(
        agent_id=agent.id,
        name="inventory_system",
        transport="http",
        url="https://your-mcp-server.com",
        headers={
            "Authorization": "Bearer your_token"
        },
        description="Access to inventory management system"
    )
    
    # Define custom tools
    client.tools.create(
        server_id=custom_server.id,
        name="check_inventory",
        description="Check product inventory levels",
        input_schema={
            "type": "object",
            "properties": {
                "product_id": {"type": "string"},
                "warehouse": {"type": "string", "enum": ["east", "west", "central"]}
            },
            "required": ["product_id"]
        }
    )

### MCP Server Implementation Example

If you want to create your own MCP server:

python

    # mcp_server.py
    from fastapi import FastAPI
    from pydantic import BaseModel
    
    app = FastAPI()
    
    class InventoryRequest(BaseModel):
        product_id: str
        warehouse: str = "all"
    
    @app.post("/mcp/tools/check_inventory")
    async def check_inventory(request: InventoryRequest):
        # Your business logic here
        inventory = await fetch_inventory(
            request.product_id, 
            request.warehouse
        )
        
        return {
            "jsonrpc": "2.0",
            "result": {
                "product_id": request.product_id,
                "total_stock": inventory.total,
                "by_warehouse": inventory.breakdown,
                "last_updated": inventory.timestamp
            }
        }
    
    @app.get("/mcp/tools/list")
    async def list_tools():
        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": [
                    {
                        "name": "check_inventory",
                        "description": "Check product inventory levels",
                        "inputSchema": {...}
                    }
                ]
            }
        }

### Tool Usage Monitoring

python

    # Monitor tool usage
    usage_stats = client.tools.get_usage_stats(
        agent_id=agent.id,
        start_date="2024-01-01",
        end_date="2024-01-31"
    )
    
    print(f"""
    Tool Usage Statistics:
    Total Calls: {usage_stats.total_calls}
    Unique Tools Used: {usage_stats.unique_tools}
    Average Response Time: {usage_stats.avg_response_time}ms
    
    Top Tools:
    """)
    
    for tool in usage_stats.top_tools:
        print(f"- {tool.name}: {tool.call_count} calls, {tool.avg_duration}ms avg")

### Best Practices for Tools

1.  **Security First**
    
    python
    
        # Always use read-only access where possible
        config = {
            "read_only": True,
            "allowed_operations": ["SELECT"],
            "forbidden_tables": ["users", "passwords", "api_keys"]
        }
    
2.  **Set Timeouts**
    
    python
    
        # Prevent long-running operations
        config = {
            "timeout": 30000,  # 30 seconds
            "retry_attempts": 3,
            "retry_delay": 1000
        }
    
3.  **Rate Limiting**
    
    python
    
        # Prevent abuse
        config = {
            "rate_limit": {
                "calls_per_minute": 60,
                "calls_per_hour": 1000,
                "burst_size": 10
            }
        }
    
4.  **Error Handling**
    
    python
    
        # Graceful degradation
        config = {
            "on_error": "continue",  # or "fail", "use_fallback"
            "fallback_message": "I couldn't access that information right now.",
            "log_errors": True
        }
    

* * *

## 8\. Multi-Agent Collaboration (A2A) {#multi-agent-collaboration-a2a}

<!-- AIDEV-NOTE: a2a-protocol; agent collaboration for complex task delegation -->
The Agent-to-Agent (A2A) protocol enables agents to collaborate on complex tasks, delegate work, and share knowledge.

### Understanding A2A

A2A allows agents to:

-   Delegate specialized tasks to other agents
-   Collaborate on complex problems
-   Share memories and knowledge
-   Coordinate multi-step workflows

### Agent Discovery

python

    # Discover available agents
    available_agents = client.agents.discover(
        capabilities=["data_analysis", "report_generation"],
        status="active"
    )
    
    for agent in available_agents:
        print(f"""
    Agent: {agent.name}
    ID: {agent.id}
    Capabilities: {', '.join(agent.capabilities)}
    Endpoint: {agent.endpoint}
    ---""")

### Creating a Coordinator Agent

python

    # Create a coordinator agent that manages other agents
    coordinator = client.agents.create(
        name="Project Coordinator",
        type="coordinator",
        model="gpt-4",
        system_prompt="""You are a project coordinator that delegates tasks to specialized agents.
        
        Available agents:
        - Research Agent: Gathers and analyzes information
        - Writer Agent: Creates reports and documentation
        - Data Agent: Processes and visualizes data
        
        Break down complex requests and delegate appropriately.""",
        
        a2a_capabilities={
            "capabilities": ["task_delegation", "coordination"],
            "can_delegate_to": ["research", "writing", "data_analysis"]
        }
    )

### Delegating Tasks

python

    # Create a task that requires multiple agents
    task = client.tasks.create(
        name="Market Analysis Report",
        description="Comprehensive analysis of the smartphone market",
        coordinator_agent_id=coordinator.id,
        subtasks=[
            {
                "name": "Research Phase",
                "agent_capability": "research",
                "input": {
                    "topics": ["smartphone sales", "market trends", "competitor analysis"],
                    "depth": "comprehensive",
                    "sources": ["industry reports", "news", "financial data"]
                }
            },
            {
                "name": "Data Analysis",
                "agent_capability": "data_analysis",
                "input": {
                    "datasets": ["sales_data", "market_share"],
                    "visualizations": ["trends", "comparisons", "projections"]
                },
                "depends_on": ["Research Phase"]
            },
            {
                "name": "Report Writing",
                "agent_capability": "writing",
                "input": {
                    "format": "executive_report",
                    "sections": ["executive_summary", "findings", "recommendations"],
                    "length": "10_pages"
                },
                "depends_on": ["Research Phase", "Data Analysis"]
            }
        ]
    )
    
    # Monitor task progress
    while task.status != "completed":
        task = client.tasks.get(task.id)
        print(f"Task Status: {task.status}")
        print(f"Progress: {task.progress * 100:.1f}%")
        
        for subtask in task.subtasks:
            print(f"  - {subtask.name}: {subtask.status}")
        
        time.sleep(5)
    
    # Get results
    results = client.tasks.get_artifacts(task.id)
    for artifact in results:
        print(f"Artifact: {artifact.name} ({artifact.type})")
        # Download or process artifacts

### Direct Agent-to-Agent Communication

python

    # Agent A requests help from Agent B
    collaboration = client.collaborations.create(
        requesting_agent_id=agent_a.id,
        responding_agent_id=agent_b.id,
        request={
            "type": "analysis_request",
            "data": {
                "customer_segments": ["enterprise", "smb", "consumer"],
                "metrics": ["satisfaction", "churn", "ltv"]
            },
            "needed_by": "2024-01-20T15:00:00Z"
        }
    )
    
    # Monitor collaboration
    updates = client.collaborations.get_updates(collaboration.id)
    for update in updates:
        print(f"{update.timestamp}: {update.message}")

### Shared Memory Spaces

python

    # Create a shared memory space for collaborating agents
    shared_space = client.memory_spaces.create(
        name="Q1 Planning Knowledge Base",
        agent_ids=[agent_a.id, agent_b.id, agent_c.id],
        permissions={
            agent_a.id: ["read", "write"],
            agent_b.id: ["read", "write"],
            agent_c.id: ["read"]
        }
    )
    
    # Agents can now share memories
    client.memories.create(
        agent_id=agent_a.id,
        memory_space_id=shared_space.id,
        type="semantic",
        content="Q1 revenue target: $10M based on current pipeline",
        shared=True
    )

### A2A Patterns

#### 1\. Specialist Pattern

python

    # Coordinator delegates to specialists
    specialists = {
        "legal": "legal_review_agent_id",
        "financial": "financial_analysis_agent_id",
        "technical": "technical_review_agent_id"
    }
    
    # Route based on content
    if "contract" in user_request:
        delegate_to = specialists["legal"]
    elif "budget" in user_request:
        delegate_to = specialists["financial"]

#### 2\. Pipeline Pattern

python

    # Sequential processing through agents
    pipeline = [
        ("data_collector", {"source": "api"}),
        ("data_processor", {"normalize": True}),
        ("analyzer", {"methods": ["statistical", "ml"]}),
        ("report_generator", {"format": "pdf"})
    ]
    
    result = initial_data
    for agent_id, config in pipeline:
        result = client.agents.process(agent_id, result, config)

#### 3\. Consensus Pattern

python

    # Multiple agents vote on decisions
    reviewers = ["agent_1", "agent_2", "agent_3"]
    reviews = []
    
    for reviewer_id in reviewers:
        review = client.agents.review(
            agent_id=reviewer_id,
            content=proposal,
            criteria=["feasibility", "cost", "impact"]
        )
        reviews.append(review)
    
    # Aggregate decisions
    decision = aggregate_reviews(reviews)

* * *

## 9\. Workflows and Automation {#workflows-and-automation}

<!-- AIDEV-NOTE: workflow-system; durable multi-step processes with state management -->
Julep v2's workflow system enables complex, multi-step processes with automatic retry, error handling, and state management.

### Understanding Workflows

Workflows are durable, fault-tolerant processes that can:

-   Span multiple agents and tools
-   Handle long-running operations
-   Automatically retry on failure
-   Maintain state across restarts

### Creating a Simple Workflow

python

    # Define a customer onboarding workflow
    workflow = client.workflows.create(
        name="Customer Onboarding",
        description="Complete onboarding process for new customers",
        steps=[
            {
                "name": "collect_information",
                "type": "agent_interaction",
                "agent_id": agent.id,
                "prompt": "Collect customer information",
                "required_fields": ["name", "email", "company", "use_case"]
            },
            {
                "name": "create_account",
                "type": "tool_execution",
                "tool": "create_customer_account",
                "input_mapping": {
                    "email": "$.steps.collect_information.email",
                    "company": "$.steps.collect_information.company"
                }
            },
            {
                "name": "send_welcome_email",
                "type": "tool_execution",
                "tool": "send_email",
                "input_mapping": {
                    "template": "welcome_email",
                    "to": "$.steps.collect_information.email",
                    "variables": {
                        "name": "$.steps.collect_information.name",
                        "account_id": "$.steps.create_account.account_id"
                    }
                }
            },
            {
                "name": "schedule_followup",
                "type": "agent_task",
                "agent_id": agent.id,
                "task_type": "prospective_memory",
                "task_data": {
                    "action": "follow_up_call",
                    "when": "+7days",
                    "context": "$.steps"
                }
            }
        ],
        error_handling={
            "retry_policy": {
                "max_attempts": 3,
                "backoff": "exponential",
                "initial_delay": 1000
            },
            "on_failure": "notify_admin"
        }
    )

### Executing Workflows

python

    # Start workflow execution
    execution = client.workflows.execute(
        workflow_id=workflow.id,
        input_data={
            "source": "website_signup",
            "campaign": "q1_promotion"
        },
        webhook_url="https://your-app.com/webhook/workflow-updates"
    )
    
    print(f"Workflow execution started: {execution.id}")
    
    # Monitor execution
    while execution.status in ["pending", "running"]:
        execution = client.workflow_executions.get(execution.id)
        print(f"Status: {execution.status}")
        print(f"Current Step: {execution.current_step}")
        print(f"Progress: {execution.progress * 100:.1f}%")
        
        time.sleep(2)
    
    # Get results
    if execution.status == "completed":
        print("Workflow completed successfully!")
        print(f"Results: {json.dumps(execution.results, indent=2)}")
    else:
        print(f"Workflow failed: {execution.error}")

### Advanced Workflow Features

#### Conditional Logic

python

    workflow_with_conditions = {
        "name": "Smart Support Routing",
        "steps": [
            {
                "name": "analyze_request",
                "type": "agent_analysis",
                "agent_id": analyzer_agent.id
            },
            {
                "name": "route_request",
                "type": "conditional",
                "conditions": [
                    {
                        "if": "$.steps.analyze_request.category == 'technical'",
                        "then": {
                            "type": "delegate",
                            "agent_id": technical_agent.id
                        }
                    },
                    {
                        "if": "$.steps.analyze_request.priority == 'high'",
                        "then": {
                            "type": "delegate",
                            "agent_id": senior_agent.id
                        }
                    },
                    {
                        "else": {
                            "type": "delegate",
                            "agent_id": general_agent.id
                        }
                    }
                ]
            }
        ]
    }

#### Parallel Execution

python

    workflow_parallel = {
        "name": "Multi-Channel Notification",
        "steps": [
            {
                "name": "notify_all",
                "type": "parallel",
                "branches": [
                    {
                        "name": "email_notification",
                        "type": "tool_execution",
                        "tool": "send_email"
                    },
                    {
                        "name": "sms_notification",
                        "type": "tool_execution",
                        "tool": "send_sms"
                    },
                    {
                        "name": "push_notification",
                        "type": "tool_execution",
                        "tool": "send_push"
                    }
                ],
                "wait_for": "all"  # or "any" for race condition
            }
        ]
    }

#### Loops and Iteration

python

    workflow_with_loop = {
        "name": "Batch Processing",
        "steps": [
            {
                "name": "get_items",
                "type": "tool_execution",
                "tool": "fetch_pending_items"
            },
            {
                "name": "process_items",
                "type": "foreach",
                "items": "$.steps.get_items.result",
                "iterator": "item",
                "steps": [
                    {
                        "name": "validate",
                        "type": "agent_interaction",
                        "agent_id": validator_agent.id,
                        "input": "$.item"
                    },
                    {
                        "name": "process",
                        "type": "tool_execution",
                        "tool": "process_item",
                        "input": "$.item"
                    }
                ],
                "concurrency": 5  # Process 5 items at a time
            }
        ]
    }

### Scheduled Workflows

python

    # Create a recurring workflow
    schedule = client.schedules.create(
        workflow_id=workflow.id,
        name="Daily Report Generation",
        cron="0 9 * * *",  # Every day at 9 AM
        timezone="America/New_York",
        input_data={
            "report_type": "daily_summary",
            "recipients": ["team@company.com"]
        },
        enabled=True
    )
    
    # Manage scheduled workflows
    schedules = client.schedules.list(active=True)
    for sched in schedules:
        print(f"{sched.name}: {sched.cron} ({sched.timezone})")
        print(f"Next run: {sched.next_run}")
        print(f"Last run: {sched.last_run} - Status: {sched.last_status}")

### Workflow Templates

python

    # Use pre-built workflow templates
    templates = client.workflow_templates.list(category="customer_service")
    
    # Create workflow from template
    workflow = client.workflows.create_from_template(
        template_id="customer_feedback_analysis",
        customizations={
            "agent_id": agent.id,
            "notification_email": "manager@company.com",
            "sentiment_threshold": 0.3
        }
    )

* * *

## 10\. Advanced Features {#advanced-features}

### Fine-Tuning Agent Behavior

python

    # Create a fine-tuning dataset
    dataset = client.datasets.create(
        name="Customer Service Interactions",
        description="High-quality customer service conversations",
        type="conversational"
    )
    
    # Add training examples
    client.datasets.add_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "input": "My order hasn't arrived and it's been two weeks!",
                "output": "I sincerely apologize for the delay with your order. I understand how frustrating this must be. Let me immediately look into this for you. Could you please provide your order number so I can track it down and ensure you receive it as soon as possible?",
                "metadata": {
                    "sentiment": "negative",
                    "category": "shipping_delay",
                    "resolution": "successful"
                }
            }
            # Add more examples...
        ]
    )
    
    # Fine-tune agent
    fine_tuning_job = client.agents.fine_tune(
        agent_id=agent.id,
        dataset_id=dataset.id,
        config={
            "epochs": 3,
            "learning_rate": 1e-5,
            "validation_split": 0.2
        }
    )
    
    # Monitor fine-tuning progress
    while fine_tuning_job.status == "running":
        job = client.fine_tuning.get(fine_tuning_job.id)
        print(f"Progress: {job.progress * 100:.1f}%")
        print(f"Current Loss: {job.current_loss:.4f}")
        time.sleep(10)

### Custom Memory Types

python

    # Define a custom memory type
    custom_memory_type = client.memory_types.create(
        name="customer_preference",
        schema={
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "preference_type": {"type": "string"},
                "value": {"type": "any"},
                "confidence": {"type": "number"},
                "learned_from": {"type": "string"}
            }
        },
        decay_function="exponential",
        importance_calculation="weighted_access"
    )
    
    # Use custom memory type
    client.memories.create(
        agent_id=agent.id,
        type="customer_preference",
        content={
            "customer_id": "cust-123",
            "preference_type": "communication_style",
            "value": "formal",
            "confidence": 0.85,
            "learned_from": "email_interactions"
        }
    )

### Advanced Analytics

python

    # Get detailed analytics
    analytics = client.analytics.get_report(
        agent_id=agent.id,
        start_date="2024-01-01",
        end_date="2024-01-31",
        metrics=[
            "conversations",
            "tokens_used",
            "tool_usage",
            "memory_growth",
            "user_satisfaction",
            "response_times"
        ]
    )
    
    # Visualize conversation patterns
    patterns = client.analytics.get_conversation_patterns(
        agent_id=agent.id,
        period="last_30_days"
    )
    
    print(f"""
    Analytics Summary:
    - Total Conversations: {analytics.conversations.total}
    - Avg Satisfaction: {analytics.user_satisfaction.average:.2f}/5
    - Avg Response Time: {analytics.response_times.average}ms
    - Total Tokens: {analytics.tokens_used.total:,}
    - Cost: ${analytics.tokens_used.cost:.2f}
    
    Top Patterns:
    """)
    
    for pattern in patterns.top_patterns:
        print(f"- {pattern.description}: {pattern.frequency} occurrences")

### Multimodal Capabilities

python

    # Enable vision capabilities
    vision_agent = client.agents.create(
        name="Visual Assistant",
        type="conversational",
        model="gpt-4-vision",
        capabilities=["vision", "image_generation"],
        system_prompt="You can analyze images and create visual content."
    )
    
    # Process image
    response = client.messages.send(
        agent_id=vision_agent.id,
        session_id=session.id,
        content="What's in this image?",
        attachments=[
            {
                "type": "image",
                "url": "https://example.com/image.jpg"
                # or base64: "data:image/jpeg;base64,..."
            }
        ]
    )
    
    # Generate image
    response = client.messages.send(
        agent_id=vision_agent.id,
        session_id=session.id,
        content="Create an image of a futuristic city at sunset"
    )
    
    # Response includes generated image URL
    print(f"Generated image: {response.attachments[0]['url']}")

### Voice Integration

python

    # Enable voice capabilities
    voice_config = {
        "voice_id": "alloy",  # or "echo", "fable", "onyx", "nova", "shimmer"
        "speed": 1.0,
        "language": "en-US"
    }
    
    # Text-to-speech
    audio_response = client.messages.send_voice(
        agent_id=agent.id,
        session_id=session.id,
        content="Hello! How can I help you today?",
        voice_config=voice_config
    )
    
    # Save audio file
    with open("response.mp3", "wb") as f:
        f.write(audio_response.audio_data)
    
    # Speech-to-text
    transcription = client.messages.transcribe(
        audio_file="user_audio.mp3",
        language="en"
    )
    
    response = client.messages.send(
        agent_id=agent.id,
        session_id=session.id,
        content=transcription.text
    )

### Export and Backup

python

    # Export agent configuration and memories
    export = client.agents.export(
        agent_id=agent.id,
        include_memories=True,
        include_conversations=True,
        format="json"  # or "sql", "parquet"
    )
    
    # Save backup
    with open(f"agent_backup_{agent.id}_{datetime.now().isoformat()}.json", "w") as f:
        json.dump(export, f)
    
    # Import to new agent
    new_agent = client.agents.import_from_backup(
        backup_data=export,
        name="Restored Agent"
    )

* * *

## 11\. API Reference {#api-reference}

### Base Configuration

python

    # API Endpoints
    BASE_URL = "https://api.julep.cloud/v1"
    
    # Headers
    headers = {
        "Authorization": "Bearer julep_pk_your_api_key",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Request-ID": str(uuid.uuid4())  # Optional request tracking
    }

### Common Parameters

python

    # Pagination
    params = {
        "limit": 20,      # Items per page (max 100)
        "offset": 0,      # Skip N items
        "order": "desc",  # "asc" or "desc"
        "sort_by": "created_at"
    }
    
    # Filtering
    filters = {
        "created_after": "2024-01-01T00:00:00Z",
        "created_before": "2024-01-31T23:59:59Z",
        "status": "active",
        "metadata.department": "sales"
    }

### Core Endpoints

#### Agents

python

    # Create Agent
    POST /agents
    Body: {
        "name": "Agent Name",
        "type": "conversational",
        "model": "gpt-4",
        "temperature": 0.7,
        "system_prompt": "...",
        "memory_config": {...},
        "metadata": {...}
    }
    
    # Get Agent
    GET /agents/{agent_id}
    
    # Update Agent
    PUT /agents/{agent_id}
    Body: { ...updates }
    
    # Delete Agent
    DELETE /agents/{agent_id}
    
    # List Agents
    GET /agents?type=research&is_active=true&limit=20

#### Sessions

python

    # Create Session
    POST /agents/{agent_id}/sessions
    Body: {
        "user_id": "user-123",
        "context_window": 4096,
        "metadata": {...}
    }
    
    # Get Session
    GET /agents/{agent_id}/sessions/{session_id}
    
    # End Session
    POST /agents/{agent_id}/sessions/{session_id}/end
    Body: {
        "reason": "user_inactive",
        "summary": "..."
    }
    
    # List Sessions
    GET /agents/{agent_id}/sessions?is_active=true

#### Messages

python

    # Send Message
    POST /agents/{agent_id}/sessions/{session_id}/messages
    Body: {
        "content": "User message",
        "context": {...},
        "attachments": [...]
    }
    
    # Get Messages
    GET /agents/{agent_id}/sessions/{session_id}/messages?limit=50
    
    # Stream Message
    POST /agents/{agent_id}/sessions/{session_id}/messages/stream
    Body: {
        "content": "User message",
        "stream": true
    }

#### Memories

python

    # Search Memories
    POST /agents/{agent_id}/memories/search
    Body: {
        "query": "search terms",
        "types": ["episodic", "semantic"],
        "limit": 10,
        "threshold": 0.7
    }
    
    # Create Memory
    POST /agents/{agent_id}/memories
    Body: {
        "type": "semantic",
        "content": "...",
        "importance": 0.8,
        "metadata": {...}
    }
    
    # Get Memory Stats
    GET /agents/{agent_id}/memories/stats

#### Tools (MCP)

python

    # List Tools
    GET /agents/{agent_id}/tools
    
    # Add Tool
    POST /agents/{agent_id}/tools
    Body: {
        "name": "tool_name",
        "config": {...}
    }
    
    # Execute Tool
    POST /agents/{agent_id}/tools/{tool_name}/execute
    Body: {
        "input": {...}
    }
    
    # Get Tool Usage
    GET /agents/{agent_id}/tools/usage?start_date=2024-01-01

#### Tasks (A2A)

python

    # Create Task
    POST /tasks
    Body: {
        "name": "Task Name",
        "coordinator_agent_id": "...",
        "subtasks": [...],
        "deadline": "2024-01-20T15:00:00Z"
    }
    
    # Get Task
    GET /tasks/{task_id}
    
    # Update Task
    PUT /tasks/{task_id}
    Body: {
        "status": "completed",
        "results": {...}
    }
    
    # Get Task Artifacts
    GET /tasks/{task_id}/artifacts

#### Workflows

python

    # Create Workflow
    POST /workflows
    Body: {
        "name": "Workflow Name",
        "steps": [...],
        "error_handling": {...}
    }
    
    # Execute Workflow
    POST /workflows/{workflow_id}/execute
    Body: {
        "input_data": {...},
        "webhook_url": "..."
    }
    
    # Get Execution Status
    GET /workflow-executions/{execution_id}
    
    # List Workflow Executions
    GET /workflows/{workflow_id}/executions

### Response Formats

#### Success Response

json

    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2024-01-15T10:30:00Z",
            ...
        },
        "meta": {
            "request_id": "req_123456",
            "duration_ms": 127
        }
    }

#### Error Response

json

    {
        "error": {
            "code": "INVALID_REQUEST",
            "message": "Temperature must be between 0 and 1",
            "details": {
                "field": "temperature",
                "value": 1.5
            }
        },
        "meta": {
            "request_id": "req_123456"
        }
    }

#### Paginated Response

json

    {
        "data": {
            "items": [...],
            "total": 245,
            "limit": 20,
            "offset": 40,
            "has_more": true
        }
    }

### Rate Limits

python

    # Rate limit headers
    {
        "X-RateLimit-Limit": "1000",      # Requests per hour
        "X-RateLimit-Remaining": "950",   # Remaining requests
        "X-RateLimit-Reset": "1705327200" # Unix timestamp
    }
    
    # Rate limit response
    429 Too Many Requests
    {
        "error": {
            "code": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests",
            "retry_after": 3600
        }
    }

### Webhooks

python

    # Webhook payload
    {
        "event": "message.created",
        "timestamp": "2024-01-15T10:30:00Z",
        "data": {
            "agent_id": "...",
            "session_id": "...",
            "message": {...}
        },
        "signature": "sha256=..."  # HMAC signature
    }
    
    # Verify webhook signature
    import hmac
    import hashlib
    
    def verify_webhook(payload, signature, secret):
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(
            f"sha256={expected}",
            signature
        )

* * *

## 12\. Best Practices {#best-practices}

<!-- AIDEV-NOTE: best-practices; production-ready guidelines for Julep v2 deployment -->
### Agent Design

1.  **Clear System Prompts**
    
    python
    
        # Good
        system_prompt = """You are a customer service agent for ACME Corp.
        
        Your responsibilities:
        1. Answer product questions accurately
        2. Help with order issues
        3. Escalate complex problems
        
        Always:
        - Be polite and professional
        - Verify order numbers before making changes
        - Offer alternatives when products are unavailable
        
        Never:
        - Share customer data with other customers
        - Make promises about delivery times you can't keep
        - Process refunds over $500 without manager approval"""
        
        # Bad
        system_prompt = "You are a helpful assistant"
    
2.  **Appropriate Model Selection**
    -   Use GPT-4 for complex reasoning tasks
    -   Use GPT-3.5 for simple, high-volume interactions
    -   Consider cost vs. quality tradeoffs
3.  **Memory Configuration**
    
    python
    
        # Configure based on use case
        memory_configs = {
            "customer_service": {
                "enable_episodic": True,     # Remember past interactions
                "enable_semantic": True,      # Store product knowledge
                "enable_implicit": True,      # Learn patterns
                "enable_prospective": False   # No need for future planning
            },
            "project_manager": {
                "enable_episodic": True,      # Track project history
                "enable_semantic": True,      # Store project details
                "enable_implicit": False,     # Less important
                "enable_prospective": True    # Critical for deadlines
            }
        }
    

### Session Management

1.  **User Identification**
    
    python
    
        # Use consistent user IDs
        session = client.sessions.create(
            agent_id=agent.id,
            user_id=f"user_{hash(email)}",  # Consistent across sessions
            metadata={
                "email": email,
                "name": name,
                "account_type": "premium"
            }
        )
    
2.  **Context Windows**
    
    python
    
        # Adjust based on conversation type
        context_windows = {
            "quick_help": 2048,      # Short interactions
            "technical_support": 4096, # Detailed troubleshooting
            "consultation": 8192     # Long-form discussions
        }
    
3.  **Session Lifecycle**
    
    python
    
        # Always clean up sessions
        try:
            session = client.sessions.create(...)
            # Conversation logic
        finally:
            client.sessions.end(
                session_id=session.id,
                summary=generate_summary(messages)
            )
    

### Tool Usage

1.  **Security First**
    
    python
    
        # Restrict tool access
        tool_config = {
            "database_query": {
                "allowed_tables": ["products", "orders"],
                "forbidden_operations": ["DROP", "DELETE", "UPDATE"],
                "timeout": 30000,
                "row_limit": 1000
            }
        }
    
2.  **Error Handling**
    
    python
    
        # Graceful tool failures
        try:
            result = client.tools.execute(tool_name, input_data)
        except ToolExecutionError as e:
            # Fallback response
            return "I'm having trouble accessing that information. Let me try another way..."
    
3.  **Tool Combinations**
    
    python
    
        # Combine tools effectively
        async def analyze_customer(customer_id):
            # Gather data from multiple tools
            tasks = [
                client.tools.execute("get_customer_info", {"id": customer_id}),
                client.tools.execute("get_order_history", {"customer_id": customer_id}),
                client.tools.execute("get_support_tickets", {"customer_id": customer_id})
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle partial failures
            customer_data = {}
            for i, result in enumerate(results):
                if not isinstance(result, Exception):
                    customer_data[tasks[i].tool_name] = result
            
            return customer_data
    

### Memory Optimization

1.  **Importance Scoring**
    
    python
    
        # Set importance based on content
        def calculate_importance(content, context):
            importance = 0.5  # Base importance
            
            # Increase for certain keywords
            important_terms = ["bug", "issue", "urgent", "deadline", "payment"]
            for term in important_terms:
                if term in content.lower():
                    importance += 0.1
            
            # Increase for customer sentiment
            if context.get("sentiment") == "negative":
                importance += 0.2
            
            # Increase for VIP customers
            if context.get("customer_tier") == "vip":
                importance += 0.2
            
            return min(importance, 1.0)
    
2.  **Memory Pruning**
    
    python
    
        # Regularly clean up old memories
        async def prune_memories(agent_id):
            # Get memory stats
            stats = await client.memories.get_stats(agent_id)
            
            if stats.total_count > 10000:
                # Remove low-importance old memories
                await client.memories.prune(
                    agent_id=agent_id,
                    older_than="90 days",
                    importance_below=0.3,
                    keep_minimum=5000
                )
    
3.  **Memory Search Optimization**
    
    python
    
        # Use specific memory types
        # Good - search only relevant types
        memories = client.memories.search(
            query="refund policy",
            types=["semantic"],  # Factual information
            limit=5
        )
        
        # Bad - searching all types
        memories = client.memories.search(
            query="refund policy",
            types=["episodic", "semantic", "implicit", "prospective"],
            limit=20
        )
    

### Workflow Best Practices

1.  **Idempotent Steps**
    
    python
    
        # Make steps repeatable
        workflow_step = {
            "name": "create_customer",
            "type": "tool_execution",
            "tool": "create_or_update_customer",  # Idempotent
            "input": {
                "email": "$.input.email",
                "name": "$.input.name"
            },
            "retry": {
                "max_attempts": 3,
                "backoff": "exponential"
            }
        }
    
2.  **Error Boundaries**
    
    python
    
        # Handle failures gracefully
        workflow = {
            "steps": [
                {
                    "name": "risky_operation",
                    "type": "tool_execution",
                    "tool": "external_api_call",
                    "error_handler": {
                        "type": "fallback",
                        "steps": [
                            {
                                "name": "use_cached_data",
                                "type": "tool_execution",
                                "tool": "get_cached_response"
                            }
                        ]
                    }
                }
            ]
        }
    
3.  **Checkpointing**
    
    python
    
        # Save progress for long workflows
        workflow = {
            "checkpoint_interval": 5,  # Save state every 5 steps
            "steps": [
                # ... many steps
            ],
            "on_resume": {
                "type": "agent_interaction",
                "prompt": "Resuming workflow from step {{checkpoint.step}}"
            }
        }
    

### Performance Optimization

<!-- AIDEV-NOTE: performance-optimization; key strategies for production scalability -->
1.  **Batch Operations**
    
    python
    
        # Process multiple items efficiently
        # Good - batch processing
        results = client.batch.process([
            {"method": "agents.get", "params": {"id": agent_id_1}},
            {"method": "agents.get", "params": {"id": agent_id_2}},
            {"method": "agents.get", "params": {"id": agent_id_3}}
        ])
        
        # Bad - individual requests
        agent_1 = client.agents.get(agent_id_1)
        agent_2 = client.agents.get(agent_id_2)
        agent_3 = client.agents.get(agent_id_3)
    
2.  **Caching**
    
    python
    
        # Cache frequently accessed data
        from functools import lru_cache
        
        @lru_cache(maxsize=100)
        def get_agent_config(agent_id):
            return client.agents.get(agent_id)
        
        # Clear cache when updating
        def update_agent(agent_id, updates):
            result = client.agents.update(agent_id, updates)
            get_agent_config.cache_clear()
            return result
    
3.  **Connection Pooling**
    
    python
    
        # Reuse connections
        from julep import JulepClient
        
        # Good - single client instance
        client = JulepClient(
            api_key="...",
            max_connections=100,
            connection_timeout=30
        )
        
        # Bad - creating new clients
        def process_message(content):
            client = JulepClient(api_key="...")  # Don't do this
            return client.messages.send(...)
    

### Monitoring and Debugging

1.  **Request Tracking**
    
    python
    
        # Track requests for debugging
        import uuid
        
        request_id = str(uuid.uuid4())
        
        response = client.messages.send(
            agent_id=agent.id,
            session_id=session.id,
            content="...",
            headers={"X-Request-ID": request_id}
        )
        
        # Log for correlation
        logger.info(f"Request {request_id}: {response.status}")
    
2.  **Performance Monitoring**
    
    python
    
        # Track performance metrics
        import time
        
        start_time = time.time()
        
        response = client.messages.send(...)
        
        duration = time.time() - start_time
        
        # Alert if slow
        if duration > 5.0:
            alert(f"Slow response: {duration:.2f}s for request {request_id}")
    
3.  **Error Logging**
    
    python
    
        # Comprehensive error logging
        import traceback
        
        try:
            response = client.messages.send(...)
        except Exception as e:
            logger.error(f"""
            Error in conversation:
            Agent: {agent.id}
            Session: {session.id}
            User: {user_id}
            Error: {str(e)}
            Traceback: {traceback.format_exc()}
            """)
            
            # Notify error tracking service
            sentry.capture_exception(e)
    

* * *

## 13\. Pricing and Limits {#pricing-and-limits}

<!-- AIDEV-NOTE: pricing-tiers; transparent cost structure for different usage levels -->
### Pricing Tiers

#### Starter Plan - $0/month

-   10,000 tokens/month included
-   2 active agents
-   Basic memory (1MB per agent)
-   Community support
-   Rate limit: 60 requests/minute

#### Professional Plan - $99/month

-   1,000,000 tokens/month included
-   10 active agents
-   Standard memory (100MB per agent)
-   Email support
-   Rate limit: 600 requests/minute
-   Advanced analytics
-   Custom tools (MCP)

#### Business Plan - $499/month

-   10,000,000 tokens/month included
-   50 active agents
-   Enhanced memory (1GB per agent)
-   Priority support
-   Rate limit: 6,000 requests/minute
-   A2A protocol access
-   Workflow automation
-   SLA guarantee

#### Enterprise Plan - Custom pricing

-   Unlimited tokens (volume pricing)
-   Unlimited agents
-   Unlimited memory
-   Dedicated support team
-   Custom rate limits
-   Private deployment option
-   Custom integrations
-   SOC 2 compliance

### Token Pricing (Beyond included amounts)

    GPT-4:         $0.03/1K input tokens, $0.06/1K output tokens
    GPT-4 Turbo:   $0.01/1K input tokens, $0.03/1K output tokens  
    GPT-3.5 Turbo: $0.001/1K input tokens, $0.002/1K output tokens
    Claude 3:      $0.015/1K input tokens, $0.075/1K output tokens

### Resource Limits

#### API Rate Limits

python

    # Rate limit headers
    {
        "X-RateLimit-Limit": "600",      # Requests per minute
        "X-RateLimit-Remaining": "599",   
        "X-RateLimit-Reset": "1705327200"
    }
    
    # Implement exponential backoff
    import time
    
    def make_request_with_retry(func, *args, max_retries=3):
        for attempt in range(max_retries):
            try:
                return func(*args)
            except RateLimitError as e:
                if attempt == max_retries - 1:
                    raise
                
                wait_time = (2 ** attempt) + random.random()
                time.sleep(wait_time)

#### Memory Limits

-   Starter: 1MB per agent
-   Professional: 100MB per agent
-   Business: 1GB per agent
-   Enterprise: Unlimited

#### Context Window Limits

-   GPT-4: 8,192 tokens (32K available on request)
-   GPT-4 Turbo: 128,000 tokens
-   GPT-3.5 Turbo: 16,385 tokens
-   Claude 3: 200,000 tokens

#### Workflow Limits

-   Max steps per workflow: 100
-   Max execution time: 1 hour
-   Max parallel executions: 10 (Business), 100 (Enterprise)

### Cost Optimization Tips

1.  **Use appropriate models**
    
    python
    
        # Route by complexity
        def select_model(task_complexity):
            if task_complexity == "simple":
                return "gpt-3.5-turbo"  # $0.002/1K tokens
            elif task_complexity == "moderate":
                return "gpt-4-turbo"    # $0.03/1K tokens
            else:
                return "gpt-4"          # $0.06/1K tokens
    
2.  **Optimize prompts**
    
    python
    
        # Concise prompts save tokens
        # Bad - verbose
        prompt = """
        You are an AI assistant. Your job is to help users.
        When a user asks you a question, you should provide
        a helpful and accurate response. Please be polite
        and professional in your responses.
        """
        
        # Good - concise
        prompt = "You are a helpful assistant. Be polite and accurate."
    
3.  **Cache responses**
    
    python
    
        # Cache common queries
        response_cache = {}
        
        def get_cached_response(query):
            cache_key = hash(query.lower().strip())
            
            if cache_key in response_cache:
                return response_cache[cache_key]
            
            response = client.messages.send(...)
            response_cache[cache_key] = response
            
            return response
    

* * *

## 14\. Troubleshooting {#troubleshooting}

<!-- AIDEV-NOTE: troubleshooting-guide; common issues and diagnostic procedures -->
### Common Issues

#### Authentication Errors

**Problem**: 401 Unauthorized

json

    {
        "error": {
            "code": "UNAUTHORIZED",
            "message": "Invalid API key"
        }
    }

**Solutions**:

1.  Verify API key is correct
2.  Check key hasn't expired
3.  Ensure proper header format:
    
    python
    
        headers = {
            "Authorization": f"Bearer {api_key}"  # Note the space after Bearer
        }
    

#### Rate Limiting

**Problem**: 429 Too Many Requests

**Solutions**:

1.  Implement exponential backoff
2.  Use batch operations
3.  Upgrade to higher tier
4.  Distribute requests over time

python

    # Rate limit handler
    class RateLimitHandler:
        def __init__(self, max_retries=3):
            self.max_retries = max_retries
        
        async def execute(self, func, *args):
            for attempt in range(self.max_retries):
                try:
                    return await func(*args)
                except RateLimitError as e:
                    if attempt == self.max_retries - 1:
                        raise
                    
                    retry_after = int(e.headers.get("Retry-After", 60))
                    await asyncio.sleep(retry_after)

#### Memory Issues

**Problem**: Agent not remembering information

**Diagnosis**:

python

    # Check memory configuration
    agent = client.agents.get(agent_id)
    print(f"Memory config: {agent.memory_config}")
    
    # Check memory stats
    stats = client.memories.get_stats(agent_id)
    print(f"Total memories: {stats.total_count}")
    print(f"Memory usage: {stats.storage_used_mb}MB")
    
    # Search for specific memory
    memories = client.memories.search(
        agent_id=agent_id,
        query="specific information",
        types=["episodic", "semantic"]
    )

**Solutions**:

1.  Ensure memory is enabled
2.  Check importance thresholds
3.  Verify consolidation is running
4.  Increase memory limits if needed

#### Conversation Context Issues

**Problem**: Agent loses context mid-conversation

**Solutions**:

1.  Check context window size
2.  Verify session is active
3.  Review summarization settings

python

    # Diagnose context issues
    session = client.sessions.get(agent_id, session_id)
    print(f"Context window: {session.context_window}")
    print(f"Messages in context: {session.message_count}")
    print(f"Token usage: {session.tokens_used}/{session.context_window}")
    
    # Increase context window
    updated_session = client.sessions.update(
        agent_id=agent_id,
        session_id=session_id,
        context_window=8192
    )

#### Tool Execution Failures

**Problem**: Tools not executing or returning errors

**Diagnosis**:

python

    # Check tool configuration
    tools = client.tools.list(agent_id=agent_id)
    for tool in tools:
        print(f"Tool: {tool.name}, Enabled: {tool.enabled}")
        print(f"Last error: {tool.last_error}")
    
    # Test tool directly
    try:
        result = client.tools.execute(
            agent_id=agent_id,
            tool_name="problem_tool",
            input={"test": "data"},
            debug=True  # Get detailed error info
        )
    except ToolExecutionError as e:
        print(f"Error: {e.message}")
        print(f"Details: {e.details}")

#### Workflow Failures

**Problem**: Workflows failing or stuck

**Diagnosis**:

python

    # Get execution details
    execution = client.workflow_executions.get(execution_id)
    print(f"Status: {execution.status}")
    print(f"Current step: {execution.current_step}")
    print(f"Error: {execution.error}")
    
    # Get step history
    history = client.workflow_executions.get_history(execution_id)
    for step in history:
        print(f"{step.timestamp}: {step.step_name} - {step.status}")
        if step.error:
            print(f"  Error: {step.error}")

### Debug Mode

Enable debug mode for detailed information:

python

    # Enable debug mode
    client = JulepClient(
        api_key="...",
        debug=True,
        log_level="DEBUG"
    )
    
    # Debug specific operations
    response = client.messages.send(
        agent_id=agent_id,
        session_id=session_id,
        content="Test message",
        debug=True  # Returns additional debug info
    )
    
    print(f"Debug info: {response.debug}")

### Health Checks

python

    # Check service health
    health = client.health.check()
    print(f"""
    Service Health:
    - API: {health.api_status}
    - Database: {health.database_status}
    - Memory Service: {health.memory_status}
    - Tool Service: {health.tool_status}
    - Workflow Engine: {health.workflow_status}
    
    Current Load:
    - Active Sessions: {health.active_sessions}
    - Queue Depth: {health.queue_depth}
    - Avg Response Time: {health.avg_response_time}ms
    """)

### Support Resources

1.  **Documentation**: [https://docs.julep.cloud](https://docs.julep.cloud/)
2.  **API Reference**: [https://api.julep.cloud/docs](https://api.julep.cloud/docs)
3.  **Community Forum**: [https://community.julep.cloud](https://community.julep.cloud/)
4.  **Discord**: [https://discord.gg/julep-cloud](https://discord.gg/julep-cloud)
5.  **Email Support**: [support@julep.cloud](https://mail.google.com/mail/?view=cm&fs=1&tf=1&to=support@julep.cloud) (Pro and above)
6.  **Status Page**: [https://status.julep.cloud](https://status.julep.cloud/)

### Submitting Bug Reports

When reporting issues, include:

python

    # Gather diagnostic information
    diagnostic_info = {
        "agent_id": agent_id,
        "session_id": session_id,
        "request_id": response.meta.request_id,
        "timestamp": datetime.now().isoformat(),
        "error_message": str(error),
        "api_version": client.version,
        "sdk_version": julep.__version__
    }
    
    # Export recent logs
    logs = client.logs.export(
        agent_id=agent_id,
        start_time=datetime.now() - timedelta(hours=1),
        include_requests=True
    )
    
    # Submit via support portal
    ticket = client.support.create_ticket(
        subject="Issue with conversation memory",
        description="Detailed description...",
        priority="high",
        attachments=[
            ("diagnostic_info.json", json.dumps(diagnostic_info)),
            ("logs.json", json.dumps(logs))
        ]
    )

* * *

## Conclusion

Congratulations! You now have a comprehensive understanding of the Julep v2 cloud platform. With its powerful cognitive memory system, extensive tool integrations, and multi-agent collaboration capabilities, you're equipped to build sophisticated AI applications.

Remember:

-   Start simple and iterate
-   Monitor your usage and costs
-   Leverage the memory system effectively
-   Use appropriate models for each task
-   Join the community for support and best practices

Happy building with Julep v2! 🚀

* * *

**Next Steps**:

1.  Create your first agent
2.  Experiment with different memory types
3.  Try integrating tools via MCP
4.  Build a simple workflow
5.  Join our Discord community

For the latest updates and features, visit [https://julep.cloud/changelog](https://julep.cloud/changelog)







