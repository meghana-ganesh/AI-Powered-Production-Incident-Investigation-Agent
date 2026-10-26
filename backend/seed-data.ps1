$localBaseUrl = "http://localhost:8081"
$renderBaseUrl = "https://ai-powered-production-incident.onrender.com"
$baseUrl = $renderBaseUrl

function Post-Json {
    param(
        [string]$Endpoint,
        [hashtable]$Body
    )

    $json = $Body | ConvertTo-Json -Depth 10

    return Invoke-RestMethod `
        -Uri "$baseUrl$Endpoint" `
        -Method Post `
        -ContentType "application/json" `
        -Body $json
}

Write-Host "========================================"
Write-Host "AI INCIDENT AGENT - SEEDING DATA"
Write-Host "========================================"

# ============================================================
# INCIDENT 1 - PAYMENT SERVICE
# Database connection pool exhaustion
# ============================================================

Write-Host "`nCreating Incident 1 - Payment Service..."

Post-Json "/api/incidents" @{
    title = "Payment API returning HTTP 500 errors"
    service = "payment-service"
    description = "Payment API started returning HTTP 500 errors after deployment v1.4.2."
    severity = "CRITICAL"
    status = "OPEN"
}

# Deployment

Post-Json "/api/deployments" @{
    timestamp = "2026-09-25T13:58:00"
    service = "payment-service"
    version = "v1.4.2"
    status = "SUCCESS"
    changeDescription = "Updated database connection pool configuration"
}

# Logs

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:04:55"
    service = "payment-service"
    level = "INFO"
    message = "PaymentService received increased request volume"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:05:12"
    service = "payment-service"
    level = "ERROR"
    message = "Failed to acquire database connection"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:05:18"
    service = "payment-service"
    level = "ERROR"
    message = "Connection pool exhausted"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:05:25"
    service = "payment-service"
    level = "ERROR"
    message = "Database connection acquisition timeout after 3000ms"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:06:02"
    service = "payment-service"
    level = "ERROR"
    message = "POST /payments failed with HTTP 500"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T14:06:10"
    service = "payment-service"
    level = "ERROR"
    message = "Unable to persist payment transaction because database connection was unavailable"
}

# Metrics

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T14:04:00"
    service = "payment-service"
    metric = "http_5xx_rate"
    value = 0.5
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T14:06:00"
    service = "payment-service"
    metric = "http_5xx_rate"
    value = 18.7
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T14:06:00"
    service = "payment-service"
    metric = "db_connection_pool_usage"
    value = 100
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T14:06:00"
    service = "payment-service"
    metric = "request_latency_p95"
    value = 4200
    unit = "milliseconds"
}


# ============================================================
# INCIDENT 2 - ORDER SERVICE
# Bad deployment causing dependency timeout
# ============================================================

Write-Host "`nCreating Incident 2 - Order Service..."

Post-Json "/api/incidents" @{
    title = "Order creation requests timing out"
    service = "order-service"
    description = "Order creation latency increased significantly after deployment v2.8.1."
    severity = "HIGH"
    status = "OPEN"
}

# Deployment

Post-Json "/api/deployments" @{
    timestamp = "2026-09-25T15:12:00"
    service = "order-service"
    version = "v2.8.1"
    status = "SUCCESS"
    changeDescription = "Updated inventory dependency client timeout configuration"
}

# Logs

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T15:17:03"
    service = "order-service"
    level = "INFO"
    message = "OrderService deployment v2.8.1 started receiving production traffic"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T15:18:11"
    service = "order-service"
    level = "WARN"
    message = "Inventory service response time exceeded 2000ms"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T15:18:35"
    service = "order-service"
    level = "ERROR"
    message = "Inventory service request timed out after 5000ms"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T15:19:02"
    service = "order-service"
    level = "ERROR"
    message = "POST /orders exceeded request timeout"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T15:19:20"
    service = "order-service"
    level = "ERROR"
    message = "Order creation failed because downstream inventory-service was unavailable"
}

# Metrics

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T15:16:00"
    service = "order-service"
    metric = "request_latency_p95"
    value = 280
    unit = "milliseconds"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T15:19:00"
    service = "order-service"
    metric = "request_latency_p95"
    value = 4800
    unit = "milliseconds"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T15:19:00"
    service = "order-service"
    metric = "http_5xx_rate"
    value = 7.8
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T15:19:00"
    service = "order-service"
    metric = "dependency_error_rate"
    value = 21.4
    unit = "percent"
}


# ============================================================
# INCIDENT 3 - INVENTORY SERVICE
# Memory pressure / high latency
# ============================================================

Write-Host "`nCreating Incident 3 - Inventory Service..."

Post-Json "/api/incidents" @{
    title = "Inventory API experiencing high latency"
    service = "inventory-service"
    description = "Inventory API latency increased due to memory pressure and garbage collection activity."
    severity = "MEDIUM"
    status = "OPEN"
}

# Deployment

Post-Json "/api/deployments" @{
    timestamp = "2026-09-25T16:05:00"
    service = "inventory-service"
    version = "v3.1.0"
    status = "SUCCESS"
    changeDescription = "Added inventory aggregation cache and expanded response payload"
}

# Logs

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T16:22:04"
    service = "inventory-service"
    level = "INFO"
    message = "Inventory aggregation cache enabled"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T16:25:12"
    service = "inventory-service"
    level = "WARN"
    message = "JVM heap usage exceeded 80 percent"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T16:26:08"
    service = "inventory-service"
    level = "WARN"
    message = "Long garbage collection pause detected: 1200ms"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T16:27:14"
    service = "inventory-service"
    level = "ERROR"
    message = "Inventory request processing exceeded latency threshold"
}

Post-Json "/api/logs" @{
    timestamp = "2026-09-25T16:28:01"
    service = "inventory-service"
    level = "WARN"
    message = "JVM heap usage reached 94 percent"
}

# Metrics

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T16:20:00"
    service = "inventory-service"
    metric = "jvm_heap_usage"
    value = 62
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T16:28:00"
    service = "inventory-service"
    metric = "jvm_heap_usage"
    value = 94
    unit = "percent"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T16:20:00"
    service = "inventory-service"
    metric = "request_latency_p95"
    value = 310
    unit = "milliseconds"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T16:28:00"
    service = "inventory-service"
    metric = "request_latency_p95"
    value = 2900
    unit = "milliseconds"
}

Post-Json "/api/metrics" @{
    timestamp = "2026-09-25T16:28:00"
    service = "inventory-service"
    metric = "gc_pause_time"
    value = 1200
    unit = "milliseconds"
}


Write-Host "`n========================================"
Write-Host "SEEDING COMPLETE"
Write-Host "========================================"

Write-Host "`nIncidents:"
Invoke-RestMethod "$baseUrl/api/incidents" | Format-Table id, title, service, severity, status

Write-Host "`nMetrics:"
Invoke-RestMethod "$baseUrl/api/metrics" | Format-Table id, timestamp, service, metric, value, unit

Write-Host "`nDeployments:"
Invoke-RestMethod "$baseUrl/api/deployments" | Format-Table id, timestamp, service, version, status

Write-Host "`nLogs:"
Invoke-RestMethod "$baseUrl/api/logs" | Format-Table id, timestamp, service, level, message