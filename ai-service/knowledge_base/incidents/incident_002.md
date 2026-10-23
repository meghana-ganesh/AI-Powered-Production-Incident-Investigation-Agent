# Incident: Increased HTTP 503 Errors

## Symptoms
The payment API returned intermittent HTTP 503 responses.
Error rates increased after a new application deployment.

## Root cause
The new deployment introduced an initialization failure.
Several application instances failed their readiness checks.

## Resolution
1. Inspect deployment logs and application startup errors.
2. Check readiness and liveness probe results.
3. Roll back the deployment if the service cannot recover.
4. Validate application health before restoring traffic.

## Tags
deployment, readiness-probe, HTTP-503, rollback