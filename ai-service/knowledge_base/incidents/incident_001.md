# Incident: Elevated API Latency

## Symptoms
The order service experienced elevated p95 latency above 2 seconds.
Several requests timed out during peak traffic.

## Root cause
A database connection pool was exhausted after a traffic increase.
Slow database queries held connections for longer than expected.

## Resolution
1. Inspect database query latency and connection pool utilization.
2. Identify long-running queries.
3. Optimize queries and review connection pool settings.
4. Monitor p95 latency and connection utilization after the change.

## Tags
database, connection-pool, latency, timeout