# Julep V2 Deployment Guide

This directory contains all deployment configurations for Julep V2, including Docker Compose setup, database migrations, and environment configuration.

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- At least 8GB RAM available for Docker
- PostgreSQL client tools (optional, for debugging)

### 1. Environment Setup

```bash
# Copy the example environment file
cp ../.env.example ../.env

# Edit .env and fill in all required values (no defaults for security)
# Required variables:
# - POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
# - HASURA_ADMIN_SECRET
# - APP_SECRET_KEY, JWT_SECRET
# - OPENAI_API_KEY
# - GRAFANA_ADMIN_PASSWORD (if using monitoring)
```

### 2. Start Core Services

```bash
cd docker

# Start core services (PostgreSQL, Hasura, App)
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Start All Services (Including Optional)

```bash
# Start with Redis caching
docker-compose --profile full up -d

# Start with monitoring (Prometheus + Grafana)
docker-compose --profile monitoring up -d

# Start everything
docker-compose --profile full --profile monitoring up -d
```

## Directory Structure

```
deployment/
├── docker/
│   ├── docker-compose.yml    # Main orchestration file
│   └── init.sql             # PostgreSQL initialization
└── README.md                # This file
```

Database migrations have been moved to `src/database/migrations/` to keep them with the application code.

## Services Overview

### Core Services (Always Running)

1. **PostgreSQL** (port 5432)
   - pgvector 0.8.0 for embeddings
   - pgmq for message queuing
   - Optimized for HNSW indexing

2. **Hasura** (port 8080)
   - GraphQL API over PostgreSQL
   - Admin console at http://localhost:8080/console
   - Real-time subscriptions enabled

3. **Julep App** (port 8000)
   - FastAPI application
   - OpenAPI docs at http://localhost:8000/docs
   - Health check at http://localhost:8000/health

### Optional Services

4. **Redis** (port 6379) - Profile: `full`
   - Caching layer
   - Session storage

5. **Prometheus** (port 9090) - Profile: `monitoring`
   - Metrics collection
   - Service monitoring

6. **Grafana** (port 3000) - Profile: `monitoring`
   - Dashboards and visualization
   - Login with admin / GRAFANA_ADMIN_PASSWORD

## Database Migrations

Migrations are located in `src/database/migrations/` and run automatically on PostgreSQL startup. They create:

- **001_initial_schema.sql**: Core agent tables
- **002_memory_system.sql**: 4-layer cognitive memory system
- **003_protocols.sql**: MCP and A2A protocol support
- **004_workflows.sql**: DBOS-compatible workflow state
- **005_functions.sql**: Utilities and triggers

### Manual Migration

```bash
# Connect to database
docker-compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

# Run specific migration
\i /app/src/database/migrations/001_initial_schema.sql

# Check migration status
\dt agents.*
\dt memory.*
\dt protocols.*
\dt workflows.*
```

## Configuration

### Environment Variables

See `../.env.example` for all available variables. Key categories:

- **Database**: Connection settings and performance tuning
- **Hasura**: GraphQL engine configuration
- **Application**: API keys, secrets, feature flags
- **Monitoring**: Metrics and observability settings

### Performance Tuning

PostgreSQL is pre-configured for optimal performance:

```yaml
shared_buffers: 4GB          # 25% of system RAM
effective_cache_size: 12GB   # 75% of system RAM
maintenance_work_mem: 2GB    # For index creation
max_parallel_workers: 4      # Parallel query execution
```

Adjust these in `.env` based on your system resources.

## Common Operations

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f postgres
docker-compose logs -f app
```

### Restart Services

```bash
# Restart single service
docker-compose restart app

# Restart all
docker-compose restart
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql

# Restore database
docker-compose exec -T postgres psql -U $POSTGRES_USER $POSTGRES_DB < backup.sql
```

### Clean Slate

```bash
# Stop and remove everything (keeps volumes)
docker-compose down

# Remove everything including data
docker-compose down -v

# Remove specific volume
docker volume rm docker_postgres_data
```

## Troubleshooting

### Services Won't Start

1. Check logs: `docker-compose logs [service_name]`
2. Verify `.env` file has all required variables
3. Ensure ports aren't already in use: `lsof -i :5432`
4. Check Docker resources: `docker system df`

### Database Connection Issues

1. Wait for PostgreSQL to be healthy: `docker-compose ps`
2. Test connection: `docker-compose exec postgres pg_isready`
3. Check credentials in `.env` match docker-compose.yml

### Performance Issues

1. Monitor connections: `docker-compose exec postgres psql -c "SELECT count(*) FROM pg_stat_activity"`
2. Check slow queries: Enable `log_min_duration_statement` in PostgreSQL
3. Review indexes: `\di` in psql

## Production Deployment

For production:

1. Use external PostgreSQL (RDS, Cloud SQL, etc.)
2. Enable SSL/TLS for all connections
3. Use proper secrets management (Vault, AWS Secrets Manager)
4. Set up monitoring and alerting
5. Configure backups and disaster recovery
6. Use Kubernetes or similar orchestration

See `CLAUDE.md` for detailed architecture and design decisions.