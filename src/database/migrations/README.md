# Database Migrations

This directory contains all database migrations for Julep V2. Migrations define the database schema and are run sequentially during initialization.

## Migration Files

- `001_initial_schema.sql` - Core agent tables and basic setup
- `002_memory_system.sql` - 4-layer cognitive memory system
- `003_protocols.sql` - MCP and A2A protocol support tables
- `004_workflows.sql` - DBOS-compatible workflow management
- `005_functions.sql` - Helper functions and triggers

## Naming Convention

Migrations follow a 3-digit prefix pattern:
- `NNN_description.sql` where NNN is a zero-padded number
- Numbers determine execution order
- Use descriptive names that indicate the migration's purpose

## Creating New Migrations

1. Create a new file with the next sequential number:
   ```bash
   touch 006_your_feature.sql
   ```

2. Start with a descriptive comment:
   ```sql
   -- Migration: Add feature X
   -- AIDEV-NOTE: migration-purpose; explain why this migration exists
   ```

3. Make migrations idempotent when possible:
   ```sql
   CREATE TABLE IF NOT EXISTS ...
   CREATE INDEX IF NOT EXISTS ...
   ```

4. Include rollback instructions in comments:
   ```sql
   -- Rollback: DROP TABLE feature_table CASCADE;
   ```

## Best Practices

1. **One logical change per migration** - Don't mix unrelated schema changes
2. **Always test locally first** - Run against a test database
3. **Consider dependencies** - Ensure tables/types exist before referencing
4. **Document thoroughly** - Include AIDEV-NOTE comments for complex logic
5. **Avoid breaking changes** - Use ALTER TABLE instead of DROP/CREATE when possible

## Running Migrations

### During Development

Migrations run automatically when starting the Docker environment:
```bash
docker-compose up -d
```

### Manual Execution

Connect to the database and run specific migrations:
```bash
docker-compose exec postgres psql -U $POSTGRES_USER -d $POSTGRES_DB

-- Run a specific migration
\i /app/src/database/migrations/006_your_feature.sql
```

### Verifying Migration Status

Check which objects exist:
```sql
-- List all schemas
\dn

-- List tables in a schema
\dt agents.*
\dt memory.*
\dt protocols.*
\dt workflows.*

-- Check specific table structure
\d agents.agents
```

## Rollback Strategy

Currently, migrations are forward-only. For rollbacks:

1. **Development**: Drop and recreate the database
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

2. **Production**: Manual rollback using documented commands
   - Each migration should document its rollback procedure
   - Test rollback procedures before production deployment

## Future Improvements

- [ ] Add migration version tracking table
- [ ] Implement proper rollback support
- [ ] Add migration validation/linting
- [ ] Create migration generator script
- [ ] Add checksum validation

## Important Notes

- Migrations are executed in numeric order during `init.sql`
- The PostgreSQL container must mount the src directory to access migrations
- Never modify existing migrations after deployment
- Always add new migrations with the next sequential number