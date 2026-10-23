# Runbook: Database Connection Pool Troubleshooting

## Purpose
Diagnose application latency and database connection exhaustion.

## Diagnostic steps
1. Inspect active and idle database connections.
2. Check connection acquisition wait times.
3. Identify slow queries and long-running transactions.
4. Review connection leaks and transaction boundaries.
5. Review pool size against database capacity and application traffic.

## Verification
Confirm that connection acquisition latency decreases.
Check that database connections return to the pool.
Verify application p95 latency and timeout rates.

## Tags
database, connection-pool, troubleshooting, performance