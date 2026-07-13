# Database Connection Timeout Runbook

## Symptoms
- High error rate or connection timeouts in service logs.
- Health check failing with "Database connection down".
- SQL operations throwing: "Connection pool exhausted", "Connection refused", or "could not connect to server".

## Recovery Steps
1. Verify if the database container/server is running and reachable.
2. Check database connection pool limits. Increase pool size if connections are exhausted.
3. Restart the database client service to clear hung connections.
4. Optimize database queries or add indexes for slow-running operations.
