# High Latency and Resource Exhaustion Runbook

## Symptoms
- API response times exceeding SLA thresholds (e.g., latency spikes, request queueing).
- CPU usage approaching 100% or thread pool exhaustion in system metrics.
- Logs indicating timeouts while waiting for database connections or downstream systems.

## Recovery Steps
1. Check CPU and memory utilization metrics of the service container.
2. Analyze slow traces or profile the application to identify hot paths.
3. Scale up resources (CPU/RAM) or increase replica count / service instances.
4. Enable rate limiting or request throttling to shed excess load and stabilize the system.
